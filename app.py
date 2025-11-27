from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import uuid

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://pythonsubject.o-r.kr"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

@app.post("/")
def run_code(req: CodeRequest):
    tmp_filename = f"/tmp/{uuid.uuid4()}.py"

    with open(tmp_filename, "w") as f:
        f.write(req.code)

    try:
        result = subprocess.run(
            ["python3", tmp_filename],
            capture_output=True,
            text=True,
            timeout=3
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "❗ 실행 시간이 너무 깁니다.",
            "returncode": -1
        }
