"""
Read the configuration csv files. 
For the spectrometer axis and digitizer states, use numpy.loadtxt. 
"""

import csv

import numpy
import matplotlib 
import matplotlib.pyplot as plt


        

class CSVReader():
    
    def __init__(self, paf):
        self.paf = paf
        
    def read_csv(self):
        
        csv.register_dialect("skipspace", delimiter = ",", skipinitialspace = True)
        
        with open(self.paf) as csvfile:
            reader = csv.DictReader(csvfile, dialect = "skipspace")
            
            out = []
            for row in reader:
                out.append(dict(row))
                
        return out
                
            




if __name__ == "__main__": 
    paf = "/Users/rbloem/Developer/TAScripts/Tests/TestData/20180216_143515_MyMeasurement/Executed steps.csv"
    
    mess_details = CSVReader(paf).read_csv()
    
#     mess_details = CSV.read_csv()
    
    for row in mess_details:
        print(row)
    