# run the most recent file and append to master csv
from main import main
from fileio.get_file_list import get_file_list, getFileDict
from fileio.getAnalysisIO import getAnalysisIO

pathOption = 1  # use standard file location
loopType = 'FX'  # FreeAPS X
vFlag = 4  # Verbose output - all files to Output location
macFlag = 0  # 0 = use Drobo; 1 use Mac hard drive

folderPath, outFlag = getAnalysisIO(pathOption, loopType, vFlag, macFlag)
fileDateList = get_file_list(folderPath)

# create fileDict
fileDict = getFileDict(folderPath, fileDateList[-1][0], loopType)

# nominal verbose output
main(fileDict, outFlag, vFlag)
