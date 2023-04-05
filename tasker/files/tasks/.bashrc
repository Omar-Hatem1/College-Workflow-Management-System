# Git
alias init='git init'
alias status='git status'
alias push='git push -u origin'
alias commit='git add . && git commit -m'
alias remote='git remote add origin'
alias branch='git branch'
alias move='git checkout'
alias ls-files='git ls-files'
alias ls-clear='git rm --cached -r'
alias clone='git clone'
# commits history
alias ls-commits='git log --oneline'
alias gitignore='touch .gitignore'
#remove last commit
alias rm-commit='git reset --soft HEAD~1'
#remove last commit and changes
alias rm-commit-changes='git reset --hard HEAD~1'
# rename last commit
alias recommit='git commit --amend -m'
# remove .git folder
alias rm-git='rm -rf .git'

# Django
alias run='python manage.py runserver'
alias migrate='python manage.py migrate'
alias migration='python manage.py makemigrations'
alias project='django-admin startproject'
alias app='django-admin startapp'
alias createsuperuser='python manage.py createsuperuser'
alias i='pipenv install'
