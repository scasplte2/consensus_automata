from product_comp import *


readme_header = "## Description\n" \
                +"Test vectors for Topl implementation of a two tree product key evolving signature scheme in the construction of [Malkin-Micciancio-Miner](https://cseweb.ucsd.edu/~daniele/papers/MMM.pdf). A full specification including protocol box descriptions is available in this repo.\n" \
                +"All values below are Hex encoded byte representations unless otherwise specified.\n" \
                +"\nTable of Contents\n" \
                +"- [Test vector - 1](#test-vector---1)\n" \
                +"- [Test vector - 2](#test-vector---2)\n" \
                +"- [Test vector - 3](#test-vector---3)\n" \
                +"- [Test vector - 4](#test-vector---4)\n" \
                +"- [Test vector - 5](#test-vector---5)\n" \
                +"- [Test vector - 6](#test-vector---6)\n" \
                +"- [Test vector - 7](#test-vector---7)\n" \
                +"- [Test vector - 8](#test-vector---8)\n" \
                +"- [Test vector - 9](#test-vector---9)\n" \
                +"- [Test vector - 10](#test-vector---10)"


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


print(readme_header)


def product_test_vector(message: str, seed_str: str, h1: int, h2: int, t_range: list[int], test_number: int):
    seed = hash(seed_str.encode())
    print("## Test Vector - "+str(test_number))
    print("### Description "
          + "\n Generate and verify a specified product composition signature at "
          + "`t = "+str(t_range)
          + "` using a provided seed, message, and heights of the two trees")
    print("### Inputs")
    print("- Seed Bytes:")
    print("```\n"+seed.hex()+"\n```")
    print("- h1 (int):")
    print("\n```"+str(h1)+"```\n")
    print("- h2 (int):")
    print("\n```"+str(h2)+"```\n")
    print("- Message (string):")
    print("```\n\"" + message + "\"\n```")
    print("- Message (bytes) with `utf-8` encoding:")
    print("```\n"+message.encode('utf-8').hex()+"\n```")
    print("### Outputs")
    product_key = key_gen_product(seed, h1, h2)
    print("- Product Composition Verification Key:")
    print("```\n"+verification_key_product(product_key).hex()+"\n```")
    print("- Product Composition Secret Key, t = 0:")
    print("```")
    product_key.print()
    print("```")
    for j in t_range:
        product_key = key_update_product(product_key, j)
        sigma = sign_product(product_key, message.encode('utf-8'))
        print("- Sigma t = "+str(j)+":")
        print("```")
        sigma.print()
        print("```")
    print("Product Composition Secret Key, t = "+str(key_time_product(product_key))+":")
    print("```")
    product_key.print()
    print("```")


product_test_vector(messages[10], seeds[10], 1, 1, [0, 1, 2, 3], 1)
product_test_vector(messages[11], seeds[11], 1, 2, [0, 2, 4, 6], 2)
product_test_vector(messages[12], seeds[12], 2, 1, [1, 3, 5, 7], 3)
product_test_vector(messages[13], seeds[13], 2, 2, [0, 5, 10, 15], 4)
product_test_vector(messages[14], seeds[14], 3, 3, [0, 21, 42, 63], 5)
product_test_vector(messages[15], seeds[15], 4, 4, [0, 85, 170, 255], 6)
product_test_vector(messages[16], seeds[16], 5, 5, [0, 341, 682, 1023], 7)
product_test_vector(messages[17], seeds[17], 6, 6, [0, 1365, 2730, 4095], 8)
product_test_vector(messages[18], seeds[18], 7, 7, [0, 5461, 10922, 16383], 9)
product_test_vector(messages[19], seeds[19], 8, 8, [0, 21845, 43690, 65535], 10)

