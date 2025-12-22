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
        text          = True,
        creationflags = subprocess.CREATE_NO_WINDOW, # 0x8000000
        cwd           = os.path.dirname(__file__),
    )
    output, err = proc.communicate(input)
    if proc.returncode != 0:
        raise RuntimeError(f"{name} error:\n{err}")
    return output

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

installer()

# npm install

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
