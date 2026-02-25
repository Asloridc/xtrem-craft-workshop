import type { Config } from "jest";

const config: Config = {
  roots: ["<rootDir>/tests"],
  collectCoverageFrom: ["<rootDir>/src/**/*.ts"],
  coverageDirectory: "coverage",
  coverageProvider: "v8",
  testEnvironment: "node",
  transform: {
    ".+\\.ts$": "ts-jest"
  },
  moduleNameMapper: {
    "@xtrem-craft/(.*)": "<rootDir>/src/$1",
  },
  workerThreads: true,
  randomize: true,
  verbose: true,
  setupFilesAfterEnv: ["jest-extended/all", "jest-chain"]
};

export default config;