import pandas as pd
from messageLogs_functions import *
from byteUtils import *
from podStateAnalysis import *
from messagePatternParsing import *

def analyzeMessageLogsNew(thisPath, thisFile, outFile, verboseFlag, numRowsBeg, numRowsEnd):

    # This is time (sec) radio on Pod stays awake once comm is initiated
    radio_on_time   = 30

    filename = thisPath + '/' + thisFile
    if verboseFlag:
        print('File relative path:', thisFile)
        print('File absolute path:', filename)

    # read the MessageLogs from the file
    commands = read_file(filename)

    # add more stuff and return as a DataFrame
    df = generate_table(commands, radio_on_time)
    # add a time_delta column
    df['timeDelta'] = (df['time']-df['time'].shift()).dt.seconds.fillna(0).astype(float)

    if numRowsBeg>0:
        headList = df.head(numRowsBeg)
        print(headList)

    if numRowsEnd>0:
        tailList = df.tail(numRowsEnd)
        print(tailList)

    # set up a few reportable values here from df, time is in UTC
    first_command = df.iloc[0]['time']
    last_command = df.iloc[-1]['time']
    send_receive_commands = df.groupby(['type']).size()
    number_of_messages = len(df)
    thisPerson, thisFinish, thisAntenna = parse_info_from_filename(thisFile)
    lastDate = last_command.date()
    lastTime = last_command.time()

    # print out summary information to command window
    print('__________________________________________\n')
    print(f' Summary for {thisFile} with {thisFinish} ending')
    print('  There were a total of {:d} messages in the log'.format(len(df)))

    # Process the dataframes and update the pod state
    # First get the pair and insert frames
    minPodProgress = 0
    maxPodProgress = 8
    podInit, emptyMessageList = getPodState(df, minPodProgress, maxPodProgress)
    setUpPodCommands = podInit[podInit.message_type=='0x3']
    numberOfSetUpPodCommands = len(setUpPodCommands)
    print('\n  Pod was initialized with {:d} messages, {:d} SetUp (0x03) required'.format(len(podInit), \
       numberOfSetUpPodCommands))
    if emptyMessageList:
        print('    ***  Detected {:d} empty message(s) while initializing the pod'.format(len(emptyMessageList)))
        print('    ***  indices:', emptyMessageList)

    # use a common function to configure requestDict, otherDict
    requestDict, otherDict = getHandledRequests()

    # Iterate through the podState to determine successful commands for requestDict
    podInitSuccessfulActions, podInitOtherMessages = getPodSuccessfulActions(podInit)

    doThePrintRequest(requestDict, podInitSuccessfulActions)

    # Now get the rest of the pod states while in pod_progress 8 and beyond
    minPodProgress = 8
    maxPodProgress = 15
    podRun, emptyMessageList = getPodState(df, minPodProgress, maxPodProgress)
    print('\n  Pod run (pod_progress>=8) included {:d} messages'.format(len(podRun)))
    if emptyMessageList:
        print('    ***  Detected {:d} empty message(s) while running the pod'.format(len(emptyMessageList)))
        print('    ***  indices:', emptyMessageList)

    # Iterate through the podState to determine successful commands for requestDict
    podSuccessfulActions, podOtherMessages = getPodSuccessfulActions(podRun)
    doThePrintRequest(requestDict, podSuccessfulActions)

    # add other analysis here  like TB timing etc

    print('Insulin delivered   : {:6.2f} u'.format(podRun.iloc[-1]['total_insulin']))

    # see if there is a fault
    faultRow = df[df.command=='02']
    if len(faultRow):
        msg = faultRow.iloc[0]['raw_value']
        pmsg = processMsg(msg)
        printDict(pmsg)

    print('\nReport other message types during pod run')
    doThePrintOther(otherDict, podOtherMessages)

    print('\nReport other message types during pod init')
    doThePrintOther(otherDict, podInitOtherMessages)

    return df, podInit, podRun
