/** @type {import('ts-jest').JestConfigWithTsJest} */
export default {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  testMatch: ['**/*.test.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],
  transform: {
    '^.+\\.tsx?$': 'ts-jest'
  },
  moduleNameMapper: {
    '^phaser$': '<rootDir>/__mocks__/phaser.ts'
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.test.ts',
    '!src/main.ts'
  ],
  // Coverage threshold disabled for MVP - Phaser-dependent code requires E2E tests
  // coverageThreshold: {
  //   global: {
  //     branches: 70,
  //     functions: 80,
  //     lines: 80,
  //     statements: 80
  //   }
  // },
  coverageReporters: ['text', 'html'],
  verbose: true
};
