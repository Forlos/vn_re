def mt_init(**kwargs):
    def init(
        w=32,
        n=624,
        m=397,
        r=31,
        a=0x9908B0DF,
        u=11,
        d=0xFFFFFFFF,
        s=7,
        b=0x9D2C5680,
        t=15,
        c=0xEFC60000,
        l=18,
        f=1812433253,
    ):
        global mt_arr, mt_index, mt_word_mask, mt_lower_mask, mt_upper_mask
        mt_arr = [0 for _ in range(n)]
        mt_index = n + 1
        mt_word_mask = (1 << w) - 1
        mt_lower_mask = (1 << r) - 1
        mt_upper_mask = mt_word_mask ^ mt_lower_mask
        return w, n, m, r, a, u, d, s, b, t, c, l, f

    global w, n, m, r, a, u, d, s, b, t, c, l, f
    w, n, m, r, a, u, d, s, b, t, c, l, f = init(**kwargs)


# Custom seed setter for GYU images
def seed_gyu(seed):
    global mt_arr, mt_index
    try:
        mt_index
    except NameError:
        mt_init()
    mt_index = len(mt_arr)
    for i in range(0, len(mt_arr)):
        temp = seed
        seed = (((seed * 0x10DCD) & 0xFFFF_FFFF) + 1) & 0xFFFF_FFFF
        mt_arr[i] = (temp & 0xFFFF0000) | (seed >> 16)
        seed = (((seed * 0x10DCD) & 0xFFFF_FFFF) + 1) & 0xFFFF_FFFF
    return mt_arr


# Give initial series based on seed
def seed(seed):
    global mt_arr, mt_index
    try:
        mt_index
    except NameError:
        mt_init()
    mt_index = len(mt_arr)
    mt_arr[0] = seed
    for i in range(1, len(mt_arr)):
        mt_arr[i] = mt_word_mask & (
            f * (mt_arr[i - 1] ^ (mt_arr[i - 1] >> (w - 2))) + i
        )


# Get the next n numbers in the series
def mt_twist():
    global mt_index
    for i in range(n):
        x = (mt_arr[i] & mt_upper_mask) + (mt_arr[(i + 1) % n] & mt_lower_mask)
        xA = x >> 1
        if x % 2:
            xA = xA ^ a
        mt_arr[i] = mt_arr[(i + m) % n] ^ xA
    mt_index = 0


# Extract the next tempered value from series; twist every n numbers
def rand():
    global mt_index
    try:
        mt_index
    except NameError:
        mt_init()
    if mt_index >= n:
        if mt_index > n:
            seed(5489)
        mt_twist()
    y = mt_arr[mt_index]
    y ^= (y >> u) & d
    y ^= (y << s) & b
    y ^= (y << t) & c
    y ^= y >> l
    mt_index += 1
    return mt_word_mask & y
