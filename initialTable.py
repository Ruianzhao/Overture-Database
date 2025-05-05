#Use pandas to read parquet files
import pandas as pd

import array

#Load the parquet file
toronto_places = pd.read_parquet('toronto_places.parquet', engine='auto')

#Prints the transposed version of the table which allows for better printing
print(toronto_places.head().T)

categoryNames = []
categoryCount = []

#This loop iterates through every place in the parquet and checks what category they are        
for curr in toronto_places['categories']:
    #This checks to make sure the dictionary isn't empty and that the primary tag exists
    if isinstance(curr, dict) and 'primary' in curr:
        #The value of the primary tag is the type of category the place is
        primary_cat = curr['primary']
        #If the category was already is category names, we just have to increment the count for that category
        if primary_cat in categoryNames:
            idx = categoryNames.index(primary_cat)
            categoryCount[idx] += 1
        else:
            #Otherwise we add it to the categoryNames and initialize its count to 1
            categoryNames.append(primary_cat)
            categoryCount.append(1)
    
#Then we convert the two arrays into an array of tuples for easier printing
for name, count in zip(categoryNames, categoryCount):
    print(f"{name}: {count}")   
    
    

    
