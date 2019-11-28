# Replace string `$KITTI_DATASET_ROOT` with value of current
# environment variable $KITTI_DATASET_ROOT in `.proto` file
# in `$PYTHONPATH/second/configs`.

import os

config_path = './second/configs'

if 'KITTI_DATASET_ROOT' not in os.environ:
    print('Environment variable KITTI_DATASET_ROOT not set.')
else:
    files = []
    # r = root, d = directories, f = files
    for r, d, f in os.walk(config_path):
        for file in f:
            files.append(os.path.join(r, file))

    for x in files:
        if x.endswith('.proto'):
            with open(x, 'r', encoding='utf-8') as f:
                text = f.read().replace('$KITTI_DATASET_ROOT',
                                        os.environ['KITTI_DATASET_ROOT'])
            with open(x, 'w', encoding='utf-8') as f:
                f.write(text)

            print('Finish replacement for {}'.format(x))
