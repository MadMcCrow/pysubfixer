# ./pysubfixer.nix
# script to generate bash script
{ python, callPackage, ... } :
# build with python 311
with python.pkgs;
buildPythonApplication {
  pname = "pysubfixer";
  version = "1.0";
  pyproject = true;
  buildInputs = [ poetry-core pyside6 ];
  propagatedBuildInputs = [pyside6];
  src = ./..;
}