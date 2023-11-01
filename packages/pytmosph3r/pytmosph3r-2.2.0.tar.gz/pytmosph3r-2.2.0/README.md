# pytmosph3r

Pytmosph3R is a Python-3 library that computes transmission spectra based on 3D atmospheric simulations, for example performed with the LMDZ generic global climate model.

## Prerequisites

* numpy

## Installing from PyPI

Pytmosph3r is available on the PyPI repository. You can install the latest version avaible with:
```
pip install pytmosph3r
```
Don't forget to install numpy beforehand.

## Installing from source

If you intend to develop or get the latest (unreleased) developments, you can clone (and move in) the current repository and then install Pytmosph3R using:
```
pip install -e .
```

Don't forget to update `pip` if errors are raised.

To generate the documentation, you will need to install the following packages:
```
pip install nbsphinx sphinx-autoapi sphinx_rtd_theme sphinxcontrib-bibtex sphinx-argparse
conda install sphinx pandoc # installs more (required) dependencies than pip
```
You can then generate the documentation by running:
```
python setup.py doc
```
(or by simply running `make` in the `doc/` folder). The documentation will be generated in the doc/html folder (you can open the [index.html](doc/html/index.html) file to check it out using your favorite browser).

Note that you need to set the environment variable `FASTCHEM_DIR` to the location of the folder containing [FastChem](https://github.com/exoclime/FastChem) if you want to use that functionality (WIP).

## Running

To get help:
```
pytmosph3r -h
```

See the [documentation](http://perso.astrophy.u-bordeaux.fr/~jleconte/pytmosph3r-doc/index.html) for more information (read instructions in `Installation` just above to generate the doc).