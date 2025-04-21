# simple flake to help using pysubfixer
{
  inputs = {
    # don't rebuild if you don't have to
    nixpkgs = {
      type = "indirect";
      id = "nixpkgs";
    };
  };
  outputs =
    { nixpkgs, ... }@inputs:
    let
      systems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];
      flake = system :
      let 
        pkgs = nixpkgs.legacyPackages.${system};
        args = {pythonVersion = pkgs.python311;};
      in {
      legacyPackages.${system}    = pkgs.callPackage ./nix/pysubfixer.nix args;
      devShells.${system}.default = pkgs.callPackage ./nix/shell.nix      args;
      apps.${system} = pkgs.callPackages ./nix/apps.nix args;
    }; 
    in
    builtins.foldl' (x: y:  x  // y) { } (map flake systems);
    
}
