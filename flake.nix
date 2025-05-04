{
  description = "Dev shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";  # or "aarch64-darwin" for macOS
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        buildInputs = [
          pkgs.python312
          pkgs.uv
          pkgs.stdenv.cc.cc.lib
          pkgs.zlib
          pkgs.bashInteractive
        ];
      };
    };
}
