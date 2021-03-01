# Dirac
A small program to numerically simulate a plane wave solution to the (2+1)D Dirac equation on a doubly staggered (in space and time) grid with optional absorbive boundary layers (imaginary potential method).

## Contact
- Author: Dominik Brandstetter, BSc.
- Affiliation: (Karl-Franzens) University Graz, Austria
- E-Mail: dominik.brandstetter@edu.uni-graz.at
- GitHub: https://github.com/brands-d/Dirac

## Installation
Clone the GitHub repository and install the program:

    git clone https://github.com/brands-d/Dirac.git
    cd Dirac
    python setup.py install

This should install install all Python dependencies from the PyPI index automatically. Using a fresh virtual environment is recommend.
To export images or movies of the solution, "FFmpeg" (https://ffmpeg.org/) is required and has to be added to the PATH.

## Usage
Start the program by executing it as a package

    python -m dirac

This will open a "Settings" window that will serve as main window. Closing it will shut down the program as well.

Adjust various settings (see tooltips for more information on individual settings) and hit "Run". The statusbar will display the progress on the simulation as well as the processing afterwards.
When it is done, a new "Player" window will open. You can open as many individual, independent player windows as you like. Closing them will not shut down the program but if not saved via the "Export" section or using the "Save" option in the setting window, all results are gone.

