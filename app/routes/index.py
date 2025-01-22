from fastapi import APIRouter, File, UploadFile, Form
from typing import List
import os
router = APIRouter()

image_folder = "app/download"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

@router.post('/upload')
async def upload_file(files: List[UploadFile] = File(...)):
    print('파일 들어옴')
    
    saved_files = []

    for file in files:
        # 파일 경로 설정 (파일 이름을 그대로 사용, 파일 이름 중복 방지를 위해 타임스탬프 추가 가능)
        file_path = os.path.join(image_folder, file.filename)
        # 파일 내용을 저장
        try:
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            print(f"파일 저장 완료: {file.filename}")
            saved_files.append(file.filename)
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")

    return {"result": "success"}
