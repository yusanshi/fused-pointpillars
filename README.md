# Fused PointPillars

> Credits: I duplicated [nutonomy/second.pytorch](https://github.com/traveller59/second.pytorch) instead of forking it for some reasons. So only commits after the first is my work. Actually this can be seen as a fork of [nutonomy/second.pytorch](https://github.com/traveller59/second.pytorch) which is a fork of [traveller59/second.pytorch](https://github.com/traveller59/second.pytorch).

Trying to modify [PointPillars](https://arxiv.org/abs/1812.05784) to use images for sensor fusion. Still working on it. The following is for original PointPillars.

## Get started

### Install necessory packages
```
apt update
apt upgrade
apt install vim git curl wget build-essential python3 python3-pip unzip tree
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python3 -m pip install torch torchvision scikit-image scipy numba pillow matplotlib fire tensorboardX protobuf opencv-python --default-timeout=100
```

### Clone this project
```
git clone git@github.com:yusanshi/fused_pointpillars.git
cd fused_pointpillars
```

### Set environment variables
In `env.sh`, set `PYTHONPATH` to this project's directory, `KITTI_DATASET_ROOT` to whatever an emypt directory you choose to store KITTI dataset.
```
vim env.sh
```
After this, source it.
```
source env.sh
```

### Download KITTI dataset
Use any methods you like, download following 4 zip files into `KITTI_DATASET_ROOT`. 
```
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_velodyne.zip
```

Use wget for example (Use -c or --continue option to enable resuming from break-point).
```
cd $KITTI_DATASET_ROOT
wget --continue https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip \
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip \
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip \
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_velodyne.zip
```

Extract them.
```
unzip 'data_object_*.zip' -q -d object_detection/
```
This will generate `training` and `testing` directories in `$KITTI_DATASET_ROOT/object_detection`.
You can use tree command to check the result.
```
tree -L 3
```
Your output should be something like this:
```
.
├── data_object_calib.zip
├── data_object_image_2.zip
├── data_object_label_2.zip
├── data_object_velodyne.zip
└── object_detection
    ├── testing
    │   ├── calib
    │   ├── image_2
    │   └── velodyne
    └── training
        ├── calib
        ├── image_2
        ├── label_2
        └── velodyne
```

Create some empty directories.
```
mkdir object_detection/training/velodyne_reduced
mkdir object_detection/testing/velodyne_reduced
```


### Prepare KITTI dataset
```
cd $PYTHONPATH/second
python3 create_data.py create_kitti_info_file --data_path=$KITTI_DATASET_ROOT/object_detection
python3 create_data.py create_reduced_point_cloud --data_path=$KITTI_DATASET_ROOT/object_detection
python3 create_data.py create_groundtruth_database --data_path=$KITTI_DATASET_ROOT/object_detection
```

### Modify path in config files

Use `replace.py` to replace string `$KITTI_DATASET_ROOT` with value of current environment variable $KITTI_DATASET_ROOT in `.proto` file in `$PYTHONPATH/second/configs`.

```
cd $PYTHONPATH
python3 replace.py
```

### Train

```
cd $PYTHONPATH/second


```

### Evaluate

```
cd $PYTHONPATH/second


```

