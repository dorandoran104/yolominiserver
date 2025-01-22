# 오토바이 헬멧 미착용 탐지 프로젝트

![1.jpg](image/1.jpg)

# 1. 프로젝트 소개

<aside>
🚩

### **주제: 오토바이 헬멧 미착용 감지 시스템**

- **목표**: 헬멧 미착용으로 인해 발생하는 교통사고를 줄이기
- **기술**: YOLO를 이용한 헬멧 미착용 감지
         OCR을 활용한 번호판 인식
- **기능**:
    1. 블랙박스 영상에서 오토바이 운전자의 헬멧 착용 여부를 실시간으로 감지
    2. 미착용이 확인되면 번호판을 OCR로 인식하여 즉각 신고 가능

### 핵심 타겟

- 블랙박스를 활용한 교통 법규 준수를 강화하여 안전한 도로 환경을 조성하고 헬멧 미착용으로 인해 발생하는 교통사고를 줄이기 원하는 교통 당국 및 관련 기관
</aside>

## 1-1. Yolo 소개

![image.png](image/image.png)

- **YOLO**는 You Only Look Once의 약자로, 빠르고 정확하게 이미지 내의 객체를 배경과 구분해 **식별하는 것(Classification)**뿐만 아니라, 이미지 내 해당 객체의 위치까지 표시하는 알고리즘으로써 컴퓨터 비전 분야에서 객체 탐지시 표준적으로 쓰인다.

## **1-2. 진행순서**

<aside>
💡

### **1. 데이터 수집**

- 헬멧 착용 및 미착용 상태의 오토바이 이미지 및 영상 수집.
- 다양한 각도, 조명, 환경에서의 이미지 확보.

### **2. 데이터 라벨링**

- LabelImg, Roboflow를 사용하여 헬멧 착용 여부와 오토바이 위치를 라벨링.
- 라벨링 클래스: rider, with helmet, without helmet, number plate

### **3. YOLO 모델 학습**

**✔ 환경 설정**

- Python 및 YOLO11 라이브러리 설치
- 필요한 라이브러리 설치: PyTorch, OpenCV, ultralytics 등.

**✔ 데이터셋 준비**

- 라벨링된 데이터를 `train`, `validation`,  8:2 로 분리.
- YOLO 형식에 맞게 데이터셋 구성, `images/` 및 `labels/` 디렉토리 정리

**✔ 모델 학습**

- YOLO 모델의 설정 파일 수정
- epochs = 100, batch = 16
- 학습 과정에서 성능 확인 (mAP, precision, recall)

### **4. 시스템 구현**

- OpenCV로 블랙박스 영상 스트림 처리.
- OCR을 통해 번호판 텍스트 추출.
- YOLO와 OCR을 실시간으로 실행.
</aside>

## **1-4. 사용툴**

<aside>
💡

- **백엔드** : python 3.10, 3.8
- **모델** : YOLO11v
- **버전 관리** : Git
- **IDE** : Visual Studio Code
</aside>

# 2. 프로젝트 개발내용

## **2-1. 데이터 수집**

- **초기 데이터 수집**
    - **캐글(Kaggle)**에서 오토바이 관련 사진 자료 약 150장을 수집하여 초기 학습 데이터로 사용.
    
    ![image.png](image/image(1).png)
    
    - 자료에는 다양한 환경에서 촬영된 오토바이 이미지가 포함되어 있었음.
- **추가 데이터 수집**
    - 블랙박스를 기준으로 탐지 시스템을 구현하기 위해 
    **국내 블랙박스 영상**을 캡처하여 약 150장을 추가로 수집.
    - 국내 도로 환경에 적합한 데이터 확보를 목표로 함.
    
    ![image.png](image/image(2).png)
    
- **라벨링 문제**
    - 캐글에서 받은 데이터의 라벨링이 프로젝트의 요구사항과 다름:
        - 예: 캐글 데이터에는 **번호판 라벨링**이 우리의 기준과 맞지 않음
    - 따라서, 기존 데이터에 번호판 라벨링을 없애고 우리의 기준에 맞는 번호판만 라벨링
- **최종 라벨링**
    - 총 **300장**의 이미지를 프로젝트 요구사항에 맞게 새롭게 라벨링:
        - 클래스: `헬멧 착용`, `헬멧 미착용`, `오토바이`, `번호판`.
    - 라벨링 도구 Labelimg를 활용하여 데이터를 일관성 있게 구성.

## **2-2. 데이터 라벨링**

- LabelImg
    - LabelImg는 이미지 주석 작업을 위한 오픈 소스 그래픽 툴로, 주로 객체 탐지 모델을 훈련하기 위해 이미지에 라벨을 붙이는 데 사용됩니다. 이 툴은 Python과 Qt5로 작성되었으며, 사용자가 이미지를 로드하고, 객체에 경계 상자를 그린 후 이를 라벨링하여 XML 형식(PASCAL VOC 포맷) 또는 YOLO 포맷으로 저장할 수 있습니다.
    
- Roboflow
    - **Roboflow**는 머신러닝 모델 개발과 데이터셋 준비를 위한 플랫폼으로, 특히 컴퓨터 비전 작업을 위한 강력한 툴을 제공합니다. 사용자는 Roboflow를 통해 이미지 주석을 추가하고, 다양한 형식으로 데이터셋을 변환하고, 모델을 훈련시키는 과정까지 쉽게 진행할 수 있습니다.
    
    | 기능 | **LabelImg** | **Roboflow** |
    | --- | --- | --- |
    | **설치 방식** | 로컬 애플리케이션 | 클라우드 기반 웹 플랫폼 |
    | **주요 용도** | 단순 이미지 라벨링 | 데이터 관리, 자동화, 모델 학습까지 통합 |
    | **자동 라벨링** | 지원하지 않음 | 지원 (AI 기반) |
    | **협업 기능** | 없음 | 있음 (팀 작업 가능) |
    | **데이터 증강** | 없음 | 있음 |
    | **사용 비용** | 무료 | 무료 플랜 + 유료 플랜 |
    | **대규모 데이터 관리** | 불편 | 최적화 |
- Roboflow는 라벨링 작업을 쉽게 수행하고 팀원들과 협업할 수 있는 장점이 있지만,
    
    유료라는 단점이 있어 LabelImg를 사용하여 라벨링 작업을 진행하였습니다.
    

## **2-3. YOLO모델 학습**

- **모델 크기**
    - **YOLO 모델 크기별 학습**:
        - `small (x)` , `small (s)`, `medium (m)`, `large (l)` 네 가지 크기의 모델을 사용하여 비교 실험.
- **데이터셋**
    - 사용 데이터: 커스터마이즈된 300장의 데이터셋 
    (`data.yaml` 파일로 구성).
    
    ![image.png](%E1%84%8B%E1%85%A9%E1%84%90%E1%85%A9%E1%84%87%E1%85%A1%E1%84%8B%E1%85%B5%20%E1%84%92%E1%85%A6%E1%86%AF%E1%84%86%E1%85%A6%E1%86%BA%20%E1%84%86%E1%85%B5%E1%84%8E%E1%85%A1%E1%86%A8%E1%84%8B%E1%85%AD%E1%86%BC%20%E1%84%90%E1%85%A1%E1%86%B7%E1%84%8C%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8C%E1%85%A6%E1%86%A8%E1%84%90%E1%85%B3%2002e6de0087eb4b21912aaf5ca1136b7c/image%203.png)
    
    - 데이터 분류:
        - `헬멧 착용`
        - `헬멧 미착용`
        - `오토바이`
        - `번호판`
- **학습 설정**
    - **기존 모델 활용**: 사전 학습된 가중치(`yolo11l.pt`)를 기반으로 추가 학습.
    - **하이퍼파라미터**:
        - 학습 횟수 (`epochs`): 100
        - 입력 이미지 크기 (`imgsz`): 640
        - 배치 크기 (`batch`): 16
        - 작업자 수 (`workers`): 8
    - **기타 설정**:
        - GPU 사용: `device=0` (GPU로 학습)
        - 조기 종료 기준 (`patience`): 50
        - 모델 저장:
            - 학습 결과 저장 활성화 (`save=True`).
            - 저장 주기 (`save_period`): 10 에포크마다 저장.
- **결과 비교 기준**
    - **모델 크기별 성능 평가**:
        - 정확도 (mAP)
        - 재현율 (Recall)
        - 정밀도 (Precision)
        - 학습 속도 (시간)
        - 모델 크기 및 메모리 사용량
    - **최적 모델 선택**:
        - 모델 크기와 성능의 균형을 기준으로 적합한 모델 선택.
- **특이사항**
    - 모델 크기에 따른 장단점:
        - `small`: 학습 속도가 빠르지만 정확도는 낮을 가능성이 있음.
        - `medium`: 속도와 성능의 균형.
        - `large`: 높은 정확도 가능하지만 메모리 사용량과 속도 저하 발생

- **학습 환경**

| **항목** | **GTX 1060** | **Colab T4** |
| --- | --- | --- |
| **성능** | 상대적으로 낮은 연산 성능 | 높은 연산 성능, Turing 아키텍처 기반 |
| **VRAM 용량** | 6GB | 16GB |
| **비용** | 초기 비용만 지불 (구매 비용) | 사용량에 따라 무료/유료 |
| **사용 편의성** | 로컬에서 직접 설정 필요 | 사전 설정된 환경 제공, 빠른 시작 가능 |
| **유지관리** | 하드웨어 관리 필요 | Google이 유지관리 담당 |
| **인터넷 의존성** | 인터넷 없이 로컬에서 학습 가능 | 인터넷 필요, 연결이 끊기면 작업 중단 가능 |
| **제한사항** | 하드웨어 업그레이드가 필요할 수 있음 | 무료 사용 시 시간/세션 제한 존재 |
| **확장성** | 동일 장비에서 확장 어려움 | 유료 플랜을 통해 고성능 GPU 사용 가능 |
- **요약**
    - **GTX 1060**은 로컬에서 직접 작업하기 적합하며 인터넷 연결이 필요 없지만, 성능과 VRAM이 제한적입니다.
    - **Colab T4**는 고성능과 대용량 VRAM을 제공하며, 클라우드 환경에서 쉽게 작업을 시작할 수 있지만, 인터넷 의존성과 세션 제한이 있습니다.

## **2-4. 시스템 구현**

- **YOLO 모델을 활용한 객체 검출**:
    - YOLO 모델(`best_n.pt`)을 사용하여 라이더, 헬멧 미착용자, 번호판을 탐지합니다.
    - 탐지된 객체는 클래스 값으로 분류되며, 특정 조건(라이더 + 헬멧 미착용 + 번호판)이 만족되면 후속 작업을 진행합니다.

- OpenCV를 활용한 동영상 스트림 처리
    - **YOLO 모델을 활용한 객체 탐지**
        - OpenCV로 읽어온 영상 프레임에서 특정 영역(예: 라이더 또는 번호판)을 잘라 YOLO 모델에 전달합니다.
        - YOLO 모델은 라이더, 헬멧 미착용, 번호판 등 객체를 검출하며, 결과는 조건에 따라 필터링됩니다.
    - **검출된 객체 저장**
        - YOLO 검출 결과에서 라이더, 헬멧 미착용, 번호판이 모두 확인되면 해당 영역 이미지를 OpenCV의 `cv2.imwrite` 함수로 저장합니다.
        - 저장된 파일은 `processed/` 디렉터리에 `rider_<타임스탬프>.png` 형식으로 저장됩니다.압축 없이 저장하도록 설정(`cv2.IMWRITE_PNG_COMPRESSION = 0`)되었습니다.
    - **처리 결과 관리**
        - OpenCV를 통해 검출된 이미지를 저장하며, 저장된 파일은 후속 분석이나 증거 자료로 활용될 수 있습니다.
        - 디렉터리 생성과 파일 저장은 자동화되어 있어 스트림 처리의 효율성을 높입니다.

- OCR을 통해 번호판 텍스트 추출
    
    <aside>
    💡
    
    OCR(Optical Character Recognition)은 **광학 문자 인식** 기술로, 이미지나 문서에서 텍스트를 자동으로 인식하고 이를 편집 가능한 텍스트로 변환하는 기술입니다. 이 기술은 스캔한 문서, 사진 또는 이미지를 처리하여 그 안의 텍스트를 추출하는 데 사용됩니다.
    
    </aside>
    
    | OCR 모델 | 장점 | 단점 | 비용 |
    | --- | --- | --- | --- |
    | **EasyOCR** | 사용 간편, 다국어 지원, 
    딥러닝 기반 | 느린 처리 속도, GPU 성능 필요 | 무료 |
    | **Tesseract** | 무료, 오픈소스, 많은 튜토리얼 | 복잡한 레이아웃 인식 약함, 낮은 정확도 | 무료 |
    | **Google Cloud Vision** | 뛰어난 정확도, 클라우드 기반 | 유료, 클라우드 연결 필요 | 사용량 기반 |
    | **AWS Textract** | 텍스트, 테이블, 폼 인식 강력 | 유료, 클라우드 연결 필요 | 사용량 기반 |
    | **Microsoft Azure OCR** | 뛰어난 성능, 다국어 지원, 클라우드 통합 | 유료, 클라우드 연결 필요 | 사용량 기반 |
    
    - EasyOCR은 속도는 상대적으로 느리지만 무료로 제공되며, 다국어를 지원하고
        
        Tesseract보다 정확도가 높습니다. 특히 흐릿한 번호판도 인식이 필요할 때도 있어 
        
        이 모델을 선택하게 되었습니다.
        
    
    - **이미지에서 텍스트 추출**
        - `reader.readtext(upscaled_image)`는 업스케일링된 번호판 이미지(`upscaled_image`)에서 텍스트를 추출합니다.
        - `results`는 EasyOCR의 인식 결과로, 각 텍스트 영역의 정보(텍스트, 위치, 신뢰도)를 포함합니다.
    - **번호판 텍스트 인식 실패 처리**
        - `results`가 비어 있을 경우, OCR이 번호판을 인식하지 못한 것으로 간주하고 경고 메시지를 출력합니다:

## **2-5. 이슈사항**

### **✔ 문제점**

1. **번호판 정보 인식 실패**
    - 헬멧을 미착용한 오토바이 운전자를 포착하였으나, 번호판에 있는 정보를 OCR로 정확히 인식하지 못하는 경우 발생.
2. **누락된 프레임**
    - 영상 처리 중 특정 프레임이 누락되어 헬멧 미착용 운전자와 번호판을 정확히 포착하지 못하는 상황 발생.

---

### **✔ 개선방향**

1. **업스케일링**
    - 번호판 영역을 확대하여 OCR이 텍스트를 더 잘 인식하도록 영상 품질 개선.
    - 이미지 해상도를 높이는 방식으로 OCR 성능 향상 시도.
2. **프레임 세분화**
    - 영상에서 프레임을 더 세밀하게 쪼개어 중요한 순간을 놓치지 않도록 처리.
    - 초당 프레임 수(Frame per Second, FPS)를 증가시켜 더 많은 데이터를 분석.

![frame_2738_rider_warning.jpg](%E1%84%8B%E1%85%A9%E1%84%90%E1%85%A9%E1%84%87%E1%85%A1%E1%84%8B%E1%85%B5%20%E1%84%92%E1%85%A6%E1%86%AF%E1%84%86%E1%85%A6%E1%86%BA%20%E1%84%86%E1%85%B5%E1%84%8E%E1%85%A1%E1%86%A8%E1%84%8B%E1%85%AD%E1%86%BC%20%E1%84%90%E1%85%A1%E1%86%B7%E1%84%8C%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8C%E1%85%A6%E1%86%A8%E1%84%90%E1%85%B3%2002e6de0087eb4b21912aaf5ca1136b7c/frame_2738_rider_warning.jpg)

![frame_27495_rider_warning.jpg](%E1%84%8B%E1%85%A9%E1%84%90%E1%85%A9%E1%84%87%E1%85%A1%E1%84%8B%E1%85%B5%20%E1%84%92%E1%85%A6%E1%86%AF%E1%84%86%E1%85%A6%E1%86%BA%20%E1%84%86%E1%85%B5%E1%84%8E%E1%85%A1%E1%86%A8%E1%84%8B%E1%85%AD%E1%86%BC%20%E1%84%90%E1%85%A1%E1%86%B7%E1%84%8C%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8C%E1%85%A6%E1%86%A8%E1%84%90%E1%85%B3%2002e6de0087eb4b21912aaf5ca1136b7c/frame_27495_rider_warning.jpg)

### **✔ 오탐지 문제**

- 라이더가 검출된 이후, 뒤쪽에 헬멧을 쓰지 않은 라이더가 추가로 검출되었을 때, 모델이 해당 라이더를 이전에 검출된 라이더와 동일 인물로 잘못 인식하는 현상이 발생.
- 잘못된 라이더 식별로 인해 정확한 위반자 기록 및 번호판 인식 오류 발생 가능.

---

**✔ 개선방향**

<aside>
💡

문제를 해결하기 위한 접근법은, 결제 시스템에서 사용되는 검증 로직을 참고하여 

두 단계의 추론 과정을 도입하는 것이었습니다. 

첫 번째 단계는 간단한 n 모델을 사용하여 1차 추론을 하고, 

이때 문제가 될 수 있는 영역을 crop한 뒤, 

두 번째 단계로 학습이 완료된 L 모델을 사용하여 2차 검증을 진행했습니다. 

이 방식은 모든 상황에서 완벽하게 작동하지는 않았지만, 대부분의 잘못된 인식 문제를 해결하는 데 유효한 결과를 보여주었습니다.

</aside>

### **✔ 프레임 드랍 현상**

- 두 모델 YOLO과 OCR 이 연속적으로 실행되면서 처리 속도가 저하되어 일부 프레임이 누락되는 문제 발생.

---

### **✔ 개선방향**

<aside>
💡

스케줄러를 통해 배치 작업을 실행했던 기억이 있어, 
서버의 병렬처리를 활용하는 방법을 떠올리게 되었다.

</aside>

- **병렬처리**
    
    서버에서 병렬 처리는 여러 작업을 동시에 처리하여 성능을 향상시키는 기법입니다. 
    
    이를 통해 서버는 더 많은 요청을 빠르게 처리할 수 있으며, 특히 많은 사용자나 요청이 동시에 들어오는 경우에 유용합니다.
    

- 프로세스 와 쓰레드

| 항목 | 프로세스 (Process) | 쓰레드 (Thread) |
| --- | --- | --- |
| **독립성** | 독립적으로 실행되며, 다른 프로세스와 메모리 공유 안 함 | 같은 프로세스 내에서 메모리 공간을 공유 |
| **메모리** | 독립적인 메모리 공간 | 프로세스의 메모리 공간을 공유 |
| **자원 소비** | 새로운 프로세스를 생성하는 데 많은 자원과 시간이 소요 | 쓰레드는 적은 자원으로 생성 가능 |
| **오류 전파** | 하나의 프로세스 오류는 다른 프로세스에 영향 안 미침 | 쓰레드 오류는 같은 프로세스 내 다른 쓰레드에 영향 미칠 수 있음 |
| **사용 예** | 웹 브라우저, 텍스트 에디터, 독립 실행 프로그램 등 | 서버에서 동시 요청 처리, 멀티태스킹 등 |
| **이미지 처리** | 독립적인 프로세스로서 각 프로세스에서 독립적인 이미지 처리 가능, 자원 소비 많음 | 동일 프로세스 내에서 여러 쓰레드가 이미지 처리 작업을 병렬로 처리 가능, 자원 효율적 |
| **HTTP 통신** | 각각의 HTTP 요청에 대해 별도의 프로세스를 생성하면, 요청을 독립적으로 처리 가능하지만, 자원 소모가 크고 느릴 수 있음 | HTTP 요청을 병렬로 처리할 수 있는 쓰레드를 활용하면, 빠르고 효율적인 처리 가능, 서버 자원 공유로 성능 향상 |

검증을 위한 이미지 처리 및 서버와의 통신을 효율적으로 수행하기 위해, 스레드를 사용하는 것이 더 적합하다고 판단하여 스레드를 활용했습니다.

### **✔ HTTP통신으로 인한 성능저하**

- 서버와의 계속되는 통신으로 인해 성능 저하 이슈 발생
    - 스케줄러를 통해 일정 간격으로 서버에 요청을 보내는데 만약 서버에서 요청을 보내는 시간보다 응답시간이 늦어져서 요청이 쌓이게 될수도 있을것같다는 생각이 들었다.

<aside>
💡

서버에서 HTTP 통신을 통해 파일을 업스케일링 및 OCR 처리하는 작업을 한 번에 실행하는 것은 여러 가지 성능 문제를 유발할 수 있습니다. 이러한 문제를 해결하기 위해 비동기 처리, 큐 시스템, 병렬 처리 등을 적용하여 서버의 자원을 효율적으로 관리하고, 클라이언트가 빠르게 응답을 받을 수 있도록 개선할 필요가 있습니다.

</aside>

<aside>
💡

서버에 10초마다 HTTP 요청을 보내는데 서버가 응답을 주는 데 20초가 걸린다면, 두 가지 주요 현상이 발생할 수 있습니다:

1. **요청 대기열의 증가**: 10초마다 새로운 요청이 서버에 도달하는데, 각 요청에 대한 응답 시간이 20초가 걸리므로, 서버는 동시에 처리해야 할 요청을 계속 쌓게 됩니다. 서버의 처리 능력을 초과하는 요청이 발생할 경우, 응답 시간이 더 길어지거나, 요청을 거부할 수 있습니다.
2. **서버 과부하**: 서버는 응답이 늦어진 상태에서 계속 요청을 처리하게 되면 자원이 부족해질 수 있습니다. CPU, 메모리, 네트워크 대역폭 등의 자원이 과도하게 소모되어 서버의 성능이 저하되거나, 서버가 다운될 위험이 생길 수 있습니다.
</aside>

---

### **✔ 개선방향**

<aside>
💡

서버는 클라이언트로부터 요청을 받으면 별도의 추가적인 비즈니스 로직을 처리하지 않고, 파일 다운로드가 완료된 후 즉시 응답을 반환하는 방식으로 설계되었습니다. 다운로드된 이미지 파일들은 스케줄러에 의해 주기적으로 불러오며, 이를 병렬 처리하기 위해 멀티스레딩 기법을 적용하여 각 파일을 독립적으로 처리합니다. 이 접근법은 효율적인 리소스 관리와 동시에 다수의 이미지 파일을 빠르게 처리할 수 있도록 돕습니다.

</aside>
