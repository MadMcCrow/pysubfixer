{
  pkgs ? import <nixpkgs> { },
  lib,
  ...
}:
with pkgs;
let 
nixtools = [ nixfmt-rfc-style deadnix ];
python = pkgs.python311;
in 
mkShell {
  packages = [  
    # ffmpeg
    ffmpeg
    # python
    python
  ] ++ (with python.pkgs; [
    pyside6
    nuitka
    ccache
    poetry-core
  ]);
}
