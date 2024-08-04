##### Intro #####
# The script installs docker and enable the docker.sock to be shared with the host
# It also install all the necessary tools for my development environment
# Run `zsh` after ssh into the container (TODO: auto set zsh as default shell)
# Run `checkhealth` in nvim to see what is missing (possibly some formatters)

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

# [asdf]
apt install -y curl git
cd ~ && git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.0

# [zsh]
apt install -y zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# [fzf]
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# [nerdfetch]
sudo curl -fsSL https://raw.githubusercontent.com/ThatOneCalculator/NerdFetch/main/nerdfetch -o /usr/bin/nerdfetch
sudo chmod +x /usr/bin/nerdfetch

# [nvim]
apt install -y ninja-build gettext cmake unzip curl build-essential
cd ~ && git clone https://github.com/neovim/neovim && cd neovim
make CMAKE_BUILD_TYPE=RelWithDebInfo
sudo make install

# [Update config]
apt install -y stow
cd ~ && git clone https://github.com/IanLiuTW/config.git && cd config
rm -rf ~/.zshrc ~/.gitconfig
stow zsh nvim git

# [nvim requirements]
export ASDF_DIR="$HOME/.asdf"
. "$HOME/.asdf/asdf.sh" && asdf plugin add lua && asdf install lua 5.1 && asdf global lua 5.1
asdf plugin add nodejs
asdf install nodejs latest
asdf global nodejs latest

apt install -y ripgrep fd-find

# [Project]
# sudo apt-get install unixodbc-dev -y
# pip install --upgrade pip
# pip install -r ./services/tupl-de-nifi-functions/requirements.txt
# pip install -r ./services/tupl-de-nifi-functions/app/requirements.txt
# pip install pytest # vs code somehow needs it to discover tests (even unittests)
