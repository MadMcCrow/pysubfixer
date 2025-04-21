# apps.nix :
# allows running apps in flake
# TODO: simplify and regroup !
{ pythonVersion, callPackage, ... } : 
let 
pysubfixer = callPackage ./pysubfixer.nix {inherit pythonVersion; } ;
in
{
pysubfixer-gui = {
    type = "app";
    program = "${pysubfixer}/bin/pysubfixer-gui";
  };
pysubfixer-cli = {
    type = "app";
    program = "${pysubfixer}/bin/pysubfixer-cli";
  };
}