import hashlib
import sys

from vn_re.formats.cpz7 import Cpz7
from vn_re.utils.util import chunks, wrapping_sub, wrapping_add, ror, rol
from vn_re.utils import md5cpz7


header_keys = [
    0xFE3A53DA,
    0x37F298E8,
    0x7A6F3A2D,
    0x43DE7C1A,
    0xCC65F416,
    0xD016A93D,
    0x97A3BA9B,
    0xAE7D39B7,
    0xFB73A956,
    0x37ACF832,
    0xA7B09C72,
    0x65EF99F3,
]

GLOBAL_NUM = 0
DATA1 = list(bytes(512))
DATA2 = list(bytes(512))

password = [
    137,
    240,
    144,
    205,
    130,
    183,
    130,
    233,
    136,
    171,
    130,
    162,
    142,
    113,
    130,
    205,
    131,
    138,
    131,
    82,
    130,
    170,
    130,
    168,
    142,
    100,
    146,
    117,
    130,
    171,
    130,
    181,
    130,
    191,
    130,
    225,
    130,
    162,
    130,
    220,
    130,
    183,
    129,
    66,
    142,
    244,
    130,
    237,
    130,
    234,
    130,
    191,
    130,
    225,
    130,
    162,
    130,
    220,
    130,
    183,
    130,
    230,
    129,
    96,
    129,
    65,
    130,
    198,
    130,
    162,
    130,
    164,
    130,
    169,
    130,
    224,
    130,
    164,
    142,
    244,
    130,
    193,
    130,
    191,
    130,
    225,
    130,
    162,
    130,
    220,
    130,
    181,
    130,
    189,
    129,
    244,
]


def header_checksum(header):
    num = 0x923A564C
    for chunk in chunks(header, 4):
        x = int.from_bytes(chunk, "little")
        num = (num + x) & 0xFFFFFFFF
    return num


def decrypt_data3(data: bytes, size: int, key: int):
    input_data = bytearray()
    dest = bytearray(size)
    for chunk in chunks(data, 4):
        input_data += (int.from_bytes(chunk, "little") ^ key).to_bytes(4, "little")

    global GLOBAL_NUM
    GLOBAL_NUM = 0x100
    data1 = list(bytes(512))
    data2 = list(bytes(512))
    ptr_arr = [input_data, 0, 0, 0]
    result = recursive_data3_decrypt(ptr_arr, data1, data2)
    for i in range(size):
        inner_result = result
        if inner_result >= 0x100:
            while True:
                if ptr_arr[2] == 0:
                    ptr_arr[3] = int.from_bytes(ptr_arr[0][0:4], "little")
                    ptr_arr[2] = 32
                    ptr_arr[0] = ptr_arr[0][4:]
                ptr_arr[2] -= 1
                x = ptr_arr[3]
                ptr_arr[3] >>= 1
                if x & 1 == 0:
                    inner_result = data1[inner_result]
                else:
                    inner_result = data2[inner_result]
                if inner_result < 0x100:
                    break
        dest[i] = inner_result
    return dest


def recursive_data3_decrypt(ptr_arr: list, data1: bytearray, data2: bytearray):
    if ptr_arr[2] == 0:
        ptr_arr[3] = int.from_bytes(ptr_arr[0][0:4], "little")
        ptr_arr[2] = 32
        ptr_arr[0] = ptr_arr[0][4:]
    ptr_arr[2] -= 1
    y = ptr_arr[3]
    ptr_arr[3] >>= 1
    if y & 1 == 0:
        return data3_zero_transform(8, ptr_arr)
    else:
        global GLOBAL_NUM
        x = GLOBAL_NUM
        GLOBAL_NUM += 1
        result = recursive_data3_decrypt(ptr_arr, data1, data2)
        data1[x] = result
        result = recursive_data3_decrypt(ptr_arr, data1, data2)
        data2[x] = result
        return x


def data3_zero_transform(n, ptr_arr):
    result = 0
    if n > ptr_arr[2]:
        if n == 0:
            return result
        edx = ptr_arr[3]
        while True:
            n -= 1
            if ptr_arr[2] == 0:
                ptr_arr[3] = int.from_bytes(ptr_arr[0][0:4], "little")
                ptr_arr[2] = 32
                ptr_arr[0] = ptr_arr[0][4:]
            ptr_arr[2] -= 1
            x = ptr_arr[3] & 1
            result = x + result * 2
            ptr_arr[3] >>= 1

            if n <= 0:
                break
    else:
        if n == 0:
            return result
        edx = ptr_arr[3]
        esi = ptr_arr[2]
        while True:
            x = edx & 1
            edx >>= 1
            result = x + result * 2
            esi -= 1
            n -= 1

            if n <= 0:
                break
        ptr_arr[2] = esi
        ptr_arr[3] = edx

    return result


def xor_with_data3(data: bytearray, data3: bytearray):
    result = bytearray()
    for i, entry in enumerate(data):
        reminder = (i + 3) % 0x3FF
        result.append(data[i] ^ data3[reminder])
    return result


def decrypt_using_password(data: bytearray, size: int, password: bytearray, key: int):
    xor_buf = bytearray()
    result = bytearray()
    for chunk in chunks(password, 4):
        v = wrapping_sub(int.from_bytes(chunk, "little"), key)
        xor_buf += (v).to_bytes(4, "little")
    k = key
    k >>= 8
    k ^= key
    k >>= 8
    k ^= key
    k >>= 8
    k ^= key
    k ^= 0xFFFFFFFB
    k &= 0x0F
    k += 7
    index = 5
    for i in range(size >> 2):
        v = int.from_bytes(xor_buf[index * 4 : (index + 1) * 4], "little")
        v ^= int.from_bytes(data[i * 4 : (i + 1) * 4], "little")
        v = (v + 0x784C5062) & 0xFFFFFFFF
        v = ror(v, k & 0xFF, 32)
        v = (v + 0x01010101) & 0xFFFFFFFF
        result += v.to_bytes(4, "little")
        index = (index + 1) % 0x18

    for i in range(size & 3, 0, -1):
        v = int.from_bytes(xor_buf[index * 4 : (index + 1) * 4], "little")
        v >>= i * 4
        v ^= data[(size - i) * 4 : ((size - i) * 4) + 1]
        v -= 0x7D
        result += v.to_bytes(1, "little")
        index = (index + 1) % 0x18
    return result


def init_decrypt_table(key1: int, key2: int):
    table = bytearray()
    for i in range(0x100):
        table += i.to_bytes(1, "little")
    v = key1
    for i in range(0x100):
        x = v
        x >>= 0x10
        x &= 0xFF
        y = table[x]
        z = table[v & 0xFF]
        table[v & 0xFF] = y
        table[x] = z

        z = v
        z >>= 8
        z &= 0xFF

        x = v
        x >>= 0x18
        y = table[x]
        v = ror(v, 2, 32)
        v = (v * 0x1A74F195) & 0xFFFFFFFF
        v = wrapping_add(v, key2)
        a = table[z]
        table[z] = y
        table[x] = a
    return table


def decrypt_data_with_decrypt_table(
    table: bytearray, data: bytearray, size: int, xor_key: int
):
    result = bytearray()
    for i in range(size):
        b = data[i]
        b ^= xor_key & 0xFF
        b = table[b]
        result += b.to_bytes(1, "little")
    return result


def decrypt_data1_with_decrypt_buf(decrypt_buf: bytearray, data: bytearray):
    result = bytearray()
    e = 0x76548AEF
    decrypt_index = 0
    for i in range(len(data) >> 2):
        b = int.from_bytes(
            decrypt_buf[decrypt_index * 4 : (decrypt_index * 4) + 4], "little"
        )
        b ^= int.from_bytes(data[i * 4 : (i * 4) + 4], "little")
        b = wrapping_sub(b, 0x4A91C262)
        b = rol(b, 3, 32)
        b = wrapping_sub(b, e)
        result += b.to_bytes(4, "little")

        decrypt_index += 1
        decrypt_index &= 3
        e = wrapping_add(e, 0x10FB562A)

    for i in range(len(data) & 3, 0, -1):
        index = len(data) - i
        b = int.from_bytes(
            decrypt_buf[decrypt_index * 4 : (decrypt_index * 4) + 4], "little"
        )
        b >>= 6
        b = (b & 0xFF) ^ data[index]
        b = wrapping_add(b, 0x37)
        result += b.to_bytes(1, "little")

        decrypt_index += 1
        decrypt_index &= 3

    return result


def decrypt_data2_with_decrypt_buf(decrypt_buf: bytearray, data: bytearray):
    result = bytearray()
    e = 0x2A65CB4F
    decrypt_index = 0
    for i in range(len(data) >> 2):
        b = int.from_bytes(
            decrypt_buf[decrypt_index * 4 : (decrypt_index * 4) + 4], "little"
        )
        b ^= int.from_bytes(data[i * 4 : (i * 4) + 4], "little")
        b = wrapping_sub(b, e)
        b = rol(b, 2, 32)
        b = wrapping_add(b, 0x37A19E8B)
        result += b.to_bytes(4, "little")

        decrypt_index += 1
        decrypt_index &= 3
        e = wrapping_sub(e, 0x139FA9B)

    for i in range(len(data) & 3, 0, -1):
        index = len(data) - i
        b = int.from_bytes(
            decrypt_buf[decrypt_index * 4 : (decrypt_index * 4) + 4], "little"
        )
        b >>= 4
        b = (b & 0xFF) ^ data[index]
        b = wrapping_add(b, 0x3)
        result += b.to_bytes(1, "little")

        decrypt_index += 1
        decrypt_index &= 3

    return result


def decrypt_data2(
    data1: bytearray,
    data2: bytearray,
    count: int,
    decrypt_table: bytearray,
    data2_size: int,
    md5_cpz7: bytearray,
):
    result = bytearray()
    previous_data = data1
    for i in range(count):
        offset = int.from_bytes(previous_data[8:12], "little")
        size = data2_size
        next_data = previous_data[int.from_bytes(previous_data[0:4], "little") :]
        if i < count - 1:
            size = int.from_bytes(next_data[8:12], "little")
        size -= offset

        internal_data2 = decrypt_data_with_decrypt_table(
            decrypt_table, data2[offset:], size, 0x7E
        )
        key = int.from_bytes(previous_data[12:16], "little")
        decrypt_buf2 = (
            (int.from_bytes(md5_cpz7[0:4], "little") ^ key).to_bytes(4, "little")
            + (
                int.from_bytes(md5_cpz7[4:8], "little") ^ wrapping_add(key, 0x11003322)
            ).to_bytes(4, "little")
            + (int.from_bytes(md5_cpz7[8:12], "little") ^ key).to_bytes(4, "little")
            + (
                int.from_bytes(md5_cpz7[12:16], "little")
                ^ wrapping_add(key, 0x34216785)
            ).to_bytes(4, "little")
        )
        internal_data2 = decrypt_data2_with_decrypt_buf(decrypt_buf2, internal_data2)
        previous_data = next_data
        result += internal_data2

    return result


def decrypt_file(
    file_contents: bytearray,
    file_size: str,
    md5_cpz7: bytearray,
    key: int,
    decrypt_table: bytearray,
    password: bytearray,
):
    contents_index = 0
    result = bytearray()
    decrypt_buf = bytearray()  # could need static size
    decrypt_buf2 = bytearray()
    v = int.from_bytes(md5_cpz7[4:8], "little") >> 2
    for b in password:
        decrypt_buf += (decrypt_table[b] ^ (v & 0xFF)).to_bytes(1, "little")
    for chunk in chunks(decrypt_buf, 4):
        decrypt_buf2 += (int.from_bytes(chunk, "little") ^ key).to_bytes(4, "little")
    c = 0x2748C39E
    a = 0x0A
    dx = key
    for i in range(file_size >> 2):
        b = int.from_bytes(decrypt_buf2[a * 4 : (a * 4) + 4], "little") >> 1
        d = (c >> 6) & 0xF
        b ^= int.from_bytes(decrypt_buf2[d * 4 : (d * 4) + 4], "little")
        b ^= int.from_bytes(
            file_contents[contents_index : contents_index + 4], "little"
        )
        b = wrapping_sub(b, dx)
        dx = c & 3
        b ^= int.from_bytes(md5_cpz7[dx * 4 : (dx * 4) + 4], "little")
        dx = key
        result += b.to_bytes(4, "little")

        c = wrapping_add(c, wrapping_add(key, b))
        a += 1
        a &= 0xF
        contents_index += 4

    for i in range(file_size & 3):
        c = file_contents[contents_index] ^ 0xAE
        result += decrypt_table[c].to_bytes(1, "little")

        contents_index += 1

    return result


def get_file_key(file, archive_data, header):
    file_key = file.file_decrypt_key
    file_key = wrapping_add(file_key, archive_data.file_decrypt_key)
    file_key ^= header.archive_data_key_decrypted
    file_key = wrapping_add(
        file_key, wrapping_sub(header.archive_data_entry_count_decrypted, 0x5C39E87B),
    )
    file_key ^= wrapping_add(
        (ror(header.file_decrypt_key_decrypted, 5, 32) * 0x7DA8F173) & 0xFFFFFFFF,
        0x13712765,
    )
    return file_key


def extract_file(filename):
    cpz = Cpz7.from_file(filename)
    data3 = decrypt_data3(
        cpz.encryption_data.data, cpz.encryption_data.data_size, cpz.encryption_data.key
    )
    data = xor_with_data3(
        cpz.raw_data[
            : cpz.header.archive_data_size_decrypted
            + cpz.header.file_data_size_decrypted
        ],
        data3,
    )
    data = decrypt_using_password(
        data,
        cpz.header.archive_data_size_decrypted + cpz.header.file_data_size_decrypted,
        password,
        cpz.header.archive_data_key_decrypted ^ 0x3795B39A,
    )
    md5_cpz7 = md5cpz7.md5(cpz.header.cpz7_md5).digest()
    decrypt_table = init_decrypt_table(
        cpz.header.archive_data_key_decrypted, int.from_bytes(md5_cpz7[4:8], "little")
    )
    data1 = decrypt_data_with_decrypt_table(
        decrypt_table,
        data[: cpz.header.archive_data_size_decrypted],
        cpz.header.archive_data_size_decrypted,
        0x3A,
    )
    decrypt_buf = (
        (
            wrapping_add(cpz.header.archive_data_key_decrypted, 0x76A3BF29)
            ^ int.from_bytes(md5_cpz7[0:4], "little")
        ).to_bytes(4, "little")
        + (
            cpz.header.archive_data_key_decrypted
            ^ int.from_bytes(md5_cpz7[4:8], "little")
        ).to_bytes(4, "little")
        + (
            wrapping_add(cpz.header.archive_data_key_decrypted, 0x1000_0000)
            ^ int.from_bytes(md5_cpz7[8:12], "little")
        ).to_bytes(4, "little")
        + (
            cpz.header.archive_data_key_decrypted
            ^ int.from_bytes(md5_cpz7[12:16], "little")
        ).to_bytes(4, "little")
    )
    data1 = decrypt_data1_with_decrypt_buf(decrypt_buf, data1)
    data2 = data[
        cpz.header.archive_data_size_decrypted : cpz.header.archive_data_size_decrypted
        + cpz.header.file_data_size_decrypted
    ]
    decrypt_table2 = init_decrypt_table(
        cpz.header.archive_data_key_decrypted, int.from_bytes(md5_cpz7[8:12], "little")
    )
    data2 = decrypt_data2(
        data1,
        data2,
        cpz.header.archive_data_entry_count_decrypted,
        decrypt_table2,
        cpz.header.file_data_size_decrypted,
        md5_cpz7,
    )
    decrypt_table3 = init_decrypt_table(
        int.from_bytes(md5_cpz7[12:16], "little"), cpz.header.archive_data_key_decrypted
    )
    archive_data = []
    index = 0
    for i in range(cpz.header.archive_data_entry_count_decrypted):
        entry = cpz.ArchiveDataEntry.from_bytes(data1[index:])
        index += entry.entry_size
        print(entry.name, entry.entry_size)
        archive_data.append(entry)

    files = {}
    index = 0
    for d in archive_data:
        files[d] = list()
        for i in range(d.file_count):
            file = cpz.FileEntry.from_bytes(data2[index:])
            index += file.entry_size
            files[d].append(file)

    for archive_data, file_list in files.items():
        for file in file_list:
            print(file.file_name)
            print(hex(file.file_size))
            contents = cpz.raw_file_data[file.offset : file.offset + file.file_size]
            file_key = get_file_key(file, archive_data, cpz.header)
            f_decrypted = decrypt_file(
                contents, file.file_size, md5_cpz7, file_key, decrypt_table3, password,
            )
            f = open("ext/" + str(file.file_name.split(b"\x00")[0], "ascii"), "wb")
            print(f_decrypted[:4])
            f.write(f_decrypted)
            f.close()


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        extract_file(filename)
