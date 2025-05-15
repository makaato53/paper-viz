from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import subprocess
import os

app = FastAPI()

@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded file to disk
        input_path = "/tmp/input.pdf"
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Run the compiled C++ binary on the file
        result = subprocess.run(
            ["./build/pdf_ingest", input_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return JSONResponse(
                status_code=500,
                content={"error": result.stderr.strip()}
            )

        return {"output": result.stdout.strip()}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
