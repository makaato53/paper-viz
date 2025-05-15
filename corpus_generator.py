# corpus_generator.py

import os
import subprocess
import tempfile
import shutil
import glob
import ast
import json
import stat
import errno

# Repos to clone
COMMUNITY_REPO = "https://github.com/3b1b/manim.git"
VIDEOS_REPO    = "https://github.com/3b1b/videos.git"

OUT_DIR = "corpus"  # output directory for JSONL files

def _handle_remove_readonly(func, path, exc_info):
    """
    Error handler for shutil.rmtree to clear read-only and retry on Windows.
    """
    err = exc_info[1]
    if func in (os.rmdir, os.remove, os.unlink) and err.errno == errno.EACCES:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

def extract_examples(repo_dir, out_handle):
    """
    Walk all .py files under repo_dir, extract the module docstring
    or first comment as description, and write the code.
    """
    pattern = os.path.join(repo_dir, "**", "*.py")
    for py_path in glob.glob(pattern, recursive=True):
        try:
            with open(py_path, 'r', encoding='utf8') as f:
                src = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue

        # parse docstring
        try:
            mod = ast.parse(src)
            desc = ast.get_docstring(mod) or ""
        except Exception:
            desc = ""

        # fallback to first comment line
        if not desc:
            for line in src.splitlines():
                if line.strip().startswith("#"):
                    desc = line.strip().lstrip("# ").strip()
                    break

        code = "\n".join(src.strip().splitlines())
        out_handle.write(json.dumps({"desc": desc, "code": code}) + "\n")

def generate_synthetic(out_handle):
    """
    Produce synthetic LaTeX→Manim scene pairs for basic patterns.
    """
    templates = [
        ("Plot $\\sin(x)$ from 0 to $2\\pi$",
         '''
from manimlib.imports import *
class SinPlot(Scene):
    def construct(self):
        axes = Axes(x_length=6, y_length=3)
        graph = axes.get_graph(lambda x: np.sin(x), [0, 2*PI])
        self.play(ShowCreation(axes), ShowCreation(graph))
        self.wait(1)
'''),
        ("Display the equation $E=mc^2$",
         '''
from manimlib.imports import *
class EquationScene(Scene):
    def construct(self):
        eq = TexMobject(r"E=mc^2")
        self.play(Write(eq))
        self.wait(1)
'''),
        # Add more templates here…
    ]
    for desc, code in templates:
        out_handle.write(json.dumps({"desc": desc, "code": code.strip()}) + "\n")

def clone_and_process(repo_url, outfile_path):
    """
    Clone the repo, extract Python examples, then clean up the temp dir.
    """
    tmp_dir = tempfile.mkdtemp()
    try:
        print(f"Cloning {repo_url} …")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, tmp_dir], check=True)
        with open(outfile_path, "w", encoding="utf8") as out_f:
            extract_examples(tmp_dir, out_f)
    finally:
        shutil.rmtree(tmp_dir, onerror=_handle_remove_readonly)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    clone_and_process(COMMUNITY_REPO, os.path.join(OUT_DIR, "manim_community.jsonl"))
    clone_and_process(VIDEOS_REPO,    os.path.join(OUT_DIR, "3b1b_videos.jsonl"))
    with open(os.path.join(OUT_DIR, "synthetic.jsonl"), "w", encoding="utf8") as out_s:
        generate_synthetic(out_s)
    print(f"Corpus generated under '{OUT_DIR}'")

if __name__ == "__main__":
    main()

