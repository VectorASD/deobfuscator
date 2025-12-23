from nodejs import babel_parse_with_cache, babel_generate
from pprint import pprint, pformat
import json
from collections import defaultdict, Counter, deque
import os



"""
let aliases = [], supers = [];
for (const item of document.getElementsByClassName("highlight-source-js")) {
    const text = item.getElementsByTagName("pre")[0].textContent;
    if (text.startsWith("interface"))
        for (const interface of text.split("interface").slice(1)) {
            const lines = interface.split("\n");
            const first_line = lines[0].split("{", 1)[0];
            const name = lines[0].split(/<:|{/)[0].trim();
            let _super = first_line.split("<:")[1];
            _super = _super ? JSON.stringify(_super.split(",").map(x=>x.trim())) : "None";
            supers.push('"' + name + '": ' + _super + ",");
            for (const line of lines.slice(1))
                if (line.includes(":")) {
                    const key = line.split(":", 1)[0].trim().replace("?","");
                    const pair = '("' + name + '", "' + key + '")';
                    let value;
                    if (line.includes("[")) {
                        value = line.split(":")[1].replaceAll(";", "").replaceAll(" ", "");
                    } else if (line.includes(":") && !line.includes('"') && line != line.toLowerCase()) {
                        value = line.split(":")[1].replaceAll(";", "").replaceAll(" ", "");
                    }
                    if (value) aliases.push(pair + ': "' + value + '",');
                }
        }
}
aliases.sort();
console.log(aliases.join("\n"));
console.log(supers.join("\n"));
"""
aliases = {
    ("ArrayExpression", "elements"): "[Expression|SpreadElement|null]",
    ("ArrayPattern", "elements"): "[Pattern|null]",
    ("ArrowFunctionExpression", "body"): "BlockStatement|Expression",
    ("AssignmentExpression", "left"): "Pattern|Expression",
    ("AssignmentExpression", "operator"): "AssignmentOperator",
    ("AssignmentExpression", "right"): "Expression",
    ("AssignmentPattern", "left"): "Pattern",
    ("AssignmentPattern", "right"): "Expression",
    ("AssignmentProperty", "value"): "Pattern",
    ("AwaitExpression", "argument"): "Expression|null",
    ("BinaryExpression", "left"): "Expression|PrivateName",
    ("BinaryExpression", "operator"): "BinaryOperator",
    ("BinaryExpression", "right"): "Expression",
    ("BindExpression", "callee"): "Expression",
    ("BindExpression", "object"): "Expression|null",
    ("BlockStatement", "body"): "[Statement]",
    ("BlockStatement", "directives"): "[Directive]",
    ("BreakStatement", "label"): "Identifier|null",
    ("CallExpression", "arguments"): "[Expression|SpreadElement]",
    ("CallExpression", "callee"): "Expression|Super|Import",
    ("CatchClause", "body"): "BlockStatement",
    ("CatchClause", "param"): "Pattern",
    ("Class", "body"): "ClassBody",
    ("Class", "decorators"): "[Decorator]",
    ("Class", "id"): "Identifier|null",
    ("Class", "superClass"): "Expression|null",
    ("ClassAccessorProperty", "key"): "Expression|PrivateName",
    ("ClassAccessorProperty", "value"): "Expression",
    ("ClassBody", "body"): "[ClassMethod|ClassPrivateMethod|ClassProperty|ClassPrivateProperty|StaticBlock]",
    ("ClassDeclaration", "id"): "Identifier",
    ("ClassMethod", "decorators"): "[Decorator]",
    ("ClassMethod", "key"): "Expression",
    ("ClassPrivateMethod", "decorators"): "[Decorator]",
    ("ClassPrivateMethod", "key"): "PrivateName",
    ("ClassPrivateProperty", "key"): "PrivateName",
    ("ClassPrivateProperty", "value"): "Expression",
    ("ClassProperty", "key"): "Expression",
    ("ClassProperty", "value"): "Expression",
    ("ConditionalExpression", "alternate"): "Expression",
    ("ConditionalExpression", "consequent"): "Expression",
    ("ConditionalExpression", "test"): "Expression",
    ("ContinueStatement", "label"): "Identifier|null",
    ("Decorator", "expression"): "Expression",
    ("Directive", "value"): "DirectiveLiteral",
    ("DoExpression", "body"): "BlockStatement",
    ("DoWhileStatement", "body"): "Statement",
    ("DoWhileStatement", "test"): "Expression",
    ("ExportAllDeclaration", "attributes"): "[ImportAttribute]",
    ("ExportAllDeclaration", "source"): "StringLiteral",
    ("ExportDefaultDeclaration", "declaration"): "OptFunctionDeclaration|OptClassDeclaration|Expression",
    ("ExportNamedDeclaration", "attributes"): "[ImportAttribute]",
    ("ExportNamedDeclaration", "declaration"): "Declaration|null",
    ("ExportNamedDeclaration", "source"): "StringLiteral|null",
    ("ExportNamedDeclaration", "specifiers"): "[ExportSpecifier|ExportNamespaceSpecifier]",
    ("ExportNamespaceSpecifier", "exported"): "Identifier",
    ("ExportSpecifier", "exported"): "Identifier|StringLiteral",
    ("ExportSpecifier", "local"): "Identifier|StringLiteral",
    ("ExpressionStatement", "expression"): "Expression",
    ("ForInStatement", "body"): "Statement",
    ("ForInStatement", "left"): "VariableDeclaration|Expression",
    ("ForInStatement", "right"): "Expression",
    ("ForStatement", "body"): "Statement",
    ("ForStatement", "init"): "VariableDeclaration|Expression|null",
    ("ForStatement", "test"): "Expression|null",
    ("ForStatement", "update"): "Expression|null",
    ("Function", "body"): "BlockStatement",
    ("Function", "id"): "Identifier|null",
    ("Function", "params"): "[Pattern]",
    ("FunctionDeclaration", "id"): "Identifier",
    ("IfStatement", "alternate"): "Statement|null",
    ("IfStatement", "consequent"): "Statement",
    ("IfStatement", "test"): "Expression",
    ("ImportAttribute", "key"): "Identifier",
    ("ImportAttribute", "value"): "StringLiteral",
    ("ImportDeclaration", "attribtues"): "[ImportAttribute]",
    ("ImportDeclaration", "source"): "StringLiteral",
    ("ImportDeclaration", "specifiers"): "[ImportSpecifier|ImportDefaultSpecifier|ImportNamespaceSpecifier]",
    ("ImportSpecifier", "imported"): "Identifier|StringLiteral",
    ("LabeledStatement", "body"): "Statement",
    ("LabeledStatement", "label"): "Identifier",
    ("LogicalExpression", "left"): "Expression",
    ("LogicalExpression", "operator"): "LogicalOperator",
    ("LogicalExpression", "right"): "Expression",
    ("MemberExpression", "object"): "Expression|Super",
    ("MemberExpression", "property"): "Expression|PrivateName",
    ("MetaProperty", "meta"): "Identifier",
    ("MetaProperty", "property"): "Identifier",
    ("ModuleExpression", "body"): "Program",
    ("ModuleSpecifier", "local"): "Identifier",
    ("Node", "loc"): "SourceLocation|null",
    ("ObjectExpression", "properties"): "[ObjectProperty|ObjectMethod|SpreadElement]",
    ("ObjectMember", "decorators"): "[Decorator]",
    ("ObjectMember", "key"): "Expression",
    ("ObjectPattern", "properties"): "[AssignmentProperty|RestElement]",
    ("ObjectProperty", "value"): "Expression",
    ("OptClassDeclaration", "id"): "Identifier|null",
    ("OptFunctionDeclaration", "id"): "Identifier|null",
    ("OptionalCallExpression", "arguments"): "[Expression|SpreadElement]",
    ("OptionalCallExpression", "callee"): "Expression",
    ("OptionalMemberExpression", "object"): "Expression",
    ("OptionalMemberExpression", "property"): "Expression|PrivateName",
    ("ParenthesizedExpression", "expression"): "Expression",
    ("PrivateName", "id"): "Identifier",
    ("Program", "body"): "[Statement|ImportDeclaration|ExportDeclaration]",
    ("Program", "directives"): "[Directive]",
    ("Program", "interpreter"): "InterpreterDirective|null",
    ("RestElement", "argument"): "Pattern",
    ("ReturnStatement", "argument"): "Expression|null",
    ("SequenceExpression", "expressions"): "[Expression]",
    ("SourceLocation", "end"): "Position",
    ("SourceLocation", "start"): "Position",
    ("SpreadElement", "argument"): "Expression",
    ("StaticBlock", "body"): "[Statement]",
    ("SwitchCase", "consequent"): "[Statement]",
    ("SwitchCase", "test"): "Expression|null",
    ("SwitchStatement", "cases"): "[SwitchCase]",
    ("SwitchStatement", "discriminant"): "Expression",
    ("TaggedTemplateExpression", "quasi"): "TemplateLiteral",
    ("TaggedTemplateExpression", "tag"): "Expression",
    ("TemplateLiteral", "expressions"): "[Expression]",
    ("TemplateLiteral", "quasis"): "[TemplateElement]",
    ("ThrowStatement", "argument"): "Expression",
    ("TryStatement", "block"): "BlockStatement",
    ("TryStatement", "finalizer"): "BlockStatement|null",
    ("TryStatement", "handler"): "CatchClause|null",
    ("UnaryExpression", "argument"): "Expression",
    ("UnaryExpression", "operator"): "UnaryOperator",
    ("UpdateExpression", "argument"): "Expression",
    ("UpdateExpression", "operator"): "UpdateOperator",
    ("VariableDeclaration", "declarations"): "[VariableDeclarator]",
    ("VariableDeclarator", "id"): "Pattern",
    ("VariableDeclarator", "init"): "Expression|null",
    ("WhileStatement", "body"): "Statement",
    ("WhileStatement", "test"): "Expression",
    ("WithStatement", "body"): "Statement",
    ("WithStatement", "object"): "Expression",
    ("YieldExpression", "argument"): "Expression|null",
}
supers = {
    "SourceLocation": None,
    "Position":       None,

    "Node":           None,
    "PrivateName":           ["Node"],
    "Program":               ["Node"],
    "Function":              ["Node"],
    "CatchClause":           ["Node"],
    "SwitchCase":            ["Node"],
    "VariableDeclarator":    ["Node"],
    "Decorator":             ["Node"],
    "Directive":             ["Node"],
    "Super":                 ["Node"],
    "Import":                ["Node"],
    "ObjectMember":          ["Node"],
    "SpreadElement":         ["Node"],
    "ArgumentPlaceholder":   ["Node"],
    "Class":                 ["Node"],
    "ClassBody":             ["Node"],
    "ClassProperty":         ["Node"],
    "ClassPrivateProperty":  ["Node"],
    "ClassAccessorProperty": ["Node"],
    "StaticBlock":           ["Node"],
    "ImportDeclaration":     ["Node"],
    "ImportAttribute":       ["Node"],
    "TemplateElement":       ["Node"],

    "Expression": ["Node"],
    "ThisExpression":           ["Expression"],
    "YieldExpression":          ["Expression"],
    "AwaitExpression":          ["Expression"],
    "ArrayExpression":          ["Expression"],
    "ObjectExpression":         ["Expression"],
    "UnaryExpression":          ["Expression"],
    "UpdateExpression":         ["Expression"],
    "BinaryExpression":         ["Expression"],
    "AssignmentExpression":     ["Expression"],
    "LogicalExpression":        ["Expression"],
    "OptionalMemberExpression": ["Expression"],
    "BindExpression":           ["Expression"],
    "ConditionalExpression":    ["Expression"],
    "CallExpression":           ["Expression"],   "NewExpression": ["CallExpression"],
    "OptionalCallExpression":   ["Expression"],
    "SequenceExpression":       ["Expression"],
    "ParenthesizedExpression":  ["Expression"],
    "DoExpression":             ["Expression"],
    "ModuleExpression":         ["Expression"],
    "TopicReference":           ["Expression"],
    "TemplateLiteral":          ["Expression"],
    "TaggedTemplateExpression": ["Expression"],
    "MetaProperty":             ["Expression"],

    "ModuleSpecifier": ["Node"],
    "ImportSpecifier":          ["ModuleSpecifier"],
    "ImportDefaultSpecifier":   ["ModuleSpecifier"],
    "ImportNamespaceSpecifier": ["ModuleSpecifier"],
    "ExportSpecifier":          ["ModuleSpecifier"],
    "ExportNamespaceSpecifier": ["ModuleSpecifier"],

    "Statement": ["Node"],
    "ExpressionStatement": ["Statement"],
    "BlockStatement":      ["Statement"],
    "EmptyStatement":      ["Statement"],
    "DebuggerStatement":   ["Statement"],
    "WithStatement":       ["Statement"],
    "ReturnStatement":     ["Statement"],
    "LabeledStatement":    ["Statement"],
    "BreakStatement":      ["Statement"],
    "ContinueStatement":   ["Statement"],
    "IfStatement":         ["Statement"],
    "SwitchStatement":     ["Statement"],
    "ThrowStatement":      ["Statement"],
    "TryStatement":        ["Statement"],
    "WhileStatement":      ["Statement"],
    "DoWhileStatement":    ["Statement"],
    "ForStatement":        ["Statement"],
    "ForInStatement":      ["Statement"],   "ForOfStatement": ["ForInStatement"],
    "Declaration":         ["Statement"],

    "Pattern": ["Node"],
    "ObjectPattern":     ["Pattern"],
    "ArrayPattern":      ["Pattern"],
    "RestElement":       ["Pattern"],
    "AssignmentPattern": ["Pattern"],

    "Literal": ["Expression"],
    "RegExpLiteral":  ["Literal"],
    "NullLiteral":    ["Literal"],
    "BooleanLiteral": ["Literal"],
    "NumericLiteral": ["Literal"],
    "BigIntLiteral":  ["Literal"],
    "DecimalLiteral": ["Literal"],
    "StringLiteral":  ["Literal"],

    "DirectiveLiteral":     ["StringLiteral"],
    "InterpreterDirective": ["StringLiteral"],

    "ObjectProperty":           ["ObjectMember"],
    "AssignmentProperty":       ["ObjectProperty"],
    "ClassMethod":              ["Function"],
    "ClassPrivateMethod":       ["Function"],
    
    "ExportDeclaration": ["Node"], 
    "ExportDefaultDeclaration": ["ExportDeclaration"],
    "ExportAllDeclaration":     ["ExportDeclaration"],
    "ExportNamedDeclaration":   ["ExportDeclaration"],

    "VariableDeclaration":             ["Declaration"],
    "FunctionDeclaration": ["Function", "Declaration"],   "OptFunctionDeclaration": ["FunctionDeclaration"],
    "ClassDeclaration":    ["Class",    "Declaration"],   "OptClassDeclaration":    ["ClassDeclaration"],

    "Identifier":              ["Expression",   "Pattern"],
    "MemberExpression":        ["Expression",   "Pattern"],
    "ArrowFunctionExpression": ["Function",     "Expression"],
    "FunctionExpression":      ["Function",     "Expression"],
    "ClassExpression":         ["Class",        "Expression"],
    "ObjectMethod":            ["ObjectMember", "Function"],
}

def get_mro():
    items = deque()
    links = defaultdict(list)
    for child, value in supers.items():
        if value is None: items.append(child)
        else:
            for parent in value: links[parent].append(child)

    mro = {parent: [] for parent in items}
    mro_seq = list(mro.items())
    while items:
        parent = items.popleft()
        for child in links[parent]:
            mro[child] = [parent, *mro[parent]]
            mro_seq.append((child, mro[child]))
            items.append(child)
    return mro, mro_seq

def extend_aliases():
    links = defaultdict(dict)
    for (item, key), alias in aliases.items():
        links[item][key] = alias
    for item, parents in mro_seq:
        # print(item)
        for parent in parents:
            try: key_alias = links[parent]
            except KeyError: continue
            # print("   ", parent, key_alias)
            for key, alias in key_alias.items():
                aliases[(item, key)] = alias
                links[item][key] = alias

mro, mro_seq = get_mro()
extend_aliases()



types = defaultdict(Counter)

def get_type(source, key, value):
    try: return aliases[(source, key)]
    except KeyError:
        try: return value["type"]
        except (KeyError, TypeError): return type(value).__name__

def recurs(item):
    try: T = item["type"]
    except KeyError: return
    item.pop("start")
    item.pop("end")
    item.pop("loc")
    if "extra" in item: del item["extra"] # например: 4096 -> 0x1000 или "meow" -> 'meow'
    if "leadingComments" in item:
        #print("~" * 77)
        #print(babel_generate(item))
        #print("~" * 77)
        del item["leadingComments"]
    if "trailingComments" in item:
        del item["trailingComments"]

    keys = tuple(key + f": {get_type(T, key, item[key])}" for key in sorted(item))
    types[T][keys] += 1
    for value in item.values():
        T = type(value)
        if T is dict: recurs(value)
        elif T is list:
            for item in value:
                if type(item) is dict: recurs(item)

if __name__ == "__main__":
    code = """
    function test(a, b) {
        return a + b;
    }
    """
    ast = babel_parse_with_cache("input.js")
    with open("ast.json", "w", encoding="utf-8") as file:
        json.dump(ast, file, indent=2, ensure_ascii=False, sort_keys=True)
    #pprint(ast)
    recurs(ast)

    for name in os.listdir("biginputs"):
        if name.endswith(".js"):
            path = os.path.join("biginputs", name)
            recurs(babel_parse_with_cache(path))

    for T in sorted(types):
        for args, count in types[T].items():
            print(f"{T}({args})   {count} шт.")

    print("\n=== Generating ===")
    new_code = babel_generate(ast)
    print(new_code)
