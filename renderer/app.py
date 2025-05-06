from fastapi import FastAPI
import subprocess, os, uuid
from pydantic import BaseModel

app = FastAPI()

class RenderJob(BaseModel):
    type: str
    latex: str

@app.post("/render")
def render_math(job: RenderJob):
    job_id = str(uuid.uuid4())
    scene_file = f"scenes/{job_id}.py"
    os.makedirs("scenes", exist_ok=True)
    with open(scene_file, "w") as f:
        f.write(f"""
from manimlib.imports import *

class RenderScene(Scene):
    def construct(self):
        stmt = TexMobject(r\"{job.latex}\")
        self.play(Write(stmt))
        self.wait(1)
""")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run([
        "manimgl", scene_file, "RenderScene",
        "-o", f"{output_dir}/{job_id}.mp4"
    ], check=True)
    return {"job_id": job_id, "video_path": f"/output/{job_id}.mp4"}
