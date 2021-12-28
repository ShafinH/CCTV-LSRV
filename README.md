# CCTV-LSRV
Code for "CCTV Camera Latent Representations for Reducing Accident Response Time" by Shafin Haque. (https://arxiv.org/abs/)

## Abstract
Emergency Medical Services' response times to accidents are crucial to saving lives in vehicle accidents. Using deep learning to instantly detect accidents in public cameras and automatically alerting authorities could help this issue. However, this would require a large set of data on public cameras to train on, but this type of data hardly exists in a usable form. Current deep learning approaches to vehicle accidents typically use first-person cameras, which are not helpful for reducing response time as we do not have access to these cameras at all times. Also, public cameras such as closed-circuit television (CCTV) pick up a much larger amount of street activity than private cameras. Thus, we create a video dataset from live closed-circuit television, so we have access to the cameras at all times. We annotate the videos with metadata to help with future trend prediction as well as give further information for each video, as they are unlabeled. We create an unsupervised learning model to train on this video dataset, and visualize latent space representations of this data in order to cluster different types of street activity and pinpoint vehicle accidents.

## Workflow

![Workflow.png](https://github.com/ShafinH/CCTV-LSRV/blob/main/workflow.png)

## Usage
### Installation
```bash
git clone https://github.com/ShafinH/CCTV-LSRV.git
cd CCTV-LSRV
```

### Requirements
Python requirements for this implementation.
```bash
pip install -r requirements.txt
```

### Data Downloader
The video downloader requires FFmpeg and downloads hour-long videos into the designated folder.
```bash
mkdir scraped_data/Maryland
python downloader.py
```

### Dataset
The dataset can be modified in the [```cctv.py```](https://github.com/ShafinH/CCTV-LSRV/blob/main/cctv_learning/datasets/cctv.py) for cutomizable training.

### Model
Pretrained checkpoints can be found in the [```checkpoints```](https://github.com/ShafinH/CCTV-LSRV/tree/main/checkpoints) folder. 
If training new model, edit [```conv_autoencoder.py```](https://github.com/ShafinH/cctv-learning/blob/main/CCTV-LSRV/models/conv_autoencoder.py) and run main.py. A 
```results/cctv``` folder will be created where model checkpoint and results can be found.
```bash
python main.py
```

### Experiments
Experiments can be run and edited by [```encoder.py```](https://github.com/ShafinH/CCTV-LSRV/blob/main/encoder.py)
```bash
python encoder.py
```
### Citation
```
@misc{haque2021cctv,
  title = {CCTV Latent Representations for Reducing Accident Response Times},
  author = {Shafin Haque},
  year = {2022},
  archivePrefix = {arXiv},
  eprint = {.},
}
```
