{ pkgs ? import <nixpkgs> {} }:
let
  pythonWithPkgs = pkgs.python3.withPackages (p: with p; [
    pillow
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonWithPkgs
  ];

  shellHook = ''
    PYTHONPATH=${pythonWithPkgs}/${pythonWithPkgs.sitePackages}
  '';
}
