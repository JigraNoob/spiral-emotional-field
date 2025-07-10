module.exports = {
    
    transform: {
        '^.+\\.js$': 'babel-jest',
        '^.+\\.jsx?$': 'babel-jest'
    },
    testEnvironment: 'jsdom',
    setupFilesAfterEnv: ['<rootDir>/tests/setupTests.js'],
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/static/js/$1',
        '^@components/(.*)$': '<rootDir>/static/js/components/$1',
        '^@utils/(.*)$': '<rootDir>/static/js/utils/$1',
        '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
    },
    testPathIgnorePatterns: ['/node_modules/', '/dist/'],
    coveragePathIgnorePatterns: ['/node_modules/', '/dist/'],
    coverageDirectory: 'coverage',
    collectCoverageFrom: [
        'static/js/**/*.{js,jsx}',
        '!static/js/**/*.test.{js,jsx}',
        '!static/js/**/*.spec.{js,jsx}',
        '!static/js/setupTests.js'
    ],
    moduleDirectories: ['node_modules', 'static/js']
};
