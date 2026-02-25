import eslint from "@eslint/js";
import typescriptEslint from "typescript-eslint";

export default typescriptEslint.config(
    eslint.configs.recommended,
    ...typescriptEslint.configs.recommended,
    ...typescriptEslint.configs.strict,
    {
        rules: {
            quotes: ["error", "double"],
            semi: ["error", "always"]
        }
    }
);