from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import re

app = FastAPI()
summarizer = pipeline("summarization")

class SummarizeRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    # Generate concise summary
    result = summarizer(req.text, max_length=150, min_length=50, do_sample=False)
    summary_text = result[0]['summary_text']

    # Extract LaTeX fragments as key items
    items = []
    for m in re.finditer(r"\$(.+?)\$", req.text):
        items.append({"type": "equation", "latex": m.group(1)})
    return {"summary": summary_text, "items": items}
