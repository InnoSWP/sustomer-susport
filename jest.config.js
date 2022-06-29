/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */
module.exports = {
	// fix weird imports in jest
  transform: {
    "\\.[jt]sx?$": "ts-jest",
  },
  globals: {
    "ts-jest": {
      useESM: true,
    },
  },
  moduleNameMapper: {
    "(.+)\\.js": "$1",
  },
  extensionsToTreatAsEsm: [".ts"],
	// end of fix

	// my config
  preset: "ts-jest",
  testEnvironment: "node",
  globals: {
    "ts-jest": {
      tsconfig: true,
    },
  },
};
