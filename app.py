from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import uuid

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/run")
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
            "stderr": "❗ 실행 시간이 너무 길어 종료되었습니다.",
            "returncode": -1
        }
