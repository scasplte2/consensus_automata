## Description
Test vectors for Topl implementation of a single tree key evolving signature in the construction of [Malkin-Micciancio-Miner](https://cseweb.ucsd.edu/~daniele/papers/MMM.pdf). A full specification including protocol box descriptions is available at ???.

All values below are Hex encoded byte representations unless otherwise specified.

## Test Vector - 1
### Description
Generate and verify a specified signature at `t=0` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (int)
```
7
```
- time step (int)
```
0
```
- message
```
6d657373616765
```
### Outputs
- vk
```
23d72240b54a6135ec7ca96013d2e4edacefc2ccad2aac861430eeb9286b4ae6
```
- sig
```
vk     : fce14b4bb0ccc19079263a8115a13fb9cf015c76f16abccb9b5ce91a9e866e6d
sig    : 90107bbc5a7d6fd9747f6076e107ce2243d635bfa5439af2464346517405420116c5135c5fa10c9468086fe8d2998a3a04e39efe5971868e4f95fe127ac81709
witness: 
    92897adc1a78d0225cd2a3ec84b94b84ac2cf175b9809aeeebea18f9958552f0
    64142027adac58b88711a61e4ca6675d16a02755fb87871d8b676ecbe829fc8a
    1c62dc579ea9b9aae5ca65998256f5a702c9cea2125f24927efd92ee97777705
    490975d0f3d5a6a99e1302a2adbff0604441f13c6b13f6d99e45d51532ba0dae
    8be89df4800275fcaf3426ce8f3b0318cc19a23274474e74e56c6d38d6ad03a0
    8592a55902f5f3ab6d2247585c5472c1d9f2132481a3d5cc39a7ff5edf435491
    9f2ed5b9d1df27926d225f8eb41c426254d4218e054f5c4a102eeccb58876596
```
## Test Vector - 2
### Description
Generate and verify a specified signature at `t=1` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (int)
```
7
```
- time step (int)
```
1
```
- message
```
6d657373616765
```
### Outputs
- vk
```
23d72240b54a6135ec7ca96013d2e4edacefc2ccad2aac861430eeb9286b4ae6
```
- sig
```
vk     : 8ad3faaeac74cd22846f2eaefa87d41f520a804c1a8c92d7eca338634e652fbd
sig    : d634d8527d79f7ee79ee1f1dfba3aa4da524b45679227ff948304820bc608409adc1444d9f369b3c1afbb720d27a32397212273f77e7f427570d4ce8a935fe0e
witness: 
    955ce11603b1ed207b11904e7bec4b5ca1985a64e2e18fd3d109854403f7bec0
    64142027adac58b88711a61e4ca6675d16a02755fb87871d8b676ecbe829fc8a
    1c62dc579ea9b9aae5ca65998256f5a702c9cea2125f24927efd92ee97777705
    490975d0f3d5a6a99e1302a2adbff0604441f13c6b13f6d99e45d51532ba0dae
    8be89df4800275fcaf3426ce8f3b0318cc19a23274474e74e56c6d38d6ad03a0
    8592a55902f5f3ab6d2247585c5472c1d9f2132481a3d5cc39a7ff5edf435491
    9f2ed5b9d1df27926d225f8eb41c426254d4218e054f5c4a102eeccb58876596
```
## Test Vector - 3
### Description
Generate and verify a specified signature at `t=10` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (int)
```
7
```
- time step (int)
```
10
```
- message
```
6d657373616765
```
### Outputs
- vk
```
23d72240b54a6135ec7ca96013d2e4edacefc2ccad2aac861430eeb9286b4ae6
```
- sig
```
vk     : 734b26feb6c78e663e0476985aa6163610f24bfad413aac1dd528fdd810bcf94
sig    : 682ac31eae1ad22025870097a8ed50d52a81842c53c89a96cc32bcdd5e5df7daa59154d66209b9d7f1a15c54b4bfd8c852075733b811d75c2a5fe6242e844d02
witness: 
    99280da00680942b45c7ce1face17413e280011bacadf1970099df137f7e23cd
    9ee0b4b3911ea215d5936e98cf4b8bc127f9ae304ea078f937d386185e3827dc
    f8021233d3de0d5fc40ac9064e6934a4dafd2a0a442619f7ef02e0e5bac22b8b
    8b88e3730f40d7aca97cbc7ae8c5da87fe004445e711233b0a8d2f1952b79655
    8be89df4800275fcaf3426ce8f3b0318cc19a23274474e74e56c6d38d6ad03a0
    8592a55902f5f3ab6d2247585c5472c1d9f2132481a3d5cc39a7ff5edf435491
    9f2ed5b9d1df27926d225f8eb41c426254d4218e054f5c4a102eeccb58876596
```
## Test Vector - 4
### Description
Generate and verify a specified signature at `t=100` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (int)
```
7
```
- time step (int)
```
100
```
- message
```
6d657373616765
```
### Outputs
- vk
```
23d72240b54a6135ec7ca96013d2e4edacefc2ccad2aac861430eeb9286b4ae6
```
- sig
```
vk     : 31439986a2c4a60f2c21b8ef73714305b97212ed69c539d804310df2dd2fa937
sig    : 66de8606af1ad8d39eaf0374ed195df9d883badf968fd5a26295a6e4f390658c390d3ec1da812a93ad9118a373bf544941073643364f451de0018bd18619cb09
witness: 
    8323964e90a191163d041a65b7892b0ecc0e0f3eb6c0354fc5c24a05567d21b1
    4e9903919fa12296699360b7edf2fce299553e29265ac3c63896ca70940b4e1c
    eaccd7fd90deae8a2f9998a653acae63a446b372a603ce6bae5a4beaa2df2563
    01483655546cbb36fa2dafca28168b3c48969664e4c1d4ee90306a2e111f4ce3
    67a86e2d941dc917affb31ffe23bf21fb7e5716bda7b351bd69277212be33d0e
    6f75812121ddf093a6195d93bb6aca4a9e0340cdb4188857f8681b758be28a52
    4fef963016cf2e19cfa3920ab5bf2a1413f40d527327aeb2d2f0a8298c345b93
```
## Test Vector - 5
### Description
Generate and verify a specified signature at `t=0` using a provided seed, message, and height
### Inputs
- seed
```
45f3d3ed97ca49b86f1ae514e55e69e0fba32124aa23eb4b70260f89f259271b
```
- height (int)
```
2
```
- time step (int)
```
0
```
- message
```
6d657373616765
```
### Outputs
- vk
```
f7048e1396222415e93193e78bed2c309c29e11996989a467dda416030be6271
```
- sig
```
vk     : 50cd517ae5d9118bef024e4947feca04c893636370ca973958b8e8fc784badd4
sig    : 5c4c7bc45754be614a1aaf28c1e271e8c5a3b4378a8fe2fed05bbc7c9f7209d6deeced944680bb36fe547496592b0a45be3c40ab513bc2ba432ca1e8ed9fa908
witness: 
    306ab72a51abb7736951b9bb8760ee608219f456c99b765a4f2ff46a59895c3c
    e6c4fad6f115d1c24da11a42fe1e9ad893ecede63d661e8cf4207b182cbcc124
```
## Test Vector - 6
### Description
Generate and verify a specified signature at `t=1` using a provided seed, message, and height
### Inputs
- seed
```
45f3d3ed97ca49b86f1ae514e55e69e0fba32124aa23eb4b70260f89f259271b
```
- height (int)
```
2
```
- time step (int)
```
1
```
- message
```
6d657373616765
```
### Outputs
- vk
```
f7048e1396222415e93193e78bed2c309c29e11996989a467dda416030be6271
```
- sig
```
vk     : 23805967370c5e2365e6fd6a4ebbf6a815caaabeee9bd1e1f073b168b8604412
sig    : b1a594b4d090fcae271587f43c787a7a99ba23bf19c8abc1cb52a614eaa91d99c6a18eb12eee582358d6f301d81f1e040a2214d19a61d632d7ef38402707b607
witness: 
    a67aa79f856ce1268d48fdf659354ccc70c383eca31afec8978c82c770b0ebd9
    e6c4fad6f115d1c24da11a42fe1e9ad893ecede63d661e8cf4207b182cbcc124
```
## Test Vector - 7
### Description
Generate and verify a specified signature at `t=2` using a provided seed, message, and height
### Inputs
- seed
```
45f3d3ed97ca49b86f1ae514e55e69e0fba32124aa23eb4b70260f89f259271b
```
- height (int)
```
2
```
- time step (int)
```
2
```
- message
```
6d657373616765
```
### Outputs
- vk
```
f7048e1396222415e93193e78bed2c309c29e11996989a467dda416030be6271
```
- sig
```
vk     : f79c37329c6af0fcab56470dd88622780212f1542959d5470e25dcf20c83fb70
sig    : b8e9d085839ca0948c7e66fd009efa2c3918f850fb937549a162ef9e140278c018ae8147981d6cb7bb35756992fb7afd90473ad292738a7c6e97a93715b1120a
witness: 
    8b4e4e018c976d01d661e0449cf2b351903f4df950d5c26608d527d12fceecae
    abb00c9449578442a966f6e2482a454608f2536d90cd912db7a67bec7fd8c5a4
```
## Test Vector - 8
### Description
Generate and verify a specified signature at `t=3` using a provided seed, message, and height
### Inputs
- seed
```
45f3d3ed97ca49b86f1ae514e55e69e0fba32124aa23eb4b70260f89f259271b
```
- height (int)
```
2
```
- time step (int)
```
3
```
- message
```
6d657373616765
```
### Outputs
- vk
```
f7048e1396222415e93193e78bed2c309c29e11996989a467dda416030be6271
```
- sig
```
vk     : 05a5b1306d00c18df680c7fc0791cd0b1f30b96b365bdb2d766a3f621f209d7a
sig    : 0cad034776232efb95b4732665d2a0477fa107c089b4248fe96c68a3950bbc36195bb53e13bd7da4ac7f3fd11cad79737901347f88490cb104ddfbb7a695b405
witness: 
    9a94aaf251089e0c6e9d80b5038a2fa24a1fb5d44b82a244fc2416c63c6a93e8
    abb00c9449578442a966f6e2482a454608f2536d90cd912db7a67bec7fd8c5a4
```