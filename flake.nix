# simple flake to help using pysubfixer
{
  inputs = {
    # don't rebuild if you don't have to
    nixpkgs = {
      type = "indirect";
      id = "nixpkgs";
    };
    # pycall tool
    pycall = {
      url = github:MadMcCrow/pycall;
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs =
    { nixpkgs, pycall, ... }@inputs:
    let
      systems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];
      flake = system :
        let 
          pkgs = nixpkgs.legacyPackages.${system};
          args = {
            python = pycall.packages.${system}.python311;
            };
        in {
        legacyPackages.${system}    = pkgs.callPackage ./nix/pysubfixer.nix args;
        devShells.${system}.default = pkgs.callPackage ./nix/shell.nix      args;
        apps.${system} = pkgs.callPackages ./nix/apps.nix args;
      }; 
    in
    builtins.foldl' (x: y:  nixpkgs.lib.recursiveUpdate x y) { } (map flake systems);
    
}
