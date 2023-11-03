##########################################################################################
import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
import time
import itertools
import operator

##### INTRODUCTION #######################################################################

'''

This file is a compilation of resuable functions in the research, made for ease of use
in future written programs.

ERROR HANDLING IS A PAIN, and I am too lazy to do it. When you use this function,
better make sure the inputs are correct. 

SIMULATIONS RAN PRIOR TO 2023/09/18 WILL HAVE DIFFERENT RESULTS DUE TO THE DIFFERENCE
IN THE RANDOM NUMBERS GENERATED. OLDER SIMULATIONS USING TIMELINE WILL NOT WORK. MAKE 
SURE TO EDIT ACCORDINGLY.

Written by: 
  Hendry. Department of Physics, University of Indonesia. 

'''

##########################################################################################
##### BLOCH SPHERE STATE VECTOR ##########################################################
##########################################################################################

def T2star():
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Returns the time constant for T2-relaxation/dephasing/decoherence in microseconds.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    (none)
    
    '''
    
    return 3.0

##########################################################################################
##### BLOCH SPHERE STATE VECTOR ##########################################################
##########################################################################################

def bloch_psi(theta, phi):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Make a qubit state parameterized by its coordinate in the Bloch sphere.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    theta   ->  polar angle.
    
    phi     ->  azimuthal angle.

    '''
    
    return (np.cos(theta / 2) * qt.basis(2, 0) 
            + np.exp(1j * phi) * np.sin(theta / 2) * qt.basis(2, 1))

##########################################################################################
##### CALCULATE COMPUTATION TIME #########################################################
##########################################################################################

def clock(start_clock):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Computes the computation time and print it on the terminal when called.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    start_clock -> The time when the clock starts.

    '''

    print(f"Computation took {time.time() - start_clock} seconds.")

##########################################################################################
##### MAKE TIMELINE ######################################################################
##########################################################################################

def timeline(input_array : list, cascade = False):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Makes a nested numpy array containing arrays of time values of multiple intervals, 
    all starting from zero. The reason for the starting point is that the final state of
    a process is interpreted as the initial state for the next process.
    
    The function also makes timestamps, which counts the time starting from zero of the 
    first entry. The zero of the second entry is taken to coincide with the end of the 
    first entry, so the end of the second entry is the sum of the ends of both entries. 
    This goes on for the subsequent entries.

    Lastly, if specified the function can cascade the timeline with the appropriate
    timestamps added to give the full time list.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    input_array ->  Lists of time intervals. It is taken as a nested list with the follo-
                    wing format:

                        [[end_1, timepoints_1], [end_2, timepoints_2], ...]
                    
                    where 'end' specifies the endpoint of the interval, and 'timepoints' 
                    specifies the number of evenly-spaced points in that interval. 

                    If timepoints are all the same, an alternative input is

                        [end_1, end_2, ..., end_last, timepoints]

    cascade     ->  Make a single list from the timeline with the stamps appropriately 
                    added. Useful in situations where plots is to be done using a single 
                    time list. 
    '''

    if is_lst := isinstance(input_array[0], list):
        end_points, num_points = np.swapaxes(input_array, 0, 1)
    else:
        end_points = input_array[ : -1]

    '''
    List comprehension utilizing the assignment operator is also possible:

    x = 0
    stamp_lst = [0, *[x := x + endpoint for endpoint in end_points]]
    '''
    
    time_line = [np.linspace(0, end_points[i], num_points[i]) if is_lst \
               else np.linspace(0, end_points[i], input_array[-1]) \
                for i in range(len(end_points))]
    
    stamp_lst = list(itertools.accumulate([0, *end_points[ : -1]], operator.add))
    
    cascaded_timelst = 0 
    if cascade:
        cascaded_timelst = np.concatenate((time_line[0], 
                            *[time_line[i] + stamp_lst[i] 
                              for i in range(1,len(end_points))]))

    return time_line, stamp_lst, cascaded_timelst

##########################################################################################
##### OU NOISE ###########################################################################
##########################################################################################

def noise_default(name = "delta"):
    
    """
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Computes [delta] and [epsilon] OU noises in Genov's Hamiltonian. 
    
    Returns a tuple (tau, sigma) for OU_module.noise

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    name    ->  Name of the noise. Is "delta" by default or if invalid input were given.

    --------------------------------------------------------------------------------------

    """
    
    tau = 25
    sigma = np.sqrt(2) / 3
    
    if name == "epsilon":
        tau = 500
        sigma  = 0.05
        
    return tau, sigma

##########################################################################################
  
def noise(timelst, sample, tau, sigma,
          seed = None, plot = False, show_time = False, name = "", 
          _tl_init_val = None, _tl_rng = None):
    
    """
    --------------------------------------------------------------------------------------
    REFERENCES
    --------------------------------------------------------------------------------------

        Genov, G. T. (2021). Ornstein-Uhlenbeck numerical simulation note. 

    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Computes [delta] and [epsilon] OU noises in Genov's Hamiltonian. 
    
    Returns an array of size (number of samples) x (number of time points).

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    timelist    -> List of time points.
   
    sample      -> Number of samples.
   
    tau         -> Relaxation time.
   
    sigma       -> Steady-state standard deviation of the noise.
    
    seed        -> Seed for reproducible results. 
    
    plot        -> Plot the result (False by default).
    
    show_time   -> Show the computation time (False by default).
    
    name        -> Name of the noise (empty by default).
                    >> 'delta'      -> delta noise
                    >> 'epsilon'    -> epsilon noise
       
    WARNING: 
    The following parameters are used exclusively for [noise_tl]. Making noise with fixed 
    initial value will result in incorrect simulation.
                                         
    _tl_init_val-> Set initial value for the noise for each sample. Is an array of length 
                   equal to the number of samples.
                            
    _tl_rng     -> Set rng for the noise.

    --------------------------------------------------------------------------------------
    
    """

    exp_term = np.exp(-(timelst[1]-timelst[0]) / tau)
    sqrt_term = np.sqrt(sigma ** 2 * (1 - exp_term ** 2))


    timepoints = len(timelst)

    start_clock =  time.time()
    
    '''
    
    The noise is normally distributed with mean = 0, following the equation written
    in Genov's note. The first term is taken from a random distribution having a 
    standard deviation of sigma. Meanwhile, the random number appearing in the 
    equation for the increments have instead a standard deviation of 1. 
    
    The output of this function will be different from the previous versions due to the
    different orders in which the random numbers are generated. 

    '''
    
    if _tl_rng:
        rng = _tl_rng
    else:
        rng = np.random.default_rng(seed = seed)
    
    '''
    WARNING: 
    
    Making new default_rng call causes the random numbers to finish. This means
    repeating a noise call with the same seed in one program run would give us
    the EXACT same noise.
    
    '''
    
    if _tl_init_val:
        init_val = _tl_init_val
    else:
        init_val = rng.normal(loc = 0, scale = sigma, size = sample)
    
    out_arr = []
    
    for i in range(sample):
        x = [init_val[i]]

        rand_unitary = rng.normal(loc = 0, scale = 1, size = timepoints - 1)
        # Writing it like this is allowed, since different [rng.normal] calls return
        # different numbers. 
        
        for j in range(timepoints - 1):
            x.append(x[j] * exp_term + rand_unitary[j] * sqrt_term)
        
        out_arr.append(x)
    
    '''
    I did some testing (unfortunately the code is messy and not saved).

    List comprehension seems useful, but the recursion present in the loop demands
    variable assignment, which seems to slow down things more. 

    And while it is stated above that the number of rng.normal calls is to be
    minimized due to the computation demands, by making rand_unitary an array
    of dimension sample * (timepoints - 1) we would need to put extra resources to
    compute the indices inside the loop, which outweights the burden of creating
    rand_unitary of dimension (timepoints-1) in each sample iteration. 

    I also tried the "MATLAB way" of creating an empty array then replacing the
    values, but it is expectedly way slower.

    A big improvement is obtained when I realized that the old version had been
    calculaing the constant sqrt_term over each loop. By fixing this the computational
    time goes down tremendously.

    In any case, this version is currently the fastest one I have come with. Not that
    it really matters, since the usual case of 2500 samples and 100 timepoints takes
    less than 10 seconds to run.
    '''
    
    # Show time if specified.
    if show_time:
        clock(start_clock)
    
    # Plot if specified.
    if plot:
        plotter(timelst, sample, [[name, out_arr]])
        # Function defined below.

    return np.array(out_arr)

##########################################################################################
##### OU NOISE + TIMELINE ################################################################
##########################################################################################

def noise_tl(timeline, sample, tau, sigma, seed = None):
    
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Compute the OU noise for every timelist contained within [timeline]. The output is
    a nested array. The first axis corresponds to the [samples], while the second axis
    corresponds to the [timeline]. I make it this way so that it can be used for [genov]
    and [genov_tl] which is designed to compute the Hamiltonian for a given sample. 

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    
    timeline    -> (see [timeline] and [noise])
    
    sample      -> (see [timeline] and [noise])
    
    tau         -> (see [timeline] and [noise])
    
    sigma       -> (see [timeline] and [noise])
    
    seed        -> (see [timeline] and [noise])
    
    '''
    
    l = len(timeline)
    
    rng = np.random.default_rng(seed = seed)
    
    out_arr = []
    for i in range(sample):
        per_sample = [noise(timelst = timeline[0], sample = 1, 
                     tau=tau, sigma=sigma, _tl_rng = rng)]

        for j in range(l-1):
            # Take last value of previous noise instance for each sample
            init_val = [per_sample[j][0][-1]]
            
            per_sample.append(noise(timelst = timeline[j + 1], sample = 1, 
                                tau = tau, sigma = sigma, _tl_rng = rng, 
                                _tl_init_val = init_val))
        
        out_arr.append(per_sample)
        # To test whether this method avoids the rng problem discussed in [noise],
        # compare this function with a single noise call made over the whole timeline.

    return out_arr

##########################################################################################
##### Genov's Hamiltonian ################################################################
##########################################################################################

def genov(timelst : np.ndarray, Omega_1 = 0, f = 1, phi = 0, g = 0, 
          omega_s = 0, xi = 0, delta = 0, epsilon = 0):
    '''               
    --------------------------------------------------------------------------------------
    REFERENCES
    --------------------------------------------------------------------------------------

        Genov, G. T. (2021). Ornstein-Uhlenbeck numerical simulation note.
        Hendry. Genov's Hamiltonian.
        Hendry. (Bloch Sphere) Hamiltonian Representation of Rotations. 

    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------

    Computes the full form of Genov's Hamiltonian in the interaction picture and RWA 
    approximation:

        H = delta(t) * sz / 2 
            + Omega_1 * f(t) * (1 + epsilon(t)) * (cos(phi(t)) * sx + sin(phi(t)) * sy)
            + g * sz * cos(omega_s * t + xi) / 2

    for ONE SAMPLE. 
    
    Returns a list which we can directly pass as a [qutip.mesolve] Hamiltonian argument. 

    The default values return the Hamiltonian argument corresponding to
        H = 0
    Other advantage of setting default values: need not specify the parameters in order.

    For multiple samples call this function for each sample. This function does not 
    support multiple-sample calls since looping will be needed for [qutip.mesolve] calls
    anyway. 

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------

    timelst -> Time list for evaluation of Hamiltonian.

    delta   -> Random noise for the precession about the z-axis, the off-resonance error.
    
    epsilon -> Random noise for f, the pulse length/amplitude error.
        
        [delta] and [epsilon] are ARRAYS obtained from [OU_module.noise]. LEAVE EMPTY
        FOR NO NOISE HAMILTONIAN.

    f       -> Modulation to the peak rabi frequency.
    
    phi     -> Axis control phase of the pulse.
        
        For the sake of simplicity, [f], and [phi] can be FUNCTIONS, LISTS, or NUMBERS.
    
    Omega_1 -> Peak rabi frequency, the frequency of the precession about the pulse axis.
    
    g       -> Probing amplitude.
    
    omega_s -> Probing frequency.
    
    xi      -> Unknown phase of probing.

        These four are CONSTANTS.

    --------------------------------------------------------------------------------------

    '''
    # Pauli matrices
    sx = qt.sigmax()
    sy = qt.sigmay()
    sz = qt.sigmaz()

    # No noise Hamiltonian
    if not(isinstance(delta, np.ndarray)):
        delta = np.zeros(shape = (len(timelst),))

    if not(isinstance(epsilon, np.ndarray)):
        epsilon = np.zeros(shape = (len(timelst),))

    # In case [f] and [phi] are not function calls,
    def ff(timelst):

        if callable(f):
            return f(timelst)
        
        elif isinstance(f, list) or isinstance(f, np.ndarray):
            return f
        
        else:
            arr_f = np.empty(shape = (len(timelst),))
            arr_f.fill(f)
            return arr_f
        
    def phii(timelst):

        if callable(phi):
            return phi(timelst)
        
        elif isinstance(phi, list) or isinstance(phi, np.ndarray) :
            return phi
        
        else:
            arr_phi = np.empty(shape = (len(timelst),))
            arr_phi.fill(phi)
            return arr_phi
        
    # Building the Hamiltonian entry for [qutip.mesolve]
    # First term, td = time dependence
    H1 = sz / 2
    H1_td = delta

    # Second term
    H2x = Omega_1 / 2 * sx
    H2x_td = ff(timelst) * (1 + epsilon) * np.cos(phii(timelst))

    H2y = Omega_1 / 2 * sy
    H2y_td = ff(timelst) * (1 + epsilon) * np.sin(phii(timelst))

    # Third term
    H3 = g / 2 * sz
    H3_td = np.cos(omega_s * timelst.astype(float) + xi)

    return [[H1, H1_td], [H2x, H2x_td], [H2y, H2y_td], [H3, H3_td]]

##########################################################################################
##### GENOV + TIMELINE ###################################################################
##########################################################################################

def genov_tl(timeline : list, Omega_1_lst = 0, f_lst = 1, phi_lst = 0, g_lst = 0, 
             omega_s_lst = 0, xi_lst = 0, delta_lst = 0, epsilon_lst = 0):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
        
    Compute the Genov Hamiltonian for every timelist contained within [timeline]. Every
    time interval has a different syntax for [genov] corresponding to the different 
    processes, so unlike in [noise_tl] the Hamiltonian parameters are taken in as LISTS.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------

    (see [timeline] and [genov]). "_lst" is added to explicitly say that the variables
    are taken as LISTS. 

    If a single number is passed in instead, this function will make a list with the same
    length as the timeline and put in that number for all entries. 

    For the OU noises, the function generates a nested array full of zeros as the default
    values. Passing in other numbers does not work and is useless for the physics, so I
    will not deal with it much. 

    Note that the first index of the noise lists passed into the argument corresponds to 
    [timeline]. 

    '''
    
    l = len(timeline)
    
    # Change the input into a list if a single number is passed in.
    param_lst = [Omega_1_lst, f_lst, phi_lst, g_lst, omega_s_lst, xi_lst]

    for i in range(len(param_lst)):

        if not(isinstance(param_lst[i], list)) and not(isinstance(param_lst[i], np.ndarray)):

            param_lst[i] = np.full(shape = (l,), fill_value = param_lst[i])

    # For the OU noises, the form is a bit different:
    noise = [delta_lst, epsilon_lst]

    for i in range(len(noise)):

        if not(isinstance(noise[i], list)) and not(isinstance(noise[i], np.ndarray)):
                
            noise[i] = [np.zeros(shape = (len(timeline[j]),)) for j in range(l)]

    # The main task is simple:
    
    return [genov(timeline[i], param_lst[0][i], param_lst[1][i], \
                             param_lst[2][i], param_lst[3][i], param_lst[4][i], \
                             param_lst[5][i], noise[0][i], noise[1][i])
            for i in range(l)]

##########################################################################################
##### EXECUTE A WHOLE SIMULATION #########################################################
##########################################################################################

def execute(timeline, rho0, Ham, reset = False, flatten = False):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
    
    This program executes multiple mesolve corresponding to different time intervals and 
    different Hamiltonians. The main purpose of this function is so that a whole 
    simulation of different operations (e.g. free precession, then 90-rotation, then free 
    precession again, then 90-rotation again) can be executed with the call of a function.
    
    To make this function as useful as possible, it needs to stay as general as possible.
    So, I made this function to output only the states of the system for the whole
    [timeline]. With QuTiP, we can do a lot of things with the states, after all.

    This function returns a nested array, each array inside contains the result states 
    from a single mesolve. 
    
    The states passed as arguments into mesolve can be chosen to  stay constant. Each 
    array are independent of each other, allowing multiple independent mesolve calls). 
    
    Another choice is to make the end state of one mesolve be the initial state for the 
    next mesolve. This is the original purpose of this function: to do sequential 
    mesolve calls with changing Hamiltonian.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------

    timeline    ->  see [timeline].

    rho0        ->  initial state.

    Ham         ->  the Hamiltonian taken as the same array as that returned by 
                    [genov_tl].

    reset       ->  choice to reset the state for the next mesolve to [rho0]. By default
                    it is [False] so the end state of one mesolve is taken as the initial
                    state for the next mesolve, allowing sequential operations.

    flatten     ->  flatten the list of mesolve solutions, making it comparable with cascaded
                    timeline. 
    '''
    
    l = len(timeline)
    
    out_arr = []

    for i in range(l):

        rho = qt.mesolve(Ham[i], rho0, timeline[i], [], []).states

        out_arr.append(rho)

        if not(reset):
            
            rho0 = rho[-1]
    
    if flatten:
        out_arr = sum(out_arr, [])
    
    return out_arr

##########################################################################################
##### The Pauli Spin Matrices ############################################################
##########################################################################################

def pauli():
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------

    Returns a list containing sigma_x, sigma_y, and sigma_z.

    '''

    return [qt.sigmax(), qt.sigmay(), qt.sigmaz()]

##########################################################################################
##### Plotting ###########################################################################
##########################################################################################

def plotter(timelst, sample, plotdata):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------

    Returns one figure containing plots of all the specified quantities vs time. 
    
    Able to do multiple samples in one plot.

    The plots are stacked vertically. 
    
    This is useful for our purposes since we usually want to compare some quantities at 
    a given time. 

    I try to keep to codes simple. Extra features are to be added when needed. 

    Note that this plotting function will not be used all that much. Considering the 
    diversity of graphs we make in the research, directly using matplotlib would be a 
    better idea.

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------

    timelst     -> Time list.

    sample      -> Number of samples. Only to be shown at the top of the figure.
    
    plotdata    -> The data to plot, written like so:
                    [
                        [plot_1_name, [
                                        [plot1_sample1], [plot1_sample2],...
                                                                            ]
                                                                             ],
                        [plot_2_name, [
                                        [plot2_sample1], [plot2_sample2],...
                                                                            ]
                                                                             ],
                        ...
                                                                                    ]
                    For example,
                    [['delta', [[delta_sample1], [delta_sample2]]], 
                     ['epsilon', [[epsilon_sample1], [epsilon_sample2]]]

                    It's a list of what to plot in each plot,
                     
                    containing a 2-entry list of the name of the vertical axis and
                    the data to plot,
                     
                    the data to plot being a list
                     
                    of lists corresponding to each sample.

                    In other words, it is a FOUR DIMENSIONAL list. 
                    
                    One might find it convoluted at first, but a little work 
                    with it should make one used to it.

                    plot_x_name can be chosen from the dictionary in the program.

    --------------------------------------------------------------------------------------
    '''

    # Making the subplotss
    fig, ax = plt.subplots(len(plotdata), num = 'Plotted with [OU_module.plotter]')

    # Make a dummy array to avoid indexing error for the case of 1 plot
    if not(isinstance(ax, np.ndarray)):
        ax = [ax, ax] 

    # Set things up for the plot
    ax[0].set_title(f'Number of samples: {sample}')
    ax[-1].set_xlabel('$time$')

    # A dictionary for naming the vertical axis
    ydict = {
        'delta'         :   "$\delta$",
        'epsilon'       :   '$\epsilon$',
        'expsigmax'     :   '$<\sigma_x>$',
        'expsigmay'     :   '$<\sigma_y>$',
        'expsigmaz'     :   '$<\sigma_z>$',
        'meanexpsigmax' :   '$\overline{<\sigma_x>}$',
        'meanexpsigmay' :   '$\overline{<\sigma_y>}$',
        'meanexpsigmaz' :   '$\overline{<\sigma_z>}$',
        ''              :   ''
    }

    # Plotting
    for i in range(len(plotdata)):
        # Get the y-label name from the input
        name = plotdata[i][0]   

        # Set the y-label
        ax[i].set_ylabel(ydict[name])
                
        for j in range(len(plotdata[i][1])):
                        # range(sample) is not used here so that
                        # plots such as 'meanexpsigmaz' with only
                        # one value for one time can be plotted 
                        # together with those whose values vary
                        # with the sample. 
            ax[i].plot(timelst, plotdata[i][1][j])
    
    plt.show()


def blochplotter(quantity, plotdata):
    '''
    --------------------------------------------------------------------------------------
    INTRODUCTION
    --------------------------------------------------------------------------------------
    This function plots the result of [qutip.mesolve] onto the bloch sphere, for multiple
    samples. Each samples is plotted in one separate plot. 

    --------------------------------------------------------------------------------------
    PARAMETERS
    --------------------------------------------------------------------------------------
    quantity    -> Object to print:
                    >> states   ->  obtained from qutip.mesolve().states
                    >> sigma    ->  obtained from qutip.mesolve().expect
                                    with e_ops = [sigmax(), sigmay(), sigmaz()]

    plotdata    -> The data to plot, written like so:
                    [[point_set_1], [point_set_2], ...]
                   
                   states   -> point_set_x = mesolve().states.

                   sigma    -> point_set_x = mesolve().expect[0], .expect[1], .expect[2]
                                                       (sigmax)    (sigmay)    (sigmaz)  

    --------------------------------------------------------------------------------------
    '''

    # List to store Bloch sphere figures
    b = []

    # Get the number of samples
    sample = len(plotdata)

    # Making one Bloch sphere for each sample, with the object plotted
    # depending on the input.
    for i in range(sample):
        b.append(qt.Bloch())

        if quantity == 'states':
            b[i].add_states(plotdata[i][0])

        if quantity == 'sigma':
            # Plot with point and line
            b[i].add_points(plotdata[i])
            b[i].add_points(plotdata[i], meth = 'l')
            # Also plot the initial and final vectors.
            b[i].add_vectors([plotdata[i][0][0], plotdata[i][1][0], plotdata[i][2][0]])
            b[i].add_vectors([plotdata[i][0][-1], plotdata[i][1][-1], plotdata[i][2][-1]])
        
        b[i].show()
    
    plt.show()

