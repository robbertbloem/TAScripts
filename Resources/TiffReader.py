from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import numpy

from skimage import io

class TiffReader():
    __images__ = None

    def __init__(self, paf):
        self.__images__ = io.imread(paf)
        
        if len(numpy.shape(self.__images__)) == 2:
            self.frames = False
        else:
            self.frames = True
        

    def get_shape(self):    
        if numpy.all(self.__images__ == None):   
            return (0,0,0)  
        else:
            return self.__images__.shape

    def get_type(self):
        return self.__images__.dtype

    def get_image(self, index = 0):
        if self.frames:
            return numpy.array(self.__images__[index])
        else:
            return numpy.array(self.__images__)











if __name__ == '__main__':

    file = "/Users/rbloem/Developer/TAScripts/Tests/TestData/20180216_143515_MyMeasurement/Frame_Visible_1_1_0.tiff"
    
#     file = "/Users/rbloem/Developer/TAScripts/Temp/TiffStack/Frame_Visible_1_1_0.tiff"
    
#     file = "/Users/rbloem/Developer/TAScripts/Temp/TiffStack/DEBUG_vis_Frames_1_1.tiff"
    
    index = 0

    reader = TiffReader(file)
    


    shape = reader.get_shape()
    print(shape)

    data_type = reader.get_type()
    print(data_type)

    tiff_499 = reader.get_image(index)
    print(tiff_499)
    

    

#----------------------------------------------------------------------------------------------------

