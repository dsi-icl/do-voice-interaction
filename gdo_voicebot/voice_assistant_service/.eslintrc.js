module.exports = {
    "env": {
        "es6": true,
        "node": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "Atomics": "readonly",
        "SharedArrayBuffer": "readonly"
    },
    "parser": "babel-eslint",
    "parserOptions": {
        "ecmaVersion": 2018,
        "sourceType": "module"
    },
    "rules": {
        "indent": ["error", 4, {
            "SwitchCase": 1,
            "VariableDeclarator": 1,
            "outerIIFEBody": 1,
            "MemberExpression": 1,
            "FunctionDeclaration": {"parameters": "first", "body": 1},
            "FunctionExpression": {"parameters": "first", "body": 1},
            "CallExpression": {"arguments": "first"},
            "ArrayExpression": "first",
            "ObjectExpression": "first",
            "ImportDeclaration": "first",
            "flatTernaryExpressions": false,
            "ignoreComments": false
        }],
        "semi": ["error", "always"],
        "quotes": ["error", "double"]
    },
};