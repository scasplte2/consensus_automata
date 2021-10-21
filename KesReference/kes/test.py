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
print("--------------------------------------------")

print("Product composition test: \nevolve the key and make some signatures...")

h1 = 12
h2 = 12
prod_key = key_gen_product(test_seed, h1, h2)
t_max = prod_key.max_time_steps()
t = 0
print("T_max =", t_max)
while t < t_max:
    t = random.randint(t, t_max+1)
    print("t =", t)
    prod_key = key_update_product(prod_key, t)
    prod_sig_t = sign_product(prod_key, message)
    prod_vk = verification_key_product(prod_key)
    print("ProductSignature verified?", verify_product_signature(prod_vk, prod_sig_t, t, message))
    print("ProductKey time =", key_time_product(prod_key))
    print("ProductSignature size =", len(prod_sig_t.encode()))

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

