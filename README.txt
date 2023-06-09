SET UP Git

# Replace <TOKEN> with your access token
export ACCESS_TOKEN=<TOKEN>

# Set the Git remote URL with the access token
git config --global url."https://<ACCESS_TOKEN>@github.com/".insteadOf "https://github.com/"

# Create a new repository
git init my-repo
cd my-repo

# Perform initial Git setup
git config user.name "Your Name"
git config user.email "your-email@example.com"

# Create an initial commit
echo "# My Repository" >> README.md
git add README.txt
git commit -m "Initial commit"

# Create the repository on the Git service
git remote add origin https://github.com/<USERNAME>/my-repo.git
git push -u origin master