import pandas as pd
import numpy as np
import copy
import datetime
import sqlite3
import biogeme.database as db
import biogeme.biogeme as bio
from biogemeutilities.filenames import getNewFileNameOverwriteOption, selectFileName
from biogemeutilities.statistics import StringNoneToList, CleanDataKeepDropVar, DescriptiveStatistics



def StringNoneToList(var):
    '''
    The purpose is to convert string and None to list

    Parameters
    ----------
    var : String or None
        

    Returns
    -------
    var : List
        Returns the input variable as a list, i.e. if the input variable is a string it returns a list with one element, and if the input variable is None it returns an empty list

    '''
    if var==None:
        var=[]
    if isinstance(var, (str))==True:
        var=[var] 
    return var




def CleanDataKeepDropVar(df, keepVar=None, dropVar=None, groupByVar=None):
    '''
    Cleans dataframe based on optional user-defined inputs

    Parameters
    ----------
    df : dataframe
        The input dataframe which should be cleaned.
    keepVar : List, string, or None, optional
        Specify variables to keep (other variables will be removed). If None is specified, then all variables are kept. The default is None.
    dropVar : List, string, or None, optional
        Specify variables to drop. Note that keepVar is applied before dropVar, so in case a variable is specified in both dropVar overrules keepVar. If None is specified, then no variables are remove. The default is None.
    groupByVar : List, string, or None, optional
        Specify additional variables to keep (other variables that are not listed here or in KeepVar will be removed). If None is specified, then no additional variables are kept. The default is None.

    Returns
    -------
    df : dataframe
        Returns the cleaned dataframe. 

    '''
    
    if keepVar==None:
        keepVar=list(df.columns)
        
        
    # Convert keepVar to a list (only relevant if a single column has been defined as a string)
    keepVar = StringNoneToList(keepVar)
    
    # Convert dropVar to a list
    dropVar = StringNoneToList(dropVar)
    
    # Convert dropVar to a list
    groupByVar = StringNoneToList(groupByVar)
    
    # Remove dropVar from keepVar+groupByVar
    keepVar = [i for i in keepVar+groupByVar if i not in dropVar]
    
    # Redefine keepVar to ensure that the column order remains as in the input dataframe (only relevant if the user has specified names in KeepVar that is different from the column order)
    keepVar = [i for i in list(df.columns) if i in keepVar]
    
    # Extract relevant columns from dataframe
    df = df[keepVar]
    
    return df
    










# Export biogeme draws
def getBioDraws(biogemeDatabase):
    '''
    Extracts the generated bio-draws into a dataframe

    Parameters
    ----------
    biogemeDatabase : biogemeDatabase
        Specify the biogemeDatabase from which the bio-draws should be extracted.

    Returns
    -------
    MyBioDraws : dataframe
        Return a dataframe with the extracted bio-draws as columns. Rows correspond to observations in data and number of draws specified in the biogeme object.

    '''
    
    # Create empty dataframe to store extracted draws
    MyBioDraws = pd.DataFrame()
    
    if biogemeDatabase.number_of_draws>0:
        # Extract draws
        listOfDraws = []
        for i in range(0,biogemeDatabase.number_of_draws):
            OneDraw = pd.DataFrame(biogemeDatabase.theDraws[:,i,:], columns=biogemeDatabase.typesOfDraws.keys())
            OneDraw.insert(loc=0, column='___draw___', value=i+1)
            listOfDraws += [OneDraw]

        # Concat all rows of draws that have been extracted from the list
        MyBioDraws = pd.concat(listOfDraws)
    else:
        print('\nNo draws generated')
    return MyBioDraws








# Export biogeme draws
def exportBioDraws(biogemeDatabase, OutputFilename=None, overwriteOutput=False, returnBioDraws=False):
    '''
    Extracts and export the generated bio-draws into a .draws file

    Parameters
    ----------
    biogemeDatabase : biogemeDatabase
        Specify the biogemeDatabase from which the bio-draws should be extracted.
    OutputFilename : string, optional
        Specify the name (without extension) of the exported output file. If None, then the name of the biogemeDatabase is used. The default is None.
    overwriteOutput : Boolean, optional
        Specify whether the output should overwrite existing output with the same name. If True, then existing files will be overwritten, and if False, then a new filename is generated according the the standard biogeme naming convention. The default is False.
    returnBioDraws : Boolean, optional
        Specify if the extracted bio-draws should be returned to the user. If True, then the output is returned, and if False, then the output is not returned. The default is False.

    Returns
    -------
    MyBioDraws : dataframe
        Return a dataframe with the extracted bio-draws as columns. Rows correspond to observations in data and number of draws specified in the biogeme object.

    '''
    
    if biogemeDatabase.number_of_draws>0:
        # Extract draws
        MyBioDraws  = getBioDraws(biogemeDatabase)
        
        # Naming output file
        if OutputFilename==None:
            OutputFilename=biogemeDatabase.name
        
        # Export
        ExportFilename = getNewFileNameOverwriteOption(name=OutputFilename, ext='draws',overwrite=overwriteOutput)
        MyBioDraws.to_csv(ExportFilename)
        
        # Print the time needed to generate the draws in the database-object
        print('\nCompleted exporting draws into file: '+ExportFilename)
        #print('Time needed to generate the draws: '+ str(biogemeObject.drawsProcessingTime))
    else:
        print('\nNo draws generated')
        
    if returnBioDraws==True:
        return MyBioDraws
    else:
        return




# Export biogeme data
def exportBioData(biogemeDatabase, keepVar=None, dropVar=None, OutputFilename=None, overwriteOutput=False, returnBioData=False):
    '''
    Extracts and export the data in the biogemeDatabase

    Parameters
    ----------
    biogemeDatabase : biogemeDatabase
        Specify the biogemeDatabase from which the bio-draws should be extracted.
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

    Returns
    -------
    MyBioData : dataframe
        Return a dataframe with the extracted bio-data.

    '''
    # Extract the dataframe from the database
    MyBioData = biogemeDatabase.data
    
    # Clean data according to keepVar and dropVar
    MyBioData = CleanDataKeepDropVar(df=MyBioData, keepVar=keepVar, dropVar=dropVar)
        
    # Export
    ExportFilenameDat = getNewFileNameOverwriteOption(name=OutputFilename, ext='dat', overwrite=overwriteOutput)
    MyBioData.to_csv(ExportFilenameDat, sep='\t')
    
    # Print the time needed to generate the draws in the database-object
    print('\nCompleted exporting data into file: '+ExportFilenameDat)
        
    if returnBioData==True:
        return MyBioData
    else:
        return

















def exportDescriptiveStatistics(biogemeDatabase,                              
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
                          #removeUnusedVariables=True
                          returnDict=False):

    
    # Naming output file
    if OutputFilename==None:
        OutputFilename=biogemeDatabase.name  

    # Create dict to store the results
    DictResult=dict()
    
    

    # Export biogeme-results
    df_obs = biogemeDatabase.data
    
    cont_obs, cat_obs = DescriptiveStatistics(df_obs, 
                                                  continiousVar=continiousVar, 
                                                  categoricalVar=categoricalVar, 
                                                  keepVar=keepVar, 
                                                  dropVar=dropVar, 
                                                  aggFunc=aggFunc,                              
                                                  dropna=dropna,
                                                  dropVal=dropVal, 
                                                  ValueLabels=ValueLabels,
                                                  nunique_threshold=nunique_threshold)
    if cont_obs.empty==False:
        DictResult['cont_obs']=cont_obs #.to_excel(writer, sheet_name='UsedDataStatistics_cont_obs')
    if cat_obs.empty==False:
        DictResult['cat_obs']=cat_obs #cat_obs.to_excel(writer, sheet_name='UsedDataStatistics_cat_obs')
    
    
    # If the data is panel, then redo the descriptive statistic at an individual level and output the results
    if biogemeDatabase.isPanel()==True: 
        
        # Only keep the first row for each panel-ID
        df_panel = biogemeDatabase.data.groupby(biogemeDatabase.panelColumn).first().reset_index()
        
        cont_panel, cat_panel = DescriptiveStatistics(df_panel, 
                                                          continiousVar=continiousVar, 
                                                          categoricalVar=categoricalVar, 
                                                          keepVar=keepVar, 
                                                          dropVar=dropVar, 
                                                          aggFunc=aggFunc,                              
                                                          dropna=dropna,
                                                          dropVal=dropVal, 
                                                          ValueLabels=ValueLabels,
                                                          nunique_threshold=nunique_threshold)
        if cont_panel.empty==False:
            DictResult['cont_panel']=cont_panel #Cont_panel.to_excel(writer, sheet_name='UsedDataStatistics_cont_panel')
        if cat_panel.empty==False:
            DictResult['cat_panel']=cat_panel #Cat_panel.to_excel(writer, sheet_name='UsedDataStatistics_cat_panel')


    
    
    
    if exportExcel==True:
    
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        OutputFilenameExcel = getNewFileNameOverwriteOption(name=selectFileName(biogemeObject=None, 
                                                                                OutputFilename=OutputFilename, 
                                                                                SpecificOutput=exportExcel), 
                                                            ext='xlsx', 
                                                            overwrite=overwriteOutput)    
    
        # Initiate writer
        writer = pd.ExcelWriter(OutputFilenameExcel, engine='xlsxwriter')
        
        for i in DictResult.keys():
            DictResult[i].to_excel(writer, sheet_name=i)
        
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        
        # Print the time needed to generate the draws in the database-object
        print('\nCompleted exporting data into file: '+OutputFilenameExcel)
        
        
        
    if exportDB==True:

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        OutputFilenameDB = getNewFileNameOverwriteOption(name=selectFileName(biogemeObject=None, 
                                                                             OutputFilename=OutputFilename, 
                                                                             SpecificOutput=exportDB), 
                                                         ext='db', 
                                                         overwrite=overwriteOutput)    
              
        # Define connection to database
        cnx = sqlite3.connect(OutputFilenameDB)
        
        for i in DictResult.keys():
            DictResult[i].to_sql(i, cnx, index=True, if_exists='replace')
        
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
    
        # Print the time needed to generate the draws in the database-object
        print('\nCompleted exporting data into file: '+OutputFilenameDB)


    if returnDict==True:
        return DictResult
    else:
        return		














class Database(db.Database):    
    #def __init__(self):
    #    super().__init__()
        


    # Export biogeme draws
    def getBioDraws(self):
        '''
        Extracts the generated bio-draws into a dataframe
    
        Returns
        -------
        MyBioDraws : dataframe
            Return a dataframe with the extracted bio-draws as columns. Rows correspond to observations in data and number of draws specified in the biogeme object.
    
        '''        
        return getBioDraws(self)



	
	

    # Export biogeme draws
    def exportBioDraws(self, OutputFilename=None, overwriteOutput=False, returnBioDraws=False):
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
    
        Returns
        -------
        MyBioDraws : dataframe
            Return a dataframe with the extracted bio-draws as columns. Rows correspond to observations in data and number of draws specified in the biogeme object.
    
        '''        
        return exportBioDraws(biogemeDatabase=self, 
                              OutputFilename=OutputFilename, 
                              overwriteOutput=overwriteOutput, 
                              returnBioDraws=returnBioDraws)





						   
    # Export biogeme data
    def exportBioData(self, keepVar=None, dropVar=None, OutputFilename=None, overwriteOutput=False, returnBioData=False):
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
    
        Returns
        -------
        MyBioData : dataframe
            Return a dataframe with the extracted bio-data.
    
        '''        
        return exportBioData(biogemeDatabase=self, 
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
                                    returnDict=False):
        
        return exportDescriptiveStatistics(biogemeDatabase=self,                              
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

    # biogemeDatabase.exportDescriptiveStatistics()


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

    # DictStatistics = biogemeDatabase.exportDescriptiveStatistics(dropVal=0,
    #                                                              ValueLabels=ValueLabels, 
    #                                                              exportExcel=True,
    #                                                              exportDB=True,
    #                                                              OutputFilename='MyOutputName', 
    #                                                              nunique_threshold=12,
    #                                                              returnDict=True)

