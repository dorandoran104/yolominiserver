import os
import shutil
from queue import Queue
from apscheduler.schedulers.background import BackgroundScheduler
from ultralytics import YOLO
import cv2
from datetime import datetime
from threading import Thread
from schedule.process_ocr import process_ocr

# YOLO 모델 로드
# model = YOLO('best_l.pt')

ocr_queue = Queue()

# 이미지 파일이 저장될 폴더 경로
file_path = 'app/download'
target_folder = 'app/file'
find_file_path = 'app/file/find'

# 이미지 확장자 목록
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.ico', '.webp']

def delete_unmatched_files(folder):
    """rider_*.png과 screenshot_*.png의 1:1 대응이 없는 파일 삭제"""
    # rider_*.png 파일 목록
    rider_files = get_rider_files(folder)
    rider_names = {os.path.basename(f).replace("rider_", "") for f in rider_files}

    # screenshot_*.png 파일 목록
    screenshot_files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.startswith("screenshot_") and f.lower().endswith(".png")
    ]
    screenshot_names = {os.path.basename(f).replace("screenshot_", "") for f in screenshot_files}

    # 1:1 대응되지 않는 rider 파일 및 screenshot 파일 삭제
    unmatched_rider_files = [
        f for f in rider_files if os.path.basename(f).replace("rider_", "") not in screenshot_names
    ]
    unmatched_screenshot_files = [
        f for f in screenshot_files if os.path.basename(f).replace("screenshot_", "") not in rider_names
    ]

    for file_path in unmatched_rider_files + unmatched_screenshot_files:
        os.remove(file_path)
        print(f"삭제된 파일: {file_path}")

def get_image_files(image_folder):
    """주어진 폴더에서 이미지 파일을 찾아 리스트로 반환"""
    image_files = []
    for file_name in os.listdir(image_folder):
        file_path = os.path.join(image_folder, file_name)
        if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file_path)
    return image_files

def get_rider_files(image_folder):
    """주어진 폴더에서 이미지 파일을 찾아 리스트로 반환"""
    image_files = []
    for file_name in os.listdir(image_folder):
        if file_name.startswith('rider_'):
            file_path = os.path.join(image_folder, file_name)
            if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in image_extensions):
                image_files.append(file_path)
    return image_files

def move_files_to_folder(image_files, target_folder):
    """이미지 파일을 다른 폴더로 이동"""
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)  # 대상 폴더가 없으면 생성
    
    for file_path in image_files:
        file_name = os.path.basename(file_path)  # 파일명만 추출
        target_path = os.path.join(target_folder, file_name)  # 새 위치에 파일 경로 설정
        
        # 파일 이동
        shutil.move(file_path, target_path)
        print(f"파일이 이동되었습니다: {file_name}")

def job_function():
    """스케줄러 작업 함수 - 주기적으로 실행"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    print(f'스케줄러 작업 실행 : {timestamp}')

    # 이미지 파일 목록 가져오기
    image_files = get_image_files(file_path)

    move_files_to_folder(image_files, target_folder)

    delete_unmatched_files(target_folder)

    image_files = get_rider_files(target_folder)

    for image_file in image_files:
        ocr_queue.put(image_file)
    

def start_scheduler():
    """스케줄러 시작"""
    print('스케줄러 시작')
    ocr_thread = Thread(target=process_ocr, args=(ocr_queue,), daemon=True)
    ocr_thread.start()

    scheduler = BackgroundScheduler()
    scheduler.add_job(job_function, 'interval', seconds=10)  # 10초마다 작업 실행
    scheduler.start()
    return scheduler