# Startup ConnectsLab pilot project

**Team Members**: 최준용, 강성구, 이상호, 곽준목

## **프로젝트 개요**

- **프로젝트 목표**: 육아 

- **기간**: 23.11.15 ~ 23.12.20

- **결과**:
> <p align="center"><img src="assets/result.jpg" width="840"></p>
>
> - 참고: 김용담강사는 발표회 당일 부재로 발표채점 생략

<br>

### 프로젝트 기술스택

![Python](https://img.shields.io/badge/Python-ffe74a.svg?style=flat&logo=Python&logoColor=blue) 
![airflow](https://img.shields.io/badge/Airflow-ffe74a.svg?style=flat&logo=Python&logoColor=blue) 
![NumPy](https://img.shields.io/badge/NumPy-4d77cf.svg?style=flat&logo=NumPy&logoColor=4dabcf)
![Pandas](https://img.shields.io/badge/Pandas-130654.svg?style=flat&logo=Pandas&logoColor=whitle) 
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C.svg?style=flat&logo=Matplotlib&logoColor=white) 
![Altair](https://img.shields.io/badge/Vega%20Altair-fbc234.svg?style=flat&logo=Vega%20Altair&logoColor=black) 
![Plotly](https://img.shields.io/badge/Plotly-262626.svg?style=flat&logo=Plotly&logoColor=white) 

<br>

## 1. 탐색적 데이터분석(EDA) 수행계획

### **Overview**

데이원컴퍼니(패스트캠퍼스)의 과거 1년치의 데이터를 분석하여 비즈니스 매출 상승 혹은 손실 감소, 고객 서비스에 기여할 만한 인사이트 도출하기. 

- 데이터셋을 살펴본 결과, 분석 가능한 **주요 요인'Factor' 4가지**를 **가정**해 보았습니다. <br> 

- 그 4가지 요인'Factor'를 가지고 교육기업의 **비즈니스 모델을 추론**하고자 했습니다.

- 추론한 비즈니스 모델을 가지고 **특징 및 강점과 약점을 파악**하여, **매출**에 어떻게 **영향**을 미치는지 살펴보았습니다.

- 결과적으로 분석결과에서 마케팅, 컨텐츠제작, 운영 등 **여러가지 관점으로 인사이트를 도출**해 보았습니다.

<br>

### **1st Step.**

현재 데이터 셋으로 어떤 **요인 ‘factor’** 을 분석할 수 있을까?

* **Factor**: **고객**
  * 실거래금액으로 매출, 결제 건, 쿠폰분석을 통해, 주 고객군을 분석한다.
  * B2C, B2B, 학생, 직장인, 기업, 신규 또는 기존 고객 인지 어느 고객이 주 고객이 되는가?
  * 주 고객군이 확인되면 마케팅에서 Audience 설정 전략을 수립 할 수 있지 않을까?

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
