# simple flake to help using pysubfixer
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
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
      in {
      legacyPackages.${system} = rec {
        pysubfixer = pkgs.callPackage ./pysubfixer.nix { };
        default = pysubfixer;
      };
      devShells.${system}.default = pkgs.callPackage ./shell.nix { };
    }; 
    in
    fold' flake {} systems;
    
}
