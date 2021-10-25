## Description
Test vectors for Topl implementation of ExtendedEd25519. This implementation conforms to [SLIP-0023](https://github.com/satoshilabs/slips/blob/master/slip-0023.md) using the Icarus process for seed -> master key (root key) generation and [Bip32-Ed25519](https://raw.githubusercontent.com/input-output-hk/adrestia/master/user-guide/static/Ed25519_BIP.pdf) for child key derivation.

All values below are Hex encoded byte representations unless otherwise specified.

## Test Vector - 1
### Description
Generate the correct master secret key from a given seed with an empty password [[ref](https://github.com/cardano-foundation/CIPs/blob/master/CIP-0003/Icarus.md#test-vectors)]
### Inputs
- seed:
```

```
- password:
```
""
```

### Outputs
- xsk:
```
leftKey  : c065afd2832cd8b087c4d9ab7011f481ee1e0721e78ea5dd609f3ab3f156d245
rightKey : d176bd8fd4ec60b4731c3918a2a72a0226c0cd119ec35b47e4d55884667f552a
chainCode: 23f7fdcd4a10c6cd2c7393ac61d877873e248f417634aa3d812af327ffe9d620
```
## Test Vector - 2
### Description
Generate the correct master secret key from a given seed and a non-empty pasword [[ref](https://github.com/cardano-foundation/CIPs/blob/master/CIP-0003/Icarus.md#test-vectors)]
### Inputs
- seed:
```

```
- password: (utf8 string)
```
"foo"
```
### Outputs
- xsk:
```
leftKey  : 70531039904019351e1afb361cd1b312a4d0565d4ff9f8062d38acf4b15cce41
rightKey : d7b5738d9c893feea55512a3004acb0d222c35d3e3d5cde943a15a9824cbac59
chainCode: 443cf67e589614076ba01e354b1a432e0e6db3b59e37fc56b5fb0222970a010e
```
## Test Vector - 3
### Description
Verify the correctness of a signature generated with an empty message given a specified extended secret key
### Inputs
- xsk:
```
leftKey  : 52f9f8c55ef9646976ee4bf8a4d10b3cdf15cfe99d899b9e6e5a0d9c77534940
rightKey : 411e817aa4047dfb9cb11cf83f1cca23079446879299e11558bcd24bcf418b15
chainCode: 936fb3418dcdf821f589fc2a5b553a094918cf69ca5e10a30e644708ab55d9aa
```
- message (length 0 bytes)
### Outputs
- xvk
```
vk       : d4d38ed7e78f2ec724b129a6842c60805d793e6731f728c8da8b310b9024f6b7
chainCode: 936fb3418dcdf821f589fc2a5b553a094918cf69ca5e10a30e644708ab55d9aa
```
- sig
```
a9821dc3aa74dbf5c1253989adf49863b0b8a761ee157ee8a10af751ec15fe417f8fc605074abeb1b3a6655871f98510d77f45031ad8b0f62b562afc90eeea0c
```
## Test Vector - 4
### Description
Verify the correctness of a signature generated with a small message given a specified extended secret key
### Inputs
- xsk:
```
leftKey  : 5d3485e54cda23759294fd0c0b46aba088e545171fdfca19aaf6c731ce4f4fe0
rightKey : ac2471e35549b1ff5ac37074ce78bdd31c272c6a29b05532bd32058e19dbc731
chainCode: bb8c3ca396a73fceb5111d1b12d8049ac8b1789be308c063b2e5a9b6e5a8c764
```
- message
```
72
```
### Outputs
- xvk
```
vk       : a2886648ddd536f2bfc3f766ba0944c4aa06bfea5ba9aae073b31e7d7c15e551
chainCode: bb8c3ca396a73fceb5111d1b12d8049ac8b1789be308c063b2e5a9b6e5a8c764
```
- sig
```
fbbbca775152d6edc69e35f34da1751f6f0f4ec74384a4dd21493c1e3c6f346d1976a76a936a01cb313425970290e9c7bac33b52449e04f66d667e16d181ef0c
```
## Test Vector - 5
### Description
Verify the correctness of a signature generated with a large message given a specified extended secret key
### Inputs
- xsk:
```
leftKey  : 59584a6365c160225924e734b5e5b7b4648eb9807fc0b48546e496a3186f4b68
rightKey : d05dea47c2f6d0cfc1d77183937e4ab198d94fe8f4fa34afe226fca6b7f26d32
chainCode: 64c5e1ffad57e36b0e9fa3a4fb268da0c134fe3ea472dbf124215b2df1d4c40e
```
- message:
```
08b8b2b733424243760fe426a4b54908632110a66c2f6591eabd3345e3e4eb98fa6e264bf09efe12ee50f8f54e9f77b1e355f6c50544e23fb1433ddf73be84d8
79de7c0046dc4996d9e773f4bc9efe5738829adb26c81b37c93a1b270b20329d658675fc6ea534e0810a4432826bf58c941efb65d57a338bbd2e26640f89ffbc
1a858efcb8550ee3a5e1998bd177e93a7363c344fe6b199ee5d02e82d522c4feba15452f80288a821a579116ec6dad2b3b310da903401aa62100ab5d1a36553e
06203b33890cc9b832f79ef80560ccb9a39ce767967ed628c6ad573cb116dbefefd75499da96bd68a8a97b928a8bbc103b6621fcde2beca1231d206be6cd9ec7
aff6f6c94fcd7204ed3455c68c83f4a41da4af2b74ef5c53f1d8ac70bdcb7ed185ce81bd84359d44254d95629e9855a94a7c1958d1f8ada5d0532ed8a5aa3fb2
d17ba70eb6248e594e1a2297acbbb39d502f1a8c6eb6f1ce22b3de1a1f40cc24554119a831a9aad6079cad88425de6bde1a9187ebb6092cf67bf2b13fd65f270
88d78b7e883c8759d2c4f5c65adb7553878ad575f9fad878e80a0c9ba63bcbcc2732e69485bbc9c90bfbd62481d9089beccf80cfe2df16a2cf65bd92dd597b07
07e0917af48bbb75fed413d238f5555a7a569d80c3414a8d0859dc65a46128bab27af87a71314f318c782b23ebfe808b82b0ce26401d2e22f04d83d1255dc51a
ddd3b75a2b1ae0784504df543af8969be3ea7082ff7fc9888c144da2af58429ec96031dbcad3dad9af0dcbaaaf268cb8fcffead94f3c7ca495e056a9b47acdb7
51fb73e666c6c655ade8297297d07ad1ba5e43f1bca32301651339e22904cc8c42f58c30c04aafdb038dda0847dd988dcda6f3bfd15c4b4c4525004aa06eeff8
ca61783aacec57fb3d1f92b0fe2fd1a85f6724517b65e614ad6808d6f6ee34dff7310fdc82aebfd904b01e1dc54b2927094b2db68d6f903b68401adebf5a7e08
d78ff4ef5d63653a65040cf9bfd4aca7984a74d37145986780fc0b16ac451649de6188a7dbdf191f64b5fc5e2ab47b57f7f7276cd419c17a3ca8e1b939ae49e4
88acba6b965610b5480109c8b17b80e1b7b750dfc7598d5d5011fd2dcc5600a32ef5b52a1ecc820e308aa342721aac0943bf6686b64b2579376504ccc493d97e
6aed3fb0f9cd71a43dd497f01f17c0e2cb3797aa2a2f256656168e6c496afc5fb93246f6b1116398a346f1a641f3b041e989f7914f90cc2c7fff357876e506b5
0d334ba77c225bc307ba537152f3f1610e4eafe595f6d9d90d11faa933a15ef1369546868a7f3a45a96768d40fd9d03412c091c6315cf4fde7cb68606937380d
b2eaaa707b4c4185c32eddcdd306705e4dc1ffc872eeee475a64dfac86aba41c0618983f8741c5ef68d3a101e8a3b8cac60c905c15fc910840b94c00a0b9d0
```
### Outputs
- xvk
```
vk       : ba6f17a0aea15adf0133ce213bf6eabfd161f3120a4f31a40ea96432277fb88d
chainCode: 64c5e1ffad57e36b0e9fa3a4fb268da0c134fe3ea472dbf124215b2df1d4c40e
```
- sig
```
b37d85d75085837957e8820278a00367f75bde4884433a6af15be9f8d103ee8dd6b4d5fefaa081bb53f33a92c9fc2cbcf3d6ad93063d9b31f8f973b6d3d4f404
```
## Test Vector - 6
### Description
Derive the correct child secret and verification keys at following path `m/0` given a specified master extended secret key
### Inputs
- root_xsk:
```
leftKey  : c05377ef282279549898c5a15fe202bc9416c8a26fe81ffe1e19c147c2493549
rightKey : d61547691b72d73947e588ded4967688f82db9628be9bb00c5ad16b5dfaf602a
chainCode: c5f419bd575f8ea23fa1a599b103f85e6325bf2d34b018ff6f2b8cf3f915e19c
```
- root_xvk
```
vk       : 2b1b2c00e35c9f9c2dec26ce3ba597504d2fc86862b6035b05340aff8a7ebc4b
chainCode: c5f419bd575f8ea23fa1a599b103f85e6325bf2d34b018ff6f2b8cf3f915e19c
```
### Outputs
- child_xsk:
```
leftKey  : 08d0759cf6f08105738945ea2cd4067f173945173b5fe36a0b5d68c8c8493549
rightKey : 4585bf3e7b11d687c4d64c73dded58915900dc9bb13f062a9532a8366dfa971a
chainCode: dcd9ae5c4ef31efedef6eedad9698a15f811d1004036b66241385081d41643cf
```
- child_xvk
```
vk       : 7110b5e86240e51b40faaac78a0b92615fe96aed376cdd07255f08ae7ae9ce62
chainCode: dcd9ae5c4ef31efedef6eedad9698a15f811d1004036b66241385081d41643cf
```
## Test Vector - 7
### Description
Derive the correct child secret and verification keys at following path `m/1` given a specified master extended secret key
### Inputs
- root_xsk:
```
leftKey  : c05377ef282279549898c5a15fe202bc9416c8a26fe81ffe1e19c147c2493549
rightKey : d61547691b72d73947e588ded4967688f82db9628be9bb00c5ad16b5dfaf602a
chainCode: c5f419bd575f8ea23fa1a599b103f85e6325bf2d34b018ff6f2b8cf3f915e19c
```
- root_xvk
```
vk       : 2b1b2c00e35c9f9c2dec26ce3ba597504d2fc86862b6035b05340aff8a7ebc4b
chainCode: c5f419bd575f8ea23fa1a599b103f85e6325bf2d34b018ff6f2b8cf3f915e19c
```
### Outputs
- child_xsk:
```
leftKey  : 888ba4d32953090155cbcbd26bbe6c6d65e7463eb21a3ec95f6b1af4c7493549
rightKey : 6b723c972aa1de225b9e8c8f3746a034f3cf67c51e45c4983968b166764cf26c
chainCode: 9216b865f39b127515db9ad5591e7fcb908604b9d5056b8b7ac98cf9bd3058c6
```
- child_xvk
```
vk       : 393e6946e843dd3ab9ac314524dec7f822e7776cbe2e084918e71003d0baffbc
chainCode: 9216b865f39b127515db9ad5591e7fcb908604b9d5056b8b7ac98cf9bd3058c6
```
## Test Vector - 8
### Description
Derive the correct child secret and verification keys at following path `m/2` given a specified master extended secret key
### Inputs
- root_xsk:
```
leftKey  : c05377ef282279549898c5a15fe202bc9416c8a26fe81ffe1e19c147c2493549
rightKey : d61547691b72d73947e588ded4967688f82db9628be9bb00c5ad16b5dfaf602a
chainCode: c5f419bd575f8ea23fa1a599b103f85e6325bf2d34b018ff6f2b8cf3f915e19c
```
- root_xvk
```
vk       : 2b1b2c00e35c9f9c2dec26ce3ba597504d2fc86862b6035b05340aff8a7ebc4b
chainCode: c5f419bd575f8ea23fa1a599b103f85e6325bf2d34b018ff6f2b8cf3f915e19c
```
### Outputs
- child_xsk:
```
leftKey  : c0b712f4c0e2df68d0054112efb081a7fdf8a3ca920994bf555c40e4c2493549
rightKey : 93f774ae91005da8c69b2c4c59fa80d741ecea6722262a6b4576d259cf60ef30
chainCode: c05763f0b510942627d0c8b414358841a19748ec43e1135d2f0c4d81583188e1
```
- child_xvk
```
vk       : 906d68169c8bbfc3f0cd901461c4c824e9ab7cdbaf38b7b6bd66e54da0411109
chainCode: c05763f0b510942627d0c8b414358841a19748ec43e1135d2f0c4d81583188e1
```
## Test Vector - 9
### Description
Derive the correct child secret and verification keys at following path `` m/0` `` given a specified master extended secret key
### Inputs
- root_xsk:
```
leftKey  : f0d0f18e6ab029166fe4e89519ab64f42aa870fc2791fc472840c3a1ba507347
rightKey : fee30dcae1ae3941bde71e9ddd19eef33d0a7b91aaa4137cea6ef4ea3c27f96a
chainCode: 1189e5ec0628974ed7846b594ed0ee2d3ef2d8f5b91d1860ffb0a065159df8be
```
### Outputs
- child_xsk:
```
leftKey  : b859fdcdafa6a4552e5d4a18c44b79daf1d40f1600f6745768ddcbd9bc507347
rightKey : b7b1cdaf0d837051ed203813f7f3c518ae8046fbd4de106bf1cde33496825a39
chainCode: 0f2f8270d4724314a2a4f7175cd5765c35dffbf5ccbbfc4f8497297e9e68510f
```
- child_xvk
```
vk       : b983b958d41fbdfecf6c0010ac667efa3cecb02ba27099afd13bc0ef0f82e60c
chainCode: 0f2f8270d4724314a2a4f7175cd5765c35dffbf5ccbbfc4f8497297e9e68510f
```
## Test Vector - 10
### Description
Derive the correct child secret and verification keys at following path `` m/0`/100` `` given a specified master extended secret key
### Inputs
- root_xsk:
```
leftKey  : f0d0f18e6ab029166fe4e89519ab64f42aa870fc2791fc472840c3a1ba507347
rightKey : fee30dcae1ae3941bde71e9ddd19eef33d0a7b91aaa4137cea6ef4ea3c27f96a
chainCode: 1189e5ec0628974ed7846b594ed0ee2d3ef2d8f5b91d1860ffb0a065159df8be
```
### Outputs
- child_xsk:
```
leftKey  : 30c9ae886a00e5524223d96824b28b1aff0419c6026dd07509e5b5a4c1507347
rightKey : 3890a9decc12d0400869d6daf095092863bba45363b8e33c257e70bf7d3548aa
chainCode: cce7b986e25839573c044c389cf8f76d8adcc6f723df9f98bfa1308f0c35282c
```
- child_xvk
```
vk       : 4b95248060cc3bd0fee38cddf2c54b5e155a38de5cfe1846873355b35cc07566
chainCode: cce7b986e25839573c044c389cf8f76d8adcc6f723df9f98bfa1308f0c35282c
```
## Test Vector - 11
### Description
Derive the correct child secret and verification keys at following path `` m/0`/100`/55 `` given a specified master extended secret key
### Inputs
- root_xsk:
```
leftKey  : f0d0f18e6ab029166fe4e89519ab64f42aa870fc2791fc472840c3a1ba507347
rightKey : fee30dcae1ae3941bde71e9ddd19eef33d0a7b91aaa4137cea6ef4ea3c27f96a
chainCode: 1189e5ec0628974ed7846b594ed0ee2d3ef2d8f5b91d1860ffb0a065159df8be
```
### Outputs
- child_xsk:
```
leftKey  : 404d45140bdc926f5bb8b8ae0442f748892ce1c07760b828a837c69bc3507347
rightKey : a80d35782afb13e7d788447446836e1082d6e66a9fba66e5c9e17fcda641c28d
chainCode: 3a5c3099aeffe333f39d4107b1f59227a7e5713b94518033a763a542ea289ee8
```
- child_xvk
```
vk       : 8e59beac508fcd431c0b7b2dae81686adf45c76c0e32af7af779ecdf78adb8fb
chainCode: 3a5c3099aeffe333f39d4107b1f59227a7e5713b94518033a763a542ea289ee8
```
## Test Vector - 12
### Description
Derive the correct child secret and verification keys at following path `` m/1852`/7091`/0`/0` `` given a specified master extended secret key
### Inputs
- root_xsk:
```
leftKey  : 2090d5cdd6bdc4537ed44f109c261f3f8dbe9c17a843a77c035f55c78a723a48
rightKey : 1c285eee9cf920be4a1e1e3564763ad100fe203b5fd79f6535943170e53597ad
chainCode: d20dd0bcf02446e2f607419163f9dbf572393b9c2258d33df59fb0e06112d285
```
### Outputs
- child_xsk:
```
leftKey  : 60befd4438750e301c86713f2c1a5178d419ff9434d9d3dcf44b9ea5a1723a48
rightKey : a14867f43dc37a11f4b82c10b5c1e7c6b5cc91bcd8c029d180f0aca62dee72f9
chainCode: 2f5d057d61cce1664344538c61c12d99f74a8a6c331a811d8ecb468b36168ef0
```
- child_xvk
```
vk       : d7a12d4f53645f9c96a82e01c7c2311d7ae95abd631b13ed08afac5c6519051e
chainCode: 2f5d057d61cce1664344538c61c12d99f74a8a6c331a811d8ecb468b36168ef0
```
## Test Vector - 13
### Description
Derive the correct child secret and verification keys at following path `` m/1852`/7091`/0`/0`/0 `` given a specified master extended secret key
### Inputs
- root_xsk:
```
leftKey  : 2090d5cdd6bdc4537ed44f109c261f3f8dbe9c17a843a77c035f55c78a723a48
rightKey : 1c285eee9cf920be4a1e1e3564763ad100fe203b5fd79f6535943170e53597ad
chainCode: d20dd0bcf02446e2f607419163f9dbf572393b9c2258d33df59fb0e06112d285
```
### Outputs
- child_xsk:
```
leftKey  : 90471ffb2cb297980d128f5aed71190f1889f53a02c0a2180e32478ba6723a48
rightKey : 733b0f3ab9538329fd45089e75d6609f2f345d3c695063ac457e5393a722c6b1
chainCode: b415521a3550f1e59fad614aa249aa3245c93005efd63faf8a02ba7787176782
```
- child_xvk
```
vk       : f119694710657f95edf110002ad3974db4c22f330b6b091355cd0b5784f04ba8
chainCode: b415521a3550f1e59fad614aa249aa3245c93005efd63faf8a02ba7787176782
```
