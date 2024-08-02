# git

## Sync folder with existing repo

```shell
git init .
git remote add origin url_of_the_repo
git fetch origin
git branch -f master origin/main
git reset .
```

## Generate ssh for GitHub

- To generate new key

```shell
ssh-keygen -t ed25519 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

Go to GitHub to add the ssh key.

- To add the github in the known_hosts if authentication error happened

```shell
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
```

- To change the existing git repo to use ssh instead of HTTPS

```shell
cd path/to/repo
nvim .git/config
```

Change the remote url to this format `git@github.com:user_name/repo_name.git`
