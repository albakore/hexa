import { defineConfig, defaultPlugins } from '@hey-api/openapi-ts';

export default defineConfig({
	input:
		'http://localhost:8000/system/openapi_schema',
	output: {
		format: 'prettier',
		lint: 'eslint',
		path: './backend/client',
	},
	plugins: [
		...defaultPlugins,
		{
			name: '@hey-api/client-next',
			// runtimeConfigPath: './hey-api.ts',
			// baseUrl: 'http://localhost:8000'
		},
		{
			name: '@hey-api/sdk',
			validator: 'zod',
			asClass: true
		},
	],
});
