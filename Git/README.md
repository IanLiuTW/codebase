# git

## Sync folder with existing repo

```shell
git init .
git remote add origin url_of_the_repo
git fetch origin
git branch -f master origin/main
git reset .
```
