# apps.nix :
# allows running apps in flake
# TODO: simplify and regroup !
{ python, callPackage, ... } : 
let 
pysubfixer = callPackage ./pysubfixer.nix {inherit python; } ;
in
rec {
pysubfixer-gui = {
    type = "app";
    program = "${pysubfixer}/bin/pysubfixer-gui";
  };
pysubfixer-cli = {
    type = "app";
    program = "${pysubfixer}/bin/pysubfixer-cli";
  };
  default = pysubfixer-gui;
}