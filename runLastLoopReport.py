# run the most recent file and append to master csv
from main import *
from get_file_list import *
from getAnalysisIO import *

vFlag = 4
filePath, outFile = getAnalysisIO(1,vFlag)
fileDateList = get_file_list(filePath)

## Rev3 analysis
main(filePath, fileDateList[-1][0], outFile, vFlag)
