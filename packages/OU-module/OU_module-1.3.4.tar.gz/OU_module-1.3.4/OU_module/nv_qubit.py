##########################################################################################
import numpy as np
import qutip as qt
import matplotlib.pyplot as plt

##### INTRODUCTION #######################################################################

'''

This file contains the [nv_qubit] class which constructs an nv qubit.

Written by: 
  Hendry. Department of Physics, University of Indonesia. 

'''

##########################################################################################

class nv_qubit():

    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
    NV qubit constructor. The Larmor frequency is in MEGAHERTZ (MHz).

    hbar is 1.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    with_state  ->  Which state to make a qubit with. One of the states of the qubit is the
                    m_s = 0 state, and the other state is determined by this parameter.

                    "+" ->  the m_s = +1 state
                    "-" ->  the m_s = -1 state

                    Passing in other things will construct an nv_qubit with "-" state. 

                    Default is "-".

    B_0         ->  The static field causing the Zeeman splitting which constructs the
                    qubit, in MILLITESLA (mT).

                    Default is 30 mT = 300 Gauss.

    '''

    def __init__(self, with_state = "-", B_0 = 30):

        self.with_state = with_state
        self.B_0 = B_0

        self.gamma = 2 * np.pi * 28 
        self.gamma_ = f"{self.gamma} MHz/mT"

        self.zero_field_splitting = 2 * np. pi * 2.87e3
        self.zero_field_splitting_ = "2.87 x 10^3 MHz"
        
        self.lower = "0"
        self.upper = "+1"

        add = self.gamma * self.B_0
        if self.with_state == "-":
            add = -add
            self.upper = "-1"
        
        self.omega_0 = self.zero_field_splitting + add
        
        self.alert = False
        if self.omega_0 < 0:
            self.omega_0 = -self.omega_0
            self.lower = "-1"
            self.upper = "0"
            self.alert = True
            
        self.omega_0_ = f"{self.omega_0} MHz"
        
    def __str__(self):
        s = "|| NV Qubit || \n"
        s += "made of electronic levels of NV center in diamond. \n\n"
        s += f"Lower State: m_s = {self.lower} \n"
        s += f"Upper State: m_s = {self.upper} \n\n"
        s += f"Larmor frequency: omega_0 = {self.omega_0_}\n"
        s += f"Recommended strength of Rabi term: Omega_1 < 0.1 * omega_0 = {0.1 * self.omega_0} MHz"
        if self.alert:
            s += f"\n\nALERT: The m_s = -1 state is lower in energy, you might not want this."
        return s
    
    def __repr__(self):
        return self.__str__()

    """
    WIP
    
    def make_energy_level_diagram():
        fig = plt.figure(num = "Energy Level Diagram of NV Center", 
                         figsize = (7, 3.5), 
                         dpi = 600)
    
    """
        
