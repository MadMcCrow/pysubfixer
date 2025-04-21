# build with nuitka
{ pythonVersion, ... } :
let 
nuitka = pythonVersion.pkgs.nuitka;
in
{
  pythonVersion.pkgs.nuitka
}