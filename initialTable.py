#Use pandas to read parquet files
import pandas as pd

import array

from collections import Counter

#Load the parquet file
toronto_places = pd.read_parquet('toronto_places.parquet', engine='auto')

#Prints the transposed version of the table which allows for better printing
print(toronto_places.head().T)
 
# Create a list to store all the categories
categories = []

#This loop goes through every place in the parquet and determines what category they are
for curr in toronto_places['categories']:
    #If the dictionary isnt empty, and the primary tag exists, then add the category
    # into the categories list
    if isinstance(curr, dict) and 'primary' in  curr:
        categories.append(curr['primary'])

#Automatically counts the amount of times each category appears in the list
#And creates a dictionary that contains the category name and appearance amount
categoryAndCount = Counter(categories)

#Prints out the dictionary line by line
for category, count in categoryAndCount.items():
    print(f"{category}: {count}")
        
