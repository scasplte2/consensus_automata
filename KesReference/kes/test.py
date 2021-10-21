from functions import *


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
h = 12
new_key = key_gen_sum(test_seed, h)
print("generated key!")
ctr = 0
randomStep = random.randint(0, pow(2, h))
print("perform sweep of time step with random correct step, only one should verify...")
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

