from product_comp import *

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

print(test_signature(verify_key, signature_bytes, test_message))

byte_var = 'test'.encode('utf-8')

message = 'message'.encode('utf-8')
test_seed = hash(byte_var)

test_sum = True
test_prod = True
test_vectors = True

if test_sum:
    print("generating sum key...")
    h = 10
    new_key = key_gen_sum(test_seed, h)
    print("generated key!")
    ctr = 0
    randomStep = random.randint(0, pow(2, h))
    print("Sum composition test: perform sweep of time step with random correct step, only one should verify...")
    for i in range(0, pow(2, h)):
        t = i
        new_key = key_update_sum(new_key, t)
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
        print("--------------------------------------------")
    if ctr == 1:
        print("Success!")
    else:
        print("Error: more than one time step verified, serious bug in code!")
        test_sum = False
    print("--------------------------------------------")

if test_prod and test_sum:
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

if test_vectors and test_sum and test_prod:
    print("--------------------------------------------")
    print("Test vectors:")
    print("seed:", HexEncoder.encode(test_seed))
    t = 0
    hv = 7
    print("h =", hv)
    sum_key_vector = key_gen_sum(test_seed, hv)
    print("sum_key VK:", HexEncoder.encode(verification_key_sum(sum_key_vector)))
    sigma_0 = sign_sum(sum_key_vector, message)
    print("message:", HexEncoder.encode(message))
    print("sigma t = 0: ", HexEncoder.encode(sigma_0.encode()))
    print("--------------------------------------------")
    sigma_1 = sign_sum(key_update_sum(sum_key_vector, 1), message)
    print("sigma t = 1: ", HexEncoder.encode(sigma_0.encode()))
    print("--------------------------------------------")
    sigma_10 = sign_sum(key_update_sum(sum_key_vector, 10), message)
    print("sigma t = 10: ", HexEncoder.encode(sigma_0.encode()))
    print("--------------------------------------------")
    sigma_100 = sign_sum(key_update_sum(sum_key_vector, 100), message)
    print("sigma t = 100: ", HexEncoder.encode(sigma_0.encode()))

