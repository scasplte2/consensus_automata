from nacl.encoding import RawEncoder
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from hashlib import blake2b
import colorama
import random

colorama.init()


def hash(msg: bytes) -> bytes:
    digest = blake2b(digest_size=32)
    digest.update(msg)
    output = digest.digest()
    return output


def chex(s: bytes):
    random.seed(s)
    style = random.randrange(8)
    fg = random.randrange(30, 38)
    s1 = ''
    bg = random.randrange(40, 48)
    fmt = ';'.join([str(style), str(fg), str(bg)])
    data = HexEncoder.encode(s)[0:8]
    s1 += '\x1b[%sm %s \x1b[0m' % (fmt, data)
    return s1


class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        if self.left is None and self.right is None:
            return True
        else:
            return False

    def get(self):
        return self.value, self.left, self.right


class SumSignature:
    def __init__(self, vk: bytes, sigma: bytes, w: list[bytes]):
        self.vk = vk
        self.sigma = sigma
        self.w = w

    @classmethod
    def decode(cls, data: bytes):
        vk = data[0:32]
        sigma = data[32:96]
        wd = data[96:]
        w = []
        for i in range(0, len(wd)//32):
            wi = wd[32*i:32*(i+1)]
            w = w + [wi]
        return cls(vk, sigma, w)

    def get(self) -> (bytes, bytes, list[bytes]):
        return self.vk, self.sigma, self.w

    def encode(self) -> bytes:
        out = self.vk + self.sigma
        for wi in self.w:
            out = out + wi
        return out


def height(n) -> int:
    if isinstance(n, Node):
        if n.is_leaf():
            return 0
        else:
            return max(height(n.left), height(n.right)) + 1
    else:
        return 0


def keygen(s: bytes) -> (SigningKey, VerifyKey):
    sk = SigningKey(seed=s)
    vk = sk.verify_key
    return sk, vk


def generate_signature(sk: SigningKey, m: bytes) -> bytes:
    sig = sk.sign(m, encoder=RawEncoder)
    sigma = RawEncoder.decode(sig.signature)
    return sigma


def test_signature(vk: VerifyKey, sigma: bytes, m: bytes) -> bool:
    try:
        vk.verify(m, sigma, encoder=RawEncoder)
        return True
    except BadSignatureError:
        return False


def doubling_prng(s: bytes) -> (bytes, bytes):
    sl = hash(b'0'+s)
    sr = hash(b'1'+s)
    return sl, sr


def seed_tree(s: bytes, h: int) -> Node:
    if h > 0:
        (sl, sr) = doubling_prng(s)
        nl = seed_tree(sl, h - 1)
        nr = seed_tree(sr, h - 1)
        return Node(sr, nl, nr)
    else:
        (sk, vk) = keygen(s)
        return Node((sk, vk), None, None)


def merkle_vk(n: Node) -> Node:
    if n.is_leaf():
        return n
    else:
        (v,  l,  r) = n.get()
        (vl, ll, lr) = l.get()
        (vr, rl, rr) = r.get()
        nl = merkle_vk(l)
        nr = merkle_vk(r)
        if l.is_leaf() and r.is_leaf():
            (skl, vkl) = vl
            (skr, vkr) = vr
            vkl_bytes = vkl.encode(encoder=RawEncoder)
            vkr_bytes = vkr.encode(encoder=RawEncoder)
            return Node((v, hash(vkl_bytes), hash(vkr_bytes)), nl, nr)
        else:
            (x, l_nl, r_nl) = nl.get()
            (y, l_nr, r_nr) = nr.get()
            (sx, xl, xr) = x
            (sy, yl, yr) = y
            return Node((v, hash(xl+xr), hash(yl+yr)), nl, nr)


def reduce_tree(n: Node) -> Node:
    if n.is_leaf():
        return n
    else:
        (v, l, r) = n.get()
        return Node(v, reduce_tree(l), None)


def key_gen_sum(s: bytes, h: int) -> Node:
    t1 = seed_tree(s, h)
    t2 = merkle_vk(t1)
    t3 = reduce_tree(t2)
    return t3


def verification_key_sum(n: Node) -> bytes:
    (v, l, r) = n.get()
    (sr, wl, wr) = v
    return hash(wl + wr)


def print_key(n: Node):
    (v, l, r) = n.get()
    if l is None and isinstance(r, Node):
        (sr, wl, wr) = v
        print("1 ", chex(wl), chex(wr), chex(hash(wl+wr)))
        print_key(r)
    elif r is None and isinstance(l, Node):
        (sr, wl, wr) = v
        print("0 ", chex(wl), chex(wr), chex(hash(wl+wr)))
        print_key(l)


def key_time_sum(n: Node) -> int:
    if n.is_leaf():
        return 0
    else:
        (v, l, r) = n.get()
        if l is None and isinstance(r, Node):
            if r.is_leaf():
                return 1
            else:
                h = height(r)
                return key_time_sum(r) + pow(2, h)
        else:
            return key_time_sum(l)


def key_update_sum(n: Node, t: int) -> Node:
    tk = key_time_sum(n)
    h = height(n)
    if tk < t < pow(2, h):
        return evolve_key(n, t)
    else:
        return n


def evolve_key(n: Node, t: int) -> Node:
    if n.is_leaf():
        return n
    else:
        (v, l, r) = n.get()
        h = height(n)
        tp = t % pow(2, h - 1)
        if t >= pow(2, h - 1):
            if isinstance(l, Node) and r is None:
                if l.is_leaf():
                    (sr, ul, ur) = v
                    (sk, vk) = keygen(sr)
                    nr = Node((sk, vk), None, None)
                    return Node(v, None, nr)
                else:
                    (sr, wl, wr) = v
                    nr = key_gen_sum(sr, h-1)
                    nrp = evolve_key(nr, tp)
                    return Node(v, None, nrp)
            else:
                nr = evolve_key(r, tp)
                return Node(v, None, nr)
        else:
            if l is None and isinstance(r, Node):
                nr = evolve_key(r, tp)
                return Node(v, None, nr)
            else:
                nl = evolve_key(l, tp)
                return Node(v, nl, None)


def sign_sum(n: Node, m: bytes) -> SumSignature:
    w = []
    (v, l, r) = n.get()
    while isinstance(l, Node) or isinstance(r, Node):
        (sr, wl, wr) = v
        if l is None and isinstance(r, Node):
            w = [wl] + w
            (v, l, r) = r.get()
        else:
            w = [wr] + w
            (v, l, r) = l.get()
    (sk, vk) = v
    sigma = generate_signature(sk, m)
    vk_bytes = vk.encode(encoder=RawEncoder)
    return SumSignature(vk_bytes, sigma, w)


def verify_sum_signature(r: bytes, sigma_t: SumSignature, t: int, m: bytes) -> bool:
    (vk, sigma, w) = sigma_t.get()
    bw = True
    if len(w) > 0:
        wl = None
        wr = None
        h = len(w)
        head, *tail = w
        if t % 2 == 0:
            wl = hash(vk)
            wr = head
            print("0 ", chex(wl), chex(wr), chex(hash(wl+wr)))
        else:
            wl = head
            wr = hash(vk)
            print("1 ", chex(wl), chex(wr), chex(hash(wl+wr)))
        w = tail
        while len(w) > 0:
            head, *tail = w
            hp = h-len(w)
            if (t//pow(2, hp)) % 2 == 0:
                wl = hash(wl+wr)
                wr = head
                print("0 ", chex(wl), chex(wr), chex(hash(wl+wr)))
            else:
                wr = hash(wl+wr)
                wl = head
                print("1 ", chex(wl), chex(wr), chex(hash(wl+wr)))
            w = tail
        bw = bw and r == hash(wl + wr)
        print("vk match? ", r == hash(wl + wr), chex(r), chex(hash(wl+wr)))
    else:
        bw = bw and r == hash(vk)
    verify_key = VerifyKey(vk, encoder=RawEncoder)
    bs = test_signature(verify_key, sigma, m)
    print("Sigma verified?", bs)
    return bw and bs
