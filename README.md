# Fuse Tools CI Dashboard

This application shows a dashboard to visualize the status of all relevant build jobs.


## Quick-start

Define an environment variable to hold your github oauth token called _GITHUB_TRAVIS_TOKEN_

```bash
export TRAVIS_TOKEN="<enter your token here>"
```

Make sure your [GitHub Token](https://github.com/settings/tokens) has the following scopes...
```bash
"read:org", "user:email", "repo_deployment", "repo:status", "write:repo_hook"
```

Now continue to setup, build and launch the project...


```bash
npm install yarn -g # ensure you have yarn on your machine globally
git clone https://github.com/lhein/build-dashboard.git # clone the project
cd build-dashboard # navigate into the project directory
pip install -r requirements.txt # install the python required libraries
yarn # install patternfly-react-seed dependencies
yarn build # build the project
python CIBackendService.py # start the rest api for retrieving the job data
yarn start # start the development server
```

## Development Scripts

Install development/build dependencies
`yarn`

Start the development server
`yarn start`

Run a production build
`yarn build`

Run the test suite
`yarn test`

Run the linter
`yarn lint`

Run the code formatter
`yarn format`

Launch a tool to inspect the bundle size
`yarn bundle-profile:analyze`

## Configurations
* [TypeScript Config](./tsconfig.json)
* [Webpack Config](./webpack.common.js)
* [Jest Config](./jest.config.js)
* [Editor Config](./.editorconfig)

## Code Quality Tools
* For accessibility compliance, we use [react-axe](https://github.com/dequelabs/react-axe)
* To keep our bundle size in check, we use [webpack-bundle-analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)
* To keep our code formatting in check, we use [prettier](https://github.com/prettier/prettier)
* To keep our code logic and test coverage in check, we use [jest](https://github.com/facebook/jest)
