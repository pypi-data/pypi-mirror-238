import pandas as pd
import numpy as np
import copy
import datetime
import sqlite3
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.results as res
from biogemeutilities.filenames import getNewFileNameOverwriteOption, selectFileName
from biogemeutilities.statistics import StringNoneToList, CleanDataKeepDropVar, DescriptiveStatistics
from biogemeutilities.database import getBioDraws, exportBioDraws, exportBioData, exportDescriptiveStatistics





  

def addVarFromDataframe(allResults, dataframe, addVar=None):
    
    # Makes sure that the addVar-input is a list (in case the user specified a single variable as a string or None)
    addVar = StringNoneToList(addVar)
    
    # Make a hard copy of the dataframe which only contains the variables the user have specified should be added
    AddData = dataframe[addVar].copy(deep=True)
    
    # Drop columns which already exists in the target dataframe
    AddData = AddData.drop(list(allResults.columns), axis=1, errors='ignore')
    
    # Left join based on the row-index, i.e 0-len(df)
    allResults_AddData = allResults.join(AddData)
    
    return allResults_AddData







# getUsedVariable
def usedVariable(biogemeObject):
    return 'Function not implemented yet'  













'''
--------------------------------------------------------------------------------------------------------------------------------------

  ______     ___       __       __  .______   .______          ___   .___________. _______ 
 /      |   /   \     |  |     |  | |   _  \  |   _  \        /   \  |           ||   ____|
|  ,----'  /  ^  \    |  |     |  | |  |_)  | |  |_)  |      /  ^  \ `---|  |----`|  |__   
|  |      /  /_\  \   |  |     |  | |   _  <  |      /      /  /_\  \    |  |     |   __|  
|  `----./  _____  \  |  `----.|  | |  |_)  | |  |\  \----./  _____  \   |  |     |  |____ 
 \______/__/     \__\ |_______||__| |______/  | _| `._____/__/     \__\  |__|     |_______|
                                                                                           

--------------------------------------------------------------------------------------------------------------------------------------
'''


def calibrate(biogemeObject, 
              calibrationSettings,
              betas, 
              betasSensitivity=None, 
              maxiter=100, 
              threshold = 0.001, 
              alpha=1, 
              plotCalibration=True, 
              ExportCalibrationLog=False, 
              ExportCalibrationExcel=False, 
              ExportCalibrationPlot=False, 
              plotDPI=200, 
              OutputFilename=None, 
              overwriteOutput=False):
    '''
    This method is used to calibrate estimated parameters (in particular alternative specific constant, aka ASC or intercepts) so that the model reproduces actual market shares (instead of sample shares)
    

    Parameters
    ----------

    biogemeObject : biogemeObject
        A biogemeObject.
    calibrationParameters : Dict
        Dict containing sub-dict for each parameter (ASC) to be calibrated with a correspond expression for the probability. 
        Should take the form of:
        
            calibrationParameters = {'ASC_TRAIN': {'prob': 'Prob. train', 'target': 0.20},
                                     'ASC_CAR'  : {'prob': 'Prob. car'  , 'target': 0.40}
                                     ...
                                     ...
                                     ...
                                     }
            where:
                - 'ASC_TRAIN' and 'ASC_CAR' are the names of the parameters (ASCs) to be calibrated
                - 'Prob. train' and 'Prob. train' refers to expression in the biogeme object containing the alternative probabilities for the respective parameters to be calibrated
                - 0.20 and 0.40 are the probabilities used to calibrate against. 
            
    betas : Dict
        Dict containing estimated parameter values.
    betasSensitivity : List, optional
        List in which each element contains a dict with parameters values drawn from the 'getBetasForSensitivityAnalysis'-function in Biogeme
    maxiter : Integer or None, optional
        Specifies an upper limit to the number of iterations for calibrating the parameters. If set to 0 or None then this is disregarded and no upper limit is defined. The default is 100.
    threshold : Float or None, optional
        Specifies the precision threshold to terminate the calibration loop. If set to -1 or None then this is disregarded and the algorith will keep looping until maxiter is reached. The default is 0.001 (equavilent to to 0.1%).
    alpha : Float or Interger, optional
        Calibration rate. The default is 1.
    plotCalibration : Boolean, optional
        If True, plots the conversion of predicted probabilities as a function of number of iteratinos. The default is True.
    ExportCalibrationLog : Boolean or string, optional
        If True, dumps a .log-file. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
    ExportCalibrationExcel : Boolean, optional
        If True, dumps a .xlsx-file. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
    ExportCalibrationPlot : Boolean, optional
        If True, dumps a .png-file. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
    plotDPI : Integer, optional
        Specifies the DPI for the plot. The deafult is 200
    OutputFilename : String or None, optional
        Is used as the name of the files in case the user request these dumped. If None is specificied, then the Biogeme-object name is used if this has been specified, otherwise '___MyCalibrationOutput___'. The default is None.
    overwrite : Boolean, optional
        Specify if the output should be overwritten. If True, then the output is overwritten, and if False, then the output is not overwritten. The default is False.

    Returns
    -------
    betasCalibrated : Dict
        Dict containing calibrated parameter values.
    betasSensitivityCalibrated : List
        List containing dicts with calibrated sensitivity parameter values. This output is only return if a list is specified in the betasSensitivity-input.
        
    '''
    
    # If maxiter is specified as none, then it is set to zero, which will disable an upper limit on the number of iterations for the calibration
    if maxiter==None:
        maxiter=0

    # If maxiter is specified as none, then it is set to zero, which will disable an upper limit on the number of iterations for the calibration
    if threshold==None:
        threshold=-1
    
    # Make a copy of the dict for calibration while maintaining the original dict of parameters
    betasCalibrated = betas.copy()
    
    # Create empty list to log results    
    listOfCalibrations = []
    
    # Initialize loop
    k=0; MaxDiff=1
    
    #while (k <maxiter+1 and MaxDiff>threshold) or (maxiter==None and MaxDiff>threshold) or (k <maxiter+1 and threshold==None):
    while (k <maxiter+1 or maxiter==0) and (MaxDiff>threshold or threshold==-1):
        print("")
         
        #--------------------------------------------
        # Calibrate features features
        #--------------------------------------------       

        # Simulate market shares
        sim= biogemeObject.simulate(theBetaValues=betasCalibrated)
        
        diff=[] # list to keep track of the differences between actual and target probabilities - used to terminate the loop when the calibration has reached a specified precision threshold
        
        # update parameters based on previous iteration - don't update the parameter in the first iteration (base level)
        for i in calibrationSettings.keys():
            prob = sim[i].mean()
            target = calibrationSettings[i]['target']
            param = calibrationSettings[i]['param']

            # Calibrate parameters
            if k>0 and param!=None and target!=None:
                for b in StringNoneToList(param):
                    betasCalibrated[b] = betasCalibrated[b]  + np.log(target   / prob * alpha)
            
            if target!=None:
                # store the diff for all alternatives
                diff += [abs(target-prob)]



        #--------------------------------------------
        # Logging features
        #--------------------------------------------                
        
        # create temp logging dataframe with 1 row each - the reason we make three dataframes is so the prob-column can be next to each other and similar with the target and parameter columns.
        logProb = pd.DataFrame(index=range(1)) #[[k]], columns=['iter'])
        logTarget = pd.DataFrame(index=range(1)) #[[k]], columns=['iter'])
        logParam = pd.DataFrame(index=range(1)) #[[k]], columns=['iter'])
                
        for i in calibrationSettings.keys():
            prob = sim[i].mean()
            target = calibrationSettings[i]['target']
            param = calibrationSettings[i]['param']
                   
            # log calibration
            logProb[i] = prob
            if target!=None:
                logTarget[i+' target'] = target 
            
            printb='['
            # loop through all parameters in list (if defined as list). 
            for idx, b in enumerate(StringNoneToList(param)):
                logParam[b] = betasCalibrated[b]
                
                # create a string with calibrated parameters which can be printed in the console
                printb = printb+b+': '+str(round(betasCalibrated[b],4))
                if idx<len(StringNoneToList(param))-1:
                    printb = printb+', '
            printb=printb+']'
            # Print updates in the console for each iteration
            print('iteration ' + str(k)+' - '+i+': '+str(round(prob,4))+' (target: '+str(target)+'), '+str(printb))
        
        # Concat the three logging-dataframes into a single dataframe and add a column recording the iteration number within the loop
        logJoined = pd.concat([logProb,logTarget,logParam], axis=1 )
        logJoined.insert(loc=0, column='iter', value=k)
                
        # append logged calibration
        listOfCalibrations += [logJoined]
        
        # compute MaxDiff to check if loop should be terminated
        MaxDiff = max(diff)
        
        k=k+1
    
    # concat all stored calibration iterations
    CalibrationLog = pd.concat(listOfCalibrations).reset_index(drop=True) #.reset_index(names='iter')
    
    
    print('calibration completed after '+str(k)+' iterations (precision: '+str(MaxDiff)+')')
    #--------------------------------------------
    # Export features
    #--------------------------------------------
      
    
    
    
    if ExportCalibrationExcel==True:   

        # Get name for '.xlsx' file        
        OutputFilenameExcel = getNewFileNameOverwriteOption(name=selectFileName(biogemeObject=biogemeObject, 
                                                                                OutputFilename=OutputFilename, 
                                                                                SpecificOutput=ExportCalibrationExcel),
                                                                     ext='xlsx', 
                                                                     overwrite=overwriteOutput)

        print('\nExporting calibration log to the file '+OutputFilenameExcel)
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter( OutputFilenameExcel, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        CalibrationLog.set_index('iter').to_excel(writer, sheet_name='CalibrationLog')
        
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
    
    
    
    # export log file
    if ExportCalibrationLog==True:

        # Get name for '.log' file
        OutputFilenameLog = getNewFileNameOverwriteOption(name=selectFileName(biogemeObject=biogemeObject, 
                                                                              OutputFilename=OutputFilename, 
                                                                              SpecificOutput=ExportCalibrationLog),
                                                                     ext='log', 
                                                                     overwrite=overwriteOutput)
        
        
        print('\nExporting calibration log to the file '+OutputFilenameLog)
        
        # Export '.log' file
        CalibrationLog.set_index('iter').to_csv( OutputFilenameLog )


        
    #--------------------------------------------
    # Plotting features
    #--------------------------------------------        
        
    # plot calibration log
    if plotCalibration == True or ExportCalibrationPlot==True:
        import matplotlib.pyplot as plt
        plt.figure(figsize = (15, 4))
        
        defaultColourCycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        k=0

        for i in calibrationSettings.keys():
            ColName=i
            if ColName+' target' in CalibrationLog.columns:
                plt.plot(CalibrationLog['iter'], CalibrationLog[ColName+' target'], label=ColName+' target', color=defaultColourCycle[k], linestyle='dashed')
            plt.plot(CalibrationLog['iter'], CalibrationLog[ColName]          , label=ColName          , color=defaultColourCycle[k], linestyle='solid' )
            k=k+1
        
        plt.ylabel('prob')
        plt.xlabel('iterations')
        plt.title('Calibration')
        
        plt.xlim(min(CalibrationLog['iter'])-0.1, max(CalibrationLog['iter'])+0.1)
        #plt.ylim(0-0.02, 1+0.02)
        plt.legend()
        
        if ExportCalibrationPlot==True:
            
            # Get name for '.png' file
            OutputFilenamePNG = getNewFileNameOverwriteOption(name=selectFileName(biogemeObject=biogemeObject, 
                                                                                 OutputFilename=OutputFilename, 
                                                                                 SpecificOutput=ExportCalibrationPlot),
                                                             ext='png', 
                                                             overwrite=overwriteOutput)
            
            print('\nExporting calibration plot to the file '+OutputFilenamePNG)
            
            # Export '.png' file
            plt.savefig(OutputFilenamePNG, dpi=plotDPI)
            
        if plotCalibration == True:
            plt.show()    


    #--------------------------------------------
    # Display calibrated paramters and return these to user
    #--------------------------------------------      
    
    print('\nCalibration of betas finished, the following parameters have been calibrated:\n')
    for p in betasCalibrated.keys():
        if betasCalibrated[p]!=betas[p]:
            print(p+': '+str(betas[p])+ ' ---> '+str(betasCalibrated[p]))	
    print('')
    
    # if sensitivity betas is given as an input, then calibrate the sensitivity betas, otherwise return only the betas
    if betasSensitivity!=None:
        betasSensitivityCalibrated = calibrateSensitivityParameters(betasSensitivity=betasSensitivity, betas=betas, betasCalibrated=betasCalibrated)
        return betasCalibrated, betasSensitivityCalibrated
    
    else:
        return betasCalibrated









'''
--------------------------------------------------------------------------------------------------------------------------------------

  ______     ___       __       __  .______   .______          ___   .___________. _______            _______. _______ .__   __.      _______. __  .___________. __  ____    ____  __  .___________.____    ____       .______      ___      .______          ___      .___  ___.  _______ .___________. _______ .______          _______.
 /      |   /   \     |  |     |  | |   _  \  |   _  \        /   \  |           ||   ____|          /       ||   ____||  \ |  |     /       ||  | |           ||  | \   \  /   / |  | |           |\   \  /   /       |   _  \    /   \     |   _  \        /   \     |   \/   | |   ____||           ||   ____||   _  \        /       |
|  ,----'  /  ^  \    |  |     |  | |  |_)  | |  |_)  |      /  ^  \ `---|  |----`|  |__            |   (----`|  |__   |   \|  |    |   (----`|  | `---|  |----`|  |  \   \/   /  |  | `---|  |----` \   \/   /        |  |_)  |  /  ^  \    |  |_)  |      /  ^  \    |  \  /  | |  |__   `---|  |----`|  |__   |  |_)  |      |   (----`
|  |      /  /_\  \   |  |     |  | |   _  <  |      /      /  /_\  \    |  |     |   __|            \   \    |   __|  |  . `  |     \   \    |  |     |  |     |  |   \      /   |  |     |  |       \_    _/         |   ___/  /  /_\  \   |      /      /  /_\  \   |  |\/|  | |   __|      |  |     |   __|  |      /        \   \    
|  `----./  _____  \  |  `----.|  | |  |_)  | |  |\  \----./  _____  \   |  |     |  |____       .----)   |   |  |____ |  |\   | .----)   |   |  |     |  |     |  |    \    /    |  |     |  |         |  |           |  |     /  _____  \  |  |\  \----./  _____  \  |  |  |  | |  |____     |  |     |  |____ |  |\  \----.----)   |   
 \______/__/     \__\ |_______||__| |______/  | _| `._____/__/     \__\  |__|     |_______|      |_______/    |_______||__| \__| |_______/    |__|     |__|     |__|     \__/     |__|     |__|         |__|           | _|    /__/     \__\ | _| `._____/__/     \__\ |__|  |__| |_______|    |__|     |_______|| _| `._____|_______/    
                                                                                                                                                                                                                                                                                                                                          

--------------------------------------------------------------------------------------------------------------------------------------
'''

def calibrateSensitivityParameters(betasSensitivity, betas, betasCalibrated):
    '''
    This function is a subfunction that calibrates sensitivity betas. It is implimented in the calibrate function, and is called if sensitivity betas are given as an input.

    Parameters
    ----------
    betasSensitivity : List
        List in which each element contains a dict with parameters values drawn from the 'getBetasForSensitivityAnalysis'-function in Biogeme
    betas : Dict
        Dict with estimated paramter values.
    betasCalibrated : Dict
        Dict with calibrated paramters values.

    Returns
    -------
    betasSensitivityCalibrated : List
        List containing dicts with calibrated sensitivity parameter values. 

    '''

    # Make a copy of the dict for calibration while maintaining the original dict of parameters
    betasSensitivityCalibrated =  copy.deepcopy(betasSensitivity)
    
    sensitivityOffset = dict()
    
    for i in betas.keys():
        if betasCalibrated[i] - betas[i] !=0:
            sensitivityOffset[i] = betasCalibrated[i] - betas[i]  
            for r in range(0,len(betasSensitivityCalibrated)):
                if i in betasSensitivityCalibrated[r]:
                    betasSensitivityCalibrated[r][i] = betasSensitivityCalibrated[r][i] + sensitivityOffset[i]

    print('Calibration of sensitivty betas finished, using the following offsets:\n')
    for i in sensitivityOffset.keys():
        print(i+': '+str(sensitivityOffset[i]))
    print('')
        
    return betasSensitivityCalibrated



# #--------------------------------------------
# # Example: Calibrate sensitivity parameters (note this is automatically done in the 'calibrate' function if both betas and betasSensitivity are provided as input. If not, the betasSensitivity can be manually calibrate afterwards)
# #--------------------------------------------

# betasSensitivityCalibrated = bioUtil.calibrateSensitivityParameters(betasSensitivity=betasSensitivity, 
#                                                                     betas=betas, 
#                                                                     betasCalibrated=betasCalibrated)













'''
--------------------------------------------------------------------------------------------------------------------------------------

     _______. __  .___  ___.  __    __   __          ___   .___________. _______            _______. _______ .__   __.      _______. __  .___________. __  ____    ____  __  .___________.____    ____ 
    /       ||  | |   \/   | |  |  |  | |  |        /   \  |           ||   ____|          /       ||   ____||  \ |  |     /       ||  | |           ||  | \   \  /   / |  | |           |\   \  /   / 
   |   (----`|  | |  \  /  | |  |  |  | |  |       /  ^  \ `---|  |----`|  |__            |   (----`|  |__   |   \|  |    |   (----`|  | `---|  |----`|  |  \   \/   /  |  | `---|  |----` \   \/   /  
    \   \    |  | |  |\/|  | |  |  |  | |  |      /  /_\  \    |  |     |   __|            \   \    |   __|  |  . `  |     \   \    |  |     |  |     |  |   \      /   |  |     |  |       \_    _/   
.----)   |   |  | |  |  |  | |  `--'  | |  `----./  _____  \   |  |     |  |____       .----)   |   |  |____ |  |\   | .----)   |   |  |     |  |     |  |    \    /    |  |     |  |         |  |     
|_______/    |__| |__|  |__|  \______/  |_______/__/     \__\  |__|     |_______|      |_______/    |_______||__| \__| |_______/    |__|     |__|     |__|     \__/     |__|     |__|         |__|     
                                                                                                                                                                                                       

--------------------------------------------------------------------------------------------------------------------------------------
'''


def simulateSensitivity(biogemeObject, 
                        betasSensitivity,
                        PrintDetailedLogger=False):
    '''
    A function to simulate sensitivity analysis which return the full un-processed simulations for each set of generated sensitivity parameters (specified by an '___Iteration___'-column in the output data). Hence the number of rows in the output correspond to the number of rows in the biogemeDatabase multiplied by the number of elements in the list of sensitivity draws (i.e. the size-parameter in the 'getBetasForSensitivityAnalysis'-function)

    Parameters
    ----------
    biogemeObject : biogemeObject
        A biogemeObject.
    betasSensitivity : List
        List in which each element contains a dict with parameters values drawn from the 'getBetasForSensitivityAnalysis'-function in Biogeme
    PrintDetailedLogger : Boolean, optional
        Enables more detailed output in the prompt. The default is False.

    Returns
    -------
    simulatedSensitivityResults : dataframe
        A dataframe with the simulated result for each set of generated sensitivity parameters.

    '''

    listOfResults = []
    i=0
    SimStartTime = datetime.datetime.now()#.strftime("%Y-%m-%d %H:%M:%S")
    print('\nSimulation of confidence intervals initiated at '+str(SimStartTime)[:-7])
    IterStartTime = SimStartTime
    for b in betasSensitivity:
        r = biogemeObject.simulate(b)
        i=i+1
        r.insert(0, '___Iteration___', i)
        listOfResults += [r]
        
        # Compute elapsed and remaining time
        IterEndTime = datetime.datetime.now()
        IterDiffTime = IterEndTime - IterStartTime
        AverageTimePerIter = (IterEndTime - SimStartTime)/i
        EstimatedTimeRemaining = AverageTimePerIter * (len(betasSensitivity)-i)
        ExpectedTimeOfCompletion = SimStartTime + AverageTimePerIter*len(betasSensitivity)
        IterStartTime = IterEndTime
        
        if PrintDetailedLogger==True:
            print('Finished: '+str(i)+'/'+str(len(betasSensitivity))+' sensitivity draws'
                  +' (Iteration completed: '+str(IterEndTime)[:-7]
                  +', Iteration time: '+str(IterDiffTime)[:-7]
                  +', Estimated time remaning: ' +str(EstimatedTimeRemaining)[:-7]
                  +', Expected time of completion: ' +str(ExpectedTimeOfCompletion)[:-7]
                  +')')
        else:
            print('Finished: '+str(i)+'/'+str(len(betasSensitivity))+' sensitivity draws'
                  +' (Iteration time: '+str(IterDiffTime)[:-7]
                  +', Estimated time remaning: ' +str(EstimatedTimeRemaining)[:-7]
                  +')')
        print("")
    simulatedSensitivityResults = pd.concat(listOfResults)
    
    return simulatedSensitivityResults    







'''
--------------------------------------------------------------------------------------------------------------------------------------

     _______. __  .___  ___.  __    __   __          ___   .___________. _______ 
    /       ||  | |   \/   | |  |  |  | |  |        /   \  |           ||   ____|
   |   (----`|  | |  \  /  | |  |  |  | |  |       /  ^  \ `---|  |----`|  |__   
    \   \    |  | |  |\/|  | |  |  |  | |  |      /  /_\  \    |  |     |   __|  
.----)   |   |  | |  |  |  | |  `--'  | |  `----./  _____  \   |  |     |  |____ 
|_______/    |__| |__|  |__|  \______/  |_______/__/     \__\  |__|     |_______|
                                                                                 

--------------------------------------------------------------------------------------------------------------------------------------
'''


 
def simulateWithCI(biogemeObject, 
                   betas=None, 
                   betasSensitivity=None, 
                   intervalSize=0.9, 
                   aggFunc=['mean'], 
                   keepVar=None, 
                   dropVar=None, 
                   groupByVar=None, 
                   ExportResultsCSV=False, 
                   ExportResultsExcel=False,
                   ExportResultsDB=True,
                   OutputFilename=None, 
                   overwriteOutput=False):
    '''
    

    Parameters
    ----------
    biogemeObject : biogemeObject
        A biogemeObject.
    betas : Dict
        Dict containing estimated parameter values.
    betasSensitivity : List
        List in which each element contains a dict with parameters values drawn from the 'getBetasForSensitivityAnalysis'-function in Biogeme
   intervalSize : Numeric or list, optional
        Specify the size of the confidence interval. If a list of values is provided the the function will compute multiple confidence intervals. The default is 0.9.
    aggFunc : string or list, optional
        Enables the user to specify which aggregated metrics should be computed, e.g. 'mean', 'std', 'median', etc. 
        If the betasSensitivity is specified, then the function will compute the confidence interval for each metric, 
        e.g. the confidence interval around the 'mean', 'std', 'median', etc.
        The default is ['mean'].
    keepVar : List, string, or None, optional
        Specify variables to keep (other variables will be removed). If None is specified, then all variables are kept. The default is None.
    dropVar : List, string, or None, optional
        Specify variables to drop. Note that keepVar is applied before dropVar, so in case a variable is specified in both dropVar overrules keepVar. If None is specified, then no variables are remove. The default is None.
    groupByVar : List, string, or None, optional
        Specify variable for which the analysis should be grouped by, e.g. compute the mean (and confidence interval) for each group. The default is None.
    groupByVarDataframe : dataframe, optional
        Specify a dataframe from which the desired groupby-variable can be joined (if they do not already exist in the smulated data). 
        Is designed to work the biogemeDatabase.data specified in the biogemeObject used for the simulation. 
        If None, then groupby-column will not be extracted from the dataframe. The default is None.
    ExportResultsCSV : Boolean or string, optional
        If True, dumps a .CSV-file with the aggregated overview. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
    ExportCalibrationExcel : Boolean, optional
        If True, dumps a .xlsx-file with the aggregated overview. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
    ExportResultsDB : Boolean, optional
        If True, dumps a .db-file with the full simulated tables - this is useful for post-processing afterward without having to re-run the entire simulation of both the estimated parameters and the sensitivity analysis. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
    OutputFilename : String or None, optional
        Is used as the name of the files in case the user request these dumped. If None is specificied, then the Biogeme-object name is used if this has been specified, otherwise '___MyCalibrationOutput___'. The default is None.
    overwrite : Boolean, optional
        Specify if the output should be overwritten. If True, then the output is overwritten, and if False, then the output is not overwritten. The default is False.

    Returns
    -------
    Overview : dataframe
        An aggregated overview of the simulated parameter (if a dict with the estimated parameters is specified) and confidence intervals (if list with generated sensitivty parameters is specified).
    simulatedResults : dataframe
        The full dataframe with simulate values (if a dict with the estimated parameters is specified)
    simulatedSensitivityResults : dataframe 
        The full dataframe with simulate sensitivity values (if list with generated sensitivty parameters is specified)

    '''

    #-----------------------------------------------------        
    # Simulate using estimated and sensitivity parameters
    #-----------------------------------------------------
    
    # Simulate 
    if isinstance(betas, dict): 
        simulatedResults = biogemeObject.simulate(betas)
    else:
        simulatedResults = None
        
    # Simulate sensitivity
    if isinstance(betasSensitivity, list):
        simulatedSensitivityResults = simulateSensitivity(biogemeObject, betasSensitivity=betasSensitivity)
    else:
        simulatedSensitivityResults = None
    
    #-----------------------------------------------------        
    # Export to db
    #-----------------------------------------------------
    
    if ExportResultsDB==True or isinstance(ExportResultsDB, str):
        
        # Get a filename for the exported DB-file
        OutputFilenameDB = getNewFileNameOverwriteOption(name=selectFileName(biogemeObject=biogemeObject, 
                                                                             OutputFilename=OutputFilename, 
                                                                             SpecificOutput=ExportResultsDB),
                                                         ext='db', 
                                                         overwrite=overwriteOutput)

        
        # Define connection to database
        cnx = sqlite3.connect(OutputFilenameDB)
        
        if isinstance(simulatedResults, pd.DataFrame):
            simulatedResults.to_sql('simulatedResults', cnx, index=True, if_exists='replace')
        
        if isinstance(simulatedSensitivityResults, pd.DataFrame):
            simulatedSensitivityResults.to_sql('simulatedSensitivityResults', cnx, index=True, if_exists='replace')
            
        # Export data to the database (this makes it easy to redo post processing - in particular to group by variables from the database not presented in the simulated results)
        biogemeObject.database.data.to_sql('data', cnx, index=True, if_exists='replace')
        
        print('\nCompleted exporting results to the file '+OutputFilenameDB)
    
    #-----------------------------------------------------        
    # Post processing: compute aggregated metrics and confidence intervals
    #-----------------------------------------------------
    
    overview = simulatePostProcessing(databaseWithResults=None,
                                      simulatedResults=simulatedResults, 
                                      simulatedSensitivityResults=simulatedSensitivityResults, 
                                      intervalSize=[0.9], 
                                      aggFunc=['mean'], 
                                      keepVar=keepVar, 
                                      dropVar=dropVar, 
                                      groupByVar=groupByVar,
                                      groupByVarDataframe=biogemeObject.database.data,
                                      ExportResultsCSV=selectFileName(biogemeObject=biogemeObject, OutputFilename=OutputFilename, SpecificOutput=ExportResultsCSV), 
                                      ExportResultsExcel=selectFileName(biogemeObject=biogemeObject, OutputFilename=OutputFilename, SpecificOutput=ExportResultsExcel),
                                      OutputFilename=OutputFilename, 
                                      overwriteOutput=overwriteOutput)
    
        
    #-----------------------------------------------------        
    # Return output
    #-----------------------------------------------------
    
    if betas!=None and betasSensitivity==None:
        return overview, simulatedResults
    if betas==None and betasSensitivity!=None:
        return overview, simulatedSensitivityResults
    if betas!=None and betasSensitivity!=None:
        return overview, simulatedResults, simulatedSensitivityResults













def simulatePostProcessing(databaseWithResults=None,
                           simulatedResults=None, 
                           simulatedSensitivityResults=None, 
                           intervalSize=[0.9], 
                           aggFunc=['mean'], 
                           keepVar=None, 
                           dropVar=None, 
                           groupByVar=None,
                           groupByVarDataframe=None,
                           ExportResultsCSV=False, 
                           ExportResultsExcel=False,
                           OutputFilename=None, 
                           overwriteOutput=False):
    '''
    A function to post-process simulated values. This is useful in case one would like to change the aggregated metrics (e.g. group by variables) without having to re-run the simulation.

    Parameters
    ----------
    databaseWithResults : .db-file
        Specify the filename (include path if not in the same directory) of a .db-file which contains the full dataframes from the simulation.
    simulatedResults : dataframe, optional
        The full dataframe with simulate values 
    simulatedSensitivityResults :  dataframe, optional
        The full dataframe with simulate sensitivity values 
   intervalSize : Numeric or list, optional
        Specify the size of the confidence interval. If a list of values is provided the the function will compute multiple confidence intervals. The default is 0.9.
    aggFunc : string or list, optional
        Enables the user to specify which aggregated metrics should be computed, e.g. 'mean', 'std', 'median', etc. 
        If the betasSensitivity is specified, then the function will compute the confidence interval for each metric, 
        e.g. the confidence interval around the 'mean', 'std', 'median', etc.
        The default is ['mean'].
    keepVar : List, string, or None, optional
        Specify variables to keep (other variables will be removed). If None is specified, then all variables are kept. The default is None.
    dropVar : List, string, or None, optional
        Specify variables to drop. Note that keepVar is applied before dropVar, so in case a variable is specified in both dropVar overrules keepVar. If None is specified, then no variables are remove. The default is None.
    groupByVar : List, string, or None, optional
        Specify variable for which the analysis should be grouped by, e.g. compute the mean (and confidence interval) for each group. The default is None.
    groupByVarDataframe : dataframe, optional
        Specify a dataframe from which the desired groupby-variable can be joined (if they do not already exist in the smulated data). 
        Is designed to work the biogemeDatabase.data specified in the biogemeObject used for the simulation. 
        If None, then groupby-column will not be extracted from the dataframe. The default is None.
    ExportResultsCSV : Boolean or string, optional
        If True, dumps a .CSV-file with the aggregated overview. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
    ExportCalibrationExcel : Boolean, optional
        If True, dumps a .xlsx-file with the aggregated overview. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
    OutputFilename : String or None, optional
        Is used as the name of the files in case the user request these dumped. If None is specificied, then the Biogeme-object name is used if this has been specified, otherwise '___MyCalibrationOutput___'. The default is None.
    overwrite : Boolean, optional
        Specify if the output should be overwritten. If True, then the output is overwritten, and if False, then the output is not overwritten. The default is False.

    Returns
    -------
    Overview, dataframe
        An aggregated overview of the simulated parameter (if a dict with the estimated parameters is specified) and confidence intervals (if list with generated sensitivty parameters is specified).

    '''
    
    #-----------------------------------------------------        
    # Get input from dataframes or database
    #-----------------------------------------------------
    
    #if simulatedResults==None and simulatedSensitivityResults==None and databaseResults==None:
        #print('Warning: all inputs empty')
        
    #if simulatedResults!=None and simulatedSensitivityResults!=None and databaseResults!=None:
        #print('Warning: inputs specified multiple places. Input from the database is used')
        
    if databaseWithResults!=None:
        
        # Define connection to database
        cnx = sqlite3.connect(databaseWithResults)
                
        
        if simulatedResults==None:
            try:
                simulatedResults = pd.read_sql_query("SELECT * FROM simulatedResults", cnx).set_index('index')
                print('simulatedResults loaded from '+databaseWithResults)
            except:
                print('simulatedResults is not in '+databaseWithResults)


        if simulatedSensitivityResults==None:
            try:
                simulatedSensitivityResults = pd.read_sql_query("SELECT * FROM simulatedSensitivityResults", cnx).set_index('index')
                print('simulatedSensitivityResults loaded from '+databaseWithResults)
            except:
                print('simulatedSensitivityResults is not in '+databaseWithResults)

        if groupByVarDataframe==None:
            try:
                groupByVarDataframe = pd.read_sql_query("SELECT * FROM data", cnx).set_index('index')
                print('groupByVarDataframe loaded from '+databaseWithResults)                
            except:
                print('groupByVarDataframe is not in '+databaseWithResults)        

    #-----------------------------------------------------        
    # Aggregate Results
    #-----------------------------------------------------

    
    aggResultsDict = calculateConfidenceInterval(simulatedResults=simulatedResults, 
                                       simulatedSensitivityResults=simulatedSensitivityResults, 
                                       intervalSize=intervalSize, 
                                       aggFunc=aggFunc, 
                                       keepVar=keepVar, 
                                       dropVar=dropVar, 
                                       groupByVar=groupByVar,
                                       groupByVarDataframe=groupByVarDataframe)
    
    # Concat all aggregated results into a single complete overwiev. Note: the top headers are reordered, so that the aggreagated metric (e.g. 'mean') are on top, and the confidence level below.
    overview = pd.concat(aggResultsDict,axis=1).reorder_levels([1,0],axis=1)
    
    
    #-----------------------------------------------------        
    # Export to CSV
    #-----------------------------------------------------

    if ExportResultsCSV==True or isinstance(ExportResultsCSV, str):
        
        # Get a filename for the exported CSV-file
        OutputFilenameCSV = getNewFileNameOverwriteOption(name=selectFileName(biogemeObject=None, 
                                                                              OutputFilename=OutputFilename, 
                                                                              SpecificOutput=ExportResultsCSV),
                                                          ext='csv', 
                                                          overwrite=overwriteOutput)
        
                
        # Export overview to CSV
        overview.to_csv( OutputFilenameCSV )
        
        print('\nCompleted exporting aggregated results to the file '+OutputFilenameCSV)
            
    #-----------------------------------------------------        
    # Export to Excel
    #-----------------------------------------------------
    
    if ExportResultsExcel==True or isinstance(ExportResultsExcel, str):

        # Get a filename for the exported Excel-file
        OutputFilenameExcel = getNewFileNameOverwriteOption(name=selectFileName(biogemeObject=None, 
                                                                                OutputFilename=OutputFilename, 
                                                                                SpecificOutput=ExportResultsExcel),
                                                            ext='xlsx', 
                                                            overwrite=overwriteOutput)
        
               
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter( OutputFilenameExcel, engine='xlsxwriter')
        
        # Export overview to excel
        overview.to_excel(writer, sheet_name='overview')
        
        # Loop through all keys in dict and export each to excel
        for i in aggResultsDict.keys():
            aggResultsDict[i].to_excel(writer, sheet_name=i)
            
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        
        print('\nCompleted exporting aggregated results to the file '+OutputFilenameExcel)

    return overview
    





# #--------------------------------------------
# # Example 1: Load input from database and post-process simulation results using default settings
# #--------------------------------------------

# overviewFromPostProcessing = bioUtil.simulatePostProcessing(databaseWithResults='MyDatabaseFromSimulateWithCI.db')


# #--------------------------------------------
# # Example 2: Load input from dataframe variables and post-process simulation results (without confidence intervals) using custom settings with single inputs
# #--------------------------------------------

# overviewFromPostProcessing = bioUtil.simulatePostProcessing(simulatedResults=simulatedResults,
#                                                             intervalSize=0.95,
#                                                             aggFunc='median')


# #--------------------------------------------
# # Example 3: Load input from dataframe variables and post-process simulation results (with confidence intervals) using custom settings with multiple inputs
# #--------------------------------------------    
    
# overviewFromPostProcessing = bioUtil.simulatePostProcessing(simulatedResults=simulatedResults,
#                                                             simulatedSensitivityResults=simulatedSensitivityResults,
#                                                             intervalSize=[0.9, 0.95], 
#                                                             aggFunc=['mean', 'std', 'min', 'median', 'max' ], 
#                                                             groupByVar=['PURPOSE', 'MALE'],
#                                                             groupByVarDataframe=biogemeObject.database.data,
#                                                             ExportResultsCSV=False, 
#                                                             ExportResultsExcel=True,
#                                                             OutputFilename='MyOutputName')  











 

def calculateConfidenceInterval(simulatedResults=None, 
                                simulatedSensitivityResults=None, 
                                intervalSize=[0.9], 
                                aggFunc=['mean'], 
                                keepVar=None, 
                                dropVar=None, 
                                groupByVar=None,
                                groupByVarDataframe=None):
    '''
    A function to compute aggregated metrics (e.g. mean, median, etc) and the confidence intervals around those metrics.

    Parameters
    ----------
    simulatedResults : dataframe, optional
        The full dataframe with simulate values 
    simulatedSensitivityResults :  dataframe, optional
        The full dataframe with simulate sensitivity values 
   intervalSize : Numeric or list, optional
        Specify the size of the confidence interval. If a list of values is provided the the function will compute multiple confidence intervals. The default is 0.9.
    aggFunc : string or list, optional
        Enables the user to specify which aggregated metrics should be computed, e.g. 'mean', 'std', 'median', etc. 
        If the betasSensitivity is specified, then the function will compute the confidence interval for each metric, 
        e.g. the confidence interval around the 'mean', 'std', 'median', etc.
        The default is ['mean'].
    keepVar : List, string, or None, optional
        Specify variables to keep (other variables will be removed). If None is specified, then all variables are kept. The default is None.
    dropVar : List, string, or None, optional
        Specify variables to drop. Note that keepVar is applied before dropVar, so in case a variable is specified in both dropVar overrules keepVar. If None is specified, then no variables are remove. The default is None.
    groupByVar : List, string, or None, optional
        Specify variable for which the analysis should be grouped by, e.g. compute the mean (and confidence interval) for each group. The default is None.
    groupByVarDataframe : dataframe, optional
        Specify a dataframe from which the desired groupby-variable can be joined (if they do not already exist in the smulated data). 
        Is designed to work the biogemeDatabase.data specified in the biogemeObject used for the simulation. 
        If None, then groupby-column will not be extracted from the dataframe. The default is None.

    Returns
    -------
    aggResultsDict, Dict
        Returns a Dict with aggregated metrics. 

    '''





    """Calculate confidence intervals on the simulated quantities"""
    NumDecimals=5
    
    # Convert variables
    if isinstance(aggFunc, (list))==False:
        aggFunc=[aggFunc]
    
    if isinstance(intervalSize, (int, float))==True:
        intervalSize=[intervalSize]
        
    groupByVar = StringNoneToList(groupByVar)

    # Create dict with empty dataframes to store the aggregated results
    aggResultsDict = dict()
        
       
    #-----------------------------------------------------        
    # Clean data
    #-----------------------------------------------------       
        
    if isinstance(simulatedResults, pd.DataFrame):
        simulatedResults = CleanDataKeepDropVar(simulatedResults, keepVar=keepVar, dropVar=dropVar, groupByVar=groupByVar)

    if isinstance(simulatedSensitivityResults, pd.DataFrame):
        simulatedSensitivityResults = CleanDataKeepDropVar(simulatedSensitivityResults, keepVar=keepVar, dropVar=dropVar, groupByVar=groupByVar)
    

    #-----------------------------------------------------        
    # Add groupby-var(from the spevified dataframe) variables specified in the groupByVar-statement to the simulated results  
    #-----------------------------------------------------
    
    if isinstance(groupByVarDataframe, pd.DataFrame):
        
        if isinstance(simulatedResults, pd.DataFrame):
            simulatedResults = addVarFromDataframe(simulatedResults, dataframe=groupByVarDataframe, addVar=groupByVar)
            
        if isinstance(simulatedSensitivityResults, pd.DataFrame):
            simulatedSensitivityResults = addVarFromDataframe(simulatedSensitivityResults, dataframe=groupByVarDataframe, addVar=groupByVar)
    


    #-----------------------------------------------------        
    # Compute aggregated results and confidence intervals
    #-----------------------------------------------------
    
    # Compute aggregated results for the estimated parameters
    if isinstance(simulatedResults, pd.DataFrame):
        simulatedResults['___Iteration___']=0
        
        # compute aggregated metrics 
        simulatedResultsAgg = simulatedResults.groupby(['___Iteration___']+groupByVar,dropna=False).agg(aggFunc)
        
        # Re-order data
        simulatedResultsAgg = simulatedResultsAgg.stack().stack().unstack(level=-2).rename_axis(simulatedResultsAgg.index.names + ['Var'])
        
        # drop '___Iteration___' column and re-order levels of multiindex so that the order is 'var' + groupByVar
        simulatedResultsAgg = simulatedResultsAgg.reorder_levels(['Var']+simulatedResultsAgg.index.names[0:-1]).droplevel('___Iteration___', axis=0)  
        
        # store output in dict
        aggResultsDict['estimated parameters'] = simulatedResultsAgg
    
    # compute aggregated results for the sensitivity parameters
    if isinstance(simulatedSensitivityResults, pd.DataFrame):
        
        # compute aggregated metrics (for each iteration so the confidence interval can be computed afterwards)
        simulatedSensitivityResultsAgg = simulatedSensitivityResults.groupby(['___Iteration___']+groupByVar,dropna=False).agg(aggFunc)
        
        # Re-order data
        simulatedSensitivityResultsAgg = simulatedSensitivityResultsAgg.stack().stack().unstack(level=-2).rename_axis(simulatedSensitivityResultsAgg.index.names + ['Var'])
        
        # drop '___Iteration___' column and re-order levels of multiindex so that the order is 'var' + groupByVar
        simulatedSensitivityResultsAgg = simulatedSensitivityResultsAgg.reorder_levels(['Var']+simulatedSensitivityResultsAgg.index.names[0:-1]).droplevel('___Iteration___', axis=0)  
        
        '''
        Confidence intervals
        '''
        #print('intervalSize:'+str(intervalSize))
        if intervalSize!=None:
            
            # Compute confidence intervals 
            for CI in intervalSize: 
                r = round((1.0 - CI) / 2.0 , NumDecimals)
                aggResultsDict[str(CI*100)+'% CI lower ('+str(r)+')']   = simulatedSensitivityResultsAgg.reset_index().groupby(['Var']+groupByVar, sort=False).quantile(r)
                aggResultsDict[str(CI*100)+'% CI upper ('+str(1-r)+')'] = simulatedSensitivityResultsAgg.reset_index().groupby(['Var']+groupByVar, sort=False).quantile(1.0 - r)

    
    
    return aggResultsDict
    

































































class BIOGEME(bio.BIOGEME):    
    #def __init__(self):
    #    super().__init__()


  


    '''
    --------------------------------------------------------------------------------------------------------------------------------------
    
     _______       ___   .___________.    ___                 ___      .__   __.  _______         _______  .______          ___   ____    __    ____   _______.
    |       \     /   \  |           |   /   \               /   \     |  \ |  | |       \       |       \ |   _  \        /   \  \   \  /  \  /   /  /       |
    |  .--.  |   /  ^  \ `---|  |----`  /  ^  \             /  ^  \    |   \|  | |  .--.  |      |  .--.  ||  |_)  |      /  ^  \  \   \/    \/   /  |   (----`
    |  |  |  |  /  /_\  \    |  |      /  /_\  \           /  /_\  \   |  . `  | |  |  |  |      |  |  |  ||      /      /  /_\  \  \            /    \   \    
    |  '--'  | /  _____  \   |  |     /  _____  \         /  _____  \  |  |\   | |  '--'  |      |  '--'  ||  |\  \----./  _____  \  \    /\    / .----)   |   
    |_______/ /__/     \__\  |__|    /__/     \__\       /__/     \__\ |__| \__| |_______/       |_______/ | _| `._____/__/     \__\  \__/  \__/  |_______/    
                                                                                                                                                               
    --------------------------------------------------------------------------------------------------------------------------------------
    '''

    


    # getBioDraws
    def getBioDraws(self):
        '''
        Extracts the generated bio-draws into a dataframe


        Returns
        -------
        MyBioDraws : dataframe
            Return a dataframe with the extracted bio-draws as columns. Rows correspond to observations in data and number of draws specified in the biogeme object.

        '''
        return getBioDraws(self.database)




    #exportBioDraws
    def exportBioDraws(self, 
                       OutputFilename=None,	
                       overwriteOutput=False,
                       returnBioDraws=False,
                       useBiogemeNameAsDefault=True):
        '''
        Extracts and export the generated bio-draws into a .draws file

        Parameters
        ----------
        OutputFilename : string, optional
            Specify the name (without extension) of the exported output file. If None, then the name of the biogemeDatabase is used. The default is None.
        overwriteOutput : Boolean, optional
            Specify whether the output should overwrite existing output with the same name. If True, then existing files will be overwritten, and if False, then a new filename is generated according the the standard biogeme naming convention. The default is False.
        returnBioDraws : Boolean, optional
            Specify if the extracted bio-draws should be returned to the user. If True, then the output is returned, and if False, then the output is not returned. The default is False.
        useBiogemeNameAsDefault : Boolean, optional
            Only relevant if OutputFilename=None. Specify if the name of the biogemeObject should be used over the name of the biogemeDatabase.  If True, then the output name of the biogemeObject is used, and if False, then the name of the biogemeDatabase is used. The default is True.

        Returns
        -------
        MyBioDraws : dataframe
            Return a dataframe with the extracted bio-draws as columns. Rows correspond to observations in data and number of draws specified in the biogeme object.

        '''
        
        # If no user-defined outputFilename has been defined and the function should default to using the name of the biogeme object rather than the databasename, then extract the biogeme name
        if useBiogemeNameAsDefault==True and OutputFilename==None:
            OutputFilename=self.modelName
	   
        return exportBioDraws(biogemeDatabase=self.database, 
                              OutputFilename=OutputFilename, 
                              overwriteOutput=overwriteOutput, 
                              returnBioDraws=returnBioDraws)




    
    #exportBioDraws
    def exportBioData(self, 
                      keepVar=None, 
                      dropVar=None,
                      OutputFilename=None,	
                      overwriteOutput=False,
                      returnBioData=False,
                      useBiogemeNameAsDefault=True):
        '''
        Extracts and export the data in the biogemeDatabase

        Parameters
        ----------
        keepVar : List, string, or None, optional
            Specify variables to keep (other variables will be removed). If None is specified, then all variables are kept. The default is None.
        dropVar : List, string, or None, optional
            Specify variables to drop. Note that keepVar is applied before dropVar, so in case a variable is specified in both dropVar overrules keepVar. If None is specified, then no variables are remove. The default is None.
        OutputFilename : string, optional
            Specify the name (without extension) of the exported output file. If None, then the name of the biogemeDatabase is used. The default is None.
        overwriteOutput : Boolean, optional
            Specify whether the output should overwrite existing output with the same name. If True, then existing files will be overwritten, and if False, then a new filename is generated according the the standard biogeme naming convention. The default is False.
        returnBioDraws : Boolean, optional
            Specify if the extracted bio-data should be returned to the user. If True, then the output is returned, and if False, then the output is not returned. The default is False.
        useBiogemeNameAsDefault : Boolean, optional
            Only relevant if OutputFilename=None. Specify if the name of the biogemeObject should be used over the name of the biogemeDatabase.  If True, then the output name of the biogemeObject is used, and if False, then the name of the biogemeDatabase is used. The default is True.

        Returns
        -------
        MyBioData : dataframe
            Return a dataframe with the extracted bio-data.

        '''
        
        # If no user-defined outputFilename has been defined and the function should default to using the name of the biogeme object rather than the databasename, then extract the biogeme name
        if useBiogemeNameAsDefault==True and OutputFilename==None:
            OutputFilename=self.modelName
        

        # INSERT FUNCTION TO REMOVE UNUSED VARIABLES! (removeUnusedVariables=True)


        return exportBioData(biogemeDatabase=self.database, 
                             keepVar=keepVar, 
                             dropVar=dropVar, 
                             OutputFilename=OutputFilename, 
                             overwriteOutput=overwriteOutput, 
                             returnBioData=returnBioData)









    def exportDescriptiveStatistics(self,                              
                                    continiousVar=None, 
                                    categoricalVar=None, 
                                    keepVar=None,
                                    dropVar=None, 
                                    aggFunc=None,                              
                                    dropna=False,
                                    dropVal=None, 
                                    ValueLabels=None, 
                                    exportExcel=True,
                                    exportDB=False,
                                    OutputFilename=None, 
                                    overwriteOutput=False,
                                    nunique_threshold=10,
                                    returnDict=False,
                                    useBiogemeNameAsDefault=True):


        # If no user-defined outputFilename has been defined and the function should default to using the name of the biogeme object rather than the databasename, then extract the biogeme name
        if useBiogemeNameAsDefault==True and OutputFilename==None:
            OutputFilename=self.modelName

        
        # INSERT FUNCTION TO REMOVE UNUSED VARIABLES! (removeUnusedVariables=True)
        
        
        return exportDescriptiveStatistics(biogemeDatabase=self.database,                              
                                           continiousVar=continiousVar, 
                                           categoricalVar=categoricalVar, 
                                           keepVar=keepVar,
                                           dropVar=dropVar, 
                                           aggFunc=aggFunc,                              
                                           dropna=dropna,
                                           dropVal=dropVal, 
                                           ValueLabels=ValueLabels, 
                                           exportExcel=exportExcel,
                                           exportDB=exportDB,
                                           OutputFilename=OutputFilename, 
                                           overwriteOutput=overwriteOutput,
                                           nunique_threshold=nunique_threshold,
                                           returnDict=returnDict)


    # #--------------------------------------------
    # # Example 1: Export descriptive statistics using default settings
    # #--------------------------------------------

    # biogemeObject.exportDescriptiveStatistics()


    # #--------------------------------------------
    # # Example 2: Export descriptive statistics using custom settings
    # #--------------------------------------------

    # # Optional labels for the descriptive analysis
    # ValueLabels = {'CAR_AV_SP':  {0: 'Not available',
    #                               1: 'Available'},
    #                'SM_AV':      {0: 'Not available',
    #                               1: 'Available'},
    #                'TRAIN_AV_SP':{0: 'Not available',
    #                               1: 'Available'}}    

    # DictStatistics = biogemeObject.exportDescriptiveStatistics(dropVal=0,
    #                                                            ValueLabels=ValueLabels, 
    #                                                            exportExcel=True,
    #                                                            exportDB=True,
    #                                                            OutputFilename='MyOutputName', 
    #                                                            nunique_threshold=12,
    #                                                            returnDict=True)



    '''
    --------------------------------------------------------------------------------------------------------------------------------------
    
      ______     ___       __       __  .______   .______          ___   .___________. _______ 
     /      |   /   \     |  |     |  | |   _  \  |   _  \        /   \  |           ||   ____|
    |  ,----'  /  ^  \    |  |     |  | |  |_)  | |  |_)  |      /  ^  \ `---|  |----`|  |__   
    |  |      /  /_\  \   |  |     |  | |   _  <  |      /      /  /_\  \    |  |     |   __|  
    |  `----./  _____  \  |  `----.|  | |  |_)  | |  |\  \----./  _____  \   |  |     |  |____ 
     \______/__/     \__\ |_______||__| |______/  | _| `._____/__/     \__\  |__|     |_______|
                                                                                               
    
    --------------------------------------------------------------------------------------------------------------------------------------
    '''
    
    
    def calibrate(self, 
                  calibrationSettings,
                  betas, 
                  betasSensitivity=None, 
                  maxiter=100, 
                  threshold = 0.001, 
                  alpha=1, 
                  plotCalibration=True, 
                  ExportCalibrationLog=False, 
                  ExportCalibrationExcel=False, 
                  ExportCalibrationPlot=False, 
                  plotDPI=200, 
                  OutputFilename=None, 
                  overwriteOutput=False):
        '''
        This method is used to calibrate estimated parameters (in particular alternative specific constant, aka ASC or intercepts) so that the model reproduces actual market shares (instead of sample shares)
        

        Parameters
        ----------

        calibrationParameters : Dict
            Dict containing sub-dict for each parameter (ASC) to be calibrated with a correspond expression for the probability. 
            Should take the form of:
            
                calibrationParameters = {'ASC_TRAIN': {'prob': 'Prob. train', 'target': 0.20},
                                         'ASC_CAR'  : {'prob': 'Prob. car'  , 'target': 0.40}
                                         ...
                                         ...
                                         ...
                                         }
                where:
                    - 'ASC_TRAIN' and 'ASC_CAR' are the names of the parameters (ASCs) to be calibrated
                    - 'Prob. train' and 'Prob. train' refers to expression in the biogeme object containing the alternative probabilities for the respective parameters to be calibrated
                    - 0.20 and 0.40 are the probabilities used to calibrate against. 
                
        betas : Dict
            Dict containing estimated parameter values
        betasSensitivity : List, optional
            List in which each element contains a dict with parameters values drawn from the 'getBetasForSensitivityAnalysis'-function in Biogeme
        maxiter : Integer or None, optional
            Specifies an upper limit to the number of iterations for calibrating the parameters. If set to 0 or None then this is disregarded and no upper limit is defined. The default is 100.
        threshold : Float or None, optional
            Specifies the precision threshold to terminate the calibration loop. If set to -1 or None then this is disregarded and the algorith will keep looping until maxiter is reached. The default is 0.001 (equavilent to to 0.1%).
        alpha : Float or Interger, optional
            Calibration rate. The default is 1.
        plotCalibration : Boolean, optional
            If True, plots the conversion of predicted probabilities as a function of number of iteratinos. The default is True.
        ExportCalibrationLog : Boolean or string, optional
            If True, dumps a .log-file. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
        ExportCalibrationExcel : Boolean, optional
            If True, dumps a .xlsx-file. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
        ExportCalibrationPlot : Boolean, optional
            If True, dumps a .png-file. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
        plotDPI : Integer, optional
            Specifies the DPI for the plot. The deafult is 200
        OutputFilename : String or None, optional
            Is used as the name of the files in case the user request these dumped. If None is specificied, then the Biogeme-object name is used if this has been specified, otherwise '___MyCalibrationOutput___'. The default is None.
        overwrite : Boolean, optional
            Specify if the output should be overwritten. If True, then the output is overwritten, and if False, then the output is not overwritten. The default is False.

        Returns
        -------
        betasCalibrated : Dict
            Dict containing calibrated parameter values.
        betasSensitivityCalibrated : List
            List containing dicts with calibrated sensitivity parameter values. This output is only return if a list is specified in the betasSensitivity-input.
            
        '''
        
        return calibrate(biogemeObject=self, 
                         calibrationSettings=calibrationSettings,
                         betas=betas, 
                         betasSensitivity=betasSensitivity, 
                         maxiter=maxiter, 
                         threshold = threshold, 
                         alpha=alpha, 
                         plotCalibration=plotCalibration, 
                         ExportCalibrationLog=ExportCalibrationLog, 
                         ExportCalibrationExcel=ExportCalibrationExcel, 
                         ExportCalibrationPlot=ExportCalibrationPlot, 
                         plotDPI=plotDPI, 
                         OutputFilename=OutputFilename, 
                         overwriteOutput=overwriteOutput)
    

    # #--------------------------------------------
    # # Example preparation
    # #-------------------------------------------- 
    
    
    # # The choice model is a logit, with availability conditions
    # prob1 = models.logit(V, av, 1)
    # prob2 = models.logit(V, av, 2)
    # prob3 = models.logit(V, av, 3)
    
    # simulate = {
    #     'Prob. train': MonteCarlo(prob1),
    #     'Prob. Swissmetro': MonteCarlo(prob2),
    #     'Prob. car': MonteCarlo(prob3)
    # }
    
    # # Create the Biogeme object
    # biogemeSimulateSensitivity = bioUtil.BIOGEME(database, simulate)
    # biogemeSimulateSensitivity.modelName = 'b05normal_mixture_simulate'

    # # Define calibration settings
    # calibrationSettings = {'Prob. train':      {'target': 0.20, 'param': 'ASC_TRAIN'},
    #                        'Prob. car':        {'target': 0.35, 'param': 'ASC_CAR'  },
    #                        'Prob. Swissmetro': {'target': 0.45, 'param': None       } }
    
    
    # #--------------------------------------------
    # # Example 1: Calibrate parameters using default setting
    # #--------------------------------------------

    # betasCalibrated, betasSensitivityCalibrated = biogemeCalibrate.calibrate(calibrationSettings=calibrationSettings, betas=betas)


    # #--------------------------------------------
    # # Example 2: Calibrate parameters and sensitivity parameters using custom settings
    # #--------------------------------------------

    # betasCalibrated, betasSensitivityCalibrated = biogemeCalibrate.calibrate(calibrationSettings=calibrationSettings,
    #                                                                          betas=betas,
    #                                                                          betasSensitivity=betasSensitivity,
    #                                                                          maxiter=100, 
    #                                                                          threshold = 0.001,
    #                                                                          ExportCalibrationExcel=True,
    #                                                                          ExportCalibrationLog=True,
    #                                                                          ExportCalibrationPlot=True,
    #                                                                          OutputFilename='MyOutputName')
    
    '''
    --------------------------------------------------------------------------------------------------------------------------------------
    
         _______. __  .___  ___.  __    __   __          ___   .___________. _______            _______. _______ .__   __.      _______. __  .___________. __  ____    ____  __  .___________.____    ____ 
        /       ||  | |   \/   | |  |  |  | |  |        /   \  |           ||   ____|          /       ||   ____||  \ |  |     /       ||  | |           ||  | \   \  /   / |  | |           |\   \  /   / 
       |   (----`|  | |  \  /  | |  |  |  | |  |       /  ^  \ `---|  |----`|  |__            |   (----`|  |__   |   \|  |    |   (----`|  | `---|  |----`|  |  \   \/   /  |  | `---|  |----` \   \/   /  
        \   \    |  | |  |\/|  | |  |  |  | |  |      /  /_\  \    |  |     |   __|            \   \    |   __|  |  . `  |     \   \    |  |     |  |     |  |   \      /   |  |     |  |       \_    _/   
    .----)   |   |  | |  |  |  | |  `--'  | |  `----./  _____  \   |  |     |  |____       .----)   |   |  |____ |  |\   | .----)   |   |  |     |  |     |  |    \    /    |  |     |  |         |  |     
    |_______/    |__| |__|  |__|  \______/  |_______/__/     \__\  |__|     |_______|      |_______/    |_______||__| \__| |_______/    |__|     |__|     |__|     \__/     |__|     |__|         |__|     
                                                                                                                                                                                                           
    
    --------------------------------------------------------------------------------------------------------------------------------------
    '''
    
    
    def simulateSensitivity(self, 
                            betasSensitivity,
                            PrintDetailedLogger=False):
        '''
        A function to simulate sensitivity analysis which return the full un-processed simulations for each set of generated sensitivity parameters (specified by an '___Iteration___'-column in the output data). Hence the number of rows in the output correspond to the number of rows in the biogemeDatabase multiplied by the number of elements in the list of sensitivity draws (i.e. the size-parameter in the 'getBetasForSensitivityAnalysis'-function)

        Parameters
        ----------
        betasSensitivity : List
            List in which each element contains a dict with parameters values drawn from the 'getBetasForSensitivityAnalysis'-function in Biogeme
        PrintDetailedLogger : Boolean, optional
            Enables more detailed output in the prompt. The default is False.

        Returns
        -------
        simulatedSensitivityResults : dataframe
            A dataframe with the simulated result for each set of generated sensitivity parameters.

        '''
        
        return simulateSensitivity(biogemeObject=self, 
                                   betasSensitivity=betasSensitivity,
                                   PrintDetailedLogger=PrintDetailedLogger)

    # #--------------------------------------------
    # # Example preparation
    # #-------------------------------------------- 
    
    
    # # The choice model is a logit, with availability conditions
    # prob1 = models.logit(V, av, 1)
    # prob2 = models.logit(V, av, 2)
    # prob3 = models.logit(V, av, 3)
    
    # simulate = {
    #     'Prob. train': MonteCarlo(prob1),
    #     'Prob. Swissmetro': MonteCarlo(prob2),
    #     'Prob. car': MonteCarlo(prob3)
    # }
    
    # # Create the Biogeme object
    # biogemeSimulateSensitivity = bioUtil.BIOGEME(database, simulate)
    # biogemeSimulateSensitivity.modelName = 'b05normal_mixture_simulate'
    
    # #--------------------------------------------
    # # Example: Simulate sensitivity
    # #--------------------------------------------
    
    # simulatedSensitivityResults = biogemeSimulateSensitivity.simulateSensitivity(betasSensitivity=betasSensitivity)
    
    
    
    '''
    --------------------------------------------------------------------------------------------------------------------------------------
    
         _______. __  .___  ___.  __    __   __          ___   .___________. _______ 
        /       ||  | |   \/   | |  |  |  | |  |        /   \  |           ||   ____|
       |   (----`|  | |  \  /  | |  |  |  | |  |       /  ^  \ `---|  |----`|  |__   
        \   \    |  | |  |\/|  | |  |  |  | |  |      /  /_\  \    |  |     |   __|  
    .----)   |   |  | |  |  |  | |  `--'  | |  `----./  _____  \   |  |     |  |____ 
    |_______/    |__| |__|  |__|  \______/  |_______/__/     \__\  |__|     |_______|
                                                                                     
    
    --------------------------------------------------------------------------------------------------------------------------------------
    '''    


    def simulateWithCI(self, 
                       betas=None, 
                       betasSensitivity=None, 
                       intervalSize=0.9, 
                       aggFunc=['mean'], 
                       keepVar=None, 
                       dropVar=None, 
                       groupByVar=None, 
                       ExportResultsCSV=False, 
                       ExportResultsExcel=False,
                       ExportResultsDB=True,
                       OutputFilename=None, 
                       overwriteOutput=False):
        '''
        

        Parameters
        ----------
        betas : Dict
            Dict containing estimated parameter values.
        betasSensitivity : List
            List in which each element contains a dict with parameters values drawn from the 'getBetasForSensitivityAnalysis'-function in Biogeme
        intervalSize : TYPE, optional
            DESCRIPTION. The default is 0.9.
        aggFunc : TYPE, optional
            Enables the user to specify which aggregated metrics should be computed, e.g. 'mean', 'std', 'median', etc. 
            If the betasSensitivity is specified, then the function will compute the confidence interval for each metric, 
            e.g. the confidence interval around the 'mean', 'std', 'median', etc.
            The default is ['mean'].
        keepVar : List, string, or None, optional
            Specify variables to keep (other variables will be removed). If None is specified, then all variables are kept. The default is None.
        dropVar : List, string, or None, optional
            Specify variables to drop. Note that keepVar is applied before dropVar, so in case a variable is specified in both dropVar overrules keepVar. If None is specified, then no variables are remove. The default is None.
        groupByVar : List, string, or None, optional
            Specify variable for which the analysis should be grouped by, e.g. compute the mean (and confidence interval) for each group. The default is None.
        ExportResultsCSV : Boolean or string, optional
            If True, dumps a .CSV-file with the aggregated overview. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
        ExportCalibrationExcel : Boolean, optional
            If True, dumps a .xlsx-file with the aggregated overview. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
        ExportResultsDB : Boolean, optional
            If True, dumps a .db-file with the full simulated tables - this is useful for post-processing afterward without having to re-run the entire simulation of both the estimated parameters and the sensitivity analysis. If a string is specified, then that is used as the filename for the exported file instead name specified in OutputFilename. If False, then the file is not exported. The default is False.
        OutputFilename : String or None, optional
            Is used as the name of the files in case the user request these dumped. If None is specificied, then the Biogeme-object name is used if this has been specified, otherwise '___MyCalibrationOutput___'. The default is None.
        overwrite : Boolean, optional
            Specify if the output should be overwritten. If True, then the output is overwritten, and if False, then the output is not overwritten. The default is False.

        Returns
        -------
        Overview, dataframe
            An aggregated overview of the simulated parameter (if a dict with the estimated parameters is specified) and confidence intervals (if list with generated sensitivty parameters is specified).
        simulatedResults, dataframe
            The full dataframe with simulate values (if a dict with the estimated parameters is specified)
        simulatedSensitivityResults, dataframe 
            The full dataframe with simulate sensitivity values (if list with generated sensitivty parameters is specified)

        '''
        
        return simulateWithCI(biogemeObject=self, 
                              betas=betas, 
                              betasSensitivity=betasSensitivity, 
                              intervalSize=intervalSize, 
                              aggFunc=aggFunc, 
                              keepVar=keepVar, 
                              dropVar=dropVar, 
                              groupByVar=groupByVar, 
                              ExportResultsCSV=ExportResultsCSV, 
                              ExportResultsExcel=ExportResultsExcel,
                              ExportResultsDB=ExportResultsDB,
                              OutputFilename=OutputFilename, 
                              overwriteOutput=overwriteOutput)
            
    
    

    # #--------------------------------------------
    # # Example preparation
    # #-------------------------------------------- 
    
    
    # # The choice model is a logit, with availability conditions
    # prob1 = models.logit(V, av, 1)
    # prob2 = models.logit(V, av, 2)
    # prob3 = models.logit(V, av, 3)
    
    # simulate = {
    #     'Prob. train': MonteCarlo(prob1),
    #     'Prob. Swissmetro': MonteCarlo(prob2),
    #     'Prob. car': MonteCarlo(prob3)
    # }
    
    # # Create the Biogeme object
    # biogemeSimulate = bioUtil.BIOGEME(database, simulate)
    # biogemeSimulate.modelName = 'b05normal_mixture_simulate'
    
    # #--------------------------------------------
    # # Example 1: Simulate with confidence intervals using default setting
    # #--------------------------------------------
    
    # overview, simulatedResults, simulatedSensitivityResults = biogemeSimulate.simulateWithCI(betas=betas, betasSensitivity=betasSensitivity)
    
    
    # #--------------------------------------------
    # # Example 2: Simulate without confidence interval using custom settings with single inputs
    # #--------------------------------------------
    
    # overview, simulatedResults = biogemeSimulate.simulateWithCI(betas=betas, 
    #                                                             intervalSize=0.95,
    #                                                             aggFunc='median', 
    #                                                             groupByVar='MALE')
    
    
    # #--------------------------------------------
    # # Example 3: Simulate only confidence intervals using custom settings with multiple inputs
    # #--------------------------------------------    
        
    # overview, simulatedSensitivityResults = biogemeSimulate.simulateWithCI(betasSensitivity=betasSensitivity,
    #                                                                        intervalSize=[0.9, 0.95], 
    #                                                                        aggFunc=['mean', 'std', 'min', 'median', 'max' ], 
    #                                                                        groupByVar=['PURPOSE', 'MALE'],
    #                                                                        ExportResultsCSV=False, 
    #                                                                        ExportResultsExcel=True,
    #                                                                        ExportResultsDB=True,
    #                                                                        OutputFilename='MyOutputName')    
    

















