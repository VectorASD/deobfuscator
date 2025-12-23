from nodejs import babel_parse_with_cache, babel_generate
from pprint import pprint, pformat
import json




def test_parser_and_generator():
    code = """
    function test(a, b) {
        return a + b;
    }
    """

    ast = babel_parse_with_cache("input.js")
    #with open("ast.json", "w", encoding="utf-8") as file:
    #    json.dump(ast, file, indent=2, ensure_ascii=False, sort_keys=True)
    #pprint(ast)

    print("\n=== Generating ===")
    new_code = babel_generate(ast)
    print(new_code)



if __name__ == "__main__":
    test_parser_and_generator()
