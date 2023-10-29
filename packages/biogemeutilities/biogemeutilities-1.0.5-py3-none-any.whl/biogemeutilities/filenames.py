from biogeme.filenames import getNewFileName

def getNewFileNameOverwriteOption(name,ext,overwrite=False):
    '''
    Expand the existing functionality of the traditional 'getNewFileName'-function in Biogeme to also include an option to let the user specify if the output should be overwritten.

    Parameters
    ----------
    name : string
        name of the file.
    ext : string
        file extension.
    overwrite : Boolean, optional
        Specify if the output should be overwritten. If True, then the output is overwritten, and if False, then the output is not overwritten. The default is False.

    Returns
    -------
    fileName : string
        name.ext if the file does not exists.  If it does, returns
           name~xx.ext (if overwrite=False), where xx is the smallest integer such that the
           corresponding file does not exist. It is designed to avoid erasing
           output files inadvertently.

    '''
    if overwrite==True:
        fileName  = name+'.'+ext
    if overwrite==False:
        fileName  = getNewFileName(name,ext)
    return fileName 



def selectFileName(biogemeObject=None, OutputFilename=None, SpecificOutput=None):
    '''
    A function to easily select the output-filename among multiple inputs based on a prioritized approach.

    Parameters
    ----------
    biogemeObject : biogemeObject, optional
        A biogemeObject, from which the name is extracted. The default is None.
    OutputFilename : string, optional
        A generic user-defined name. The default is None.
    SpecificOutput : string, optional
        A specific user-defined name. The default is None.

    Returns
    -------
    OutputFilename : string
        A filename based on the following prioritization: 1) SpecificOutput, 2) OutputFilename, 3) biogemeObject.modelname.

    '''
    # If the user has specificied a custom name for the specific extension then use that over the generic name (variable "OutputFilename")
    if isinstance(SpecificOutput, str):
        OutputFilename=SpecificOutput
    
    # Else if, the user has simply specified the boolean value True for the specific filetype then use the generic name (variable "OutputFilename")
    elif SpecificOutput==True and isinstance(OutputFilename, str):
        OutputFilename=OutputFilename
    
    # Otherwise, if a custom have has not been specified then use the name of the biogeme object 
    elif biogemeObject!=None:
        OutputFilename = biogemeObject.modelName
        
    return OutputFilename

