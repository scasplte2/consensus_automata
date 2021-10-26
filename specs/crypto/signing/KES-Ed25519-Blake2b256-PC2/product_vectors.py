from product_comp import *


messages = ["language shares a common tongue",
            "huddled masses with socks",
            "arriving on time and late",
            "wonder where width went",
            "me or it - either way you jump off",
            "just over that hill: the one one wants one",
            "my legs cramp, my head moves its mouth",
            "strip language of emotion, end up with operate",
            "nevertheless, again more",
            "predicate, pontificate, travel long distances and speak truth",
            "it as do be it he me or",
            "in a short while craft - not much to do about it",
            "turn a single letter - it becomes a bird or later",
            "a string pulled out of a word endlessly, never snaps",
            "disabled and detained, probably dispelled",
            "place it on a stump",
            "nature speaks to those who disappear into it",
            "all the images my eyes have seen now memory?",
            "limited potential so must rely on hope or help",
            "olfactory workers on break"]


seeds = ["lineage",
         "order",
         "threshold",
         "conductor",
         "vigorous",
         "swiftly",
         "enumerate",
         "recede",
         "vacuum",
         "pavement",
         "interference",
         "quagmire",
         "detritus",
         "friendly",
         "negligence",
         "lounge",
         "utopia",
         "fragment",
         "isolate",
         "pretend"]


def line():
    print("--------------------------------------------------------------------------------------------------")


def product_test_vector(message: str, seed: str, h1: int, h2: int, t_range: list[int], test_number: int):
    line()
    print("Product Test Vector: "+str(test_number))
    print("Seed String: \""+seed+"\"")
    print("Seed Bytes: ["+seed.encode().hex()+"]")
    print("h1 =", h1)
    print("h2 =", h2)
    print("Message String: \"" + message + "\"")
    print("Message Bytes: ["+message.encode().hex()+"]")
    product_key = key_gen_product(seed.encode(), h1, h2)
    print("Sum Composition Verification Key:")
    print("["+verification_key_product(product_key).hex()+"]")
    print("Product Composition Secret Key, t = 0:")
    print("Tau 1:")
    print_vector(product_key.tau_1)
    print("Tau 2:")
    print_vector(product_key.tau_2)
    print("Product Key Seed:")
    print("["+product_key.seed.hex()+"]")
    print("Product Key Sum Signature:")
    product_key.sigma_1.print()
    line()
    for j in t_range:
        product_key = key_update_product(product_key, j)
        sigma = sign_product(product_key, message.encode())
        print("sigma t = "+str(j)+":")
        sigma.print()
        line()
    print("Product Composition Secret Key, t = "+str(key_time_product(product_key))+":")
    print("Tau 1:")
    print_vector(product_key.tau_1)
    print("Tau 2:")
    print_vector(product_key.tau_2)
    print("Product Key Seed:")
    print("["+product_key.seed.hex()+"]")
    print("Product Key Sum Signature:")
    product_key.sigma_1.print()


product_test_vector(messages[10], seeds[10], 1, 1, [0, 1, 2, 3], 11)
product_test_vector(messages[11], seeds[11], 1, 2, [0, 2, 4, 6], 12)
product_test_vector(messages[12], seeds[12], 2, 1, [1, 3, 5, 7], 13)
product_test_vector(messages[13], seeds[13], 2, 2, [0, 5, 10, 15], 14)
product_test_vector(messages[14], seeds[14], 3, 3, [0, 21, 42, 63], 15)
product_test_vector(messages[15], seeds[15], 4, 4, [0, 85, 170, 255], 16)
product_test_vector(messages[16], seeds[16], 5, 5, [0, 341, 682, 1023], 17)
product_test_vector(messages[17], seeds[17], 6, 6, [0, 1365, 2730, 4095], 18)
product_test_vector(messages[18], seeds[18], 7, 7, [0, 5461, 10922, 16383], 19)
product_test_vector(messages[19], seeds[19], 8, 8, [0, 21845, 43690, 65535], 20)

