{
  pkgs ? import <nixpkgs> { },
  lib,
  ...
}:
let 
python = pkgs.python311;
in 
pkgs.mkShell.override { stdenv = pkgs.stdenvNoCC; } {
  packages = with pkgs; [
    #nix
    nixfmt-rfc-style
    deadnix
    # ffmpeg
    ffmpeg
    # python
    python
  ] ++ (with python.packages; [
    pyQt6
    pyinstaller
  ]);
}
