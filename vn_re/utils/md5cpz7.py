import vn_re.utils.md5base
from vn_re.utils.util import wrapping_add


class MD5(vn_re.utils.md5base.MD5):
    def __init_state(self):
        self.__A, self.__B, self.__C, self.__D = (
            0xC74A2B02,
            0xE7C8AB8F,
            0x38BEBC4E,
            0x7531A4C3,
        )

    def __set_buffers(self):
        return [
            self.__C ^ 0x53A76D2E,
            wrapping_add(self.__B, 0x5BB17FDA),
            wrapping_add(self.__A, 0x6853E14D),
            self.__D ^ 0xF5C6A9A3,
        ]


def md5(arg=None):
    """Create a new md5 object"""
    return MD5(arg)
