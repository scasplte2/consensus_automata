from product_comp import *


def print_split(data: bytes):
    string = data.hex()
    n = 64
    chunks = [string[iii:iii + n] for iii in range(0, len(string), n)]
    for chunk in chunks:
        print(chunk)


test_message = 'message'.encode('utf-8')

# Generate a new random signing key
signing_key = SigningKey.generate()

# Sign a message with the signing key
sig = signing_key.sign(test_message, encoder=RawEncoder)

# Obtain the verify key for a given signing key
verify_key = signing_key.verify_key

verify_key.verify(sig, encoder=RawEncoder)
signature_bytes = RawEncoder.decode(sig.signature)
verify_key.verify(test_message, signature_bytes, encoder=RawEncoder)

# print(test_signature(verify_key, signature_bytes, test_message))

byte_var = 'test'.encode('utf-8')

message = 'message'.encode('utf-8')
test_seed = hash(byte_var)

test_sum = False
test_prod = False
test_vectors = True

if test_sum:
    print("generating sum key...")
    h = 7
    new_key = key_gen_sum(test_seed, h)
    print("generated key!")
    ctr = 0
    randomStep = random.randint(0, pow(2, h))
    print("Sum composition test: perform sweep of time step with random correct step, only one should verify...")
    for i in range(0, pow(2, h)):
        t = i
        new_key = key_update_sum(new_key, t)
        print(height(new_key))
        new_key_bytes = new_key.encode()
        print("private key byte length:", len(new_key_bytes))
        new_key = Node.decode(new_key_bytes)
        print(height(new_key))
        print_key(new_key)
        print("key time:", key_time_sum(new_key))
        signature = sign_sum(new_key, message)
        signature_bytes = signature.encode()
        print("Signature byte length:", len(signature_bytes))
        signature = SumSignature.decode(signature_bytes)
        r = verification_key_sum(new_key)
        if verify_sum_signature(r, signature, randomStep, message):
            print("verified!")
            ctr = ctr + 1
        else:
            print("verification failed...")
        print("----------------------------------------------------------------")
    if ctr == 1:
        print("Success!")
    else:
        print("Error: more than one time step verified, serious bug in code!")
        test_sum = False
    print("----------------------------------------------------------------")

if test_prod:
    print("----------------------------------------------------------------")
    print("Testing product key update consistency...")
    h1 = 4
    h2 = 4
    prod_key = key_gen_product(test_seed, h1, h2)
    try:
        for i in range(0, prod_key.max_time_steps()):
            prod_key = key_update_product(prod_key, i)
            prod_key_2 = key_update_product(key_gen_product(test_seed, h1, h2), i)
            sig1 = sign_product(prod_key, message)
            sig2 = sign_product(prod_key_2, message)
            if prod_key.encode() != prod_key_2.encode():
                print("key bytes didn't match.")
                raise ValueError
            if sig1.encode() != sig2.encode():
                print("signature bytes didn't match.")
                raise ValueError
        print("Success!")
    except ValueError:
        print("Test failed, keys did not match!")
        test_prod = False
    print("----------------------------------------------------------------")

if test_prod:
    print("Product composition test: \nevolve the key and make some signatures...")
    h1 = 10
    h2 = 10
    prod_key = key_gen_product(test_seed, h1, h2)
    t_max = prod_key.max_time_steps()
    t_axis = random.sample(range(0, t_max), 100)
    t_axis.sort()
    print("T_max =", t_max)
    try:
        for t in t_axis:
            print("t =", t)
            prod_key = key_update_product(prod_key, t)
            prod_key_bytes = prod_key.encode()
            prod_key = ProductKey.decode(prod_key_bytes)
            if t != key_time_product(prod_key):
                print("Key update error!")
                raise ValueError
            prod_sig_t = sign_product(prod_key, message)
            prod_vk = verification_key_product(prod_key)
            b_vk = verify_product_signature(prod_vk, prod_sig_t, t, message)
            print("ProductSignature verified?", b_vk)
            print("ProductKey time =", key_time_product(prod_key))
            print("ProductSignature size =", len(prod_sig_t.encode()))
            if not b_vk:
                raise ValueError
        print("Success!")
    except ValueError:
        print('Test Failed!')
        test_prod = False

if test_vectors:
    print("----------------------------------------------------------------")
    print("Sum Test vectors 1:")
    print("seed:")
    print_split(test_seed)
    t = 0
    hv = 7
    print("h =", hv)
    sum_key_vector = key_gen_sum(test_seed, hv)
    print("sum_key VK:")
    print_split(verification_key_sum(sum_key_vector))
    sigma_0 = sign_sum(sum_key_vector, message)
    print("message:")
    print_split(message)
    print("sigma t = 0: ")
    print_split(sigma_0.encode())
    print("----------------------------------------------------------------")
    sigma_1 = sign_sum(key_update_sum(sum_key_vector, 1), message)
    print("sigma t = 1: ")
    print_split(sigma_1.encode())
    print("----------------------------------------------------------------")
    sigma_10 = sign_sum(key_update_sum(sum_key_vector, 10), message)
    print("sigma t = 10: ")
    print_split(sigma_10.encode())
    print("----------------------------------------------------------------")
    sigma_100 = sign_sum(key_update_sum(sum_key_vector, 100), message)
    print("sigma t = 100: ")
    print_split(sigma_100.encode())

if test_vectors:
    print("----------------------------------------------------------------")
    print("Sum Test vectors 2:")
    vector_seed_2 = hash(b'01')
    print("seed:")
    print_split(vector_seed_2)
    t = 0
    hv = 2
    print("h =", hv)
    sum_key_vector = key_gen_sum(test_seed, hv)
    print("sum_key VK:")
    print_split(verification_key_sum(sum_key_vector))
    message_vector_2 = hash(b'02')
    sigma_0 = sign_sum(sum_key_vector, message)
    print("message:")
    print_split(message)
    print("----------------------------------------------------------------")
    print("sigma t = 0: ")
    print_split(sigma_0.encode())
    print("----------------------------------------------------------------")
    sigma_1 = sign_sum(key_update_sum(sum_key_vector, 1), message)
    print("sigma t = 1: ")
    print_split(sigma_1.encode())
    print("----------------------------------------------------------------")
    sigma_2 = sign_sum(key_update_sum(sum_key_vector, 2), message)
    print("sigma t = 2: ")
    print_split(sigma_2.encode())
    print("----------------------------------------------------------------")
    sigma_3 = sign_sum(key_update_sum(sum_key_vector, 3), message)
    print("sigma t = 3: ")
    print_split(sigma_3.encode())


if test_vectors:
    print("----------------------------------------------------------------")
    print("Product Test vectors 1:")
    print("seed:")
    print_split(test_seed)
    t = 0
    h1 = 5
    h2 = 9
    print("h1 =", h1)
    print("h2 =", h2)
    prod_key_vector = key_gen_product(test_seed, h1, h2)
    print("prod_key VK:")
    print_split(verification_key_product(prod_key_vector))
    sigma_0 = sign_product(prod_key_vector, message)
    print("message:")
    print_split(message)
    print("----------------------------------------------------------------")
    print("sigma t = 0: ")
    print_split(sigma_0.encode())
    print("----------------------------------------------------------------")
    sigma_100 = sign_product(key_update_product(prod_key_vector, 100), message)
    print("sigma t = 100: ")
    print_split(sigma_100.encode())
    print("----------------------------------------------------------------")
    sigma_1000 = sign_product(key_update_product(prod_key_vector, 1000), message)
    print("sigma t = 1000: ")
    print_split(sigma_1000.encode())
    print("----------------------------------------------------------------")
    sigma_10000 = sign_product(key_update_product(prod_key_vector, 10000), message)
    print("sigma t = 10000: ")
    print_split(sigma_10000.encode())

if test_vectors:
    print("----------------------------------------------------------------")
    print("Product Test vectors 2:")
    print("seed:")
    print_split(test_seed)
    t = 0
    h1 = 2
    h2 = 2
    print("h1 =", h1)
    print("h2 =", h2)
    prod_key_vector = key_gen_product(test_seed, h1, h2)
    print("prod_key VK:")
    print_split(verification_key_product(prod_key_vector))
    print("message:")
    print_split(message)
    print("----------------------------------------------------------------")
    for i in range(0, prod_key_vector.max_time_steps()):
        prod_key_vector = key_update_product(prod_key_vector, i)
        sigma_i = sign_product(prod_key_vector, message)
        print("sigma t = "+str(i)+": ")
        print_split((sigma_i.encode()))
        print("----------------------------------------------------------------")
