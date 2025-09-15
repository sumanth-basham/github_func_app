
# github_func_app

## Deployment Best Practices

1. **Environment Separation**: Use separate Azure Function Apps and secrets for Dev, QA, and Prod. Never share credentials or resources between environments.
2. **Branch Strategy**: Use dedicated branches for each environment (e.g., `dev`, `qa`, `main`).
3. **Secrets Management**: Store Azure publish profiles and app names as GitHub secrets for each environment.
4. **Automated CI/CD**: Use GitHub Actions workflows to automate deployment on branch push.
5. **Testing**: Always test in Dev and QA before deploying to Prod.
6. **Rollback**: Keep previous deployment packages for quick rollback if needed.

## Deployment Steps

### Step-by-Step Deployment Instructions

1. **Prepare Azure Function Apps**
	- Create three separate Azure Function Apps in your Azure portal: one each for Dev, QA, and Prod.
	- Download the publish profile for each Function App.

2. **Set GitHub Secrets**
	- In your GitHub repository, go to Settings > Secrets and variables > Actions.
	- Add the following secrets for each environment:
	  - `AZURE_FUNCTIONAPP_NAME_DEV`, `AZURE_FUNCTIONAPP_PUBLISH_PROFILE_DEV`
	  - `AZURE_FUNCTIONAPP_NAME_QA`, `AZURE_FUNCTIONAPP_PUBLISH_PROFILE_QA`
	  - `AZURE_FUNCTIONAPP_NAME_PROD`, `AZURE_FUNCTIONAPP_PUBLISH_PROFILE_PROD`
	- The `*_NAME` is the name of your Azure Function App. The `*_PUBLISH_PROFILE` is the content of the publish profile XML file (paste as a secret).

3. **Branching**
	- Use the `dev` branch for development deployments, `qa` for QA, and `main` for production.
	- Make sure your code changes are committed to the correct branch for the intended environment.

4. **Push Code**
	- Commit and push your changes to the appropriate branch (`dev`, `qa`, or `main`).

5. **Automatic Workflow Execution**
	- The corresponding GitHub Actions workflow (`azure-functions-dev.yml`, `azure-functions-qa.yml`, or `azure-functions-prod.yml`) will run automatically.
	- The workflow will:
	  - Set up Python
	  - Install dependencies
	  - Zip the function app
	  - Deploy to the correct Azure Function App using the secrets

6. **Monitor Deployment**
	- Check the Actions tab in GitHub for workflow status and logs.
	- Verify deployment in the Azure portal by checking the Function App for updates.

7. **Testing and Promotion**
	- Test your app in the Dev environment first.
	- Once validated, merge changes to the `qa` branch for QA deployment.
	- After QA approval, merge to `main` for production deployment.

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
