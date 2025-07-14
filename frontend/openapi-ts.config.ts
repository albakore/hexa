import { defineConfig, defaultPlugins } from '@hey-api/openapi-ts';

export default defineConfig({
	input:
		'http://localhost:8000/openapi.json',
	output: {
		format: 'prettier',
		lint: 'eslint',
		path: './backend/client',
	},
	plugins: [
		...defaultPlugins,
		{
			name: '@hey-api/sdk',
			validator: 'zod',
			asClass: true
		},
	],
});
