""" Script to be used to analyze WaveModeNMA data.
Copyright Nanosurf AG 2023
License - MIT
"""

#%%
#Import libraries
import datetime as datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pathlib
import sys
import time

from nanosurf.lib.util import nhf_reader, gwy_export, fileutil
from scipy.interpolate import griddata
from scipy.optimize import curve_fit

#Define functions
### Analysis functions ###
def analyze_force_curve(distance_nm:np.array, force_nN:np.array):
    analysis_result = {}
    ### Define index to split advance and retract part of force curve ###
    points_per_period: int = len(distance_nm)
    points_per_half_period: int = int(points_per_period/2)
    
    ### Get max force as force at center of cycle###
    max_force_index = points_per_half_period
    max_force = force_nN[max_force_index]
    analysis_result["max_force"] = max_force

    ### Get adhesion as minimum point of retract part ###
    adhesion = np.min(force_nN[max_force_index:-1])
    adhesion_index = np.where(force_nN[max_force_index:-1] == adhesion)[0][0]+max_force_index
    analysis_result["adhesion"] = adhesion*-1
    analysis_result["adhesion_distance"] = distance_nm[adhesion_index]

    ### Get stiffness from slope of in contact retract part###
    try:
        popt, _ = curve_fit(f=fit_func_linear, xdata=np.array(
            distance_nm[max_force_index:adhesion_index]), ydata=np.array(force_nN[max_force_index:adhesion_index]))
        slope = popt[0]
        offset = popt[1]
    except:
        slope = np.nan  # Put NaN if fit was not successful
        offset = np.nan
    analysis_result["stiffness"] = slope*-1
    analysis_result["slope_distance"] = np.array(distance_nm[max_force_index:adhesion_index])
    analysis_result["slope_force"] = fit_func_linear(np.array(distance_nm[max_force_index:adhesion_index]),slope,offset)

    ### Get effective elasticity from hertz fit of in contact retract part###
    try:
        popt, _ = curve_fit(f=fit_func_hertz, xdata=np.array(
            distance_nm[max_force_index:adhesion_index]), ydata=np.array(force_nN[max_force_index:adhesion_index]))
        e_eff = popt[0]
        x0 = popt[1]
    except:
        e_eff = np.nan  # Put NaN if fit was not successful
        x0 = np.nan
    analysis_result["elasticity"] = e_eff*1e9 #nN/nm^2 to nN/m^2 (Pa)
    analysis_result["contact_point"] = x0
    analysis_result["hertz_distance"] = np.array(distance_nm[max_force_index:adhesion_index])
    analysis_result["hertz_force"] = fit_func_hertz(np.array(distance_nm[max_force_index:adhesion_index]),e_eff,x0)

    return analysis_result


def analyze_nma_data(ch_nma_free_wave: nhf_reader.NHFDataset , ch_nma_deflection: nhf_reader.NHFDataset, ch_nma_interaction: nhf_reader.NHFDataset, ch_topography_in_um: nhf_reader.NHFDataset, deflection_sensitivity:float, spring_constant:float) -> np.ndarray:
    """ Cuts the interaction signal into segments that are analyzed as single force-distance curves using the free wave signal as distance.
    Assumes that free wave and interaction signal are well synchronized and that the baseline was well corrected during measurement.
    Calculates maximum force, which is the peak value of the interaction signal.

    Parameters
    ----------
        nma_free_wave: np.ndarray
            The cantilever deflection signal out of contact with surface.
            It is used to describe distance data.
        nma_interaction: np.ndarray
            The cantilever deflection signal out of contact with surface subtracted from 
            the cantilever deflection signal with intermittent surface contact.
        topography:np.ndarray
            The array with the topography information.
            Used to read the number of lines and points
        deflection_sensitivity:float
            Factor in m/V used to scale cantilever deflection data from V to m
        spring_constant:float
            Factor in N/m used to scale cantilever deflection data from m to N

    Return
    ------
        max_force_matrix: np.ndarray
            Includes the maximum force of the force-distance curves as image matrix.
            The maximum force is the value in the middle of the curve.
        adhesion_matrix: np.ndarray
            Includes the adhesion of the force-distance curves as image matrix.
            The adhesion is calculated as minimum of the retract part of the curve.
        slope_matrix: np.ndarray
            Includes the slope of the force-distance curves as image matrix.
            The slope is calculated from the linear fit of the retract part of the curve
            between maximum force and adhesion value.

    """
    max_force_list: list = []
    adhesion_list: list = []
    stiffness_list: list = []
    elasticity_list: list = []

    image_number_of_line = ch_topography_in_um.dataset.shape[0]
    image_points_per_line = ch_topography_in_um.dataset.shape[1]
    
    nma_free_wave = ch_nma_free_wave.dataset
    nma_free_wave_unit = ch_nma_free_wave.attribute['base_calibration_unit']
    if(nma_free_wave_unit =='V'):
        nma_free_wave_nm = [scale_V_to_m(x,deflection_sensitivity)*1E9 for x in nma_free_wave]
    if(nma_free_wave_unit =='m'):
        nma_free_wave_nm = [x*1E9 for x in nma_free_wave]

    nma_deflection = ch_nma_deflection.dataset
    nma_deflection_unit = ch_nma_deflection.attribute['base_calibration_unit']
    if(nma_deflection_unit =='V'):
        nma_deflection_nm = [scale_V_to_m(x,deflection_sensitivity)*1E9 for x in nma_deflection]
    if(nma_deflection_unit =='m'):
        nma_deflection_nm = [x*1E9 for x in nma_deflection]

    nma_interaction = ch_nma_interaction.dataset
    nma_interaction_unit = ch_nma_interaction.attribute['base_calibration_unit']
    if(nma_interaction_unit =='V'):
        nma_interaction_nN = [scale_m_to_N(scale_V_to_m(x,deflection_sensitivity),spring_constant)*1E9 for x in nma_interaction]
    if(nma_interaction_unit =='m'):
        nma_interaction_nN = [scale_m_to_N(x,spring_constant)*1E9 for x in nma_interaction]
    if(nma_interaction_unit =='N'):
        nma_interaction_nN = [x*1E9 for x in nma_interaction]

    num_of_curves = int(image_points_per_line * image_number_of_line)
    #distance_nm: np.ndarray = np.array(nma_free_wave_nm)
    distance_nm: np.ndarray = np.array(nma_deflection_nm)
    points_per_period: int = len(nma_free_wave_nm)

    next_print_time = time.time()

    for i in range(num_of_curves):
        ### Analyze single F-d-curve here ###
        start_index: int = i * points_per_period
        end_index: int = i * points_per_period + points_per_period
        force_nN = np.array(nma_interaction_nN[start_index:end_index])
        distance_nm2 = np.array(distance_nm[start_index:end_index])
        analysis_result = analyze_force_curve(distance_nm2,force_nN)
        max_force_list.append(analysis_result['max_force'])
        adhesion_list.append(analysis_result['adhesion'])
        stiffness_list.append(analysis_result['stiffness'])
        elasticity_list.append(analysis_result['elasticity'])

        if(i<50):
            distance_nm2=distance_nm2-analysis_result['contact_point']
            plt.plot(distance_nm2, force_nN)
            plt.scatter(distance_nm2[int(points_per_period/2)], analysis_result['max_force'])
            plt.scatter(analysis_result['adhesion_distance']-analysis_result['contact_point'], analysis_result['adhesion']*-1)
            #plt.plot(analysis_result["slope_distance"], analysis_result["slope_force"])
            plt.plot(analysis_result['hertz_distance']-analysis_result['contact_point'], analysis_result['hertz_force'])
            print(f"Effective Elasticity (Hertz): {analysis_result['elasticity']*1e-9} GPa")
            print(f"Contact Point: {analysis_result['contact_point']}")
            
            plt.show()


        ### Print curve number to show progress in console ###
        if time.time() > next_print_time:
            print(f"Analyzed curves: {i+1}/{num_of_curves}, {int(i/num_of_curves*100):d}%")
            next_print_time = time.time() + 0.5

    ### Transform lists into image matrix ###
    adhesion_matrix = np.flipud(np.reshape(
        adhesion_list, (image_number_of_line, image_points_per_line)))
    max_force_matrix = np.flipud(np.reshape(
        max_force_list, (image_number_of_line, image_points_per_line)))
    stiffness_matrix = np.flipud(np.reshape(
        stiffness_list, (image_number_of_line, image_points_per_line)))
    elasticity_matrix = np.flipud(np.reshape(
        elasticity_list, (image_number_of_line, image_points_per_line)))
    
    return max_force_matrix, adhesion_matrix, stiffness_matrix, elasticity_matrix


### Fitting functions ###
def fit_func_linear(x: np.ndarray, slope: float, offset: float) -> np.ndarray:
    """
    Linear function that calculates the value of a line given a set of x values, slope, and y-intercept.

    Parameters
    ----------
        x: float or array-like
            The independent variable(s) for the linear function.
        slope: float
            The slope of the line.
        offset: float
            The y-intercept of the line.

    Returns
    -------
        y: float or array-like
            The dependent variable(s) for the linear function, calculated as slope*x + offset.
    """
    return slope*x+offset


def fit_func_hertz(x, e_eff, x0):
    """
    Function that calculates the tip sample force based on Hertz model.

    Parameters
    ----------
        x: float or array-like
            The independent variable(s) for the linear function.
        e_eff: float
            The effective youngs modulus of cantilever and sample.
        x0: float
            The contact point of the measurement.

    Returns
    -------
        y: float or array-like
            The calculated force based on effective youngs modulus and cantilever tip radius.
    """
    r = 10 #tip radius in nm
    return (4/3)*e_eff*np.sqrt(r)*(x0-x)**1.5


def fit_func_sneddon(x, e_sample, x0):
    """
    Function that calculates the tip sample force based on Sneddon model.

    Parameters
    ----------
        x: float or array-like
            The independent variable(s) for the linear function.
        e_sample: float
            The youngs modulus of the sample.
        x0: float
            The contact point of the measurement.

    Returns
    -------
        y: float or array-like
            The calculated force based on sample youngs modulus, poisson ratio and opening angle of cantilever tip.
    """
    alpha=np.deg2rad(25)
    nu_sample = 0.5
    return (2/np.pi)*e_sample/(1-nu_sample**2)*np.tan(alpha)*(x0-x)**2


### Conversion function ###
def convert_file(source_file:pathlib.Path, target_file:pathlib.Path) -> bool:
    """ Converts a .nhf file to .gwy file

    Parameters
    ----------
        source_file:pathlib.Path
            File to be converted.
        target_file:pathlib.Path
            Converted file.

    Return
    ------
        done:bool
            Returns True if conversion was successful.

    """
    ### Open file instance ###
    nhf_file = nhf_reader.NHFFileReader(verbose=True)
    if nhf_file.read(source_file) == False:
        print("Could not read file")
        exit()
    if nhf_file.version() < (1,1):
        print(f"Unknown file version: {nhf_file.version()}")
        exit()
    print(f"Found {nhf_file.measurement_count()} measurements in file:")
    print(nhf_file.measurement.keys())

    ### Read image attributes ###
    print("Reading first measurement in file")
    measurement_name = nhf_file.measurement_name(0)
    measurement = nhf_file.measurement[measurement_name]
    image_points_per_line = measurement.attribute['image_points_per_line']
    image_number_of_line  = measurement.attribute['image_number_of_lines']
    image_size_x_um = 1e6 * measurement.attribute['image_size_x']
    image_size_y_um = 1e6 * measurement.attribute['image_size_y']
    deflection_sensitivity = measurement.attribute['spm_probe_calibration_deflection_sensitivity']
    spring_constant = measurement.attribute['spm_probe_calibration_spring_constant']
    excitation_frequency = measurement.attribute['wave_frequency']
    resonance_frequency = measurement.attribute['spm_probe_calibration_resonance_frequency']

    ### Read channels ###
    print("Reading channels")
    segment_name = 'Forward'
    segment = measurement.segment[segment_name]
    ch_topography = segment.read_channel('Position Z')
    ch_nma_free_wave = measurement.read_channel('NMA Free Wave')
    ch_nma_deflection = segment.read_channel('NMA Deflection')
    ch_nma_interaction = segment.read_channel('NMA Interaction')
    ch_topography_in_mu = ch_topography
    ch_topography_in_mu.dataset = np.flipud(np.reshape(np.array(1e6 * ch_topography.dataset), (image_number_of_line, image_points_per_line)))
    
    ### Analyze F-curves ###
    print("Start Analyzing")
    max_force_matrix, adhesion_matrix, stiffness_matrix, elasticity_matrix = analyze_nma_data(
        ch_nma_free_wave, ch_nma_deflection, ch_nma_interaction, ch_topography_in_mu, deflection_sensitivity, spring_constant)
    print("Done")
    ### Export data to gwyddion file ###
    done = gwy_export.savedata_gwy(target_file, 
                            size_info=gwy_export.GwySizeInfo(
                                x_range=image_size_x_um*1e-6,
                                y_range=image_size_y_um*1e-6,
                                unit_xy="m"
                            ),
                            data_sets=[ch_topography_in_mu.dataset*1e-6, max_force_matrix*1e-9, adhesion_matrix*1e-9, stiffness_matrix, elasticity_matrix],
                            data_labels=["Topography", "Max Force","Adhesion","Stiffness","Elasticity_Hertz"],
                            data_units=['m', 'N', 'N', 'N/m', 'Pa'])
    if done:
        print(f"Saved result in gwyddion file at:\n{target_file}")
    else:
        print(f"Could not save gwyddion file to: \n{target_file}")
    return True


### Auxilliary functions ###
def scale_V_to_m(data_V: np.ndarray, deflection_sensitivity: float) -> np.ndarray:
    """ Scales the cantilever deflection data from the measured voltage (V) to a distance (m) by multiplying it with the calibrated deflection sensitivity.

    Parameters
    ----------

        data_V: np.ndarray
            Data array to be scaled from voltage (V) to distance (m).
        deflection_sensitivity: float
            Factor for converting measured data from V to m.

    Return
    ------
        result: np.ndarray
            Scaled data array.

    """
    return data_V*deflection_sensitivity


def scale_m_to_N(data_m: np.ndarray, spring_constant: float) -> np.ndarray:
    """ Transforms the cantilever deflection data from distance (m) to a force (N) by multiplying it with the calibrated deflection sensitivity.

    Parameters
    ----------

        data_m: np.ndarray
            Data array to be scaled from distance (m) to force (N).
        spring_constant: float
            Factor for converting measured data from m to N.

    Return
    ------
        result: np.ndarray
            Scaled data array.

    """
    return data_m*spring_constant


def subtract_free_wave(nma_free_wave: np.ndarray, nma_deflection: np.ndarray) -> np.ndarray:
    """ Calculates and returns the cantilever interaction data by subtracting the cantilever deflection out of contact from the 
    cantilever deflection with intermitted sample surface contact.

    Parameters
    ----------

        nma_free_wave: np.ndarray
            The cantilever deflection signal out of contact with surface.
        nma_deflection: np.ndarray
            The cantilever deflection signal with intermittent surface contact.

    Return
    ------
        nma_interaction: np.ndarray
            The cantilever deflection signal out of contact with surface subtracted from 
            the cantilever deflection signal with intermittent surface contact.

    """
    nma_interaction = []
    for i in range(0, len(nma_free_wave)):
        nma_interaction.append(nma_deflection[i]-nma_free_wave[i])
    return nma_interaction


def remove_outliers(matrix: np.ndarray, sigma=3.0)->np.ndarray:
    """ Removes outliers of 2D matrix based on sigma as width of trust interval

    Parameters
    ----------
        matrix: np.ndarray
            Contains matrix to be modified.
        sigma: float
            Width of trust interval.

    Return
    ------
        matrix: np.ndarray
            Contains matrix with removed outliers.

    """
    matrix = matrix.astype(float)
    z_scores = np.abs((matrix - np.nanmean(matrix)) / np.nanstd(matrix))
    outliers = z_scores > sigma
    matrix[outliers] = np.nan
    return matrix


def interpolate_matrix(matrix: np.ndarray)->np.ndarray:
    """ Interpolates nan data of 2D matrix to overwrite empty data.

    Parameters
    ----------
        matrix: np.ndarray
            Contains matrix to be modified.

    Return
    ------
        matrix: np.ndarray
            Contains matrix with interpolated data.

    """
    n_rows, n_cols = matrix.shape
    x = np.arange(n_cols)
    y = np.arange(n_rows)
    xx, yy = np.meshgrid(x, y)
    valid_indices = np.where(~np.isnan(matrix))
    matrix = griddata(valid_indices, matrix[valid_indices], (xx, yy), method='linear').T
    return matrix


def get_demo_app_folder() -> pathlib.Path:
    return pathlib.Path(os.path.abspath(__file__)).parent


def process_all_files_in_folder(folder:pathlib.Path, from_suffix:str, to_suffix) -> bool:
    done = True
    list_of_source_files = [file for file in pathlib.Path(folder).glob(f'**/*{from_suffix}')]
    if len(list_of_source_files) > 0:
        for current_file in list_of_source_files:
           done=process_file(current_file,from_suffix,to_suffix)
           if done == False:
               break
    else:
        print(f"No source-files to found in {folder}")
    return done


def process_file(file:pathlib.Path, from_suffix:str, to_suffix) -> bool:
    done = True
    if file.is_file():
        print(f"Processing file: {file.name}")  
        target_file = file.with_suffix(to_suffix)
        done = convert_file(file, target_file)
        if done == False:
            print("Error while processing data. Abort.")
    else:
        print(f"{file} not found.")
    return done



if __name__ == "__main__":
    cmd_line_option_ask_folder = False
    cmd_line_option_ask_file = True
    cmd_line_option_process_file = False
    path_of_the_directory = get_demo_app_folder() / "example_data"
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-ask_folder": cmd_line_option_ask_folder = True
        if sys.argv[1] == "-ask_file": cmd_line_option_ask_file = True
        if sys.argv[1] == "-process_file": cmd_line_option_process_file = True
    else:
        cmd_line_option_ask_file = True
    
    if cmd_line_option_ask_folder:
        path_of_the_directory = fileutil.ask_folder()
        if path_of_the_directory is not None:
            process_all_files_in_folder(path_of_the_directory, ".nhf", ".gwy")
        else:
            print("no folder was given")
    elif cmd_line_option_ask_file:
        path_of_the_directory = fileutil.ask_open_file()
        if path_of_the_directory is not None:
            process_file(path_of_the_directory, ".nhf", ".gwy")
        else:
            print("no file was given")
    elif cmd_line_option_process_file:
        path_of_the_directory = None
        path_of_the_directory = pathlib.Path(sys.argv[2])
        if path_of_the_directory is not None:
            process_file(path_of_the_directory, ".nhf", ".gwy")
        else:
            print("no file was given")
    else:
        print("no option selected")
        print("available options:")
        print("-ask_folder")
        print("-ask_file")
        print("-process_file")

# %%
