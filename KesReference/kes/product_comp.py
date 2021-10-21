from sum_comp import *


class ProductKey:
    def __init__(self, tau_1, sigma_1, seed, r_2, tau_2):
        self.tau_1 = tau_1
        self.sigma_1 = sigma_1
        self.seed = seed
        self.r_2 = r_2
        self.tau_2 = tau_2


class ProductSignature:
    def __init__(self, sigma_1: SumSignature, sigma_2: SumSignature, r_2: bytes):
        self.sigma_1 = sigma_1
        self.sigma_2 = sigma_2
        self.r_2 = r_2

    @classmethod
    def decode(cls, data: bytes, h1: int, h2: int):
        sig_bytes = 96
        sig_1 = data[0: sig_bytes + 32*h1]
        sig_2 = data[sig_bytes + 32*h1: 2*sig_bytes + 32*h1 + 32*h2]
        r_2 = data[2*sig_bytes + 32*h1 + 32*h2:  2*sig_bytes + 32*h1 + 32*h2 + 32]
        sigma_1 = SumSignature.decode(sig_1)
        sigma_2 = SumSignature.decode(sig_2)
        return cls(sigma_1, sigma_2, r_2)

    def encode(self) -> bytes:
        return self.sigma_1.encode() + self.sigma_2.encode() + self.r_2

    def get(self) -> (SumSignature, SumSignature, bytes):
        return self.sigma_1, self.sigma_2, self.r_2


def key_gen_product(s: bytes, h1: int, h2: int):
    (s1, s2) = doubling_prng(s)
    (s3, s4) = doubling_prng(s2)
    tau_1 = key_gen_sum(s1, h1)
    tau_2 = key_gen_sum(s3, h2)
    r_2 = verification_key_sum(tau_2)
    sigma_1 = sign_sum(tau_1, r_2)
    return ProductKey(tau_1, sigma_1, s4, r_2, tau_2)


def verification_key_product(key: ProductKey) -> bytes:
    return verification_key_sum(key.tau_1)


def key_time_product(key: ProductKey) -> int:
    h2 = height(key.tau_1)
    t1 = key_time_sum(key.tau_1)
    t2 = key_time_sum(key.tau_2)
    return t1*pow(2, h2) + t2


def sign_product(key: ProductKey, m: bytes):
    sigma_2 = sign_sum(key.tau_2, m)
    return ProductSignature(key.sigma_1, sigma_2, key.r_2)


def verify_product_signature(vk: bytes, sigma: ProductSignature, t: int, m: bytes) -> bool:
    h2 = len(sigma.sigma_2.w)
    t1 = t // pow(2, h2)
    t2 = t % pow(2, h2)
    b1 = verify_sum_signature(vk, sigma.sigma_1, t1, sigma.r_2)
    b2 = verify_sum_signature(sigma.r_2, sigma.sigma_2, t2, m)
    return b1 and b2


def key_update_product(key: ProductKey, t: int) -> ProductKey:
    t_key = key_time_product(key)
    h1 = height(key.tau_1)
    h2 = height(key.tau_2)
    if t_key < t < pow(2, h1 + h2):
        i = key_time_sum(key.tau_1)
        t1 = t // pow(2, h2)
        t2 = t % pow(2, h2)
        if i < t1:
            s1 = None
            s2 = key.seed
            while i < t1:
                (s1, s2) = doubling_prng(s2)
                i = i+1
            tau_1 = evolve_key(key.tau_1, t1)
            tau_2 = key_gen_sum(s1, h2)
            r_2 = verification_key_sum(tau_2)
            sigma_1 = sign_sum(tau_1, r_2)
            tau_2 = evolve_key(tau_2, t2)
            return ProductKey(tau_1, sigma_1, s2, r_2, tau_2)
        else:
            tau_2 = evolve_key(key.tau_2, t2)
            return ProductKey(key.tau_1, key.sigma_1, key.seed, key.r_2, tau_2)
    else:
        return key






