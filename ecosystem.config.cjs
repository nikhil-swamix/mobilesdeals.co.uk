export default {
	apps: [
		{
			name: 'mobilesdeals.co.uk',
			script: 'bun run preview',
			env_production: {
				NODE_ENV: 'production'
			},
			env_development: {
				NODE_ENV: 'development'
			}
		}
	]
};
