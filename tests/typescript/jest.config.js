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
  coverageReporters: ['text', 'lcov', 'html'],
  // Coverage is collected from generated folder via CLI --collectCoverageFrom
};
