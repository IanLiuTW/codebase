# NOTE:
# 1. Change the version of the default programming language (i.e. Python) in `devcontainer.json`.
# 2. Enable the project setttings at `Project Setup` section.

# [Docker]
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg -y
sudo install -m 0755 -d /etc/apt/keyrings -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
# Install cli tool and link the socket
sudo apt-get install docker-ce-cli -y
ln -s "/var/run/docker-host.sock" "/var/run/docker.sock"

##### Project Setup - Python #####
# sudo apt-get install unixodbc-dev -y
# pip install --upgrade pip
# pip install -r ./requirements.txt
# pip install pytest

git clone https://github.com/IanLiuTW/config && chmod +x ./config/_scripts/dev_env/setup_apt.sh && ./config/_scripts/dev_env/setup_apt.sh
