{
  pkgs ? import <nixpkgs> { },
  lib,
  ...
}:
let 
nixtools = [ nixfmt-rfc-style deadnix ];
python = pkgs.python311;
in 
pkgs.mkShell.override { stdenv = pkgs.stdenvNoCC; } {
  packages = with pkgs; [
    
    # ffmpeg
    ffmpeg
    # python
    python
  ] ++ (with python.packages; [
    pyQt6
    pyinstaller
  ]);
}
