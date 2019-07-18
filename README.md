# `x-sampling`: Sample sound transforming with GANs

![](https://img.shields.io/badge/lab-cclab-red.svg)
![](https://img.shields.io/badge/year-2019s-green.svg)

## Max for Live

use `maxpat` file as max audio effect (`.amxd`).
then run `run.py`

```shell
python run.py
```

## Model Training

Use official implementation [/chrisdonahue/wavegan](https://github.com/chrisdonahue/wavegan)

### Dataset

get the Dataset **Speech Commands Zero through Nine (SC09)** from Adversarial Audio Synthesis (ICLR 2019)

```shell
sh get_data.sh
```

### Requirements

```shell
pip install tensorflow-gpu==1.12.0
pip install scipy==1.0.0
pip install matplotlib==3.0.2
pip install librosa==0.6.2
pip install tensorboard==1.12.1
```

or

```shell
pip install -r requirements.txt
```

## Generation

on