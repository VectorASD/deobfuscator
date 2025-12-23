from nodejs import babel_parse_with_cache, babel_parse, babel_generate
from pprint import pprint, pformat
import json

from analizer import aliases, mro




def test_parser_and_generator():
    ast = babel_parse_with_cache("input.js")
    #with open("ast.json", "w", encoding="utf-8") as file:
    #    json.dump(ast, file, indent=2, ensure_ascii=False, sort_keys=True)
    #pprint(ast)

    print("\n=== Generating ===")
    print(babel_generate(ast))



def printer(node):
    def get_type(value):
        if type(value) is not dict: return 0, f"TypeError(type is {type(value).__name__!r}, not dict)"
        if "type" not in value:     return 0, f"NodeError('type' is not defined)"
        return 1, value["type"]
    def check_type(value, alias):
        types = set(alias.split("|"))
        if "null" in types:
            if value is None: return 0, "null"
            types.remove("null")
        else:
            if value is None: return 0, "null (ValueError)"
        is_node, Type = get_type(value)
        if not is_node: return 0, Type

        if Type in types: return 1, Type
        parents = mro[Type]
        for parent in parents:
            if parent in types: return 1, Type
        return 0, f"ValueError('type' = {Type}<:{'<:'.join(parents)}, not {alias})"

    def visit_node(node, Type, level=0):
        level += 1
        pad = "  " * level
        for key, value in node.items():
            if key in {"type", "start", "end", "loc", "extra", "leadingComments", "trailingComments"}: continue
            alias = aliases.get((Type, key))
            if not alias:
                print(f"{pad}{key} = {value!r}")
                continue

            if alias[0] == "[":
                if type(value) not in (list, tuple):
                    print("f{pad}{key} = [TypeError(type is {type(value).__name__!r}, not list|tuple)]")
                    continue
                if not value:
                    print(f"{pad}{key} = []")
                    continue
                print(f"{pad}{key} = [")
                for item in value:
                    is_node, subtype = check_type(item, alias[1:-1])
                    if is_node:
                        print(f'{pad}  ({subtype}):')
                        visit_node(item, subtype, level+1)
                    else: print(f"{pad}  {subtype}")
                print(f"{pad}]")
                continue

            is_node, subtype = check_type(value, alias)
            if is_node:
                print(f'{pad}{key} ({subtype}):')
                visit_node(value, subtype, level)
            else: print(f"{pad}{key} = {subtype}")

    is_node, Type = get_type(node)
    if is_node:
        print(f'root ({Type}):')
        visit_node(node, Type)
    else: print("error:", Type)

def visitor(ast):
    def check_type(node, T):
        if node["type"] != T:
            raise ValueError(f'Ожидался узел типа {T}, не {node["type"]}')

    def File(node):
        check_type(node, "File")
        printer(node)#node["program"])

    File(ast)



def main():
    # ast = babel_parse_with_cache("input.js")
    code = """
var x = 123;
console.log(x);
    """
    ast = babel_parse(code)
    visitor(ast)

if __name__ == "__main__":
    # test_parser_and_generator()
    main()
