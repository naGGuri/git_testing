import logging
import time
import uuid
from fastapi import FastAPI, Request
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/var/log/fastapi/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fastapi-app")

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # 요청 로깅
    logger.info(f"Request started: {request.method} {request.url.path}")

    response = await call_next(request)

    # 응답 시간 계산
    process_time = time.time() - start_time
    logger.info(f"Request completed: {request.method} {request.url.path} - Took: {process_time:.4f}s")

    return response

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/error")
async def trigger_error():
    logger.error("Error endpoint called - Generating sample error")
    return {"error": "This is a sample error log message"}

@app.get("/uuid")
async def generate_uuid():
    """
    고유한 UUID를 생성하여 반환합니다.
    """
    unique_id = str(uuid.uuid4())
    logger.info("생성된 UUID: %s", unique_id)
    return {"uuid": unique_id}

@app.post("/length")
async def calculate_length(data: dict):
    """
    입력받은 텍스트의 길이를 계산합니다.
    """
    text = data.get("text", "")
    length = len(text)
    logger.info("입력된 텍스트 : %s, 글자 수 : %d", text, length)   
    return {"text": text, "length": length}

@app.get("/time")
async def get_server_time():
    """
    현재 서버 시간을 반환합니다.
    """
    current_time = datetime.now().isoformat()
    logger.info("현재 서버 시간 : %s", current_time)
    return {"server_time": current_time}
