module.exports = {
    "env": {
        "browser": true,
        "es6": true
    },
    "extends": [
        "eslint:recommended",
        "plugin:react/recommended"
    ],
    "globals": {
        "Atomics": "readonly",
        "SharedArrayBuffer": "readonly"
    },
    "parserOptions": {
        "ecmaFeatures": {
            "jsx": true
        },
        "ecmaVersion": 2018,
        "sourceType": "module"
    },
    "plugins": [
        "react"
    ],
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
            "ignoreComments": false,
            "ignoredNodes": ["JSXElement *", "JSXElement"]
        }],
        "semi": ["error", "always"],
        "quotes": ["error", "double"],
        "jsx-quotes": ["error", "prefer-double"],
        "react/jsx-indent": ["error", 4, {checkAttributes: true, indentLogicalExpressions: true}],
        "react/jsx-indent-props": ["error", "first"]
    },
    "settings": {
        "react": {
            "createClass": "createReactClass",
            "pragma": "React",
            "version": "detect"
        }
    }
};