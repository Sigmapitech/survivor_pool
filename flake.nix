{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    applySystems = nixpkgs.lib.genAttrs ["x86_64-linux"];
    eachSystem = f: applySystems (system: f nixpkgs.legacyPackages.${system});
  in {
    devShells = eachSystem (pkgs: {
      default = pkgs.mkShell {
        packages = let
          front-deps = with pkgs; [
            eslint
            nodejs
            typescript
          ];
        in front-deps;
      };
    });
  };
}

