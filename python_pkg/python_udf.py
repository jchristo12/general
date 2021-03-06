# =============================================================================
# Creates a correlation heatmap
# =============================================================================
def corr_heatmap(data):
    #import necessary modules
    import numpy as np
    import seaborn as sb
    #calculate the correlation matrix (auto detects numerical features)
    corr = data.corr()
    #generate a mask for the upper triangle of the correlation matrix
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    #set up a custom colormap
    cmap = sb.diverging_palette(240, 10, as_cmap=True)
    #draw the heatmap
    sb.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap=cmap, vmax=1.0, vmin=-1.0, center=0,
               square=True, linewidth=0.5)

# =============================================================================
# Reads in API keys and stores the desired key
# =============================================================================
def read_key(file_path, source):
    import json
    path = file_path
    with open(path) as k:
        result = json.load(k)
    api_key = result[source]
    return api_key

# =============================================================================
# Finds the pairwise correlation of data frame features and returns those above a threshold
# =============================================================================
def corr_to_df_summary(dataframe, threshold=0.75):
    """
    Reads in a dataframe and turn the correlation matrix into a dataframe listing the pairwise correlations\n
    Returns the variables that have a correlation above a given threshold (default = 0.75)
    """
    #import necessary packages
    import numpy as np
    #creates the correlation matrix
    corr = dataframe.corr(method='pearson')
    #creates the upper triangle of the correlation matrix
    corr_triu = corr.where(~np.tril(np.ones(corr.shape)).astype(np.bool))
    #turn the matrix into a pairwise dataframe
    corr_triu = corr_triu.stack()
    #make it prettier
    corr_triu.name = 'Pearson R'
    corr_triu.index.names = ['Var1', 'Var2']
    #return a dataframe corresponding to a correlation threshold
    result = corr_triu[corr_triu >= threshold].to_frame()
    return result

# =============================================================================
# Flips a dictionary's keys and values
# =============================================================================
def dict_key_value_flip(dict_):
    """
    Takes a dictionary and makes each value a key with the old serving as the new value\n
    Returns a new dictionary
    """
    result = {old: new for new, old_all in dict_.items() for old in old_all}

    return result

# =============================================================================
# Builds an iterable helper tool so that you can acces the next item
# =============================================================================
def pairwise(iterable):
    """Takes an iterable and returns the current and next items"""
    import itertools
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

# =============================================================================
# Finds the items not in or in the list
# =============================================================================
def in_list(list1, list2, in_=True):
    if in_ != True:
        output = [item for item in list2 if item not in list1]
    else:
        output = [item for item in list2 if item in list1]

    return output
