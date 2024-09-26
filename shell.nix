with import <nixpkgs> {};

( let
    filemanagement = pkgs.python3.pkgs.buildPythonPackage rec {
      name = "filemanagement";
      #pname = "filemanagement";
      version = "0.0.1";

      src = fetchFromGitHub { 
        owner = "yurimimi";
        repo = "${name}";
        rev = "cba327fe0e4d87beb30c2bb200f0470bb1082cad";
      };
      #src = pkgs.fetchgit{
      #  url = "git@github.com:yurimimi/filemanagement.git";
      #  rev = "cba327fe0e4d87beb30c2bb200f0470bb1082cad";
      #  #sha256 = "43c2c9e5e7a16b6c88ba3088a9bfc82f7db8e13378be7c78d6c14a5f8ed05afd";
      #};
      #src = ./dist;

      pyproject = true;
      #propagatedBuildInputs = [ pytest numpy pkgs.libsndfile ];

      dependencies = [
        survey
        # some others
      ];

      #meta = {
      #  homepage = "http://github.com/yurimimi/yui";
      #  description = "Your utility integrator";
      #  license = licenses.mit;
      #  maintainers = with maintainers; [ yurimimi ];
      #};

      #preConfigure = ''
      #  export LDFLAGS="-L${pkgs.fftw}/lib -L${pkgs.fftwFloat}/lib -L${pkgs.fftwLongDouble}/lib"
      #  export CFLAGS="-I${pkgs.fftw}/include -I${pkgs.fftwFloat}/include -I${pkgs.fftwLongDouble}/include"
      #'';
    };

  in pkgs.python3.buildEnv.override rec {
    #extraLibs = with pkgs.python3.pkgs; [
    extraLibs = with pkgs.python3.pkgs; [
      pkgs.python3.pkgs.numpy
      filemanagement
    ];
    #ignoreCollisions = true;
  }
).env
# What is this .env?
# You can also use the env attribute to create local environments with needed
# packages installed. This is somewhat comparable to virtualenv. For example,
# running nix-shell with the above shell.nix will drop you into a shell
# where Python will have the specified packages in its path.

# python.buildEnv arguments
#  extraLibs: List of packages installed inside the environment.
#  postBuild: Shell command executed after the build of environment.
#  ignoreCollisions: Ignore file collisions inside the environment (default is
#    false).
#  permitUserSite: Skip setting the PYTHONNOUSERSITE environment variable in
#    wrapped binaries in the environment.
