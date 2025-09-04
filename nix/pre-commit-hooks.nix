{pkgs}: let
  activate = pkgs.lib.foldr (x: prev: prev // {${x}.enable = true;}) {};
in
  {
    commit-name = {
      enable = true;
      name = "commit name";
      stages = ["commit-msg"];
      entry = ''
        ${pkgs.python310.interpreter} ${../check_commit_msg.py}
      '';
    };
  }
  // activate [
    "biome"
    "black"
    "trim-trailing-whitespace"
    "alejandra"
    "deadnix"
  ]
