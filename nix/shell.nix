# shell for developmnent
{
  mkShell,
  lib,
  python,
  ...
}:
mkShell {
  packages = [  
    ffmpeg
    python
  ] ++
  (with python.pkgs; [
    pycall
    pyside6
    nuitka
    ccache
    poetry-core
  ]) ++
  [ 
    nixfmt-rfc-style
    deadnix
  ];
}
