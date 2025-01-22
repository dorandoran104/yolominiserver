from queue import Queue, Empty
from ultralytics import YOLO
import cv2
import easyocr
import os
import shutil
import time
reader = easyocr.Reader(['ko'])  # 한국어와 영어 지원

# YOLO 모델 로드
model = YOLO('best_l.pt')

upscale_path = 'app/upscale'

def process_ocr(ocr_queue: Queue):
    """OCR 처리 작업"""
    while True:
        file_path = None
        try:
            # 큐에서 파일 가져오기 (5초 대기, 없으면 Empty 예외 발생)
            file_path = ocr_queue.get(timeout=5)
            # ocr_queue.task_done()
            print('')
            print('-' * 50)
            print(f"업스케일링 처리 중: {file_path}")
            print('-' * 50)
            print('')

            image = cv2.imread(file_path)
            file_name = file_path.split('/')[-1]
            
            if image is None:
                print("이미지를 로드할 수 없습니다. 경로를 확인하세요.")
                continue

            results = model.predict(image, verbose=False)
            detections = results[0].boxes
            
            upscaled_image = None
            for box in detections:
                cls = int(box.cls[0].item())
                if cls == 3:  # 클래스 3: Number Plate
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # 바운딩 박스 좌표 (x1, y1, x2, y2)
                    # 바운딩 박스 영역 잘라내기
                    cropped_image = image[y1:y2, x1:x2]
                    # 모델 로드
                    sr = cv2.dnn_superres.DnnSuperResImpl_create()
                    path = 'EDSR_x4.pb'  # 모델 경로
                    sr.readModel(path)
                    # 모델의 이미지 스케일 지정 (여기서는 EDSR x3 모델 사용)
                    sr.setModel('edsr', 4)
                    # 이미지 업스케일링
                    upscaled_image = sr.upsample(cropped_image)

            # 결과 이미지 저장
            # cv2.imwrite(f'{upscale_path}/{file_name}', upscaled)
            if upscaled_image is None:
                print('')
                print('-' * 50)
                print('업스케일링 : 번호판 인식 안됨')
                print('-' * 50)
                print('')
                continue
            
            print('')
            print('-' * 50)
            print('업스케일링 완료')
            print('-' * 50)
            print('')

            # OCR 작업 처리
            print('')
            print('-' * 50)
            print('OCR 작업 처리 중...')
            print('-' * 50)
            print('')

            results = reader.readtext(upscaled_image)

            if len(results) == 0:
                print('')
                print('-' * 50)
                print('OCR : 번호판 인식 어려움')
                print('-' * 50)
                print('')
                # if file_path and os.path.exists(file_path):
                #     try:
                #         os.remove(file_path)
                #         print(f"파일 삭제 완료: {file_path}")
                #     except Exception as delete_error:
                #         print(f"파일 삭제 중 오류 발생: {delete_error}")
                #         time.sleep(1)  # 잠시 대기 후 재시도 가능
                # else:
                #     if file_path:
                #         print(f"파일 경로가 존재하지 않거나 None: {file_path}")
                #     continue

            for result in results:
                text = result[1]  # 추출된 텍스트
                print(f"Detected text: {text}")
            
            ####
            # 번호판 인식 텍스트 조인
            join_text = ''.join([result[1] for result in results])
            print(f"조인된 텍스트: {join_text}")
            if(join_text == ''):
                continue
            
            # 파일 경로 설정
            file_path_ = f'app/file'
            new_file_name = file_name.replace('rider_', '')

            rider_folder_path = os.path.join(file_path_, f'{file_name}')
            screenshot_folder_path = os.path.join('app', 'file', f'screenshot_{new_file_name}')

            # 타임스탬프 추가
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            # 새로운 파일명 설정 (rider와 screenshot 모두 타임스탬프 포함)
            new_rider_name = f"rider_{join_text}_{timestamp}.png"
            new_screenshot_name = f"screenshot_{join_text}_{timestamp}.png"

            new_rider_path = os.path.join('app', 'search', new_rider_name)
            new_screenshot_path = os.path.join('app', 'search', new_screenshot_name)
            
            # 디렉토리가 존재하지 않으면 생성
            os.makedirs(os.path.dirname(new_rider_path), exist_ok=True)
            os.makedirs(os.path.dirname(new_screenshot_path), exist_ok=True)

            try:
                # 파일 이동
                shutil.move(rider_folder_path, new_rider_path)  # rider 파일 이동
                shutil.move(screenshot_folder_path, new_screenshot_path)  # screenshot 파일 이동
                print(f"{new_rider_name}, {new_screenshot_name} 파일이 'find' 폴더로 이동되었습니다.")
            except Exception as e:
                print(f"파일 이동 중 오류 발생: {e}")

            print('')
            print('-' * 50)
            print(f"OCR 작업 완료: {file_name}")
            print('-' * 50)
            print('')

            # 작업 성공적으로 완료되었음을 알림
            # ocr_queue.task_done()

        except Empty:
            # 큐가 비어 있으면 대기
            print('')
            print('-' * 50)
            print("처리할 작업이 없습니다. 대기 중...")
            print('-' * 50)
            print('')

        except Exception as e:
            # 작업 중 오류 처리
            print('')
            print('-' * 50)
            print(f"OCR 처리 중 오류 발생: {e}")
            print('-' * 50)
            print('')
            print(e.format_exc())

            # if file_path and os.path.exists(file_path):
            #     try:
            #         os.remove(file_path)
            #         print(f"파일 삭제 완료: {file_path}")
            #     except Exception as delete_error:
            #         print(f"파일 삭제 중 오류 발생: {delete_error}")
            #         time.sleep(1)  # 잠시 대기 후 재시도 가능
            # else:
            #     if file_path:
            #         print(f"파일 경로가 존재하지 않거나 None: {file_path}")

        finally:
            if file_path:
                ocr_queue.task_done()
            # 파일 처리 후 삭제 (성공, 오류 상관 없이)
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"파일 삭제 완료: {file_path}")
                except Exception as delete_error:
                    print(f"파일 삭제 중 오류 발생: {delete_error}")
                    time.sleep(1)  # 잠시 대기 후 재시도 가능
            else:
                if file_path:
                    print(f"파일 경로가 존재하지 않거나 None: {file_path}")

            # task_done은 항상 마지막에 호출
            
