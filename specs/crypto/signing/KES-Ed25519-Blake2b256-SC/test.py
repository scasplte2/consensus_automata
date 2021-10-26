from sum_comp import *


test_message = 'message'.encode('utf-8')

byte_var = 'test'.encode('utf-8')

test_seed = hash(byte_var)

test_sum = True

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
    signature = sign_sum(new_key, test_message)
    signature_bytes = signature.encode()
    print("Signature byte length:", len(signature_bytes))
    signature = SumSignature.decode(signature_bytes)
    r = verification_key_sum(new_key)
    if verify_sum_signature(r, signature, randomStep, test_message):
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

