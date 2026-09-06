import { defineConfig } from "orval";

export default defineConfig({
  default: {
    input: {
      target: "http://localhost:8010/schema/openapi.json",
    },
    output: {
      mode: "tags",
      target: "./src/lib/api/gen",
      schemas: "./src/lib/api/gen/model",
      client: "fetch",
      override: {
        mutator: {
          path: "./src/lib/api/custom-fetch.ts",
          name: "customFetch",
        },
      },
      clean: true,
    },
  },
});
