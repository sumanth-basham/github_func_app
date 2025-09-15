
# github_func_app

## Deployment Best Practices

1. **Environment Separation**: Use separate Azure Function Apps and secrets for Dev, QA, and Prod. Never share credentials or resources between environments.
2. **Branch Strategy**: Use dedicated branches for each environment (e.g., `dev`, `qa`, `main`).
3. **Secrets Management**: Store Azure publish profiles and app names as GitHub secrets for each environment.
4. **Automated CI/CD**: Use GitHub Actions workflows to automate deployment on branch push.
5. **Testing**: Always test in Dev and QA before deploying to Prod.
6. **Rollback**: Keep previous deployment packages for quick rollback if needed.

## Deployment Steps

1. Commit and push code to the appropriate branch (`dev`, `qa`, or `main`).
2. GitHub Actions workflow for that environment runs automatically.
3. Workflow installs dependencies, zips the app, and deploys to the correct Azure Function App using secrets.
4. Monitor workflow and Azure portal for deployment status.

## GitHub Actions Workflow YAML Explanation

Each environment has its own workflow file:
- `.github/workflows/azure-functions-dev.yml` (Dev)
- `.github/workflows/azure-functions-qa.yml` (QA)
- `.github/workflows/azure-functions-prod.yml` (Prod)

### Key YAML Statements

```
on:
	push:
		branches:
			- dev  # or qa, main
```
*Triggers workflow on push to the specified branch.*

```
jobs:
	build-and-deploy:
		runs-on: ubuntu-latest
		steps:
			- uses: actions/checkout@v4
```
*Defines the job and checks out the code.*

```
			- name: Set up Python
				uses: actions/setup-python@v5
				with:
					python-version: '3.11'
```
*Sets up the Python environment.*

```
			- name: Install dependencies
				run: |
					python -m pip install --upgrade pip
					pip install -r requirements.txt
```
*Installs required Python packages.*

```
			- name: Archive function app
				run: zip -r functionapp.zip .
```
*Creates a zip archive of the app for deployment.*

```
			- name: Deploy to Azure Functions (Env)
				uses: Azure/functions-action@v1
				with:
					app-name: ${{ secrets.AZURE_FUNCTIONAPP_NAME_ENV }}
					package: functionapp.zip
					publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE_ENV }}
```
*Deploys the app to the Azure Function App using environment-specific secrets.*

Replace `ENV` with `DEV`, `QA`, or `PROD` as appropriate for each workflow.
