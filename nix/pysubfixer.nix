# ./default.nix
# script to generate bash script
{  python311Packages, ... }:
# build with python 311
with python311Packages;
buildPythonApplication {
  pname = "pysubfixer";
  version = "1.0";
  pyproject = true;
  buildInputs = [ poetry-core ];
  src = ./.;
}
