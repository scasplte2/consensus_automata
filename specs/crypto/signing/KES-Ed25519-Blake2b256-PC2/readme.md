## Description
Test vectors for Topl implementation of a two tree product key evolving signature in the construction of [Malkin-Micciancio-Miner](https://cseweb.ucsd.edu/~daniele/papers/MMM.pdf). A full specification including protocol box descriptions is available at `papers/kes_formal_spec`

All values below are Hex encoded byte representations unless otherwise specified.

Table of Contents
- [Test vector - 1](#test-vector---1)
- [Test vector - 2](#test-vector---2)
- [Test vector - 3](#test-vector---3)
- [Test vector - 4](#test-vector---4)
- [Test vector - 5](#test-vector---5)
- [Test vector - 6](#test-vector---6)
- [Test vector - 7](#test-vector---7)
- [Test vector - 8](#test-vector---8)
- [Test vector - 9](#test-vector---9)
- [Test vector - 10](#test-vector---10)
- [Test vector - 11](#test-vector---11)
- [Test vector - 12](#test-vector---12)
- [Test vector - 13](#test-vector---13)
- [Test vector - 14](#test-vector---14)
- [Test vector - 15](#test-vector---15)
- [Test vector - 16](#test-vector---16)
- [Test vector - 17](#test-vector---17)
- [Test vector - 18](#test-vector---18)
- [Test vector - 19](#test-vector---19)
- [Test vector - 20](#test-vector---20)

## Test Vector - 1
### Description
Generate and verify a specified signature at `t=0` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(5, 9)
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
superSig: 
    vk     : 5341a0d00b700317420b12614dc34df074b6600c724a0d6d14e48d5d6b13f1ec
    sig    : 71df89cc7a3d2efef4dbbea78e218fb02e98224e4cf3f3dea03ac33e2126715dc118b182339b6610f0b42422f84fe106bf1547dc008f536d8e6605a7df659d0f
    witness: 
        20c389fdd2a1158838c6a9360613af63b652bbb32e5ddfacb9d9d3b264bfbad7
        1b09af6bfa67bc552dfe988b195cfc56842b8d2dfd4393cb39d65ae3f536f444
        82be9fed061437dbc8e4def34e6b62b0b31b10ad0c12e3a29c6c127e174b29f9
        c48c1b5929507328ba3c06778cf01340e5c0f0baa4266011ee7bfa77f9b8908d
        f78af2eeea581c8d9528b73c1ad4f1b64c012f6374a14a79f830f52d3ef478fa
subSig: 
    vk     : 3635de621250f44cebe8bcc3bead7dea8c6dcbb686e38c52ddcb32744000c694
    sig    : 77afaf41afd853c313ccae12dfe2c0cd748f4f6d934c4326a29fc5ec52289fb6edda33c37b27a2a124d190f5b8a313b55a4a690a625f8cd2432e14e4b23ba504
    witness: 
        142f528ba5137889730d25a2220ce5cfa47b43fa5ff8a63f1de29bd04db0da03
        152b26d8fc94280cb283247c75eb8a84aeb73bae07cbf93aa0b838cc798fa59e
        9f2f7e4f1bb778edd2cdc618f07929a4e837c8f7409f679e56ddf11ce0ea43de
        d1a8f6080547e22f8c91492457757c23070c3e5484ccb926e3c9f9323c136277
        6c4d456ea6b7d680d8e417d0fac5a8619096c8cf9d2655e3de0197a598bf6c04
        8b2582f4f8859a40c3ed83062341e03610386b29ffc2c78f19f2e3f1526fec98
        37dacd2bcff52fe4ab19171fe654d00bad32b3acefbc3eea81c169111a1bcb0e
        e073875d9285867946bcc0646682d5714c18af5d624c34cc1dca780f75f009f7
        807e42158dae0527d19c29e0de8b674a1506003b2a0fd56357a3f5262a2c2863
subRoot: 7c90e4b7fee6254fd3b19a93da32fe4b38f16b5f16c6362cf5e45d184275bc19
```
## Test Vector - 2
### Description
Generate and verify a specified signature at `t=100` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(5, 9)
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
superSig: 
    vk     : 5341a0d00b700317420b12614dc34df074b6600c724a0d6d14e48d5d6b13f1ec
    sig    : 71df89cc7a3d2efef4dbbea78e218fb02e98224e4cf3f3dea03ac33e2126715dc118b182339b6610f0b42422f84fe106bf1547dc008f536d8e6605a7df659d0f
    witness: 
        20c389fdd2a1158838c6a9360613af63b652bbb32e5ddfacb9d9d3b264bfbad7
        1b09af6bfa67bc552dfe988b195cfc56842b8d2dfd4393cb39d65ae3f536f444
        82be9fed061437dbc8e4def34e6b62b0b31b10ad0c12e3a29c6c127e174b29f9
        c48c1b5929507328ba3c06778cf01340e5c0f0baa4266011ee7bfa77f9b8908d
        f78af2eeea581c8d9528b73c1ad4f1b64c012f6374a14a79f830f52d3ef478fa
subSig: 
    vk     : 5231ade3d2740ff4bdc287e99a58bd56ec92374864b1d127f1285e157943b0b5
    sig    : c1a9cc3d4cb081b80be98fbd156085071831d017c2767b0da524c02be80e948a2fc1365422c55777a9558948d9d14652e3a1371fb10304563f558afd2e228305
    witness: 
        e98b22232fc5437eff92b806497809db2f3135ab71b97bc2f805b15235f5f0ca
        0daf104308b01c79a7808f543acf0df6567db3d025e45d0d6a0e6055c6e81422
        3a9fe793cd40a147ea48be2e9bc1e36ea6e70e9a73c89b84b7188953c381be9b
        dca51174175f69fc08b299c66a623c43f7e25eaf987045e633495457dae642a7
        27e15fa89c1228ffd59d3a25c533cfd5be827b04b4aae0fbd32f488f8df17fa5
        1fee2ef73c4046a6f823eb67a7c7b1172244fb1ecef4ee092bd1232d133dc771
        4aafbaf11433164d788f5eab6c1ed0453649a66b0514f69595bd3ad1bc06b8a0
        e073875d9285867946bcc0646682d5714c18af5d624c34cc1dca780f75f009f7
        807e42158dae0527d19c29e0de8b674a1506003b2a0fd56357a3f5262a2c2863
subRoot: 7c90e4b7fee6254fd3b19a93da32fe4b38f16b5f16c6362cf5e45d184275bc19
```
## Test Vector - 3
### Description
Generate and verify a specified signature at `t=1000` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(5, 9)
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
superSig: 
    vk     : 02809b50903ef7e9b7fbd0b58d21343b7bc22b82f3a2303462a1b209dd7e1680
    sig    : 3522030d147629bd7cbe714950547d0068892beccdc23d6c04ce16e18df074a99e07483b0d66c725ab7baaa1fcfe1d200436969a1316e06cdb8cdea54fd15b07
    witness: 
        2d01c07011e40a2a4c704465a31cf00362fec8f0101d2c0a90695fe6141e3b9e
        1b09af6bfa67bc552dfe988b195cfc56842b8d2dfd4393cb39d65ae3f536f444
        82be9fed061437dbc8e4def34e6b62b0b31b10ad0c12e3a29c6c127e174b29f9
        c48c1b5929507328ba3c06778cf01340e5c0f0baa4266011ee7bfa77f9b8908d
        f78af2eeea581c8d9528b73c1ad4f1b64c012f6374a14a79f830f52d3ef478fa
subSig: 
    vk     : eab5ac4fbdea4abdb3cb41f1b631be0135467d487fbe8a3d95690a590fe3b914
    sig    : 58643994bf491871f4832d8bde1152d24511fd06060ca831a5cf81678926befda0c5859e2a1cbb620ab31f16fecb41775b2f6ddfe06af226dedae9e1d5cbb909
    witness: 
        b570d287a785cd570091398cdb79eaea6262ea53e03e6104e3ecc87f0eec2b1a
        d7c38397afb518efe4257f1bf6b0aa7d3d2b6290869e94664a9ef21fb40d4477
        16dd122580ff8be52e18399d63434e4b7f85ad56b10812931ff3e4e5a9a4c545
        0fac56d10fdd9a0b62b21903f0f60328e54d8e739336dbab570cef3bd02cc477
        237e7d0d662d731a9ef694b18e07536333aaa9884d734cbef2e615caaf74523a
        baefbb6c243ac1fdfdfdfb554e0a8128edd55fccbf8c23a4513a8149b73d2d13
        39c695f2025bb63522d668a6a21c6654fd87fa48b58487486d852332e1fb1e16
        2670c8fe60d329367121760987270bc315c3932b54fa775e14e5ad00a346a7d9
        35585689b45a8d105e1574af501f1b598ec522044ef90e6d98c49f0ea3a617dd
subRoot: 81d4b9ff3f266b3b996f58a16b779670af9ecab3039c992459a1756a4fc469fb
```
## Test Vector - 4
### Description
Generate and verify a specified signature at `t=10000` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(5, 9)
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
superSig: 
    vk     : 73bbd820fcc162b82b778f5a663a343bef6a2f298799277a166e9e106a626fe8
    sig    : 7ab013374a29b04fa6c17ced560509add4b4dad78590ce7218bcdcbbdff43cbf868656e3a5e278fd7c1315b536c91c2c38ccfce05d5441f75b2dd2da9f3c2001
    witness: 
        4565b493d58888919a2655033bbf82a6e7759adc23458d6ab48ebfd235692bb6
        1d39f1c5cc95c21e59bd499cdaff454a20e41d588879222bdfba13671b4d1890
        ca27359774961846e146909bee8d592a5521762287751d48163287837b9dbdf8
        298a14fb4040c3234dc63560334b80e52eb20511bde6252fbc36300dbf4f4d2d
        02ae690e28498bcc82f35abfffd9df1eeceeddacee9e804c2adf15cf5846873f
subSig: 
    vk     : fcf1a2070e878e9ea91d4d91338ed2adc4ff22a188f45428e17119fd658fbf86
    sig    : fcbc170933bb9b9027b2b1c520772d98ae406103d44caf529bf6fbc6573bdd2ac030ae82bcf3bf796db2ba1187dba3f773b683da566c351e289b66c6a2ceb203
    witness: 
        ce7ec46dc143984669ad58fd57b701306e3bae7517e6011cfd61701c2c1fb70e
        a64275472c7e55ce0853865f786ce36879f0e6e30cc71337ba5bb031a4408460
        1d17a056b6f1c75b9efd8793967aa16f84f18e321374b9300ca7df0736b50815
        4bdc90293ce6823abedf8145d32bfa3144d5cdd28e7144fa73d117f24c34f374
        1fe9375c9e6b4b7d8f91373ac378e629ad6f81842d60b407d10b7de327033066
        cb95dd05dc6371d563c10d813158ccd4f78023374c869652f4a5534b67247470
        8194b36b5286b101ef511b68e0d6bbe9230c3119617971d4bb4355e9b688f92c
        c12950636791f4b1565989161699718964fc927d543f93e2fcd527d68d772773
        526d7f53eceac46811c9bea8c5608a29dddfef4bd4f50d404dbf33adae1ba05b
subRoot: 893a6b48cb64151193e14c884b27aa48f4bd117024314e3a05c1c3482f9d248d
```
## Test Vector - 5
### Description
Generate and verify a specified signature at `t=0` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : cd70c2ca7e7aa30d30a42d3942fc66a61a9c2e529c62d484349eb8f1fc147598
    sig    : 6b0e8491dee6e45b33bcd722830d17ce2aa29ee29c52dc9fc59b81384f50c6db0a44c1672158181c56b3f36ffe8f742291bde78c0e4a464a038fe127b821910d
    witness: 
        e12acecfa9c538e4fc3f5425016d02020a0f02e630ae31cf5c2a05eb00aa1062
        e11c7506a01038764afde8ee51dc83cbf9e139d71ae74de6d9a178275fa66dee
subSig: 
    vk     : 400f9810f44d71a3083b825bf3e7eb1077e601a07e33bea9c2b219b983ba9d5b
    sig    : cd64432855e1cc084d1538e01301e5ebc120fb8900a5f80969623f334c61681c595fde08e74308a12f085203e5d5eadf74ae37e0ba45f5fed36ec23921a32f0c
    witness: 
        771fc11fc0b5e2afff98ad998bc732b77000f0a02e18f840dc43ad9620bb5e32
        632a83885a1e256219d404012874e43ac0c0140a37450ea8c94c54a2ef0e5de6
subRoot: d6d40e62a4657e8b787bf95e48be0294815dc219d6b6cc706f14cffe20283df5
```
## Test Vector - 6
### Description
Generate and verify a specified signature at `t=1` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : cd70c2ca7e7aa30d30a42d3942fc66a61a9c2e529c62d484349eb8f1fc147598
    sig    : 6b0e8491dee6e45b33bcd722830d17ce2aa29ee29c52dc9fc59b81384f50c6db0a44c1672158181c56b3f36ffe8f742291bde78c0e4a464a038fe127b821910d
    witness: 
        e12acecfa9c538e4fc3f5425016d02020a0f02e630ae31cf5c2a05eb00aa1062
        e11c7506a01038764afde8ee51dc83cbf9e139d71ae74de6d9a178275fa66dee
subSig: 
    vk     : 8b68125a2c08153f09b4b796975f3901813c3f37d9ba681152b3d4628bbbb039
    sig    : b0faf57d6490f6946e3a87ca99c8315925bb57bdbd4ee8bd6fefebfbb55b9d03a2311fd8cae36ed8c209c6f1caa29ceafc3c936f3964eb8f45bd456e991ade05
    witness: 
        8fdd02f07eeb535bab4ec29a37f2205af19bc37996618518dacfbf6d8ffe6ad9
        632a83885a1e256219d404012874e43ac0c0140a37450ea8c94c54a2ef0e5de6
subRoot: d6d40e62a4657e8b787bf95e48be0294815dc219d6b6cc706f14cffe20283df5
```
## Test Vector - 7
### Description
Generate and verify a specified signature at `t=2` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : cd70c2ca7e7aa30d30a42d3942fc66a61a9c2e529c62d484349eb8f1fc147598
    sig    : 6b0e8491dee6e45b33bcd722830d17ce2aa29ee29c52dc9fc59b81384f50c6db0a44c1672158181c56b3f36ffe8f742291bde78c0e4a464a038fe127b821910d
    witness: 
        e12acecfa9c538e4fc3f5425016d02020a0f02e630ae31cf5c2a05eb00aa1062
        e11c7506a01038764afde8ee51dc83cbf9e139d71ae74de6d9a178275fa66dee
subSig: 
    vk     : de314d2f2b7cbfb629513dbf80ad6326a0c8636c1295fe51ab0e5806c9bf0951
    sig    : e82ab7c4be3e060fdfabff244c6f275cf6885c6175b6ae56eab34b4e8ab48b7c341f00d0f444fb4691b12d30c7634e9bc6fa32ef67c94a8eec09da3abdf1e501
    witness: 
        196e302e294309da07b768fdf74c1d1f6dcaa892ef9d183f9ffebb2022ba483e
        023b29fbf6e126ffbd61b88fb23aedc289a4fa288b6aa5f715304c916a33adca
subRoot: d6d40e62a4657e8b787bf95e48be0294815dc219d6b6cc706f14cffe20283df5
```
## Test Vector - 8
### Description
Generate and verify a specified signature at `t=3` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : cd70c2ca7e7aa30d30a42d3942fc66a61a9c2e529c62d484349eb8f1fc147598
    sig    : 6b0e8491dee6e45b33bcd722830d17ce2aa29ee29c52dc9fc59b81384f50c6db0a44c1672158181c56b3f36ffe8f742291bde78c0e4a464a038fe127b821910d
    witness: 
        e12acecfa9c538e4fc3f5425016d02020a0f02e630ae31cf5c2a05eb00aa1062
        e11c7506a01038764afde8ee51dc83cbf9e139d71ae74de6d9a178275fa66dee
subSig: 
    vk     : 377f52d8a60c8bda36ea45a2548c8fd9c3df0332763936e1306c7bf271fd0df8
    sig    : 73dd29405ed440d7aa33ae65f48b6f77f7566674cbb09dc56b46676cd33cffdb7b3d85304441b297ac0fe2489a0a99a99fff18895e49fe751b9d534170768c0d
    witness: 
        eb0260cebd9f572dfedb8177ba65dd1dc6b18f2c474afaf8495327eff638666e
        023b29fbf6e126ffbd61b88fb23aedc289a4fa288b6aa5f715304c916a33adca
subRoot: d6d40e62a4657e8b787bf95e48be0294815dc219d6b6cc706f14cffe20283df5
```
## Test Vector - 9
### Description
Generate and verify a specified signature at `t=4` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : cd1e480e6b8ea5ad623a0c94e369d10c49fb03141f12dc101ef3e68cae893d74
    sig    : 71352a07fc6668ae2630b9395497ce507213065bbffbb8b24d61ad51a8203322cec890e082565efa5c0f9336893e72cdb920a7e1bdb924a67485b38bd87b5f04
    witness: 
        8810074f64014c5e936d8cb9149111315846b06189e994aaf02fcc7589531e46
        e11c7506a01038764afde8ee51dc83cbf9e139d71ae74de6d9a178275fa66dee
subSig: 
    vk     : fd6f7231b2dd6bb643f136f70b902182e293861cdcb7b5958b64e0a26a59aabb
    sig    : 6c9ac95796e9b452b4129fbd829321e8a6284dfa194b4bf259fea140a1363808221dfe34afaa7331e6cf9701892642bad24282f1afe272788ddfb7977e39ff0a
    witness: 
        73f408ffa177d3db68320e4d6c481dc5dcc991b479c563782e263c27babf59e4c3d325ec8fdb1974d25b8a9fd30799e5d82a1701ce40cfd5c99b61db71590a53
subRoot: c3a937f515f361c521b981e9490183ef09b7ece84d70f3ccbfaade0193765939
```
## Test Vector - 10
### Description
Generate and verify a specified signature at `t=5` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : cd1e480e6b8ea5ad623a0c94e369d10c49fb03141f12dc101ef3e68cae893d74
    sig    : 71352a07fc6668ae2630b9395497ce507213065bbffbb8b24d61ad51a8203322cec890e082565efa5c0f9336893e72cdb920a7e1bdb924a67485b38bd87b5f04
    witness: 
        8810074f64014c5e936d8cb9149111315846b06189e994aaf02fcc7589531e46
        e11c7506a01038764afde8ee51dc83cbf9e139d71ae74de6d9a178275fa66dee
subSig: 
    vk     : da796c3c4faf0f0ca5d0fcfa70da49b684e879e9908540ff2fccaec5c168abef
    sig    : ca4f20fc83b5d726388295af5962a5cf18b9f8ed0bf5e7a91ca13282c2ddfbe75974decf4f13af0e04e1dae274f7e86a20a3da48e52ef79f31b27c62a641c70f
    witness: 
        2a0b1968f37875d650d8f02869d7adfffa270072d960841068caa2f1d5d90af3
        c3d325ec8fdb1974d25b8a9fd30799e5d82a1701ce40cfd5c99b61db71590a53
subRoot: c3a937f515f361c521b981e9490183ef09b7ece84d70f3ccbfaade0193765939
```
## Test Vector - 11
### Description
Generate and verify a specified signature at `t=6` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : cd1e480e6b8ea5ad623a0c94e369d10c49fb03141f12dc101ef3e68cae893d74
    sig    : 71352a07fc6668ae2630b9395497ce507213065bbffbb8b24d61ad51a8203322cec890e082565efa5c0f9336893e72cdb920a7e1bdb924a67485b38bd87b5f04
    witness: 
        8810074f64014c5e936d8cb9149111315846b06189e994aaf02fcc7589531e46
        e11c7506a01038764afde8ee51dc83cbf9e139d71ae74de6d9a178275fa66dee
subSig: 
    vk     : 11ec807feeffef60aa6bda29e00aa3ee44c58b777517d9cf50bc1cb765a17c6b
    sig    : 41a3bf23cef17d27c20da1a85442c103dbf1f3cd40223ef024449c6bd3eeeac4047b2f39c0f2da23bd7dc2ade5c19138143b5321e32bd798fc04feeac333e40b
    witness: 
        aec61259a4029713d52eb00cbcb0d4020feb7ff574dc7400c10952f30d13ba2a
        96bbeaa330c862b16e7027157d7396edf58f3a95bd61c94722ffffa850611c62
subRoot: c3a937f515f361c521b981e9490183ef09b7ece84d70f3ccbfaade0193765939
```
## Test Vector - 12
### Description
Generate and verify a specified signature at `t=7` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : cd1e480e6b8ea5ad623a0c94e369d10c49fb03141f12dc101ef3e68cae893d74
    sig    : 71352a07fc6668ae2630b9395497ce507213065bbffbb8b24d61ad51a8203322cec890e082565efa5c0f9336893e72cdb920a7e1bdb924a67485b38bd87b5f04
    witness: 
        8810074f64014c5e936d8cb9149111315846b06189e994aaf02fcc7589531e46
        e11c7506a01038764afde8ee51dc83cbf9e139d71ae74de6d9a178275fa66dee
subSig: 
    vk     : 035aea2adbf42f0a9ad583a43507284dc18cd29c555ec34d86473dc614999dc0
    sig    : b372f56ab73b2d31a6ae5325141bfd074ecc1626f9720a21004a3ef2d4eafe3f8a3146e30410ae3b4be5a069fac49e2737ea936a3213cbfdb9f53c628934a005
    witness: 
        427e29b5b45d60ec17b66a042ec712e8e3dd5ae5283ad078ca5fbd7c9139fc49
        96bbeaa330c862b16e7027157d7396edf58f3a95bd61c94722ffffa850611c62
subRoot: c3a937f515f361c521b981e9490183ef09b7ece84d70f3ccbfaade0193765939
```
## Test Vector - 13
### Description
Generate and verify a specified signature at `t=8` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : c7f53fc20220c285436a69b965f623bac27206aebef3869166a34f9787c4eae0
    sig    : a85fd9344308da548684e66804755ddf906dd3afa809c25030d1c877a43e80c95bd1b0855cd4cf79a2536ef7efe17fb646da4c9a347e803f1aab4b404eda570e
    witness: 
        6124e45fc2767fd95ee865e3f44c6a40dbbfc9f97755eb5fcb75e9b5e765292b
        bad815791cc77037f445e4cdb13814330d64f558e719f689063fe54d99c68ab3
subSig: 
    vk     : 909746adb18644d7fa05635a1168f60759442d6b396aab16fd7cfc1ed229fc1b
    sig    : 6a4b2282f4e09e23fccef406d6da0f96b701cb86cb872534f86f2f65f04e6b974eb897e0f7d23d090b36627cf7b4da36cdba2bf993237360edb9a1d173318b0b
    witness: 
        907227db62752945a085e116f1e03dd301e482c793614012e2dd7e6a6d56bffe
        36f4d2179dc55404242e651e1bfa08888519d9afe3e5d8f24260e3591a26378b
subRoot: b7bf456b91cf1ee2fe2e53b85a7c05699001838ddde1a0bfc02b82ad0ff48afe
```
## Test Vector - 14
### Description
Generate and verify a specified signature at `t=9` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : c7f53fc20220c285436a69b965f623bac27206aebef3869166a34f9787c4eae0
    sig    : a85fd9344308da548684e66804755ddf906dd3afa809c25030d1c877a43e80c95bd1b0855cd4cf79a2536ef7efe17fb646da4c9a347e803f1aab4b404eda570e
    witness: 
        6124e45fc2767fd95ee865e3f44c6a40dbbfc9f97755eb5fcb75e9b5e765292b
        bad815791cc77037f445e4cdb13814330d64f558e719f689063fe54d99c68ab3
subSig: 
    vk     : dc37313f4f4e94c221c7a1f6b7b7caec245fc9884e5146e40a12b31eaa246bd9
    sig    : 9fa7e9be4a3629e19dcd8f9001bed3dc657503bdb2120fa6cda801b814fa0385e34b6a41715da778fd63e5b8afed126a3ae34af6eb1192b99d2bb78bf569b00f
    witness: 
        8dc6d93c6d0f4c5c5707b16ef33e57b05ccb70b7255a7e2578134adadaf068c5
        36f4d2179dc55404242e651e1bfa08888519d9afe3e5d8f24260e3591a26378b
subRoot: b7bf456b91cf1ee2fe2e53b85a7c05699001838ddde1a0bfc02b82ad0ff48afe
```
## Test Vector - 15
### Description
Generate and verify a specified signature at `t=10` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : c7f53fc20220c285436a69b965f623bac27206aebef3869166a34f9787c4eae0
    sig    : a85fd9344308da548684e66804755ddf906dd3afa809c25030d1c877a43e80c95bd1b0855cd4cf79a2536ef7efe17fb646da4c9a347e803f1aab4b404eda570e
    witness: 
        6124e45fc2767fd95ee865e3f44c6a40dbbfc9f97755eb5fcb75e9b5e765292b
        bad815791cc77037f445e4cdb13814330d64f558e719f689063fe54d99c68ab3
subSig: 
    vk     : ac7d5440d96aead889564622df2d297d02a599ff51611c1b392aba9319ed7622
    sig    : 1eb966d0f02812d957e7a995ef04a61e828aec1c76bffdadf608dc09a1e45b81a05b5df5985ae022551b3ea1bb1a61ae147ffde149038de26ffb145b3eed2c0c
    witness: 
        f9e842372c0b6d0684cc2c7b72c167b32594359f22c167cad1c4d955f22dc3b5
        3594e6bb41a6603b5202a3a1af6a497539fdc4b1f1fc9cdcad6db95d664e5f07
subRoot: b7bf456b91cf1ee2fe2e53b85a7c05699001838ddde1a0bfc02b82ad0ff48afe
```
## Test Vector - 16
### Description
Generate and verify a specified signature at `t=11` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : c7f53fc20220c285436a69b965f623bac27206aebef3869166a34f9787c4eae0
    sig    : a85fd9344308da548684e66804755ddf906dd3afa809c25030d1c877a43e80c95bd1b0855cd4cf79a2536ef7efe17fb646da4c9a347e803f1aab4b404eda570e
    witness: 
        6124e45fc2767fd95ee865e3f44c6a40dbbfc9f97755eb5fcb75e9b5e765292b
        bad815791cc77037f445e4cdb13814330d64f558e719f689063fe54d99c68ab3
subSig: 
    vk     : ea00e819c7c5f084d0970f33f85ea57ad495ccf5fff3f4348db9210d2436199c
    sig    : d7896635aaaf5e83164c3bd23f4f82f57537274630dd739144814a623e910cd80f4aa2b69716ea5bb76c8b1c2c3881bbb7c2bc56d0a0db8629241ccb49a5000b
    witness: 
        f39760c7bbf16fcd8c55843bc8a4d83df245833e4b1b83acd1439b871ea0887a
        3594e6bb41a6603b5202a3a1af6a497539fdc4b1f1fc9cdcad6db95d664e5f07
subRoot: b7bf456b91cf1ee2fe2e53b85a7c05699001838ddde1a0bfc02b82ad0ff48afe
```
## Test Vector - 17
### Description
Generate and verify a specified signature at `t=12` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : 20cd480cb6301921de265b521282101868546dda12324612ff680eb8a087fdeb
    sig    : ca39f7ee313f526d1d9ea7a72afc1adea8cdace953430e3f8a6192071b2556c2dfc86316f8b97c84b9fa1e2e1f9c8b1427cc948b19279d71cc9bd2a78c09450d
    witness: 
        1191de3c853856f921ba6e7d2af912b85c57ab63309c26e1bb20eedc5da46ec5
        bad815791cc77037f445e4cdb13814330d64f558e719f689063fe54d99c68ab3
subSig: 
    vk     : 5f15882e6a1df6fe87256aa55c06723b4c115ce6e17e1ca356ecc0eefa6de978
    sig    : b72990cdb8fd4b878dd7da8abe8a74bc5f22a78b86ae089daf4e0b196a5784fad1eeb4b52765c75f43d1c8682826b1888926759c89888d43c180e3de91238e06
    witness: 
        0f3db5877d0d277d829ca7a4c6658b25b50f05e6f8705a077054ccf96f8aaffc
        0587141592eb1c3acedf8e4396a676fa6d208ef80707b4f5d5b315bc6a2cd25b
subRoot: b54941cdab70926043c01528a6f2140becf23bbb54a6967c1c03deeccc4d9552
```
## Test Vector - 18
### Description
Generate and verify a specified signature at `t=13` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : 20cd480cb6301921de265b521282101868546dda12324612ff680eb8a087fdeb
    sig    : ca39f7ee313f526d1d9ea7a72afc1adea8cdace953430e3f8a6192071b2556c2dfc86316f8b97c84b9fa1e2e1f9c8b1427cc948b19279d71cc9bd2a78c09450d
    witness: 
        1191de3c853856f921ba6e7d2af912b85c57ab63309c26e1bb20eedc5da46ec5
        bad815791cc77037f445e4cdb13814330d64f558e719f689063fe54d99c68ab3
subSig: 
    vk     : d539e0e9eeae1cbe9e6bdbde6290813878e01ca893fc66c05e6df9cb9051026a
    sig    : 02f927ae52ad54eea3be82f1e6b9e7d87cc1ba4e2298061d3056ab5d9f0ab5f98b9a1a6a303395cc587f62c51215c18f630b38cf1676761abac7ff1b1c361d0c
    witness: 
        e23027eba091ea26e9b320430d18a14600fcd6fc0ad68598d9b4d01572980266
        0587141592eb1c3acedf8e4396a676fa6d208ef80707b4f5d5b315bc6a2cd25b
subRoot: b54941cdab70926043c01528a6f2140becf23bbb54a6967c1c03deeccc4d9552
```
## Test Vector - 19
### Description
Generate and verify a specified signature at `t=14` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : 20cd480cb6301921de265b521282101868546dda12324612ff680eb8a087fdeb
    sig    : ca39f7ee313f526d1d9ea7a72afc1adea8cdace953430e3f8a6192071b2556c2dfc86316f8b97c84b9fa1e2e1f9c8b1427cc948b19279d71cc9bd2a78c09450d
    witness: 
        1191de3c853856f921ba6e7d2af912b85c57ab63309c26e1bb20eedc5da46ec5
        bad815791cc77037f445e4cdb13814330d64f558e719f689063fe54d99c68ab3
subSig: 
    vk     : 362a3f71774fe220e0548569dd5ae31ddea2432a50dd1a944dd051dcd018bb08
    sig    : 1e25a05567b2ee652a71a0a841b2ca5bf9158f170eb4377c0e39876dd53f9e7f70e672ad8f0969b41c7666831536abd2b3775eaaea6764eafa67d357ec3b5106
    witness: 
        455117c29e74eb92a1e0d839d54ae8a9351ec945c8d55ef9fa9d0bad7be65676
        41ac461346992772b1f1a731bc77f3e95ce23fc8b390862dccdfce8f2a879df4
subRoot: b54941cdab70926043c01528a6f2140becf23bbb54a6967c1c03deeccc4d9552
```
## Test Vector - 20
### Description
Generate and verify a specified signature at `t=15` using a provided seed, message, and height
### Inputs
- seed
```
928b20366943e2afd11ebc0eae2e53a93bf177a4fcf35bcc64d503704e65e202
```
- height (super: Int, sub: Int)
```
(2, 2)
```
- message
```
6d657373616765
```
### Outputs
- vk
```
2054136f5b6c9fd65e0d0ed4e44996fae4c1e34b7b5f6acb18c29c3f79abd7d4
```
- sig
```
superSig: 
    vk     : 20cd480cb6301921de265b521282101868546dda12324612ff680eb8a087fdeb
    sig    : ca39f7ee313f526d1d9ea7a72afc1adea8cdace953430e3f8a6192071b2556c2dfc86316f8b97c84b9fa1e2e1f9c8b1427cc948b19279d71cc9bd2a78c09450d
    witness: 
        1191de3c853856f921ba6e7d2af912b85c57ab63309c26e1bb20eedc5da46ec5
        bad815791cc77037f445e4cdb13814330d64f558e719f689063fe54d99c68ab3
subSig: 
    vk     : 1bc13cd6eba707385bbef73385764d1e8ecd7acbc94a7209cf3fea7c629fc985
    sig    : 68483f79dcc1b864673f1249102f5c9711214b852a3de31fdb9c8940b8d7f4c3035ede99d086ed7616880a73e58a7c50b37096e02daf46d666ab72844cb26708
    witness: 
        0faa3127cb4b57238c8ba696dc1327819a0a07155ef1b9912f22068bd723b64c
        41ac461346992772b1f1a731bc77f3e95ce23fc8b390862dccdfce8f2a879df4
subRoot: b54941cdab70926043c01528a6f2140becf23bbb54a6967c1c03deeccc4d9552
```
