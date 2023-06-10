## SET UP Git

### Replace <TOKEN> with your access token
export ACCESS_TOKEN=<TOKEN>

### Set the Git remote URL with the access token
git config --global url."https://<ACCESS_TOKEN>@github.com/".insteadOf "https://github.com/"

### Create a new repository
git init my-repo
cd my-repo

### Perform initial Git setup
git config user.name "Your Name"
git config user.email "your-email@example.com"

### Create an initial commit
echo "# My Repository" >> README.md
git add README.txt
git commit -m "Initial commit"

### Create the repository on the Git service
git remote add origin git https://github.com/arybach/mlops-prefect-flows.git
git push -u origin master


## SETUP Prefect deployment

* add git repository just for .py files in jupyter as project repo contains dockerfiles and docker-compose.yml:
* check in jupyter that it's set:
> git version -v
init prefect project:
> prefect project init

* in the prefect.yaml file
* add prefect.projects.steps.git_clone_project settings to pull:

pull:
- prefect.projects.steps.set_working_directory:
    directory: /home/work
- prefect.projects.steps.git_clone_project:
        repository: https://github.com/
        branch: main
        access_token: null

* add workpool mlops-prefect-pool via localhost:4200 ui (using Local subprocess option)
* then in terminal:
> prefect deploy orchestrate.py:main_flow -n taxi -p mlops-prefect-pool

create a new version of orchestrate_s3.py with data being downloaded from s3 bucket
> prefect deploy orchestrate_s3.py:main_flow_s3 -n taxi_s3 -p mlops-prefect-pool

modify deployment.yaml (docs https://docs.prefect.io/2.10.13/tutorial/projects/)

deployments:
- name: taxi_local
  entrypoint: ./orchestrate.py:main_flow
  workpool: 
      name: mlops-prefect-pool
  schedule: {}
- name: s3_taxi
  entrypoint: ./orchestrate_s3.py:main_flow_s3
  workpool: 
      name: mlops-prefect-pool
  schedule: {}