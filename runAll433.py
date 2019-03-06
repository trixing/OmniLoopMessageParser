# runAll LoopReportFiles in the associated folder
from analyzeMessageLogs import *
from get_file_list import *

filePath = 'm:/SharedFiles/LoopReportFiles'
outFile = 'm:/SharedFiles/LoopReportPythonAnalysis/output_master.csv'
fileDateList = get_file_list(filePath)

verboseFlag =  0   # if this is 1 then more print stmts
numRowsBeg  =  0   # if >0, print this many messages from beginning of record
numRowsEnd  =  0   # if >0, print this many messages from end of record

count=0
for row in fileDateList:
    thisFile = row[0]
    (thisPerson, thisFinish, thisAntenna) = parse_info_from_filename(thisFile)
    if thisAntenna != '433MHz':
        print('    Skipping : ', thisFile)
        continue
    print('Processing: ', thisFile)
    analyzeMessageLogs(filePath, thisFile, outFile, verboseFlag, numRowsBeg, numRowsEnd)
    count += 1

print('Completed running', count,'files')
