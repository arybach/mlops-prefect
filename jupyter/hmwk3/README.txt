# Before running - from hmwk3 copy * to main jupyter/ folder

## Dockerfile settings
the following envs should be defined:
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
AWS_REGION
PREFECT_API_URL
PREFECT_API_KEY
using 
export ARG AWS_ACCESS_KEY_ID="..."
export ARG AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="..."
export PREFECT_API_URL="..."
export PREFECT_API_KEY="..."

check:
echo $PREFECT_API_URL
echo $PREFECT_API_KEY

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
git remote add origin git https://github.com/arybach/mlops-prefect.git
git push -u origin master

## docker-compose up - if prefect_mlops locks up db -> restart docker-compose (ctrl+C -> docker-compose up)
check docker logs mlops -> click on the jupyter link
check docker logs prefect_mlops -> 0.0.0.0:4200 to see prefect cli


## SETUP Prefect deployment

* add git repository just for .py files in jupyter as project repo contains dockerfiles and docker-compose.yml:
mine is - https://github.com/arybach/code.git

* check in jupyter that it's set:
> git version -v
init prefect project:
> prefect project init

* copy prefect.yaml to prefect_git.yaml (unfortunately there's mo option to set which prefect.yaml to use for a specific deploymnet, 
so going back and forth renaming the two)
* in the prefect_git.yaml file
* add prefect.projects.steps.git_clone_project settings to pull:

pull:
- prefect.projects.steps.set_working_directory:
    directory: /home/work
- prefect.projects.steps.git_clone_project:
        repository: https://github.com/...
        branch: main
        access_token: null (or add access token if needed)

* add workpool mlops-prefect-pool via localhost:4200 ui (using Local subprocess option) if not done previously
modify deployment.yaml (docs https://docs.prefect.io/2.10.13/tutorial/projects/)

modify deployment.yaml:

deployments:
- name: taxi_local
  entrypoint: ./orchestrate.py:main_flow_local
  workpool: 
      name: mlops-prefect-pool
  schedule: {}
- name: taxi_s3
  entrypoint: ./orchestrate_s3.py:main_flow_s3
  workpool: 
      name: mlops-prefect-pool
  schedule: {}
- name: taxi_params
  entrypoint: ./orchestrate_params.py:main_flow_params
  args:
    - --train_path
    - "./data/green_tripdata_2023-01.parquet"
    - --val_path
    - "./data/green_tripdata_2023-02.parquet"
  workpool: 
      name: mlops-prefect-pool
  schedule: {}

  when fetching from repo into existing ./code dir use access token (although with no git repo initialized git clone should work without the token)

  ## RUN the jupyter prefect.ipynb file cell by cell carefully reading instructions...