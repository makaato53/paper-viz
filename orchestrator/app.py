from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import uuid

app = FastAPI()
redis_client = redis.Redis(host="redis", port=6379)

class PaperContent(BaseModel):
    paper_id: str
    sections: dict  # e.g. {"theorem": "...", "proof": "..."}

@app.post("/enqueue")
def enqueue(content: PaperContent):
    job_id = str(uuid.uuid4())
    payload = content.json()
    redis_client.rpush("job_queue", payload)
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def status(job_id: str):
    # placeholder: check result store
    return {"job_id": job_id, "status": "pending"}
