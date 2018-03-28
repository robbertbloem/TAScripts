"""
mess is a 6D array:
0: n_cycles: number of times all configurations have been measured. 
1: n_config: number of configurations, loaded before the measurement.
2: n_states: number of DI states, for example the chopper.
3: n_frames: unless all frames are stored and imported, this is 1.
4: n_ypixels: y axis. Usually 8 pixels or so. 
5: n_xpixels: spectrometer axis. 


"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import imp

import os

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import TAScripts.Resources.ClassTools as CT

import TAScripts.Resources.ReadMeasurement as RM

imp.reload(RM)

class TA_Measurement(CT.ClassTools):

    def __init__(self, path = "", date = "", time = "", basename = ""):
        
        # normalize path, use OS-appropriate separator
        if path[-1] != os.sep:
            path += os.sep
    
        self.path = path
        self.date = date
        self.time = time
        self.basename = basename
        
        basefilename = "{:s}_{:s}_{:s}".format(date, time, basename)

        basepath ="{:s}{:s}{:s}{:s}{:s}".format(path, date, os.sep, basefilename, os.sep)
        
        self.filedict = {"path": path, "date": date, "time": time, "basename": basename, "basepath": basepath, "basefilename": basefilename}
        

    def import_data(self, all_frames = False):
        self.mess, metadata = RM.import_TA_measurement(self.filedict, all_frames)
        self.extract_metadata(metadata)


    def extract_metadata(self, metadata):

        self.notes = metadata["Notes"]
        self.file_version = metadata["FileVersion"]
        self.n_cycles = metadata["n_cycles"]
        self.n_config = metadata["n_config"]
        self.n_states = metadata["n_states"]
        self.n_frames = metadata["n_frames"]
        self.n_spectrometer = len(metadata["spectrometer_axis"])
        self.n_xpix = metadata["n_xpix"]
        self.n_ypix = metadata["n_ypix"]
        self.n_shots = metadata["n_shots"]
        self.spectrometer_axis = metadata["spectrometer_axis"]
        



    def average_cycles(self):

        new_mess = numpy.zeros((1, self.n_config, self.n_states, self.n_frames, self.n_ypix, self.n_xpix))
        new_mess[0,:,:,:,:,:] = numpy.average(self.mess, axis = 0)
        self.mess = new_mess
        self.n_cycles = 1

    def average_frames(self):

        new_mess = numpy.zeros((self.n_cycles, self.n_config, self.n_states, 1, self.n_ypix, self.n_xpix))
        new_mess[:,:,:,0,:,:] = numpy.average(self.mess, axis = 3)
        self.mess = new_mess
        self.n_frames = 1


    def average_y_pixels(self):

        new_mess = numpy.zeros((self.n_cycles, self.n_config, self.n_states, self.n_frames, 1, self.n_xpix))
        new_mess[:,:,:,:,0,:] = numpy.average(self.mess, axis = 4)
        self.mess = new_mess
        self.n_ypix = 1




#     def plot_data(self, ax, wl_range):
        




if __name__ == "__main__": 
    
    path = "/Users/rbloem/Developer/TAScripts/Tests/TestData/20180216_143515_MyMeasurement" 
    fiets = TAMeasurement(path)

    fiets.import_data()
    print(fiets)
    fiets.average_cycles()
    print(fiets)
    fiets.average_y_pixels()
    print(fiets)
    
    plt.plot(fiets.mess[0,0,0,0,0,:])
    plt.plot(fiets.mess[0,0,1,0,0,:])
    plt.show()
#     
#     print(fiets)