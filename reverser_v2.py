from nodejs import babel_parse, babel_generate
from pprint import pprint, pformat
import json



if __name__ == "__main__":
    code = """
    function test(a, b) {
        return a + b;
    }
    """
    with open("input.js", "r", encoding="utf-8") as file:
        code = file.read()

    print("=== Parsing ===")
    ast = babel_parse(code)
    with open("ast.json", "w", encoding="utf-8") as file:
        json.dump(ast, file, indent=2, ensure_ascii=False, sort_keys=True)
    #pprint(ast)

    print("\n=== Generating ===")
    new_code = babel_generate(ast)
    print(new_code)
