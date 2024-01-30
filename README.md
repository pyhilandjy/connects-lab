# Startup ConnectsLab pilot project

**Team Members**: 최준용, 강성구, 이상호, 곽준목

## **프로젝트 개요**

- **프로젝트 목표**: Instagram에서 #육아일기 데이터를 크롤링 및 Dashboard 작성

- **기간**: 23.11.15 ~ 23.12.20

> <p align="center"><img src="assets/result.jpg" width="840"></p>


<br>

### 프로젝트 기술스택

![Python](https://img.shields.io/badge/Python-ffe74a.svg?style=flat&logo=Python&logoColor=blue) 
![Docker](https://img.shields.io/badge/Docker-4d77cf.svg?style=flat&logo=Docker&logoColor=4dabcf)
![Airflow](https://img.shields.io/badge/Airflow-130654.svg?style=flat&logo=Pandas&logoColor=whitle) 
![Dash](https://img.shields.io/badge/Dash-11557C.svg?style=flat&logo=Matplotlib&logoColor=white) 
![AWS](https://img.shields.io/badge/AWS-262626.svg?style=flat&logo=Plotly&logoColor=white) 

<br>

## 1. 현 프로젝트에 맞는 Pipeline 구성하기

### **Overview**

- 생애초기(0-4세)는 뇌 신경망의 발달이 폭발적으로 일어나는 시기이다.

- 이 시기에 다양한 외부 자극을 접하고 소화하며 아이들의 두뇌가 성장한다.

- 가장 중요한 외부 자극 중 하나가 ‘부모의 말’ 이다.

- 한 가정에서 아이가 성장하는 동안의 대화내용을 담은 음성파일이 회사측에 존재 하지 않는다.

- 필요로하는 데이터와 유사한 데이터는 Instagram의 **#육아일기** 라고 판단하였다.

- Instagram의 데이터로 추후 고객들에게 보여질 Dashboard를 구상하고 확인하기 위한 프로젝트.

<br>

### **1st Step.**

Instagram에서 유사한 데이터 크롤링

* **#육아일기**
  * Web으로 인스타그램에서 #육아일기 를 검색했을때 15개의 게시물로 제한되어있다.
  * META에서 Instagram graph API를 사용하여 보았지만 데이터 수집을 위한 API가 아니라 광고를 목적으로 한 API라 판단.
  * 대안책으로 꾸준히 업데이트를 하는 유저의 계정을 수작업으로 선별 후 선별된 계정의 게시물 크롤링
     *(instagram_job.py)

* **Factor**: **상품**, **카테고리**
  * 매출 및 결제건을 통한 주력 카테고리 및 상품을 확인한다.
  * 상품명 분석을 통해 패키지, 프리미엄, 단일코스 중 무엇이 매출에 주요 요소인가?.

* **Factor**: **계절성**
  * 1~12월동안 매출확인을 통해 매출에서 계절성을 띄는지 파악한다.
  * 요일별 결제건 추이로 요일성 또한 파악.
  * 계절성에 따른 마케팅 계획을 수립할 수 있는지 확인.

* **Factor**: **품질**
  * 상품별 카테고리별 환불율을 확인하여 품질를 파악.
  * ‘쿠폰이름’ 분석을 통해 쿠폰의 종류 및 할인, 유효한 결제건을 확인.
  * 퀄리티가 높은 상품 혹은 카테고리를 분류할 수 있지 않을까?

### **2nd Step.**
* 분석한 Factor를 이용해서 데이원컴퍼니의 **비즈니스 모델**을 추론해보자.
* 데이원컴퍼니는 **누구**에게 **무엇**을 **어느 때**에 서비스 하고 있고, 그 Quality 즉 **품질**을 파악할 수 있을까?

### **3rd Step.**
* **추론한** 데이원컴퍼니의 **비즈니스모델**에서 **특징들**은 **무엇**일까?
* 궁극적으로 **강점**은 어떻게 **더 보완**할 수 있을지? **약점**은 어떻게 **제거** 할 수 있을까?
* 그로인한 **매출 증대**는 가능한가?

<br>

## 2. 데이터 전처리 Data Preprocessing
