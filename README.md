***Sorry but the project is abandoned and archived.***

---

# Fused PointPillars

> Credits: I duplicated [nutonomy/second.pytorch](https://github.com/nutonomy/second.pytorch) instead of forking it for some reasons. So only commits after the first is my work. Actually this can be seen as a fork of [nutonomy/second.pytorch](https://github.com/nutonomy/second.pytorch) which is a fork of [traveller59/second.pytorch](https://github.com/traveller59/second.pytorch).

Trying to modify [PointPillars](https://arxiv.org/abs/1812.05784) to use images for sensor fusion. Still working on it. The following is for original PointPillars.

## Get started

### Clone this project
Choose a directory to clone the project.
```bash
git clone git@github.com:yusanshi/fused-pointpillars.git
```

### Download KITTI dataset
Choose whatever an emypt directory to store KITTI dataset. Let's call it `KITTI_DATASET_ROOT`. Use any methods you like, download following 4 zip files into `KITTI_DATASET_ROOT`.
```
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_velodyne.zip
```

Use wget for example (Use -c or --continue option to enable resuming from break-point).
```bash
cd KITTI_DATASET_ROOT
wget --continue https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip \
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip \
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip \
https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_velodyne.zip
```

Extract them.
```bash
sudo apt install unzip
unzip 'data_object_*.zip' -q -d object_detection/
```
This will generate `training` and `testing` directories in `KITTI_DATASET_ROOT/object_detection`.
You can use tree command to check the result.
```bash
sudo apt install tree
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
```bash
mkdir object_detection/training/velodyne_reduced
mkdir object_detection/testing/velodyne_reduced
```

### Use Docker image
In Docker, a running instance of an image is a container. We will use image `nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04` from Cuda official images.
```bash
docker run -it --rm --gpus all nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04 bash
```
In above command, `--gpus all` tells docker to use all your GPU resources. `nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04` is the image name on which the container will be created. `bash` is the command to execute after loading of the container.

However, you can't access files on host machine using above command. In order to access your code and Kitti dataset files, use `-v` parameter to map `fused-pointpillars` and `KITTI_DATASET_ROOT` into your container.

For example, map `~/fused-pointpillars` on host machine into `/fused-pointpillars` in container.
```bash
docker run -it --rm --gpus all -v ~/fused-pointpillars:/fused-pointpillars nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04 bash
```
You will add two `-v` since both this project and KITTI dataset are mapped.

### Install necessory packages
```bash
apt update
apt upgrade
apt install vim git curl wget build-essential python3 python3-pip
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python3 -m pip install torch torchvision scikit-image scipy numba pillow matplotlib fire tensorboardX protobuf opencv-python shapely pybind11 --default-timeout=100

# Install SparseConvNet
git clone https://github.com/facebookresearch/SparseConvNet
cd SparseConvNet/
vim develop.sh # Change python to python3
bash develop.sh
```

Since you have modified the container a lot, you may want to save it to a new image for future use. 

```bash
# In your host machine, not in the container

# Get container ID
docker ps
docker commit <container_id> <name>
```

Then next time you want to run this, just replace `nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04` with the new name.

### Set environment variables
In `env.sh`, set `PYTHONPATH` to this project's directory, `KITTI_DATASET_ROOT` to KITTI dataset directory. Here you will use paths in Docker container (mapped path) instead of those in your host machine.
```bash
vim env.sh
```
After this, source it.
```bash
source env.sh
```

### Prepare KITTI dataset
```bash
cd $PYTHONPATH/second
python3 create_data.py create_kitti_info_file --data_path=$KITTI_DATASET_ROOT/object_detection
python3 create_data.py create_reduced_point_cloud --data_path=$KITTI_DATASET_ROOT/object_detection
python3 create_data.py create_groundtruth_database --data_path=$KITTI_DATASET_ROOT/object_detection
```

### Train

```bash
cd $PYTHONPATH/second
python3 ./pytorch/train.py train --config_path=./configs/pointpillars/car/xyres_16.proto --model_dir=./model
```
You can change `config_path` to other config files in `./configs/pointpillars`. If `model_dir` doesn't exist, a new model will be trained, or training will be resumed from the last checkpoint.

### Evaluate

```bash
cd $PYTHONPATH/second
python3 ./pytorch/train.py evaluate --config_path=./configs/pointpillars/car/xyres_16.proto --model_dir=./model
```
Results will be saved in `model_dir/eval_results/step_xxx`.

