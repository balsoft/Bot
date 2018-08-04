with import <nixpkgs> {};

( let
	dawg-python = python35.pkgs.buildPythonPackage rec {
				pname = "DAWG-Python";
				      version = "0.7.2";
				      src = python35.pkgs.fetchPypi {
				        inherit pname version;
				        sha256 = "089lbrcqz025scl1ri9hza803cbsd98xbkq5y81cl716ws334pja";
				      };
				
				      doCheck = false;
			};
	docopt = python35.pkgs.buildPythonPackage rec {
			pname = "docopt";
			      version = "0.6.1";
			      src = python35.pkgs.fetchPypi {
			        inherit pname version;
			        sha256 = "0dda54xiyl17079jhsll8v2cwbkvsmm4gsckc2z27g1zfw599bbi";
			      };
			
			      doCheck = false;
		};
	pymorphy2-dicts = python35.pkgs.buildPythonPackage rec {
		pname = "pymorphy2-dicts";
		      version = "2.4.393442.3710985";
		      src = python35.pkgs.fetchPypi {
		        inherit pname version;
		        sha256 = "0jlyqxx808qvaq5gldd0cri0ziskgydgh1rgjhf9r4ghnl168z5y";
		      };
		
		      doCheck = false;
	};
    pymorphy2 = python35.pkgs.buildPythonPackage rec {
      pname = "pymorphy2";
      version = "0.8";
	  buildInputs = [pymorphy2-dicts docopt dawg-python];
      src = python35.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "13yvmjddwjygc5kfs9wqya6zzjvmz4v140alzaia6y3gbqgw54ih";
      };

      doCheck = false;
    };

  in python35.withPackages (ps: [pymorphy2 pymorphy2-dicts dawg-python])
).env