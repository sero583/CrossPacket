/** @type {import('jest').Config} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.test.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: 'tsconfig.json'
    }]
  },
  verbose: true,
  testTimeout: 30000,
  coverageDirectory: './coverage',
  coverageReporters: ['text', 'lcov', 'html'],  // Collect coverage from the generated TypeScript files we're testing
  collectCoverageFrom: [
    '../../generated/typescript/**/*.ts',
    '!../../generated/typescript/node_modules/**',
  ],};
