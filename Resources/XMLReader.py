"""

"""

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET

class XMLReader():  

    def __init__(self, paf):    
        
        self.paf = paf
        self.tree = ET.parse(self.paf)
        self.root = self.tree.getroot()
        
    def get_root(self):
        return self.root
        
    def get_TA_metadata(self):
        
        metadata = {}
    
        for child in self.root:
            
            if child.tag == "FileVersion":
                metadata["FileVersion"] = int(child.text)
        
        
            if child.tag == "MetaData":
                for subchild in child:
                    metadata[subchild.tag] = subchild.text
            
        return metadata






if __name__ == "__main__": 
    paf = "/Users/rbloem/Developer/TAScripts/Tests/TestData/20180216_143515_MyMeasurement/20180216_143515_MyMeasurement.copy.xml"
    
    reader = XMLReader(paf)
    
    metadata = reader.get_TA_metadata()
    
    print(metadata)