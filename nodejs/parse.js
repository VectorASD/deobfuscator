const fs = require("fs");
const parser = require("@babel/parser");

let code = "";
process.stdin.on("data", chunk => code += chunk);
process.stdin.on("end", () => {
  try {
    const ast = parser.parse(code, {
      sourceType: "unambiguous",
      allowReturnOutsideFunction: true,
      allowAwaitOutsideFunction: true,
      plugins: [
        "jsx",
        "classProperties",
        "classPrivateProperties",
        "classPrivateMethods",
        "dynamicImport",
        "optionalChaining",
        "nullishCoalescingOperator",
        "numericSeparator",
        "objectRestSpread",
        "topLevelAwait"
      ]
    });
    process.stdout.write(JSON.stringify(ast, null, 2));
  } catch (err) {
    process.stderr.write("Parse error:\n" + err.toString());
    process.exit(1);
  }
});
