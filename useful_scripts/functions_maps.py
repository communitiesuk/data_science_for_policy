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

