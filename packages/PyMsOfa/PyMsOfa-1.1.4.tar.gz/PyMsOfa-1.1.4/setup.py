from setuptools import Extension,setup,find_packages
import glob

long_desc ='''
This package is a Python package for the Standards of Fundamental Astronomy (SOFA) service of the International Astronomical Union (IAU). It implements the python package PyMsOfa for SOFA service in three ways: 

(1) *PyMsOfa.ctypes* : a python wrapper package based on a foreign function library for Python , 

(2) *PyMsOfa.cffi* : a python wrapper package with the foreign function interface for Python calling C code ,

(3) *PyMsOfa.python* : a python package directly written in pure python codes from SOFA subroutines. 

*Attention* : In Microsoft Windows, the *PyMsOfa.ctypes* module and the *PyMsOfa.cffi* module can't be used after installing them in pypi, but they can be installed and used by `github <https://github.com/CHES2023/PyMsOfa>`_.  

It implements all 247 functions in the SOFA service and is based on the latest version released on Oct 11, 2023.

This Python package can be suitable for the astrometric detection of habitable planets of the Closeby Habitable Exoplanet Survey (`CHES <https://doi.org/10.1088/1674-4527/ac77e4>`_ ) mission and for the frontier themes of black holes and dark matter related to astrometric calculations and other fields.

*PyMsOfa* is a `Python <http://www.python.org/>`_ module for accessing `International Astronomical Union <http://www.iau.org/>`_'s `SOFA library <http://www.iausofa.org/>`_ from Python. SOFA (Standards of Fundamental Astronomy) is a set of algorithms and procedures that implement standard models used in fundamental astronomy.

*PyMsOfa* is not a part of SOFA routines but a Python package for the SOFA C library. Thus, no calculations are made into the PyMsOfa package based on ctypes and cffi interface, which are all delegated to the underlying SOFA C library.

*PyMsOfa* is neither distributed, supported nor endorsed by the International Astronomical Union. In addition to *PyMsOfa*’s license, any use of this module should comply with `SOFA’s license and terms of use <http://www.iausofa.org/tandc.html>`_. Especially, but not exclusively, any published work or commercial products including results achieved by using *PyMsOfa* shall acknowledge that the SOFA software was used to obtain those results.

To cite *PyMsOfa* in publications use:

> 1.    Ji, Jiang-Hui, Tan, Dong-jie, Bao, Chun-hui, Huang, Xiu-min, Hu, Shoucun, Dong, Yao, Wang, Su. 2023, PyMsOfa: A Python Package for the Standards of Fundamental Astronomy (SOFA) Service, Research in Astronomy and Astrophysics, https://doi.org/10.1088/1674-4527/ad0499

> 2.	Ji, Jiang-Hui, Li, Hai-Tao, Zhang, Jun-Bo, Fang, Liang, Li, Dong, Wang, Su, Cao, Yang, Deng, Lei, Li, Bao-Quan, Xian, Hao, Gao, Xiao-Dong, Zhang, Ang, Li, Fei, Liu, Jia-Cheng, Qi, Zhao-Xiang,  Jin, Sheng, Liu, Ya-Ning, Chen, Guo, Li, Ming-Tao, Dong, Yao, Zhu, Zi, and CHES Consortium. 2022, CHES: A Space-borne Astrometric Mission for the Detection of Habitable Planets of the Nearby Solar-type Stars, Research in Astronomy and Astrophysics, 22, 072003, https://doi.org/10.1088/1674-4527/ac77e4

'''

sofa_lib = Extension("PyMsOfa.libsofa_c",
                       glob.glob('./C/*.c'),
                       depends=["./C/sofa.h", "./C/sofam.h"],
                       include_dirs=["./C"])
        
setup(
    name='PyMsOfa',
    version='1.1.4',
    author='Ji, jianghui',
    author_email="jijh@pmo.ac.cn",
    maintainer='Tan, dongjie',
    maintainer_email='djtan@pmo.ac.cn',
    description='a Python package for the Standards of Fundamental Astronomy (SOFA) service',
    long_description=long_desc,
    ext_modules = [sofa_lib],
    packages = find_packages(),
    license='MIT',   
    install_requires=[],
    include_package_data = True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.0",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Astronomy"
    ]
)
