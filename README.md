# lang_classify
A nn model detacting an audio is Taiwanese or Chinese.
## Requirement
* ffmpeg
* youtube-dl
## Setup

## Preprocess
Requirement: Mno .wavfile with sample_rate = 8192.

ps: `preprocess/collect.py`, `preprocess/convert.py` and `preprocess/convert.sh` may be helpful.

Using audio in `wav/` building dataset in `feature/`.
```
$ ./preprocess/build_feature 
```
Taiwanese 001.wav~529.wav => boy, 530.wav~ => girl

## Training
Set your data size in train.py.

Trining model:
```
$ ./train.py
```

Tensorboard:
```
tensorboard --logdir=logs/
```

## Evaluation
```
$ ./eval.py
```
