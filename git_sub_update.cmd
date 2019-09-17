echo git bash commands to update submodules to latest
rem Automated login
git config --global credential.helper wincred

git submodule update --remote --merge --recursive gearshift                                                 
git submodule update --remote --merge --recursive rF2headlights                               
git push
