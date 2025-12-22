const fs = require("fs");
const generator = require("@babel/generator").default;

let json = "";
process.stdin.on("data", chunk => json += chunk);
process.stdin.on("end", () => {
  try {
    const ast = JSON.parse(json);
    const output = generator(ast, { compact: false, comments: true });
    process.stdout.write(output.code);
  } catch (err) {
    process.stderr.write("Generate error:\n" + err.toString());
    process.exit(1);
  }
});
