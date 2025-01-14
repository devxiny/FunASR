import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from funasr import AutoModel
import os
import uuid

app = FastAPI()

model = AutoModel(
    model="outputs",
    device="cuda",
    model_hub="ms",
)


@app.post("/asr")
async def asr(audio_file: UploadFile = File(...), hotword: str = None):
    try:
        unique_id = uuid.uuid4()
        file_extension = audio_file.filename.split(".")[-1]
        file_path = f"temp_{unique_id}.{file_extension}"
        with open(file_path, "wb") as buffer:
            buffer.write(await audio_file.read())
        res = model.generate(input=file_path, batch_size_s=300, hotword=hotword)
        os.remove(file_path)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50009)
