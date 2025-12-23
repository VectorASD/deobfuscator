# choco install nodejs-lts
# node -v     v24.12.0
# npm -v     11.6.2

# npm install @babel/parser @babel/generator
# npm list
# nodejs@1.0.0 C:\Users\VectorASD\Desktop\reverser\nodejs
# +-- @babel/generator@7.28.5
# `-- @babel/parser@7.28.5

import subprocess
import json
import os
import shutil
import pickle
from glob import glob
import requests

NODE = shutil.which("node")
if NODE is None:
    raise RuntimeError("Node.js не найден в PATH. Возможно, нужен перезапуск python GUI после 'choco install nodejs-lts' >:{")
# print(NODE) # C:\Program Files\nodejs\node.EXE

def communicator(path: tuple[str, str], input: str = None, name: str = "Communicator") -> str:
    proc = subprocess.Popen(
        path,
        stdin  = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
      # text          = True,   "text" gives cp1251, but requires utf-8 encoding.
        creationflags = subprocess.CREATE_NO_WINDOW, # 0x8000000
        cwd           = os.path.dirname(__file__),
    )
    output, err = proc.communicate(input.encode("utf-8") if input else None)
    if proc.returncode != 0:
        err = err.decode("utf-8", errors="replace")
        raise RuntimeError(f"{name} error:\n{err}")
    return output.decode("utf-8", errors="replace")

def babel_parse(code: str) -> dict:
    output = communicator((NODE, "parse.js"), code, "Parser")
    return json.loads(output)

def babel_generate(ast: dict) -> str:
    output = communicator((NODE, "generate.js"), json.dumps(ast), "Generator")
    return output

def installer():
    path = os.path.join(os.path.dirname(__file__), "node_modules")
    if os.path.exists(path): return

    print("[Installer] node_modules не найден. Запускаю npm install...")
    output = communicator((NODE, "-e", "require('child_process').execSync('npm install', {stdio: 'inherit'})"), None, "Installer")
    print("    ", end="")
    print(*output.replace("\n\n", "\n").strip().split("\n"), sep="\n    ")
    print("[Installer] Установка завершена.")

installer() # npm install

def babel_parse_with_cache(path: str):
    cache_path = path + ".ast"
    mtime = os.stat(path).st_mtime
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as file:
            mtime2, ast = pickle.load(file)
            if mtime2 == mtime:
                print(f"=== Parsing {os.path.basename(path)!r} (from .ast) ===")
                return ast

    print(f"=== Parsing {os.path.basename(path)!r} (from .js) ===")
    with open(path, "r", encoding="utf-8") as file:
        code = file.read()
    print(path)
    ast = babel_parse(code)

    with open(cache_path, "wb") as file:
        pickle.dump((mtime, ast), file)
    return ast

import os
from glob import glob
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def babel_parse_from_url(
    names,
    protocols=(b"http", b"https"),
    agent=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36"
    ),
    workers=8,
):
    js_names = set()
    url_names = set()

    # Собираем *.js и *.js.url
    for name in names:
        js_names.update(glob(name))
        url_names.update(glob(name + ".url"))

    # Собираем URL → имя файла
    urls = {}
    for url_name in url_names:
        js_name, ext = os.path.splitext(url_name)
        if ext == ".url" and not os.path.exists(js_name):
            with open(url_name, "rb") as file:
                for line in file:
                    line = line.split(b" #", 1)[0].strip()
                    if line.split(b"://", 1)[0] in protocols:
                        urls[line.decode("utf-8")] = js_name

    if urls:
        def download(url, js_name):
            try:
                r = requests.get(url, headers={"User-Agent": agent}, timeout=20)
                r.raise_for_status()
                return r.content, js_name, None
            except Exception as e:
                return None, js_name, e

        print(f"[INFO] Скачиваю {len(urls)} файлов...")

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [
                pool.submit(download, url, js_name)
                for url, js_name in urls.items()
            ]

            for future in as_completed(futures):
                content, js_name, error = future.result()
                if error:
                    print(f"[ERROR] Не удалось скачать {js_name}: {error}")
                else:
                    print(f"[OK] {js_name} скачан")
                    js_names.add(js_name)
                    with open(js_name, "ab") as f:
                        f.write(content)
                        f.write(b"\n")

    return tuple(map(babel_parse_with_cache, js_names))




if __name__ == "__main__":
    # Пример JS-кода
    code = """
    function test(a, b) {
        return a + b;
    }
    """

    print("=== Parsing ===")
    ast = babel_parse(code)
    print(json.dumps(ast, indent=2, ensure_ascii=False, sort_keys=True))

    print("\n=== Generating ===")
    new_code = babel_generate(ast)
    print(new_code)
