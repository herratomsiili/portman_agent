// jest.config.js
export default {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    // setupFilesAfterEnv: ['@testing-library/jest-dom/extend-expect'],
    setupFilesAfterEnv: ['<rootDir>/setupTests.ts']
}
