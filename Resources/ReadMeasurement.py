"""
mess is a 6D array:
0: n_cycles: number of times all configurations have been measured. 
1: n_config: number of configurations, loaded before the measurement.
2: n_states: number of DI states, for example the chopper.
3: n_frames: unless all frames are stored and imported, this is 1.
4: n_ypixels: y axis. Usually 8 pixels or so. 
5: n_xpixels: spectrometer axis. 


test change
"""
import imp

import os

import numpy

import TAScripts.Resources.CSVReader as CSV
import TAScripts.Resources.TiffReader as TIFF
import TAScripts.Resources.XMLReader as XMLR

imp.reload(CSV)
imp.reload(TIFF)
imp.reload(XMLR)

def cleanup_log_csv(csv_dict):

    n_config = 0
    config_temp = []
    n_cycles = 0
    
    none_row = []
    for r in range(len(csv_dict)):
        if csv_dict[r]["image"] == None:
            none_row.append(r)

    for r in range(len(none_row)):
         del(csv_dict[none_row[r]])                

    for row in csv_dict:
        row["cycle"] = int(row["cycle"])
        if row["cycle"] > n_cycles:
            n_cycles = row["cycle"]
        
        row["confignr"] = int(row["confignr"])
        if row["confignr"] not in config_temp:
            config_temp.append(row["confignr"])
            n_config += 1
        
        if "delay_fs" in row:
            row["delay_unit"] = "fs"
            row["delay"] = row.pop("delay_fs")
        elif "delay_ps" in row:
            row["delay_unit"] = "ps"
            row["delay"] = row.pop("delay_ps")
        row["delay"] = float(row["delay"])
        
        if "wavelength_nm" in row:
            row["wavelength_unit"] = "nm"
            row["wavelength"] = row.pop("wavelength_nm")
        row["wavelength"] = float(row["wavelength"])
        
        row["n_shots"] = int(row["n_shots"])
        
        row["image"] = row["image"].split()

        
    return csv_dict, n_config, n_cycles




def cleanup_config_csv(csv_dict, metadata):

    
    metadata["n_config"] = len(csv_dict)
    
    # make a dictionary for all configurations
    metadata["configs"] = [{}] * metadata["n_config"]
    
    
    if "delay_fs" in csv_dict[0]:
        metadata["delay_unit"] = "fs"
    elif "delay_ps" in csv_dict[0]:
        metadata["delay_unit"] = "ps"

    if "wavelength_nm" in csv_dict[0]:
        metadata["wavelength_unit"] = "nm"

    
    
    for r in range(len(csv_dict)):
        
        
        
        if "delay_fs" in csv_dict[r]:
            metadata["configs"][r]["delay"] = float(csv_dict[r]["delay_fs"])
        elif "delay_ps" in csv_dict[r]:
            metadata["configs"][r]["delay"] = float(csv_dict[r]["delay_ps"])

        if "wavelength_nm" in csv_dict[r]:
            metadata["configs"][r]["center_wavelength"] = float(csv_dict[r]["wavelength_nm"])
            
        metadata["configs"][r]["n_shots"] = float(csv_dict[r]["n_shots"])



    
    print(metadata)
    
    return metadata
        
 
    
    
    # 
#     config_temp = []
#     n_cycles = 0
#     
#     none_row = []
#     for r in range(len(csv_dict)):
#         if csv_dict[r]["image"] == None:
#             none_row.append(r)
# 
#     for r in range(len(none_row)):
#          del(csv_dict[none_row[r]])                
# 
#     for row in csv_dict:
#         row["cycle"] = int(row["cycle"])
#         if row["cycle"] > n_cycles:
#             n_cycles = row["cycle"]
#         
#         row["confignr"] = int(row["confignr"])
#         if row["confignr"] not in config_temp:
#             config_temp.append(row["confignr"])
#             n_config += 1
#         
#         if "delay_fs" in row:
#             row["delay_unit"] = "fs"
#             row["delay"] = row.pop("delay_fs")
#         elif "delay_ps" in row:
#             row["delay_unit"] = "ps"
#             row["delay"] = row.pop("delay_ps")
#         row["delay"] = float(row["delay"])
#         
#         if "wavelength_nm" in row:
#             row["wavelength_unit"] = "nm"
#             row["wavelength"] = row.pop("wavelength_nm")
#         row["wavelength"] = float(row["wavelength"])
#         
#         row["n_shots"] = int(row["n_shots"])
#         
#         row["image"] = row["image"].split()
# 
#         
#     return csv_dict, n_config, n_cycles


def import_TA_measurement(filedict, all_frames = False, n_cycles_cheat = -1):
    
    # import XML file 
    paf = filedict["basepath"] + filedict["basefilename"] + ".xml"
    XML = XMLR.XMLReader(paf)
    metadata = XML.get_TA_metadata()
    
    metadata["axes"] = [0] * 6
    metadata["axes_units"] = [0] * 6

    # import configurations
    paf = filedict["basepath"] + filedict["basefilename"] + "_configuration.csv"
    configurations = CSV.CSVReader(paf).read_csv()    
    metadata = cleanup_config_csv(configurations, metadata)

    # import log file with all executed steps
    paf = filedict["basepath"] + filedict["basefilename"] + "_execution_log.csv"
    mess_details = CSV.CSVReader(paf).read_csv()    
    mess_details, n_config, n_cycles = cleanup_log_csv(mess_details)
    
    if n_cycles_cheat > 0:
        n_cycles = n_cycles_cheat
    
    
    n_states = len(mess_details[0]["image"])
    metadata["n_cycles"] = n_cycles
    metadata["n_config"] = n_config
    metadata["n_states"] = n_states
    metadata["n_shots"] = mess_details[0]["n_shots"]
 
    if all_frames:
        n_frames = int(metadata["n_shots"] / n_states)
    else:
        n_frames = 1   
    metadata["n_frames"] = n_frames

    # import spectrometer axis
    paf = filedict["basepath"] + filedict["basefilename"] + "_vis_calibration.csv"
    xaxis = numpy.loadtxt(paf, delimiter = ",", skiprows = 1)[:,1]
    metadata["spectrometer_axis"] = xaxis


    # determine shape of the data
    paf = filedict["basepath"] + mess_details[0]["image"][0]
    temp = TIFF.TiffReader(paf)
    shape = temp.get_shape()

    metadata["n_ypix"] = shape[0]
    metadata["n_xpix"] = shape[1]
    
#     print(metadata)

    mess = numpy.zeros((n_cycles, n_config, n_states, n_frames, metadata["n_ypix"], metadata["n_xpix"]))

    if all_frames:

        for cycle in range(n_cycles):   
            for config in range(n_config):     
                cyco = cycle * n_config + config
                       
#                 print(cycle, config, cyco)

                # import states
                paf = filedict["basepath"] + "AllDigitizerData" + os.sep + filedict["basefilename"] + "_Digitizer_" + str(cycle+1) + "_1.csv"
                states = numpy.loadtxt(paf, delimiter = ",", skiprows = 1, usecols = 0)
                
                # no idea why this is saved as state == 1
                state = 1
                filename = mess_details[cyco]["image"][state][:-7] + ".tiff"
                paf = filedict["basepath"] + "AllFrames" + os.sep + filename

                temp = TIFF.TiffReader(paf)
        
                state = 0    
                idx = numpy.where(states == 0)[0]         
                mess[cycle, config, state, :, :, :] = temp.get_image(index = idx)
                
                state = 1  
                idx = numpy.where(states > 0)[0]            
                mess[cycle, config, state, :, :, :] = temp.get_image(index = idx)
  
    
    else:
    
        for cycle in range(n_cycles):   
            for config in range(n_config):     
                cyco = cycle * n_config + config
                for state in range(n_states):
            
#                     print(cycle, config, cyco, state)

                    paf = filedict["basepath"] + mess_details[cyco]["image"][state]    
#                     print(paf)        
                    temp = TIFF.TiffReader(paf)
                    mess[cycle, config, state, 0, :, :] = temp.get_image()
        
    return mess, metadata
                

    





if __name__ == '__main__':

    path = "/Users/rbloem/Developer/TAScripts/Tests/TestData/20180216_143515_MyMeasurement"

    import_TA_measurement(path)