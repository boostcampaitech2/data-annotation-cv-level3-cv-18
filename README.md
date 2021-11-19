# :zero: Get Our Results

1. Conda Environments *(Recommended)* 

   ```bash
   $ conda create -n data_annotation python=3.7.2
   $ conda activate data_annotation
   $ pip install -r requirements.txt
   ```

2. Code Execution : `convert_mlt.py`
   
   ```bash
   train.py --data_dir ../input/data/ICDAR19_MLT_ufo --ckpt_name latest.pth --wandb_name 2019_MLT --batch_size 32
   ```

3. Code Execution : `train.py` 

   ```bash
   # ICDAR 2019 모든 언어의 이미지를 dst_dir로 복사하고 메타데이터를 ufo 포맷으로 변환
   python convert_mlt.py --src_dir ../input/data/ICDAR19_MLT --dst_dir ../input/data/ICDAR19_MLT_ufo --is_mlt19 True
   ```
   
# :one: Overview

## 1.0. 대회의 목적 

1. OCR Task 에 대해 조금이나마 이해하고 Detector 의 성능을 높여본다.
2. 모델의 성능을 높이기 위해 Model-Centric 접근법이 아닌 **Data-Centric 접근법**을 익힌다.
3. UP-Stage 에서 제공해주는 Annotation Tool 을 이용하고 Annotation Guide 를 통해 라벨링 작업을 직접 수행하며 데이터의 귀중함을 몸소 깨닫고 좋은 Annotation Guide 란 무엇인지 생각해본다.
4. 여러 공개 데이터셋을 찾아보고 Annotation File 의 형식을 통합해본다.

## 1.1. Annotation 작업

### 1.1.1. 작업의 목적

본 데이터의 가공 목적은 OCR 엔진의 성능을 향상시키기 위함입니다.  
다양한 도메인으로의 성능이 높은 OCR 엔진을 생성하기 위해 학습 데이터를 구축하는 작업입니다.

### 1.1.2. 가공 데이터

글자영역이 있는 실사 이미지를 기준으로 가공합니다.   
실사 이미지는 메뉴판, 영수증, 책표지, 노선도, 간판 등 실생활에서 찍는 이미지를 의미합니다.

### 1.1.3. 작업 문서 수

약 5,000장 (캠퍼 개인별 10장)

# :two: Project Outline

## 2.0. Topic

Optical Character Recognition (a.k.a. OCR) is a technology which allow computer to recognize characters in an image. OCR consists of three modules; Text Detector, Text Recognition, Serializer. We suppose that a skeleton model only having text detector is already deployed. And then, we try to enhance the model performance with Data-Centric approaches such as data collection, applying public datasets, data augmentations, except modifying model structure.

## 2.1. Envirionments

We use V100 GPU (32GB).

## 2.2. Collaboration Tools

We use github, notion, wandb for our collaborations.

## 2.3. Structure

* Input and output of model
  * input: Images of ICDAR17-MLT and ICDAR19-MLT and Annotation file with UFO format.
  * output: Bounding boxes in images.
* Model and dataset that we use.
  * model: EAST ([An Efficient and Accurate Scene Text Detector](https://arxiv.org/abs/1704.03155))
  * dataset: [ICDAR19-MLT](https://rrc.cvc.uab.es/?ch=15)

## 2.4. Benefits

We are going to use pretrained weights of the best model in this competition to get good performance in side project.



# :three: Carry Out the Project

## 3.1. Problem Definition

When people pay by card or recoginize a card with their camera, some infomation in the card is often automatically entered. And also, when a car enter a parking lot, the car number is automatically entered. Like these, OCR technology allows computers to recoginize some characters in an image. And this is one of the representative technologies currently widely used in the field of computer vision.  

Because it is hard to implement the three modules in OCR task, we are going to solve only text detection task in terms of Data-Centric. So, we don't modify the fixed model structure(**VGG16**) and pretrained weights(**ImageNet**).

## 3.2. Procedures

* **<u>Week 01</u>**: Research (Data Production) and execute baseline codes.
* **<u>Week 02</u>**: Add datasets, modify baseline codes for WandB and write the wrap-up report.

## 3.3. Experiments and Observation

| Dataset                   | 언어          |          수량 | inputsize | LB score | 비고 |
| ------------------------- | ------------- | ------------: | :-------: | :------: | :--: |
| SynthText + ICDAR2017-MLT | KOR, ENG      | 850,000 + 536 |    512    |  0.372   | [1]  |
| ICDAR2017-MLT             | KOR, ENG, ETC |           536 |    512    |  0.527   | [1]  |
| ICDAR2017-MLT             | KOR, ENG, ETC |         1,063 |    512    |  0.563   | [2]  |
| ICDAR2017-MLT             | KOR, ENG, ETC |         1,063 |   1024    |  0.594   | [2]  |
| ICDAR2019-MLT             | 모든 언어     |        10,000 |    512    |  0.669   | [3]  |
| ICDAR2019-MLT             | 모든 언어     |        10,000 |   1024    |  0.640   | [4]  |

**[1]** Default (ICDAR2017-MLT 한글 데이터셋 200 epoch 학습)

- SynthText 의 경우, 시간 문제로 1 epoch 만 학습시키고 extractor 부분만 사용
- ICDAR2017-MLT 의 한글 데이터셋을 이용하여 전체 모델 학습 (extractor 부분도 재학습)

**[2]** ICDAR2017-MLT의 Valid set 추가, 200 epoch, batch 크기 다름

**[3]** 한국어 데이터셋의 경우 ICDAR2017-MLT와 ICDAR2019-MLT 데이터셋 동일

**[4]** 85 epoch 학습

# :four: Results of Project Execution

## 4.1. Final Model

| Key           |        Value        | 비고                                   |
| ------------- | :-----------------: | -------------------------------------- |
| Text Detector |   EAST *(fixed)*    | Pretrained Weight - ImageNet *(fixed)* |
| Backbone      |  VGG 16 *(fixed)*   | Pretrained Weight - ImageNet *(fixed)* |
| Optimizer     |        Adam         |                                        |
| Learning Rate |        1e-4         |                                        |
| LR Scheduler  |     MultiStepLR     |                                        |
| Loss          | EAST Loss *(fixed)* |                                        |
| Batch Size    |          32         |                                        |
| Epochs        |         200         |                                        |
| Input Size    |         512         |                                        |

## 4.2. Final Metric in the Competition

|               | Public LB |     Private LB      |
| :-----------: | :-------: | :-----------------: |
| **F1 Score**  |  0.6690   | 0.6710 **(+0.002)** |
|  **Recall**   |  0.5760   | 0.5830 **(+0.007)** |
| **Precision** |  0.7790   | 0.7910 **(+0.012)** |

> 점수가 오히려 향상되었다.

# :five: Participants

| Name           | Github                                      | Role                                       |
| -------------- | ------------------------------------------- | ------------------------------------------ |
| 김서기 (T2035) | [링크](https://github.com/seogi98)          | ICDAR 2017 데이터셋 적용                   |
| 김승훈 (T2042) | [링크](https://github.com/lead-me-read-me)  | SynthText, ICDAR 2017 데이터셋 적용        |
| 배민한 (T2260) | [링크](https://github.com/Minhan-Bae)       | Research, ICDAR 2017 데이터셋 적용         |
| 손지아 (T2113) | [링크](https://github.com/oikosohn)         | WandB 설정, ICDAR 2017, 2019 데이터셋 적용 |
| 이상은 (T2157) | [링크](https://github.com/lisy0123)         | ICDAR 2017 데이터셋 적용                   |
| 조익수 (T2213) | [링크](https://github.com/projectcybersyn2) | ICDAR 2017 데이터셋 적용                   |

