module.exports = {
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
	],
	deploy: {
		prod: {
			user: 'ubuntu',
			host: ['13.43.25.172'],
			ref: 'origin/main',
			repo: 'https://github.com/nikhil-swamix/mobilesdeals.co.uk.git',
			path: '/home/ubuntu/test.mobilesdeals.co.uk',
			key: 'c:\\Users\\User\\.ssh\\mobilesdeals.co.uk.pem',
			// 'post-deploy': 'pnpm install'
		}
	}
};
