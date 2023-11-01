# -*- coding: future_fstrings -*-

#Program to run tirshaker
from omegaconf import OmegaConf
import os
import sys
import copy
import psutil as psu
import random
import time
import re
from scipy import stats
from astropy.io import fits
import numpy as np
from dataclasses import dataclass, field
from typing import List
from TRM_errors.common.common import print_log,write_tirific,load_tirific,\
            set_format,set_limits,tirific_template,finish_current_run,check_pid
import subprocess
from datetime import datetime

class DefFileError(Exception):
    pass

class TirificOutputError(Exception):
    pass

class TirshakerInputError(Exception):
    pass

'''Extract the existing errors if present'''
def get_existing_errors(Tirific_Template, fit_groups, log =False):
    log_statement = ''
    for group in fit_groups:
        fit_groups[group]['ERRORS'] = []
        for disk in fit_groups[group]['DISKS']:
            if disk == 1:
                par = group
            else:
                par = f"{group}_{disk}"
            errors = load_tirific(Tirific_Template,[f'# {par}_ERR'],array=True )
            if len(errors) == 0.:
                fit_groups[group]['ERRORS'].append(None)
            else:
                rings = fit_groups[group]['RINGS']
                fit_groups[group]['ERRORS'].append(np.mean(errors[rings[0]:rings[1]+1]))

    return log_statement
'''Extract the fitting parameters from PARMAX, PARMIN and DELSTART  '''
def get_variations(Tirific_Template, fit_groups, log =False):
    log_statement = ''
    parmax = Tirific_Template['PARMAX'].split()
    parmin = Tirific_Template['PARMIN'].split()
    delta = Tirific_Template['DELSTART'].split()
    for group in fit_groups:
        fit_groups[group]['PARMAX'] = float(parmax[fit_groups[group]['COLUMN_ID']])
        fit_groups[group]['PARMIN'] = float(parmin[fit_groups[group]['COLUMN_ID']])
        fit_groups[group]['FIT_DELTA'] = float(delta[fit_groups[group]['COLUMN_ID']])
    return log_statement

'''Extract the fitting parameters from the fitting VARY line '''
def get_groups(in_groups, no_rings = 3, log = False):
    group_dict = {}   
    log_statement = ''
    log_statement += print_log(f'''GET_GROUPS: We have found the following unformatted groups from VARY:
{'':8s}{in_groups}
''',log)
    for i,group in enumerate(in_groups):
        log_statement += print_log(f'''GET_GROUPS: We are processing {group}
''',log)
        parameter = group.split()
        count = 1
        current_parameter = f'{re.sub("[^a-zA-Z]+", "", parameter[0])}_{count}'
        while current_parameter in group_dict:
            count += 1
            current_parameter = f'{re.sub("[^a-zA-Z]+", "", parameter[0])}_{count}'
        if  parameter[0][0] == 'i':
            current_parameter = current_parameter[1:]
            parameter[0] = f'!{parameter[0][1:]}'
          
        group_dict[current_parameter] = {'COLUMN_ID': i}
        disks = parameter[0].split('_')
        try:
            group_dict[current_parameter]['DISKS'] =  [int(disks[1])]
        except IndexError:
            group_dict[current_parameter]['DISKS'] =  [1]
        #Individual or block
        if parameter[0][0] == '!':
            group_dict[current_parameter]['BLOCK'] = False  
        elif  parameter[0][0] == 'i':
            current_parameter = current_parameter[1:]
            group_dict[current_parameter]['BLOCK'] = False          
        else:
            group_dict[current_parameter]['BLOCK'] = True
      
        
        for part in parameter[1:]:
            if part[0].isnumeric():
                if ':' in part:
                    in_rings = [int(x) for x in part.split(':')]
                    if in_rings.sort():
                        in_rings.sort()
                    in_rings = np.array(in_rings,dtype=int)
                    
                else:
                    in_rings = np.array([int(part),int(part)])

                if 'RINGS' not in group_dict[current_parameter]:
                    group_dict[current_parameter]['RINGS'] = in_rings
                else:
                    if np.array_equal(group_dict[current_parameter]['RINGS'],in_rings):
                        pass
                    else:
                        raise DefFileError("The VARY settings in this deffile are not acceptable you have different rings for one block.")
            else:
                disks = part.split('_')
                try:
                    group_dict[current_parameter]['DISKS'].append(int(disks[1]))
                except IndexError:
                    group_dict[current_parameter]['DISKS'].append(1)
        if 'RINGS' not in group_dict[current_parameter]:
            group_dict[current_parameter]['RINGS'] = np.array([1,no_rings],dtype=int)

        if group_dict[current_parameter]['RINGS'][0] == group_dict[current_parameter]['RINGS'][1] :
            group_dict[current_parameter]['BLOCK'] = False
          
        log_statement += print_log(f'''GET_FIT_GROUPS: We determined the group {group_dict[current_parameter]}
''',log) 
    return group_dict, log_statement

def set_fitted_variations(fit_groups,log=False):
    log_statement = ''
    for group in fit_groups:
        fit_groups[group]['VARIATION'] = [0., 'a']
        for i,disk in enumerate(fit_groups[group]['DISKS']):
            if fit_groups[group]['ERRORS'][i] == None:
                ini_var = 0.
            else: 
                ini_var = fit_groups[group]['ERRORS'][i]
            if fit_groups[group]['FIT_DELTA'] > ini_var:
                ini_var =  fit_groups[group]['FIT_DELTA']
            if ini_var >  fit_groups[group]['VARIATION'][0]:
                fit_groups[group]['VARIATION'][0] = ini_var
        fit_groups[group]['VARIATION'][0] *= 5.
    return log_statement

def set_manual_variations(fit_groups,variation= None,\
                                    cube_name= None,log=False):
    log_statement = ''
    hdr = fits.getheader(cube_name)
    if not 'CUNIT3' in hdr:
        if abs(hdr['CDELT3']) > 100:
            hdr['CUNIT3'] = 'm/s'
        else:
            hdr['CUNIT3'] = 'km/s'
        log_statement += print_log(f'''CLEAN_HEADER:
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Your header did not have a unit for the third axis, that is bad policy.
{"":8s} We have set it to {hdr['CUNIT3']}. Please ensure that this is correct.'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
''',log)
    if hdr['CUNIT3'].upper() == 'HZ' or hdr['CTYPE3'].upper() == 'FREQ':
        log_statement += print_log('CLEAN_HEADER: FREQUENCY IS NOT A SUPPORTED VELOCITY AXIS.', log)
        raise TirshakerInputError('The Cube has frequency as a velocity axis this is not supported')

    
    if hdr['CUNIT3'] == 'm/s':
        hdr['CDELT3'] = hdr['CDELT3']/1000.
   
    for group in fit_groups:
        log_statement += print_log(f'''SET_MANUAL_VARIATIONS: processing {group}
''',log)
        groupbare = group.split('_')
        input = copy.deepcopy(getattr(variation,groupbare[0]))
        if input[1].lower() == 'res':
            if input[2].lower() == 'arcsec':
                input[0] = input[0] * hdr['BMAJ']*3600.
            elif input[2].lower() == 'degree':
                input[0] = input[0] * hdr['BMAJ']
            elif input[2].lower() == 'angle':
                raise TirshakerInputError(f''' We have no way to relate an angle to the resolution of the cube''')
            elif input[2].lower() == 'km/s':
                input[0] = input[0] * hdr['CDELT3']
            elif input[2].lower() == 'm/s':
                input[0] = input[0] * hdr['CDELT3']*1000.
            elif input[2].lower() == 'jy/arcsec**2':
                if 'NOISE' in hdr or 'FATNOISE' in hdr:
                    try:
                        noise = hdr['FATNOISE']
                    except KeyError:
                        noise = hdr['NOISE']
                else:
                   raise TirshakerInputError(f''' We have no way to relate an SBR to the cube without the noise level in the header''') 
                noise = noise*(2. *np.pi / (np.log(256.)))\
                    *hdr['BMAJ']*hdr['BMIN']*3600**2
                input[0] = input[0] * hdr['CDELT3']*noise
        fit_groups[group]['VARIATION'] = [input[0], input[3]]
    return log_statement


def get_manual_groups(cfg, rings = 1, cube_name='None', log= False):
    #First we get the groups that were fitted from file
    groups = cfg.variations.VARY.split(',')
    # And lets translate to a dictionary with the various fitting parameter type and
    # first we disentangle the tirific fitting syntax into a dictionary
    fit_groups,log_statement = get_groups(groups, no_rings = rings, log = log)
    #Then we set the  variation we want for the tirshaker for every group
    log_statement += set_manual_variations(fit_groups,variation=cfg.variations,\
                                    cube_name=cube_name,log=log)
    return fit_groups


def get_fitted_groups(Tirific_Template, log= False):
    #First we get the groups that were fitted from file
    groups = Tirific_Template['VARY'].split(',')
    # And lets translate to a dictionary with the various fitting parameter type and
    # first we disentangle the tirific fitting syntax into a dictionary
    fit_groups,log_statement = get_groups(groups, log = log)
    # Then we attach the fiiting variations to the groups
    log_statement += get_variations(Tirific_Template, fit_groups, log=log)
    # Check whether there are any errors present in the def file
    log_statement += get_existing_errors(Tirific_Template, fit_groups,log=log)
    #Then we set the  variation we want for the tirshaker for every group
    log_statement += set_fitted_variations(fit_groups,log=log)
    return fit_groups

get_fitted_groups.__doc__ =f'''
 NAME:
    get_fit_groups
 PURPOSE:
    get the groups that are fitting, whether they are a block or not and their expected errors

 CATEGORY:
    support_functions

 INPUTS:
    Tirific_Template =  the def file to get errors.
 OPTIONAL INPUTS:

 KEYWORD PARAMETERS:

 OUTPUTS:
     tirshaker settings
 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 EXAMPLE:

 NOTE:
'''

    
def run_tirific(current_run, work_dir = os.getcwd(),deffile = 'tirific.def' ,tirific_call= 'tirific',\
                log=False, max_ini_time = 600, verbose = True):
    log_statement = print_log(f'''Starting a tirific run
''',log)
    restart_file = f"{work_dir}/restart_Error_Shaker.txt"   
    #Get the output fits file and def file defined in workdir+ deffile
    output_deffile = load_tirific(f'{work_dir}/{deffile}', Variables = ['TIRDEF'])[0]
    # Then if already running change restart file
    restart = False
    try:
        if check_pid(current_run.pid):
            restart = True
    except:
        pass 
    if restart:
        log_statement += print_log(f'''RUN_TIRIFIC: We are using an initialized tirific in {work_dir} with the file {deffile}
''',log)

        with open(restart_file,'a') as file:
            file.write("Restarting from previous run \n")
    else:
        log_statement += print_log(f'''RUN_TIRIFIC: We are inizializing a new TiRiFiC in {work_dir} with the file {deffile}
''',log)
        with open(restart_file,'w') as file:
            file.write("Initialized a new run \n")
        current_run = subprocess.Popen([tirific_call,f"DEFFILE={deffile}","ACTION= 1"],\
                                       stdout = subprocess.PIPE, stderr = subprocess.PIPE,\
                                       cwd=work_dir,universal_newlines = True)

    currentloop =1
    max_loop = 0
    counter = 0

    current_process= psu.Process(current_run.pid)

    initialized = datetime.now()
    '''
    if Configuration['TIMING']:
        time.sleep(0.1)
        with open(f"{Configuration['LOG_DIRECTORY']}Usage_Statistics.txt",'a') as file:
            file.write(f"# TIRIFIC: Initializing Tirific at stage = {fit_type}, Loop = {Configuration['ITERATIONS']} {datetime.now()} \n")
            CPU,mem = get_usage_statistics(Configuration,current_process)
            file.write(f"{datetime.now()} CPU = {CPU} % Mem = {mem} Mb for TiRiFiC \n")
    else:
    '''
    time.sleep(0.1)

    if verbose:
        print(f"\r{'':8s}RUN_TIRIFIC: 0 % Completed", end =" ",flush = True)
    triggered = False
    for tir_out_line in current_run.stdout:
        tmp = re.split(r"[/: ]+",tir_out_line.strip())
        counter += 1
        '''
        if (counter % 50) == 0:
            if Configuration['TIMING']:
                with open(f"{Configuration['LOG_DIRECTORY']}Usage_Statistics.txt",'a') as file:
                    if tmp[0] == 'L' and not triggered:
                        if tmp[1] == '1':
                            file.write(f"# TIRIFIC: Started the actual fitting {datetime.now()} \n")
                    CPU,mem = get_usage_statistics(Configuration,current_process)
                    file.write(f"{datetime.now()} CPU = {CPU} % Mem = {mem} Mb for TiRiFiC \n")
        '''
        if tmp[0] == 'L':
            if not triggered:
                triggered = True
            if int(tmp[1]) != currentloop and verbose:
                print(f"\r{'':8s}RUN_TIRIFIC: {set_limits(float(tmp[1])-1.,0.,float(max_loop))/float(max_loop)*100.:.1f} % Completed", end =" ",flush = True)
            currentloop  = int(tmp[1])
            if max_loop == 0:
                max_loop = int(tmp[2])
 

        if tmp[0].strip() == 'Finished':
            break
        if tmp[0].strip() == 'Abort':
            break
        if not triggered:
            #Check that the initialization doesn't take to long
            check = datetime.now()
            diff = (check-initialized).total_seconds()
            if diff > max_ini_time:
                log_statement += print_log(f'''RUN_TIRIFIC: After {diff/60.} min we could not find the expected output from the tirific run. 
running in the directory = {work_dir} 
and the file deffile = {deffile}                         
''',log)
                raise TirificOutputError(f'''{diff/60.} minutes after initialization the fitting has still not started.
We were running {deffile} and failed to find the output {output_deffile}.
''')
    if verbose:
        print(f'\n')
    '''
    if Configuration['TIMING']:
        with open(f"{Configuration['LOG_DIRECTORY']}Usage_Statistics.txt",'a') as file:
            file.write(f"# TIRIFIC: Finished this run {datetime.now()} \n")
            CPU,mem = get_usage_statistics(Configuration,current_process)
            file.write(f"{datetime.now()} CPU = {CPU} % Mem = {mem} Mb for TiRiFiC \n")
    '''
    if verbose:
        print(f"{'':8s}RUN_TIRIFIC: Finished the current tirific run.")

    #The break off goes faster sometimes than the writing of the file so let's make sure it is present
    time.sleep(1.0)
    wait_counter = 0
    
    while not os.path.exists(f'{work_dir}/{output_deffile}') and wait_counter < 100.:
        time.sleep(0.3)
        wait_counter += 1
        if wait_counter/10. == int(wait_counter/10.):
            print(f"\r Waiting for {output_deffile}. \n", end = "", flush = True)
            log_statement += print_log(f'''RUN_TIRIFIC: we have waited {0.3*wait_counter} seconds for the output of tirific but it is not there yet.
''',log)
        if not  os.path.exists(output_deffile):
            log_statement += print_log(f'''RUN_TIRIFIC: After 30 seconds we could not find the expected output from the tirific run. We are raising an error for this galaxy.
''',log)
            raise TirificOutputError(f'''The tirific subprocess did not produce the correct output, most likely it crashed.
We were running {deffile} and failed to find the output  {output_deffile}.
''')
    if not log:
        return current_run
    else:
        return current_run,log_statement

run_tirific.__doc__ =f'''
 NAME:
    run_tirific

 PURPOSE:
    Check whether we have an initialized tirific if not initialize and run else restart the initialized run.

 CATEGORY:
    support_functions

 INPUTS:
    Configuration = Standard FAT configuration
    current_run = subprocess structure of tirific

 OPTIONAL INPUTS:


    fit_type = 'Undefined'
    type of fitting

    stage = 'initial'
    stage of the fitting process

    max_ini_time = 600
    maximum time it can take for tirific to initialize 
    Higher ini times take longer

 OUTPUTS:

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''



#The actual tirshaker
def tirshaker(Tirific_Template_In, log = False, directory = f'{os.getcwd()}/Error_Shaker/',\
              fit_groups=None,tmp_name_out = 'Error_Shaker_Out.def',tirific_call = 'tirific',\
              iterations = None, random_seed = None, mode = 'mad',initialization_mode = None,out_file='Shaken_Errors.def'):
    Tirific_Template= copy.deepcopy(Tirific_Template_In)
    log_statement = ''
    # Initiate rng
    if random_seed == None:
        random_seed = random.seed(891)
    if fit_groups == None:
        raise TirshakerInputError(f'You have to define the interested groups, there is no default')
    random.seed(random_seed)
    # Find the number of rings
    nur = int(Tirific_Template['NUR'])
    # Here we collect all parameter_groups as listed above and convert the lists into numbers
    '''
    # This is collecting the the actuala values for every fit group but it does not take the rings into account. 
    # Then through the parameter groups and collect the parameter_groups
    allnumbers_in = []
    for j in range(len(parameter_groups)):
        numbers = []
        # Then go through the parameter_groups
        for k in range(len(parameter_groups[j])):
            #Once we checked all we can replace para with parameter_groups and use the input without =
            numbers.append([float(l) for l in Tirific_Template[parameter_groups[j][k]].split()])
            if parameter_groups[j][k] == 'CONDISP':
                pass
            else:
                while len(numbers[-1]) < nur:
                    numbers[-1].append(numbers[-1][-1])

        allnumbers_in.append(numbers)

    allnumbers_out = []
    '''
    #Make sure some settings are blank
   
    Tirific_Template['OUTSET'] = ''
    Tirific_Template['PROGRESSLOG'] = ''
    Tirific_Template['TEXTLOG'] = ''
    Tirific_Template['TIRSMO'] = ''
    Tirific_Template['COOLGAL'] = ''
    Tirific_Template['TILT'] = ''
    Tirific_Template['BIGTILT'] = ''
    if initialization_mode == None:
        if nur < 15:
            Tirific_Template['INIMODE'] = 2
        else:
            Tirific_Template['INIMODE'] = 3
    else:
        Tirific_Template['INIMODE'] = initialization_mode

    Tirific_Template['LOGNAME'] = 'Error_Shaker.log'
    Tirific_Template['TIRDEF'] = tmp_name_out
    current_run='not set'
    fit_groups['TO_COLLECT'] = []
    fit_groups['COLLECTED'] = {}
    for group in  fit_groups:
        if group not in ['COLLECTED','TO_COLLECT']:
            for disk in fit_groups[group]['DISKS']:
                para = group.split('_')[0]
                if disk != 1:
                    para = f'{para}_{disk}'
                if para not in  fit_groups['TO_COLLECT']:
                    fit_groups['TO_COLLECT'].append(para)
                fit_groups['COLLECTED'][para] = []
    for i in range(iterations):
        Current_Template = copy.deepcopy(Tirific_Template)
        Current_Template['RESTARTID']= i
        # Provide some info where we are
        log_statement += print_log(f'''
        ******************************
        ******************************
        *** Tirshaker iteration {i:02d} ***
        ******************************
        ******************************
''',log)
        #Looping through all block
        for group in  fit_groups:
            if group not in ['COLLECTED','TO_COLLECT']:
                if fit_groups[group]['BLOCK']:
                    #If a block use the same variation for all rings in the groups
                    variations = [fit_groups[group]['VARIATION'][0]*random.uniform(-1.,1.)]\
                        *(fit_groups[group]['RINGS'][1]-fit_groups[group]['RINGS'][0]+1)
                else:
                    #If not a block use a different variation for all rings in the groups
                    variations = [fit_groups[group]['VARIATION'][0]*random.uniform(-1.,1.) for x \
                                in range(fit_groups[group]['RINGS'][0],fit_groups[group]['RINGS'][1]+1)]

                for disk in fit_groups[group]['DISKS']:
                    para = group.split('_')[0]
                    if disk != 1:
                        para = f'{para}_{disk}'
                    current_list = [float(x) for x in Current_Template[para].split()]
                    while len(current_list) < nur:
                        current_list.append(current_list[-1])
                    for l in range(fit_groups[group]['RINGS'][0],fit_groups[group]['RINGS'][1]+1):
                        if fit_groups[group]['VARIATION'][1] == 'a':
                            current_list[int(l-1)] += variations[int(l-fit_groups[group]['RINGS'][0])]
                        else:
                            current_list[int(l-1)] *= (1+variations[int(l-fit_groups[group]['RINGS'][0])])
                    format = set_format(para)
                    Current_Template[para] = ' '.join([f'{x:{format}}' for x in current_list])
        write_tirific(Current_Template, name =f'{directory}/Error_Shaker_In.def',full_name= True )
       
        current_run = run_tirific(current_run,deffile='Error_Shaker_In.def',work_dir = directory,tirific_call=tirific_call, \
                                max_ini_time= int(300*(int(Tirific_Template['INIMODE'])+1)))
     
        # Read the values of the pararameter groups
        for parameter in fit_groups['TO_COLLECT']:
            fit_groups['COLLECTED'][parameter].append(load_tirific(f"{directory}/{tmp_name_out}",\
                    Variables = [parameter],array=True))
   
    fit_groups['FINAL_ERR'] = {}     
    for parameter in fit_groups['TO_COLLECT']:
        print(f'Processing {parameter}')
        all_iterations = np.array(fit_groups['COLLECTED'][parameter],dtype=float)
        fit_groups['FINAL_ERR'][parameter] = np.zeros(all_iterations[0].size) 
        for ring in range(all_iterations[0].size):
            all_its = all_iterations[:,ring]
            
            if mode == 'mad':
                median = np.median(all_its)
                mad = stats.median_abs_deviation(all_its)
                madsigma = stats.median_abs_deviation(all_its) 
                average = np.average(all_its) 
                # Wow, np.std is the standard deviation using N and not N-1 in the denominator. So one has to use
                #std = np.sqrt(float(len(allparamsturned[j][k][l]))/float(len(allparamsturned[j][k][l])-1))*np.std(np.array(allparamsturned[j][k][l]))  
                std = np.std(all_its,ddof=1)     
                final = stats.tmean(all_its, (median-3*madsigma, median+3*madsigma))
                final_err =  stats.tstd(all_its, (median-3*madsigma, median+3*madsigma))
                fit_groups['FINAL_ERR'][parameter][ring] = final_err
                log_statement += print_log(f'TIRSHAKER: Parameter: {parameter} Ring: {ring} Pure average+-std: {average:.3e}+-{std:.3e} Median+-madsigma: {median:.3e}+-{madsigma:.3e} Average+-sigma filtered: {final:.3e}+-{final_err:.3e} \n')
    print(fit_groups['FINAL_ERR'])
    '''madsigma = stats.median_abs_deviation(
    for group in fit_groups:
        for disk in fit_groups[group]['DISKS']: 

    # Calculate mean and error
    allnumbers_final = []
    allnumbers_final_err = []
    for j in range(len(allnumbers_in)):
        allnumbers_final.append([])
        allnumbers_final_err.append([])
        for k in range(len(allnumbers_in[j])):
            allnumbers_final[j].append([])
            allnumbers_final_err[j].append([])
            for l in range(len(allnumbers_in[j][k])):
                # Attempt to use mad statistics for this
                if mode == 'mad':

                    median = np.median(np.array(allparamsturned[j][k][l]))
#                    mad = stats.median_absolute_deviation(np.array(allparamsturned[j][k][l]))
                    # Careful! This involves a scaling by 1.4826 by default as the default scale = 1.4826
                    madsigma = stats.median_abs_deviation(np.array(allparamsturned[j][k][l]))
                    average = np.average(np.array(allparamsturned[j][k][l]))
                    # Wow, np.std is the standard deviation using N and not N-1 in the denominator. So one has to use
                    std = np.sqrt(float(len(allparamsturned[j][k][l]))/float(len(allparamsturned[j][k][l])-1))*np.std(np.array(allparamsturned[j][k][l]))
                    allnumbers_final[j][k].append(stats.tmean(np.array(allparamsturned[j][k][l]), (median-3*madsigma, median+3*madsigma)))
                    allnumbers_final_err[j][k].append(stats.tstd(np.array(allparamsturned[j][k][l]), (median-3*madsigma, median+3*madsigma)))
                    log_statement += print_log('TIRSHAKER: Parameter: {:s} Ring: {:d} Pure average+-std: {:.3e}+-{:.3e} Median+-madsigma: {:.3e}+-{:.3e} Average+-sigma filtered: {:.3e}+-{:.3e} \n'.format(\
                                parameter_groups[j][k], l+1, average, std, median, madsigma, allnumbers_final[j][k][-1], allnumbers_final_err[j][k][-1])\
                                ,log)
                else:
                    allnumbers_final[j][k].append(np.average(np.array(allparamsturned[j][k][l])))
                    allnumbers_final_err[j][k].append(np.sqrt(float(len(allparamsturned[j][k][l]))/float(len(allparamsturned[j][k][l])-1))*np.std(np.array(allparamsturned[j][k][l])))
    '''

    for parameter in fit_groups['TO_COLLECT']:
        print(parameter)
        format = set_format(parameter)
        Tirific_Template.insert(f'{parameter}',f'# {parameter}_ERR',f"{' '.join([f'{x:{format}}' for x in fit_groups['FINAL_ERR'][parameter]])}") 
        print(Tirific_Template[f'# {parameter}_ERR'])       
    # Put them into the output file
    # Write it to a copy of the file replacing the parameters


    log_statement += finish_current_run(current_run,log=log)
    write_tirific(Tirific_Template, name = f'{directory}/{out_file}',full_name=True)
    print(f'{directory}/{out_file}')
    return log_statement
  
   
tirshaker.__doc__ =f'''
 NAME:
    tirshaker

 PURPOSE:
    obtain errors through a FAT implemention of tirshaker developed by G.I.G. Jozsa.

 CATEGORY:
    run_functions

 INPUTS:
    Configuration = Standard FAT configuration
    outfileprefix (str)                    : Prefix to output parameters in outfilename
    parameter_groups (list of lists of str): List of parameters (parameter groups) that will be changed simultaneously
    rings (list of list of int)            : Ring numbers to be changed in parameter groups, starting at 1
    block (list of bool)                   : Change all rings by the same value (if True) or single rings (False). If the latter, the same ring for different parameters is changed by the same value
    variation (list of float)              : Amplitude of variation
    variation_type (list of str)           : Type of variation, 'a' for absolute, 'r' for relative
    iterations (int)                       : Number of re-runs
    random_seed (int)                      : Seed for random generator
    mode (str)                             : If 'mad' implements an outlier rejection.

 OPTIONAL INPUTS:


 OUTPUTS:

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
 This is a re-imaged version of the code developed by G.I.G. Jozsa found at  https://github.com/gigjozsa/tirshaker.git

 Takes a tirific def file filename and varies it iterations times
 and runs it as many times to then calculate the mean and the
 standard deviation of parameters that have been varied, both are
 put into the tirific deffile outfilename.

 With parameter_groups parameter groups are defined that are varied
 homogeneously. This is a list of list of parameter names including
 the '='-sign.  Caution! At this stage it is essential that in the
 .def file there is the '='-sign directly attached to the parameter
 names and that there is a space between parameter values and the
 '='.

 For each parameter group (list of parameter names), the values of
 the rings specified in rings (which is a list of integers, the
 list member corresponding to the parameter with the same index in
 parameter_groups) are varied. Block is a list of indicators if the
 values should be varied by ring (similar to the !-sign in the VARY
 parameter of tirific) or as a whole, again indices indicating the
 associated parameter group. Variation quantifies the maximum
 variation of the parameter (again indices matching), with
 variation type (indices matching) 'a' indicating an absolute
 variation, 'r' indicating a relative one. Parameters are varied by
 a uniform variation with maximal amplitude variation. So if a
 parameter is x and v the variation, the parameter gets changed by
 a number between -v and v in case the matching variation type is
 'a' and it gets changed by a number between -v*x and v*x if the
 matching variation type is 'r'. Tirific is started iterations
 times with varied input parameters but otherwise identical
 parameters (except for output files which are suppressed) and the
 results are recorded. For each varied parameter the mean and
 standard deviation is calculated and returned in the output .def
 file outfilename. In outfilename LOOPS is set to 0 and any output
 parameter is preceded by a prefix outfileprefix. Random_seed is
 the random seed to make the process deterministic. If mode ==
 'mad', the median and the MAD is calculated and, based on that,
 values beyond a 3-sigma (sigma estimated from MAD) bracket around
 the median are rejected before calculating mean and standard
 deviation.

'''

# This functions sets up the defirent parameters that are needed for tirshaker call
def run_tirshaker(cfg, log=False):
    log_statement = ''
    #Read in the deffile
    Tirific_Template = tirific_template(filename=f'{cfg.general.directory}/{cfg.tirshaker.deffile_in}')
    # First we make a directory to keep all contained
    if not os.path.isdir(f'{cfg.general.directory}/{cfg.tirshaker.directory}/'):
        os.mkdir(f'{cfg.general.directory}/{cfg.tirshaker.directory}/')

    #Change the name and run only 2 LOOPS
    Tirific_Template['RESTARTNAME']= f"restart_Error_Shaker.txt"
   
    if cfg.tirshaker.individual_loops == -1:
        pass
    else:
        Tirific_Template['LOOPS'] = cfg.tirshaker.individual_loops
     #Some parameters are stripped by tirific so to make sure they are always there we add theif not present
    if 'GR_CONT' not in Tirific_Template:
        Tirific_Template['GR_CONT']=' '
    if 'RESTARTID' not in Tirific_Template:
        Tirific_Template['RESTARTID'] = '0'
    
    #Determine the error block from the  fit settings.
    if cfg.tirshaker.mode == 'fitted':
        fit_groups = get_fitted_groups(Tirific_Template)
    elif cfg.tirshaker.mode == 'manual':
        fit_groups = get_manual_groups(cfg, rings = int(Tirific_Template['NUR']),\
                            cube_name = Tirific_Template['INSET'])
    else:
        log_statement += print_log(f'''RUN_TIRSHAKER: The Tirshaker mode {cfg.tirshaker.mode} is not yet fully functional. Please use a different mode
''',log)
        raise TirshakerInputError(f'''RUN_TIRSHAKER: The Tirshaker mode {cfg.tirshaker.mode} is not yet fully functional. Please use a different mode
''')
    # Only change the inset after extracting all info
    Tirific_Template['INSET'] = f"../{Tirific_Template['INSET']}"
    out = [f'Parameter = {x} with block = {fit_groups[x]["BLOCK"]} for the rings {fit_groups[x]["RINGS"]} and disks {fit_groups[x]["DISKS"]} varied by {fit_groups[x]["VARIATION"][0]}. \n' for x in fit_groups ]
    log_statement += print_log(f'''RUN_TIRSHAKER: We are shaking with the following parameters:
{''.join(out)}
''',log)
    

                                    
    log_statement += tirshaker(Tirific_Template, log = log, directory = f'{cfg.general.directory}/{cfg.tirshaker.directory}',\
            fit_groups =fit_groups ,tirific_call = cfg.tirshaker.tirific,\
            iterations = cfg.tirshaker.iterations, \
            mode = 'mad',initialization_mode= cfg.tirshaker.inimode,out_file=cfg.tirshaker.deffile_out)
 
    