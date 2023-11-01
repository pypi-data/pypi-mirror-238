# distutils: language = c++

# -*- mode: python -*-
#!python
#cython: language_level=3
#cython: boundscheck=False
#cython: wraparound=False
# Comments above are special. Please do not remove.
cimport numpy as np  # needed for function arguments
import numpy as np # needed for np.empty_like

ctypedef np.float32_t float_t
ctypedef np.float64_t double_t
ctypedef np.int32_t int_t

#cimport from .pxd
from .fastchem cimport FastChem as C_FastChem

cdef class PyFastChem:
    cdef C_FastChem[double]* c_fastchem

    def __cinit__(self, file, verbose):
        self.c_fastchem = new C_FastChem[double](file.encode('utf-8'), verbose)

    def calcDensities(self,
    np.ndarray[dtype=double_t, ndim=3, mode="c"] temperature,
    np.ndarray[dtype=double_t, ndim=3, mode="c"] pressure):
        cdef vector[double] T = temperature.ravel()
        cdef vector[double] P = pressure.ravel()*10 # FastChem uses pressure in dyn cm-2
        cdef vector[vector[double] ] densities
        cdef vector[double] h_densities
        cdef vector[double] mean_mol_weight
        self.c_fastchem.calcDensities(T, P, densities, h_densities, mean_mol_weight)
        return np.asarray(T), np.asarray(P), np.asarray(densities).T, np.asarray(h_densities), np.asarray(mean_mol_weight)

    def getSpeciesNumber(self):
        return self.c_fastchem.getSpeciesNumber()
    def getSpeciesName(self, index):
        return self.c_fastchem.getSpeciesName(index)
    def getSpeciesSymbol(self, index):
        return self.c_fastchem.getSpeciesSymbol(index)
    def getSpeciesIndex(self, symbol):
        return self.c_fastchem.getSpeciesIndex(symbol.encode('utf-8'))
    def getSpeciesMolecularWeight(self, species_index):
        return self.c_fastchem.getSpeciesMolecularWeight(species_index)

    def __dealloc__(self):
        del self.c_fastchem