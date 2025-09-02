{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    git-hooks,
  }: let
    applySystems = nixpkgs.lib.genAttrs ["x86_64-linux"];
    eachSystem = f: applySystems (system: f nixpkgs.legacyPackages.${system});
  in {
    checks = eachSystem (pkgs: let
      activate = pkgs.lib.foldr (x: prev: prev // {${x}.enable = true;}) {};
      hooks =
        {
          commit-name = {
            enable = true;
            name = "commit name";
            stages = ["commit-msg"];
            entry = ''
              ${pkgs.python310.interpreter} ${./check_commit_msg.py}
            '';
          };
        }
        // activate [
          "black"
          "isort"
          "trim-trailing-whitespace"
          "alejandra"
          "deadnix"
        ];
    in {
      pre-commit-check = git-hooks.lib.${pkgs.system}.run {
        inherit hooks;
        src = ./.;
      };
    });

    formatter = eachSystem (pkgs: pkgs.alejandra);

    devShells = eachSystem (pkgs: {
      default = let
        py-env = pkgs.python3.withPackages (p:
          with p; [
            aiohttp
            aiocache
            fastapi
            isort
            markdownify
            pydantic
            pymysql
            pydantic-settings
            python-dotenv
            ruff
            sqlmodel
            uvicorn
            fastapi
            fastapi-cli
          ]);
      in
        pkgs.mkShell {
          inherit (self.checks.${pkgs.system}.pre-commit-check) shellHook;

          packages = let
            front-deps = with pkgs; [
              eslint
              nodejs
              typescript
            ];
            back-deps = with pkgs; [
              py-env
              black
              isort
            ];
          in
            [py-env] ++ front-deps ++ back-deps;
        };
    });
  };
}
