#!/bin/bash

echo Enter user.name:
read name
echo Enter user.email:
read email

git config --global user.name  ${name}
git config --global user.email  ${email}

# util settings
git config --global help.autocorrect 30
git config --global core.autocrlf false
git config --global core.quotepath false

# colors
git config --global color.diff auto
git config --global color.status auto
git config --global color.branch auto

# git command alias
git config --global alias.aa   "add ."
git config --global alias.c    commit
git config --global alias.cm   "commit --amend -C HEAD"
git config --global alias.co   checkout
git config --global alias.cb   "checkout -b"
git config --global alias.sw   switch
git config --global alias.cl   clone
git config --global alias.s    status
git config --global alias.ss   "status -sb"
git config --global alias.b    branch
git config --global alias.bu   "branch -u"
git config --global alias.bm   "branch -m"
git config --global alias.bv   "branch -vv"
git config --global alias.mg   merge
git config --global alias.re   remote
git config --global alias.rev  "remote -v"
git config --global alias.rea  "remote add"
git config --global alias.res  "remote set-url"
git config --global alias.rer  "remote rename"
git config --global alias.reem "remote remove"
git config --global alias.rs   "reset"
git config --global alias.rsh  "reset HEAD"
git config --global alias.rshs "reset HEAD --soft"
git config --global alias.rshh "reset HEAD --hard"
git config --global alias.sta  stash
git config --global alias.stap "stash pop"
git config --global alias.staa "stash apply"
git config --global alias.stad "stash drop"
git config --global alias.rv   revert
git config --global alias.f    fetch
git config --global alias.pu   push
git config --global alias.puu  "push -u"
git config --global alias.pl   pull
git config --global alias.di   diff
git config --global alias.type "cat-file -t"
git config --global alias.dump "cat-file -p"
git config --global alias.rl   reflog
git config --global alias.l    log
git config --global alias.ls   "log --stat"
git config --global alias.lo   "log --oneline"
git config --global alias.lc   "log --pretty=oneline"
git config --global alias.lss  "log --show-signature"
git config --global alias.ll   "log --pretty=format:'%h [%Cgreen%an%Creset] %ad - %ar : %s%d' --graph --date=short"
git config --global alias.lg   "log --graph --pretty=format:'%Cred%h%Creset %ad |%C(yellow)%d%Creset %s %Cgreen(%cr)%Creset [%Cgreen%an%Creset]' --abbrev-commit --date=short"
git config --global alias.alias "config --get-regexp ^alias\."

# For Windows
git config --global alias.ig  "!gi() { curl -sL https://www.gitignore.io/api/$@ ;}; gi"
git config --global alias.iga "!gi() { curl -sL https://www.gitignore.io/api/$@ ;}; gi >> .gitignore"
git config --global alias.iac "!giac() { git init && git add . && git commit -m 'init' ;}; giac"
git config --global core.editor notepad

# For Linux/macOS
git config --global alias.ig  '!'"gi() { curl -sL https://www.gitignore.io/api/\$@ ;}; gi"
git config --global alias.iga '!'"gi() { curl -sL https://www.gitignore.io/api/\$@ ;}; gi >> .gitignore"
git config --global alias.iac '!'"giac() { git init && git add . && git commit -m 'init' ;}; giac"