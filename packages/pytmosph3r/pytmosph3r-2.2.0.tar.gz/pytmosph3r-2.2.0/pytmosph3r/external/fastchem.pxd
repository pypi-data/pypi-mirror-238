from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp cimport bool
cimport numpy as np
import numpy as np

ctypedef np.npy_uint32 uint

cdef extern from "fastchem.h" namespace "fastchem" nogil:
    cdef cppclass FastChem[T]:
        FastChem(string& model_parameter_file, unsigned int verbose_level_init)
        FastChem(FastChem &obj)

        unsigned int calcDensities(double temperature, double pressure,
                                vector[double]& density_n_out, double& h_density_out, double& mean_molecular_weight_out)
        unsigned int calcDensities(vector[double]& temperature, vector[double]& pressure,
                                vector [ vector[double] ]& density_out,
                                vector[double]& h_density_out, vector[double]& mean_molecular_weight_out)
        unsigned int calcDensities(double temperature, double pressure,
                                vector[double]& density_n_out, double& h_density_out, double& mean_molecular_weight_out,
                                vector[unsigned int]& element_conserved_out,
                                unsigned int& nb_iterations_out, unsigned int& nb_chemistry_iterations_out)
        unsigned int calcDensities(vector[double]& temperature, vector[double]& pressure,
                                vector [ vector[double] ]& density_out,
                                vector[double]& h_density_out, vector[double]& mean_molecular_weight_out,
                                vector[ vector[uint] ]& element_conserved_out,
                                vector[unsigned int]& fastchem_flags,
                                vector[unsigned int]& nb_iterations_out, vector[unsigned int]& nb_chemistry_iterations_out)
        unsigned int calcDensities(vector[double]& temperature, vector[double]& hydrogen_pressure,
                                vector [ vector[double] ]& density_out,
                                vector[double]& mean_molecular_weight_out,
                                vector[ vector[uint] ]& element_conserved_out,
                                vector[unsigned int]& fastchem_flags,
                                vector[unsigned int]& nb_chemistry_iterations_out)
        string getSpeciesName(unsigned int species_index)
        string getSpeciesSymbol(unsigned int species_index)
        unsigned int getSpeciesNumber()
        unsigned int getSpeciesIndex(string symbol)
        string getElementName(unsigned int species_index)
        string getElementSymbol(unsigned int species_index)
        unsigned int getElementNumber()
        double getSpeciesMolecularWeight(unsigned int species_index)
        void setVerboseLevel(unsigned int level)
        void setMaxChemistryIter(unsigned int nb_steps)
        void setMaxPressureIter(unsigned int nb_steps)
        void setMaxNewtonIter(unsigned int nb_steps)
        void setMaxBisectionIter(unsigned int nb_steps)
        void setMaxNelderMeadIter(unsigned int nb_steps)
        void setChemistryAccuracy(double chem_accuracy)
        void setPressureAccuracy(double pressure_accuracy)
        void setNewtonAccuracy(double newton_accuracy)
        void useScalingFactor(bool use_switch)
