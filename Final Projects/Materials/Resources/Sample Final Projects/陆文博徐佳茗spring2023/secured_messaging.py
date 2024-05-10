import random
import math


def _fast_power_modulo(a, b, c):
    a = a % c
    ans = 1
    while b != 0:
        if b & 1:
            ans = (ans * a) % c
        b >>= 1
        a = (a * a) % c
    return ans


def _mod_inverse(a, m):
    g = math.gcd(a, m)
    if g != 1:
        raise ValueError('No modular inverse exists')
    else:
        return pow(a, -1, m)


def _miller_rabin_primality_testing(n: int, k: int = 7) -> bool:
    # prevent potential infinite loop when d = 0
    if n < 2:
        return False

    # Decompose (n - 1) to write it as (2 ** r) * d
    # While d is even, divide it by 2 and increase the exponent.
    d = n - 1
    r = 0

    while not (d & 1):
        r += 1
        d >>= 1

    # Test k witnesses.
    for _ in range(k):
        # Generate random integer a, where 2 <= a <= (n - 2)
        a = random.randint(2, n - 3) + 1

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == 1:
                # n is composite.
                return False
            if x == n - 1:
                # Exit inner loop and continue with next witness.
                break
        else:
            # If loop doesn't break, n is composite.
            return False

    return True


def _is_prime(number: int) -> bool:
    # Run primality testing with (minimum + 1) rounds.
    return _miller_rabin_primality_testing(number)


def _random_big_prime_number_generator() -> (int, int):
    def helper(bit_length):
        while True:
            integer = random.getrandbits(bit_length) | 1
            # Test for primeness
            if _is_prime(integer):
                return integer
    while True:
        p, q = helper(1024), helper(1024)
        if p != q:
            return p, q


class RSA:
    def __init__(self):
        self.prime1, self.prime2 = _random_big_prime_number_generator()
        self.n = self.prime1 * self.prime2

    def _generate_keypair(self):
        phi = (self.prime1 - 1) * (self.prime2 - 1)
        e = random.randrange(1, phi)
        gcd = math.gcd(e, phi)
        while gcd != 1:
            e = random.randrange(1, phi)
            gcd = math.gcd(e, phi)
        d = _mod_inverse(e, phi)
        return (e, self.n), (d, self.n)

    def show_public_private_key_pair(self):
        return self._generate_keypair()

    def brute_force_attack_estimation(self):
        # Approximate time required to factor an integer of n bits using the General Number Field Sieve algorithm
        def factor_time(n):
            return math.exp(math.pow((64*n/9), 1/3) * pow(math.log(n), 2/3))

        # Approximate time required to decrypt an RSA ciphertext with a brute-force attack
        def decrypt_time(n):
            bits = math.log2(n)
            factor_bits = bits / 2
            factor_time_sec = factor_time(factor_bits)
            # Estimation based on Aurora,
            # 2 exaFLOPS in computing power ~ a quintillion (2^60 or 10^18) calculations per second
            # Aurora is a planned supercomputer to be completed in 2023 by Intel
            return factor_time_sec / ((2 * 10 ** 18) * 365 * 24 * 60 * 60)

        # Example usage: estimate time to decrypt an RSA ciphertext with 2048-bit modulus
        time_years = decrypt_time(self.n)
        print(f"Estimated time to decrypt: {time_years:.2f} years, with current technology")

    @staticmethod
    def encrypt(peer_public_key, message):
        e, n = peer_public_key
        # print(e, n)
        cipher = [(_fast_power_modulo(ord(char), e, n)) if char else 0 for char in message]
        return cipher

    @staticmethod
    def decrypt(private_key, message):
        d, n = private_key
        plain = [chr(_fast_power_modulo(char, d, n)) for char in message]
        return ''.join(plain)


if __name__ == '__main__':
    # print(_random_big_prime_number_generator())
    encrypt = RSA()
    encrypt.brute_force_attack_estimation()
    public, private = encrypt.show_public_private_key_pair()
    # public_key, private_key = generate_keypair(p, q)
    msg = 'Hello, world!'
    encrypted = encrypt.encrypt(public, msg)

    decrypted = encrypt.decrypt(private, encrypted)
    print('Original msg:', msg)
    print('Encrypted msg:', encrypted)
    print('Decrypted msg:', decrypted)
