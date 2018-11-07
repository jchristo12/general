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
# 
# =============================================================================
