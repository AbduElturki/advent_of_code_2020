def GetSecretLoopSize(pub_key, init_sub):
    val = 1
    loop_size = 0
    while val != pub_key:
        val = (val * init_sub) % 20201227
        loop_size += 1
    return loop_size

def Encrypt(subject_val, loop_size):
    val = 1
    for _ in range(loop_size):
        val = (val * subject_val) % 20201227
    return val


if __name__ == "__main__":
    with open("input.txt") as f:
        public_keys = [int(x.strip()) for x in f.readlines()]

    secret_loop_1 = GetSecretLoopSize(public_keys[0],7)
    encrypted_m = Encrypt(public_keys[1], secret_loop_1)
    print("Part 1:", encrypted_m)
    print("There are no (real) part 2 for today's puzzle.")
