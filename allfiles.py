import os.path
#tool_prefix='JSON'
#kind_prefix='json'
#tool_suffix='-cJSON' # Antlr does not have suffix

common_prefix='./results/out/'
kinds=['-invalid-single/', '-invalid-mult/']
valid_prefix = 'project/bin/testfiles/'
valid_suffix = '-valid/'


ininames='''\
02aaf66820894d1b833271da95740b64.ini
03d9d18ef6004208abcb3c7f02710d40.ini
04b78aa09feb4986a5081572e6177328.ini
05606e4eb3d84e2cbb626a16d9946ddb.ini
0af5a86b599e487f9cb008cec87d9c3f.ini
11b22fcb485f4a5291f05eccaa576823.ini
15027701cec74115ac3b0b7857520ae5.ini
15e85720f2504b5bad79116e2b76b1b1.ini
17397f8878cf48938d91fa9dc2f7e220.ini
1a2a89f9637047f3af9d4821a3026622.ini
1a748ad35c4e433ca33698872f10bcf0.ini
1e977052ac3845068e0482fd6900b05d.ini
21cb41024aa04ab5b7a72f1c3015cbc1.ini
248d59e5d5c544d3b3e5fde86ae32fab.ini
2679f986d5e9442dbf5d87671df76cbe.ini
26b98eab60ba454dad5c456316161247.ini
27d46c1be9344fa1b0ed55137f8be636.ini
334a4fd72a184ffe8fd43c9d26a4048e.ini
341449945dc446c3b73c5e072851c62d.ini
34156eb2bb344d33a1e3c3fd7343ebb0.ini
35a62177fd524cb794c91a6a6f760c28.ini
3bb4d88e43a0492cab0cbb544fa8aca2.ini
4269915eb132401bb97b2db3a8b8f6d4.ini
43d41527a7de4b3a9167afb780d2d677.ini
44781a384cf14d95abec149a000f3403.ini
4932e254b68b4d25908eeffeb7866e38.ini
4bec67f1c14249c8aeec9b2e7aee293f.ini
4ff53a02ba134bc3aa892daa55b9bfe3.ini
507f98b2c58047eaaa2b2b7420b4c8aa.ini
51c7eecba3c54a9c90bbfbc808db3c26.ini
54a80bdc3ecc41569f798aa786c58fb1.ini
54acb241c87e4014b1fd59bb9cde707e.ini
59a8685104584a2c9df4200876f4796b.ini
5b0696535a464ab1ba0315a25ded5566.ini
5b0a05b5a23942c681c87f3162a031fa.ini
5f69c3fa7bfc41f89c316f0b467b2e8b.ini
650b74f71bec4e2391dc331481e5fb14.ini
6525efe77abe45ab90286870fba59ef9.ini
65f8a36b4c7341d387e8fc3a2bc87b4f.ini
6bbf163a7b7d4fcc93c265663502cfb3.ini
6cf54ba20f6c49438fcfab030c5e9db5.ini
7010be0e664d4c91aa92815c09db3f1d.ini
716ee960c13a4bd0a754d05c4e27b2dd.ini
71ace347216246d1a65dcfbc400a3785.ini
75822dd358784dc686cca39493271d41.ini
78834115320e49918c376d5109a684a5.ini
8983ac67661a4c1493ec0bdd06a4e0e1.ini
95c0e7f4c98b40ca9c99c100fd324cfc.ini
a151d5f6a1014242ba88bdffe555d347.ini
d2aa86baed034368a3dd64f191428b26.ini'''.split('\n')

jsonnames='''\
6831.json
912.json
7021.json
8161.json
2891.json
2014.json
6542.json
1116.json
4569.json
7714.json
6241.json
5206.json
4114.json
2371.json
7364.json
6964.json
2662.json
4470.json
8516.json
3788.json
7616.json
7753.json
5851.json
5200.json
4310.json
6643.json
5096.json
2092.json
7875.json
5063.json
8714.json
8240.json
3660.json
8216.json
8345.json
2322.json
7823.json
2355.json
3790.json
4350.json
2108.json
6188.json
2466.json
4838.json
6491.json
7278.json
8772.json
6234.json
7576.json
8396.json'''.split('\n')

sexpnames='''\
0070c87bc7654c53afd2b0fbde6566e7.lisp
008083ae0559438ea8c922310dde9ecc.lisp
01e11bc5f55348ce8fde032be8b26672.lisp
01e9585e8ed14a7f9ff64b8753abaef8.lisp
0203059e1b32433da3a3573239f467a7.lisp
02f0bc50c3564ed3b2176313904760d8.lisp
030aa5dfde994218af150b852419b2aa.lisp
03a81a26667345058cd3b11eb34f90c2.lisp
03d5563b4f6e4735bed326bb3e56488c.lisp
04111f5523534f1aa05b3542a66b4db7.lisp
0424d987e4df4cbfa327ad35cb3eedb3.lisp
049292e9a3c244c48d1f19e410eab767.lisp
04a6533e7f0046129820d3e77f412f49.lisp
04eaa8b211e44621998759b4d586d2c3.lisp
04f0e02d71be490faf99beba44b8a23e.lisp
05637b6be3cf463ea80b0d023a668015.lisp
05a0188ca0274ce5a92b6e7319940537.lisp
05a37ed9483d427e99a48e6eb3d5b487.lisp
061cccf1fbad40c8a16f550b4793af72.lisp
06904a68dd4c4c068ff7ef7fca52ca28.lisp
069ca063d61d42a7adfa190e22d740aa.lisp
06b600297a4f4676ba93622ed77049ea.lisp
06bed6114877426ba58bfb4faac5c678.lisp
06c69f7afe84404a9eef9938583eaf43.lisp
06dcb2d6bdff40fca94dc79c9848f623.lisp
0716bab024024f2cbb937b79c295a07f.lisp
0758fe85bf75456e9e2b80485ab00d5d.lisp
07715f4e764c419db75e06828628fa74.lisp
084f1d849cdd4e29a1bf961a4c50b95d.lisp
085591729ad9482a9a7d0ba5c6903376.lisp
08d73f8da6b04c01ba832d06b0df05a0.lisp
08e5c2804efc4459a5088161ee7f5457.lisp
08eab81d2d63423d90ab24e7b10464d2.lisp
095dacec0c6b456ba43dad2cb6e59f82.lisp
09a46e29587c4621a89bb18be4fc072e.lisp
09d9ec0f8f64452680457530acc44626.lisp
0a2bfc94e30a430db07b3874676003aa.lisp
0a657c248bab48bfb5804042d8d6ef29.lisp
0aa56bb3e14d4443b1383029dd1bd44b.lisp
0ab1336013864dd79e125879a26bc16b.lisp
0af54540b2b94159ba1dc4f59dd5b97d.lisp
0b0cdb500783415cb1cdcc9390415d58.lisp
0b0d3e38fd14408cb9b6a2736871aa22.lisp
0b773e43be8f4904a1168406f6ef1353.lisp
0bbc8c884d704217b029d84d4668b5da.lisp
0c38002778474475b951196e21fb1a66.lisp
0c3d884bbeb4464ba4192b5a53461ee4.lisp
0c7b228f860a4b72b9830995320cb947.lisp
0d20b074b5ca4beda67afa507f3e8848.lisp
0ddb12b4f00046d9b7bc7aa35d5d2de2.lisp'''.split('\n')

tinycnames='''\
d89ae260cb9e0a00d8b1448da6b2ce73.c
da06e564702c8fa3165d64219abae6ff.c
dcab71d568275d772047cbab47a97311.c
dd1c0e1a8117f569694f113305a9a032.c
dde6f3e8342d2db7ec0672026363d8ed.c
de1f48029931c33632a8650afa9689b2.c
dedf5b8f78ea5279dee2684f0d5f4920.c
def425b85260acc0f7a6259831d37085.c
df2635637298a79cfe3ef6262492ce1f.c
df9a8a5d2e129ec5ac4e809b4333265e.c
e061eef4352334d3ee290fec2baa0b33.c
e1918264e68cc742b823c90b21f63964.c
e1c07ab7609479202fb03e9f8085804e.c
e250bce557c54aed4fd5b49489e6741c.c
e273975e2715ff5d2f3ff1040c5f28cb.c
e2b39c37087833d258ad9a012995f259.c
e2b88d2793a00dd0a1995fd2565342e5.c
e39d529bc7015ec6eaa2b54060d369e4.c
e581cd3de513b8da1293be1ca9871f11.c
e6d674fdf964c5afce4e74d393ffc469.c
e70362e00d35d657666d6735be76c3f2.c
e7aa03a2d736853af718feb925ce011f.c
e84a7a55ed395c0c0ecc3abbcf439d9e.c
e8ae38b9b426acc956f05b9e33ad1b80.c
e98f0653097c09cb8361933668838f5e.c
e9caa3ea66b000c4332e58399ab4a444.c
e9fd0c2aa6a72bfdef18109126dfdd7d.c
ea98c1e914dd459eb86996d2ca99bbb6.c
eb8f9d51a9d325ac4de750fabb963302.c
ebaabc8938b058e8663af28e1fc377e8.c
ebe8997df416bfe3763fbb6b3d806801.c
ec244e8cc5853f7b3459d4fcc7daf4c2.c
ec6295b3be871c32fb13d09ec44ecc12.c
ed098c718bfe381fac3214222e682427.c
efe07d515f1ef758cb564f0186199ec0.c
f03c5cec3d87f0844e13ba9c4cd7cd37.c
f168f2f055be9849475911aa88a9b0a3.c
f2797c5dcd82275fb0cfcab64f04a9cf.c
f2a58825dce52705b57d3226c5ff8d51.c
f3c72ccf24dd61c1a9c5bdf7216739e7.c
f6cc4e6f67c806376fb4596a9b7f3227.c
f77b5dd2ce5604108c3c369a1c362014.c
f85be888c266bf2723e2594e347efff3.c
f8d3fe0c7f9995c1cbde303dbe111eba.c
f8e3a93fd340f77b9348830250cc14e8.c
f9210dbac1e064902126801e05c2c33f.c
f9e6f878e075137020b0e4418c16b118.c
fc21cfbea2474f618e667f5f2d18cbb9.c
fd23de76a537323e39ea610a768e0737.c
ff21ea78c5ffd528e7bc640c76fbc4ca.c'''.split('\n')

#assert len(names) == 50
#print(repr(names))
# tool_names='bRepair DDMin DDMaxG Antlr DDMax'.split(' ')

files = {
        'ini': {
            'files': ininames,
            'tool_prefix': 'INI',
            'kind_prefix': 'ini',
            'tool_suffix': '-INI',
            },
        'json': {
            'files':jsonnames,
            'tool_prefix': 'JSON',
            'kind_prefix': 'json',
            'tool_suffix': '-cJSON',
            },
        'sexp': {'files': sexpnames,
            'tool_prefix': 'SExp',
            'kind_prefix': 'sexp',
            'tool_suffix': '-SExpParser',
            },
        'tinyc': {'files': tinycnames,
            'tool_prefix': 'TinyC',
            'kind_prefix': 'tinyc',
            'tool_suffix': '-TinyC',
                  }
        }


def produce_files(tool, fmt):
    for kind in kinds:
        for k in files[fmt]['files']:
            original = valid_prefix + files[fmt]['kind_prefix'] + valid_suffix + k
            assert os.path.exists(original)

            invalid = valid_prefix + files[fmt]['kind_prefix'] + kind + k
            assert os.path.exists(invalid)
            if tool == 'Antlr':
                fname = common_prefix + files[fmt]['tool_prefix'] + tool + '-' + files[fmt]['kind_prefix'] + kind + k
            else:
                fname = common_prefix + files[fmt]['tool_prefix'] + tool + '-' + files[fmt]['kind_prefix'] + kind + k + files[fmt]['tool_suffix']
            assert os.path.exists(fname)
            result = (tool, fname)
            yield (original, invalid, result)

