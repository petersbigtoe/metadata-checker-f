with import <nixpkgs> {};

mkShell {
  buildInputs = [
    exiftool
    python311
  ];
};
