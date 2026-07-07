import * as Babel from "@babel/standalone";

const BOOTSTRAP_PREFIXES = [
  "col-", "row", "container", "text-", "d-", "justify-",
  "align-", "mt-", "mb-", "ms-", "me-", "pt-", "pb-", "p-", "m-",
  "img-fluid",
];

const CSS_NAMED_COLORS = new Set([
  "red", "blue", "green", "black", "white", "gray", "grey",
  "yellow", "orange", "purple", "pink", "brown", "cyan",
  "magenta", "lime", "navy", "teal", "maroon", "olive",
  "silver", "gold", "transparent", "currentcolor",
]);

function parseSource(code) {
  return Babel.packages.parser.parse(code, {
    sourceType: "module",
    plugins: ["jsx"],
  });
}

function sliceNode(code, node) {
  return code.slice(node.start, node.end);
}

function isHookCall(node) {
  if (node.type !== "VariableDeclaration") return false;
  const decl = node.declarations[0];
  if (!decl || !decl.init) return false;
  const init = decl.init;
  return (
    init.type === "CallExpression" &&
    init.callee.type === "Identifier" &&
    init.callee.name.startsWith("use")
  );
}

function collectPatternNames(pattern, names) {
  if (!pattern) return;
  if (pattern.type === "Identifier") {
    names.push(pattern.name);
  } else if (pattern.type === "ArrayPattern") {
    pattern.elements.forEach((el) => collectPatternNames(el, names));
  } else if (pattern.type === "ObjectPattern") {
    pattern.properties.forEach((p) => collectPatternNames(p.value, names));
  }
}

function getDeclaredNames(node) {
  const names = [];
  node.declarations.forEach((decl) => collectPatternNames(decl.id, names));
  return names;
}

/**
 * Parses a section's raw jsx_code and pulls out its structural
 * parts. Handles two shapes:
 *  - Inline sections: plain JSX markup, no wrapping function.
 *  - Full components: a whole file with imports, a function
 *    declaration, hooks, and a return statement.
 */
function extractComponentParts(jsxCode) {
  const ast = parseSource(jsxCode);
  const body = ast.program.body;

  const imports = [];
  let functionNode = null;

  for (const node of body) {
    if (node.type === "ImportDeclaration") {
      imports.push(sliceNode(jsxCode, node));
    } else if (node.type === "FunctionDeclaration") {
      functionNode = node;
    } else if (
      node.type === "ExportDefaultDeclaration" &&
      node.declaration.type === "FunctionDeclaration"
    ) {
      functionNode = node.declaration;
    } else if (
      node.type === "ExportNamedDeclaration" &&
      node.declaration &&
      node.declaration.type === "FunctionDeclaration"
    ) {
      functionNode = node.declaration;
    }
  }

  if (!functionNode) {
    // No function wrapper — this is an inline section, already
    // plain JSX. Parse it as an expression instead so the same
    // downstream wrapping logic works for both cases.
    return {
      imports: [],
      hoisted: [],
      returnExpr: jsxCode.trim(),
      isJsxDirect: true,
    };
  }

  const hoisted = [];
  let returnExpr = null;
  let isJsxDirect = false;

  for (const stmt of functionNode.body.body) {
    if (stmt.type === "ReturnStatement") {
      const arg = stmt.argument;
      isJsxDirect = arg.type === "JSXElement" || arg.type === "JSXFragment";
      returnExpr = sliceNode(jsxCode, arg);
    } else if (isHookCall(stmt)) {
      hoisted.push({
        text: sliceNode(jsxCode, stmt),
        names: getDeclaredNames(stmt),
      });
    } else {
      // Helper functions / plain consts. Hoisted as-is — NOT
      // collision-protected against same-named helpers in a
      // different section. That would need real scope analysis,
      // out of scope for this pass; a naming collision here
      // surfaces as a visible JS "duplicate declaration" error
      // at compile time, not a silent bug.
      hoisted.push({ text: sliceNode(jsxCode, stmt), names: [] });
    }
  }

  return { imports, hoisted, returnExpr, isJsxDirect };
}

function applySuffix(text, names, suffix) {
  let result = text;
  for (const name of names) {
    const pattern = new RegExp(`\\b${name}\\b`, "g");
    result = result.replace(pattern, `${name}${suffix}`);
  }
  return result;
}

/**
 * Prefixes every CSS selector with an ancestor scope class
 * (".demo3 .Mission" instead of renaming the class itself),
 * matching a JSX wrapper of <div className="demo3">.
 * @keyframes blocks are protected — their internal selectors
 * (0%, 50%, from, to) are animation steps, not class selectors.
 */
export function scopeCssWithPrefix(cssCode, prefix) {
  const keyframeBlocks = [];

  const protectedCss = cssCode.replace(
    /@keyframes\s+[\w-]+\s*\{(?:[^{}]|\{[^{}]*\})*\}/g,
    (match) => {
      keyframeBlocks.push(match);
      return `__KEYFRAME_BLOCK_${keyframeBlocks.length - 1}__`;
    }
  );

  let scoped = protectedCss.replace(/([^{}\n]+)\{/g, (full, selector) => {
    if (selector.trim().startsWith("@media")) {
      return full;
    }
    const parts = selector
      .split(",")
      .map((part) => `.${prefix} ${part.trim()}`);
    return parts.join(", ") + " {";
  });

  keyframeBlocks.forEach((block, i) => {
    scoped = scoped.replace(`__KEYFRAME_BLOCK_${i}__`, block);
  });

  return scoped;
}

export function extractAllClasses(jsxCode) {
  const pattern = /className\s*=\s*["']([^"']+)["']/g;
  const classes = new Set();
  let match;

  while ((match = pattern.exec(jsxCode))) {
    match[1].split(/\s+/).forEach((c) => classes.add(c));
  }

  return [...classes]
    .filter((c) => !BOOTSTRAP_PREFIXES.some((p) => c.startsWith(p)))
    .sort();
}

export function extractAllColors(cssCode) {
  const colors = new Set();

  (cssCode.match(/#[0-9a-fA-F]{3,8}\b/g) || []).forEach((c) => colors.add(c));
  (cssCode.match(/rgba?\([^)]+\)/g) || []).forEach((c) => colors.add(c));
  (cssCode.match(/[a-zA-Z]+/g) || []).forEach((word) => {
    if (CSS_NAMED_COLORS.has(word.toLowerCase())) {
      colors.add(word.toLowerCase());
    }
  });

  return [...colors].sort();
}

export function sanitizeComponentName(name) {
  const parts = name.split(/[^a-zA-Z0-9]+/).filter(Boolean);
  let pascal = parts.map((p) => p[0].toUpperCase() + p.slice(1)).join("");

  if (!pascal || !/[a-zA-Z]/.test(pascal[0])) {
    pascal = "Section" + pascal;
  }

  return pascal;
}

/**
 * Scopes one section: parses it, wraps its returned JSX in
 * <div className="school">, and scopes its CSS to match. Works
 * identically for inline sections and full components — after
 * this step, both are just "a scoped JSX block plus hoisted
 * hook declarations."
 */
export function scopeSection(section) {
  const prefix = section.school.toLowerCase();
  const parts = extractComponentParts(section.jsx_code);

  const wrappedReturn = `<div className="${prefix}">\n${parts.returnExpr}\n</div>`;
  const scopedCss = scopeCssWithPrefix(section.css_code, prefix);

  return {
    ...section,
    imports: parts.imports,
    hoisted: parts.hoisted,
    wrappedReturn,
    css_code: scopedCss,
  };
}

/** Builds one standalone component file for "separate" mode. */
export function buildSeparateComponent(scopedSection, componentName) {
  const importsBlock = scopedSection.imports.join("\n");
  const hoistedBlock = scopedSection.hoisted
    .map((h) => "  " + h.text.replace(/\n/g, "\n  "))
    .join("\n");

  return (
    `${importsBlock}${importsBlock ? "\n" : ""}` +
    `import "./${componentName}.css";\n\n` +
    `function ${componentName}() {\n` +
    (hoistedBlock ? hoistedBlock + "\n\n" : "") +
    `  return (\n` +
    `    ${scopedSection.wrappedReturn}\n` +
    `  );\n` +
    `}\n\n` +
    `export default ${componentName};\n`
  );
}

/** Merges multiple already-scoped sections into one coherent file. */
export function buildCombinedFile(scopedSections) {
  const allImports = new Set();
  const hoistedBlocks = [];
  const returnBlocks = [];

  scopedSections.forEach((section, index) => {
    section.imports.forEach((imp) => allImports.add(imp));

    const suffix = `_${index}`;
    const hookNames = section.hoisted.flatMap((h) => h.names);

    const renamedHoisted = section.hoisted.map((h) =>
      h.names.length > 0 ? applySuffix(h.text, hookNames, suffix) : h.text
    );

    if (renamedHoisted.length > 0) {
      hoistedBlocks.push(
        `  // --- ${section.school} / ${section.section_name} ---\n` +
          renamedHoisted.map((t) => "  " + t.replace(/\n/g, "\n  ")).join("\n")
      );
    }

    const finalReturn =
      hookNames.length > 0
        ? applySuffix(section.wrappedReturn, hookNames, suffix)
        : section.wrappedReturn;

    returnBlocks.push(
      `      {/* ${section.school} / ${section.section_name} */}\n      ${finalReturn}`
    );
  });

  const importBlock = Array.from(allImports).join("\n");
  const cssCode = scopedSections.map((s) => s.css_code).join("\n\n");

  const jsxCode =
    `${importBlock}${importBlock ? "\n\n" : ""}` +
    `function CombinedPage() {\n` +
    (hoistedBlocks.length ? hoistedBlocks.join("\n\n") + "\n\n" : "") +
    `  return (\n` +
    `    <>\n` +
    returnBlocks.join("\n\n") +
    `\n    </>\n` +
    `  );\n` +
    `}\n\n` +
    `export default CombinedPage;\n`;

  return { jsxCode, cssCode };
}

/** Builds Home.jsx importing every separate component. */
export function buildHomeFile(componentNames) {
  const imports = componentNames
    .map((name) => `import ${name} from "./${name}";`)
    .join("\n");
  const tags = componentNames.map((name) => `      <${name} />`).join("\n");

  return (
    `${imports}\n\n` +
    `function Home() {\n` +
    `  return (\n` +
    `    <>\n` +
    tags +
    `\n    </>\n` +
    `  );\n` +
    `}\n\n` +
    `export default Home;\n`
  );
}