##### Intro #####
# The script installs docker and enable the docker.sock to be shared with the host
# It also install all the necessary tools for the python development environment
# NOTE:
# 1. Change the version of the default programming language (i.e. Python) in `devcontainer.json`.
# 2. Enable the project setttings at `Project Setup` section.
# 3. Run `checkhealth` in nvim to see what is missing (possibly some formatters).
# TODO:
# - Make Clipboard work for neovim
# - Migrate to Nix

##### Devcontainer Setup #####
# [Nix]
# curl -L https://nixos.org/nix/install | sh -s -- --daemon --yes
# if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
#   . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
# fi

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

# [asdf and some languages]
cd ~ && git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.0
export ASDF_DIR="$HOME/.asdf" && . "$HOME/.asdf/asdf.sh" 
asdf plugin add lua && asdf install lua 5.1 && asdf global lua 5.1
asdf plugin add nodejs && asdf install nodejs latest && asdf global nodejs latest

##### Project Setup - Python #####
# sudo apt-get install unixodbc-dev -y
# pip install --upgrade pip
# pip install -r ./requirements.txt
# pip install pytest

##### Development Environment Setup #####
# [zsh]
apt install -y zsh
sudo chsh -s /usr/bin/zsh $USER
# [eza]
wget -c https://github.com/eza-community/eza/releases/latest/download/eza_aarch64-unknown-linux-gnu.tar.gz -O - | tar xz
sudo chmod +x eza && sudo chown root:root eza && sudo mv eza /usr/local/bin/eza
# [zoxide]
curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
# [fzf]
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --all

# [nvim]
apt install -y ninja-build gettext cmake unzip curl build-essential
cd ~ && git clone https://github.com/neovim/neovim && cd neovim
make CMAKE_BUILD_TYPE=RelWithDebInfo
sudo make install
apt install -y ripgrep fd-find

# [nerdfetch]
sudo curl -fsSL https://raw.githubusercontent.com/ThatOneCalculator/NerdFetch/main/nerdfetch -o /usr/bin/nerdfetch
sudo chmod +x /usr/bin/nerdfetch

# [stow configs]
apt install -y stow
cd ~ && git clone https://github.com/IanLiuTW/config.git && cd config
rm -rf ~/.zshrc ~/.gitconfig
stow zsh nvim git starship
