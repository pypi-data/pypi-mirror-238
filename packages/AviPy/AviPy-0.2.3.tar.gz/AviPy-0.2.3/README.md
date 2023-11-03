# AviPy

## Overview
AviPy is a Python package specifically developed for the purposes of the Flight Operations Engineering (FOE) course at the HvA. For the purposes of the FOE assignments, many pieces of code can be shared between projects. That is what motivated the creation of a Python package, that can be used as a common repository for code snippets useful for the projects.

## Table of Contents
- [Features](#features)
- [Where to get it](#where-to-get-it)
- [Installation](#installation)
- [Documentation](#documentation)
- [License](#license)

## Features
The AviPy package includes many classes and functions useful for FOE projects. These are the main features of AviPy:
- The qty module contains classes for every SI-Unit used in aviation-related calculations. One can declare a variable with a distance unit like this: `height = qty.Distance.Ft(5000)`, what the Distance class does under the hood, is that the value in ft is converted to a value in meters. When the user wants to retrieve the value in any unit, on can do this `height.ft`, which will return the value in feet.
- The geo module contains the Coord class, which is a wrapper for a pair of latitude and longitude values. The class comes with many useful functions related to coordinates.
- The constants module contains commonly used constants in the field of aviation.
- The atmosphere module contains many useful functions related to earth's atmosphere.

## Where to get it
To obtain the code, so you can use it for yourself, clone the repository to your system:
```bash
git clone https://github.com/pcs03/AviPy.git
```

## Installation
To install the package to your system, so you can import the module in your own project, AviPy can be installed using pip:
```bash
pip install path/to/avipy
```
This command will install the package to your local system. If you have a virtual environment activated while executing the command, the package will be installed to your virtual environment.

## Documentation
[Docs](https://github.com/pcs03/AviPy/tree/main/docs)

## License
[GNU General Public License V3.0](https://github.com/pcs03/AviPy/blob/main/LICENSE)
