''' Fixing pathway '''
import os
import sys
module_path = os.path.abspath(os.path.join(''))
if module_path not in sys.path:    
    sys.path.append(module_path)


''' Importing packages '''
import numpy as np
import pandas as pd
import math

def add_legend(legend, ax, title, text_size=10):
    """
    add_legend() allows for the LA selected to be put on the legend alongside the quantile colours

    legend = the legend that will be amended
    ax = the matplotlib axes that it'll plot on
    title = optional title to add to the legend
    """
    from matplotlib.patches import Patch

    # Get the handles (colours, shapes) from legend
    handles = legend.legendHandles

    # Edit the labels in legend
    ## quantile are typically formatted with commas, e.g. 1, 2, instead of 1-2
    ## these lines fix this
    labels_pip = [t.get_text() for t in ax.get_legend().get_texts()]
    labels_pip = [p.replace(", ", " - ") for p in labels_pip]
    
    # Initialises the legend 
    legend._legend_box = None
    legend._init_legend_box(handles, labels_pip)
    legend._set_loc(legend._loc)
    legend.set_title(title, prop={'weight':'bold',"size":text_size})
    legend.get_frame().set_alpha(None)


def recentre_map(shp, ax, ratio, padding):
    """
    recentre_map() takes in the LA selected and centres the map on that LA

    shp = the shapefile (LA)
    ax = the matplotlib axes that it'll plot on
    ratio = the aspect ratio of the final map plot. Would recommend 1.5
    padding = the amount of space around the LA in the map. Would recommend 7500
    """
    x_centroid = shp.centroid.x.iloc[0]
    y_centroid = shp.centroid.y.iloc[0]

    xdif = shp['x_dif'].iloc[0]
    ydif = shp['y_dif'].iloc[0]

    # Set the ratio to be set by the user. Would recommend 1:1.5 for x:y 
    new_xlim = ((xdif + padding) / 2)
    new_ylim = new_xlim * ratio

    # Set the x and y limits for the map around the LA
    ax.set_xlim(x_centroid - new_xlim, x_centroid + new_xlim)
    ax.set_ylim(y_centroid - new_ylim, y_centroid + new_ylim)

def dimensions(df):
    df[['minx', 'miny', 'maxx', 'maxy']] = df.bounds
    df['x_dif'] = (df['maxx'] - df['minx'])
    df['y_dif'] = (df['maxy'] - df['miny'])

# Compacts text so that each line is a maximum of x characters
def compact_text(text_list, threshold = 14):
    # Purpose = Tidy up text so it can fit under a chart. I.e. replacing some spaces with "\n"
    ''' Define the output variable and a useful function '''
    output = []
    ''' Loop through each element in the list '''
    for i in range(len(text_list)):
        ''' Split the text up '''
        element = text_list[i].split()
        ''' Edit the text'''
        # if the text is one word then no edits requried
        if len(element) == 1:
            out = text_list[i]
        else:
            # If there is a whitespace, we loop through each word in 
            # the text adding a new row when the line threshold is met
            row = ""       
            out = []
            for x in element:
                if len(row) == 0:
                    # If the row is empty, populate it
                    row = x
                elif len(row) + len(x) < threshold + 1:
                    # If adding the next word to the row doesn't push it 
                    # over the threshold, add it to the row
                    row = row + " " + x
                else:
                    # If adding the next word does push it over the 
                    # threshold, then stard a new row
                    out.append(row)
                    row = x
                # If we've ran out of words, add the current row to the output
                if x == element[-1]:
                    out.append(row)
            out = "\n".join(out)
        ''' Add to output list '''
        output.append(out)
    return output

