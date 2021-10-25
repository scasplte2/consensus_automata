from sum_comp import *


class ProductKey:
    def __init__(self, tau_1, sigma_1, seed, tau_2):
        self.tau_1 = tau_1
        self.sigma_1 = sigma_1
        self.seed = seed
        self.tau_2 = tau_2

    def max_time_steps(self) -> int:
        return pow(2, height(self.tau_1) + height(self.tau_2))

    def encode(self):
        tau_1_bytes = self.tau_1.encode()
        tau_2_bytes = self.tau_2.encode()
        sigma_bytes = self.sigma_1.encode()
        nt1 = len(tau_1_bytes).to_bytes(4, byteorder='big')
        ns = len(sigma_bytes).to_bytes(4, byteorder='big')
        return nt1 + tau_1_bytes + ns + sigma_bytes + self.seed + tau_2_bytes

    @classmethod
    def decode(cls, data: bytes):
        ptr = 0
        nt1 = int.from_bytes(data[ptr:ptr+4], byteorder='big')
        ptr = ptr + 4
        tau_1 = Node.decode(data[ptr:ptr+nt1])
        ptr = ptr + nt1
        ns = int.from_bytes(data[ptr:ptr+4], byteorder='big')
        ptr = ptr + 4
        sigma_1 = SumSignature.decode(data[ptr:ptr+ns])
        ptr = ptr + ns
        seed = data[ptr:ptr+32]
        ptr = ptr + 32
        tau_2 = Node.decode(data[ptr:])
        return cls(tau_1, sigma_1, seed, tau_2)


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


def erase_leaf_sk(n: Node) -> Node:
    if n.is_leaf():
        (sk, vk) = n.value
        return Node((None, vk), None, None)
    else:
        if n.left is None and isinstance(n.right, Node):
            return Node(n.value, None, erase_leaf_sk(n.right))
        else:
            return Node(n.value, erase_leaf_sk(n.left), None)


def key_gen_product(s: bytes, h1: int, h2: int):
    (s1, s2) = doubling_prng(s)
    (s3, s4) = doubling_prng(s2)
    tau_1 = key_gen_sum(s1, h1)
    tau_2 = key_gen_sum(s3, h2)
    r_2 = verification_key_sum(tau_2)
    sigma_1 = sign_sum(tau_1, r_2)
    tau_1 = key_update_sum(tau_1, 0)
    return ProductKey(tau_1, sigma_1, s4, tau_2)


def verification_key_product(key: ProductKey) -> bytes:
    return verification_key_sum(key.tau_1)


def key_time_product(key: ProductKey) -> int:
    h2 = height(key.tau_2)
    t1 = key_time_sum(key.tau_1)
    t2 = key_time_sum(key.tau_2)
    return t1*pow(2, h2) + t2


def sign_product(key: ProductKey, m: bytes):
    sigma_2 = sign_sum(key.tau_2, m)
    r_2 = verification_key_sum(key.tau_2)
    return ProductSignature(key.sigma_1, sigma_2, r_2)


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
            tau_1 = erase_leaf_sk(tau_1)
            return ProductKey(tau_1, sigma_1, s2, tau_2)
        else:
            tau_2 = evolve_key(key.tau_2, t2)
            return ProductKey(key.tau_1, key.sigma_1, key.seed, tau_2)
    else:
        return key






