{
  description = "A Nix flake for Python 3 and uv with auto-managed virtualenv and dependency sync";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.uv
          ];

          shellHook = ''
            set -e

            # --- Virtual environment setup ---
            if [ ! -d .venv ]; then
              echo "⚙️  Creating virtual environment for Python ${python.version}..."
              uv venv --python ${python.interpreter}
            fi
            source .venv/bin/activate

            # Ensure uv always uses this Python
            export UV_PYTHON=${python.interpreter}

            # --- Initialize project if needed ---
            if [ ! -f pyproject.toml ] && [ ! -f main.py ]; then
              echo "📦 Initializing new uv project..."
              uv init --package .
            fi

            # --- Dependency management ---
            if [ -f pyproject.toml ]; then
              if [ ! -f uv.lock ] || [ pyproject.toml -nt uv.lock ]; then
                echo "🔒 Updating dependency lockfile..."
                uv lock
              fi

              echo "🔄 Syncing dependencies..."
              uv sync
            fi

            echo "✅ Environment ready with Python $(python -V)"
          '';
        };

        apps.default = {
          type = "app";
          program = "${pkgs.writeShellScript "run" ''
            exec ${pkgs.uv}/bin/uv run main.py "$@"
          ''}";
        };
      });
}
