from sum_comp import *


readme_header = "## Description\n"\
                +"Test vectors for Topl implementation of a single tree key evolving signature scheme in the construction of [Malkin-Micciancio-Miner](https://cseweb.ucsd.edu/~daniele/papers/MMM.pdf). A full specification including protocol box descriptions is available in this repo.\n"\
                +"All values below are Hex encoded byte representations unless otherwise specified.\n"\
                +"\nTable of Contents\n"\
                +"- [Test vector - 1](#test-vector---1)\n"\
                +"- [Test vector - 2](#test-vector---2)\n"\
                +"- [Test vector - 3](#test-vector---3)\n"\
                +"- [Test vector - 4](#test-vector---4)\n"\
                +"- [Test vector - 5](#test-vector---5)\n"\
                +"- [Test vector - 6](#test-vector---6)\n"\
                +"- [Test vector - 7](#test-vector---7)\n"\
                +"- [Test vector - 8](#test-vector---8)\n"\
                +"- [Test vector - 9](#test-vector---9)\n"\
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


def sum_test_vector(message: str, seed_str: str, h: int, t_range: list[int], test_number: int):
    seed = hash(seed_str.encode())
    print("## Test Vector - "+str(test_number))
    print("### Description "
          + "\n Generate and verify a specified sum composition signature at "
          + "`t = "+str(t_range)
          + "` using a provided seed, message, and height")
    print("### Inputs")
    print("- Seed Bytes:")
    print("```\n"+seed.hex()+"\n```")
    print("- h (int):")
    print("\n```"+str(h)+"```\n")
    print("- Message (string):")
    print("```\n\"" + message + "\"\n```")
    print("- Message (bytes) with `utf-8` encoding:")
    print("```\n"+message.encode('utf-8').hex()+"\n```")
    print("### Outputs")
    sum_key = key_gen_sum(seed, h)
    print("- Sum Composition Verification Key:")
    print("```\n"+verification_key_sum(sum_key).hex()+"\n```")
    print("- Sum Composition Secret Key, t = 0:")
    print("```")
    print_vector(sum_key)
    print("```")
    for j in t_range:
        sum_key = key_update_sum(sum_key, j)
        sigma = sign_sum(sum_key, message.encode('utf-8'))
        print("- Sigma t = "+str(j)+":")
        print("```")
        sigma.print()
        print("```")
        print("- Sum Composition Secret Key, t = "+str(key_time_sum(sum_key))+":")
        print("```")
        print_vector(sum_key)
        print("```")


sum_test_vector(messages[0], seeds[0], 1, [0, 1], 1)
sum_test_vector(messages[1], seeds[1], 2, [0, 1, 2, 3], 2)
sum_test_vector(messages[2], seeds[2], 3, [0, 2, 5, 7], 3)
sum_test_vector(messages[3], seeds[3], 4, [0, 5, 10, 15], 4)
sum_test_vector(messages[4], seeds[4], 5, [0, 10, 21, 31], 5)
sum_test_vector(messages[5], seeds[5], 6, [0, 21, 42, 63], 6)
sum_test_vector(messages[6], seeds[6], 7, [0, 42, 85, 127], 7)
sum_test_vector(messages[7], seeds[7], 8, [0, 85, 170, 255], 8)
sum_test_vector(messages[8], seeds[8], 9, [0, 170, 341, 511], 9)
sum_test_vector(messages[9], seeds[9], 10, [0, 341, 682, 1023], 10)

