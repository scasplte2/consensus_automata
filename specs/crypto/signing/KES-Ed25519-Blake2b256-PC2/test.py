from product_comp import *


test_message = 'message'.encode('utf-8')

byte_var = 'test'.encode('utf-8')

test_seed = hash(byte_var)

print("----------------------------------------------------------------")
print("Testing product key update consistency...")
h1 = 4
h2 = 4
prod_key = key_gen_product(test_seed, h1, h2)
try:
    for i in range(0, prod_key.max_time_steps()):
        prod_key = key_update_product(prod_key, i)
        prod_key_2 = key_update_product(key_gen_product(test_seed, h1, h2), i)
        sig1 = sign_product(prod_key, test_message)
        sig2 = sign_product(prod_key_2, test_message)
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
        prod_sig_t = sign_product(prod_key, test_message)
        prod_vk = verification_key_product(prod_key)
        b_vk = verify_product_signature(prod_vk, prod_sig_t, t, test_message)
        print("ProductSignature verified?", b_vk)
        print("ProductKey time =", key_time_product(prod_key))
        print("ProductSignature size =", len(prod_sig_t.encode()))
        if not b_vk:
            raise ValueError
    print("Success!")
except ValueError:
    print('Test Failed!')
    test_prod = False
