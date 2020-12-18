from setuptools import setup, find_packages
from dirac import (__version__, __author__, __email__,
                   __directory__, __github__, __license__)

description_path = __directory__ / 'resources/misc/description.txt'
with open(description_path, 'r') as file:
    description = file.read()

setup(
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['numpy>=1.19.0', 'qdarkstyle>=2.8.1', 'pyqt5>=5.15.2',
                      'h5py>=3.1.0', 'pyqtgraph>=0.11.0', 'PyOpenGL>=3.1.5'],
    python_requires='>=3.9.0',
    name='Dirac Equation',
    version=__version__,
    description=description,
    url=__github__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    keywords=['computational physics', 'dirac equation', 'pml',
              'perfectly matched layers', 'staggered grid', '(2+1)D'],
)
