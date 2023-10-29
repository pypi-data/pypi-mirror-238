"""
Created on Wed Oct 25 21:14:51 2023

@author: mthor
"""
import pandas as pd



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










def DescriptiveStatisticsContinious(df, 
                                    keepVar=None, 
                                    dropVar=None,
                                    aggFunc=None):
    '''
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    keepVar : TYPE, optional
        DESCRIPTION. The default is None.
    dropVar : TYPE, optional
        DESCRIPTION. The default is None.
    aggFunc : String, List or None, optional
        Defines which summary statistics will be generated. 
        If unspecified (i.e. None) the statistics will be generated from the describe() function in pandas

    Returns
    -------
    DescriptiveStatisticsContinious : TYPE
        DESCRIPTION.

    '''
    if df.empty==True:
        # Create empty dataframe to return if no variables are defined for the analysis
        Cont = pd.DataFrame()    


    
    # Process data according to keep/drop/groupby-variables
    df = CleanDataKeepDropVar(df, keepVar=keepVar, dropVar=dropVar)
    
    
    if df.empty==False:    
        if aggFunc==None:
            #Cont = df.groupby(groupByVar, dropna=dropna).describe().transpose()
            Cont = df.describe().transpose()
        else:
            #Cont = df.groupby(groupByVar, dropna=dropna).agg(aggFunc).transpose()
            Cont = df.agg(aggFunc).transpose()
                
    return Cont










def DescriptiveStatisticsCategorical(df, 
                                     keepVar=None, 
                                     dropVar=None,
                                     dropna=False,
                                     dropVal=None, 
                                     ValueLabels=None):
    '''
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    keepVar : TYPE, optional
        DESCRIPTION. The default is None.
    dropVar : TYPE, optional
        DESCRIPTION. The default is None.
    dropna : TYPE, optional
        DESCRIPTION. The default is False.
    dropVal : Int, float, list or None, optional
        Define which values are not included in the output. The main intended use case for this feature was to remove zeros from dummy-variables (for which it is sufficient to only show the "positive" outcomes), but the feature has been generalised so that the user can specify a number (or list) of values to be excluded from the analysis. 
    ValueLabels : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    Cat : TYPE
        DESCRIPTION.

    '''
    
    if df.empty==True:
        # Create empty dataframe to return if no variables are defined for the analysis
        Cat = pd.DataFrame()

    
    # Process data according to keep/drop/groupby-variables
    df = CleanDataKeepDropVar(df, keepVar=keepVar, dropVar=dropVar)
    
    # Create empty dataframe
    listOfResults = []
    
    for column in df:
        temp = df.groupby([column], dropna=False).size().to_frame('count').reset_index().rename(columns={column:'value'})
        temp['share']=temp['count']/temp['count'].sum()
        temp['percent']=temp['share']*100
        temp.insert(0, 'variable', value=column)
        
    	# Remove all rows which contains values present in the dropVal-input
        if dropVal!=None:
            if isinstance(dropVal, (int, float))==True:
                dropVal=[dropVal]
            for i in dropVal:
                temp = temp[temp['value'] != i]
                
            # Computes the percentage 
            temp['share of shown values']=temp['count']/temp['count'].sum()
            temp['percent of shown values']=temp['share of shown values']*100       
        
        # append the processed variable to the Cat-table
        listOfResults += [temp]
    
    Cat = pd.concat(listOfResults)
    
        
    # Add value labels
    if ValueLabels!=None and isinstance(ValueLabels, (dict))==True:
        Cat.insert(2, 'description', value=" ")
        for k1 in ValueLabels.keys():
            for k2 in ValueLabels[k1].keys():
                Cat.loc[((Cat['variable'] == k1) & (Cat['value'] == k2) ), 'description'] = ValueLabels[k1][k2]

    Cat = Cat.set_index(['variable', 'value'])  
    
    return Cat

#ValueLabels = {'CAR_AV_SP':{0: 'no',
#                            1: 'yes'},
#               'SM_AV'    :{0: 'no',
#                            1: 'yes'}}
#
#test5 = DescriptiveStatisticsCategorical(df=df2, 
#                                    keepVar=['TRAIN_AV_SP','CAR_AV_SP','SM_AV'], 
#                                    groupByVar='CHOICE', 
#                                    dropVar='TRAIN_AV_SP', 
#                                    dropna=False, 
#                                    ValueLabels=ValueLab)
#test5















def ClassifyContiniousCategoricalVar(df,nunique_threshold=10):
    '''
    

    Parameters
    ----------
    df : dataframe
        Dataframe in which the column should be classified as containing continious or categorical values.
    nunique_threshold : Integer or None, optional
        Specify the threshold for number of unique values a column must exceed in order to be classified as containing continious values. The default is 10.

    Returns
    -------
    continiousVar : List
        List with variables classified as being continious.
    categoricalVar : List
        List with variables classified as being categorical.

    '''
    # Extract all column names from dataframe
    ColNames = list(df.columns)
    

    if nunique_threshold==None:
        nunique_threshold=0

    continiousVar= []
    categoricalVar=[]

    for i in ColNames:
        NumUniqueVal = df[i].nunique()
        if NumUniqueVal <= nunique_threshold:
            categoricalVar = categoricalVar + [i]
        else:
            continiousVar = continiousVar + [i]

    return continiousVar,categoricalVar













# ADD: SortAlphabetically (otherwise use column sequence in data)
def DescriptiveStatistics(df, 
                          continiousVar=None, 
                          categoricalVar=None, 
                          keepVar=None,
                          dropVar=None, 
                          aggFunc=None,                              
                          dropna=False,
                          dropVal=None,
                          nunique_threshold=10, 
                          ValueLabels=None):
    
    # Process data according to keep/drop/groupby-variables
    df = CleanDataKeepDropVar(df, keepVar=keepVar, dropVar=dropVar)

    
    # If the user define a list of continiousVar then the remaining variables (which are not specificied in groupByVar or dropVar) are assumed to be categoricalVar. 
    # If the user define a list of categoricalVar then the remaining variables (which are not specificied in groupByVar or dropVar) are assumed to be continiousVar. 
    # If the user did not specified neither continiousVar nor categoricalVar, then the variables are claasified as being continious or categorial based on them number of unique values in each column (threshold value is defined by the nunique_threshold-parameter)
    # If the threshold-parameter is set to None (or 0) then all variables will be classified as continious 
    if continiousVar==None and categoricalVar==None:
        continiousVar,categoricalVar = ClassifyContiniousCategoricalVar(df,nunique_threshold=nunique_threshold)
        
    continiousVar=StringNoneToList(continiousVar)   
    categoricalVar=StringNoneToList(categoricalVar)    
    
    # Subtract the categorical list from the continious list (in the sub-functions these list will be cleaned for groupByVar and dropVar)
    continiousVar = list(set(continiousVar) - set(categoricalVar))
    
    
    continious = DescriptiveStatisticsContinious(df, 
                                                 keepVar=continiousVar, 
                                                 dropVar=None, 
                                                 aggFunc=aggFunc)
    
    categorical = DescriptiveStatisticsCategorical(df, 
                                                   keepVar=categoricalVar, 
                                                   dropVar=None, 
                                                   dropna=dropna,
                                                   dropVal=dropVal, 
                                                   ValueLabels=ValueLabels)
    
    
	
    return continious, categorical



