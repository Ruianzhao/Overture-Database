#Use pandas to read parquet files
import pandas as pd

import array

from collections import Counter

#Load the parquet file
toronto_places = pd.read_parquet('toronto_places.parquet', engine='auto')

montreal_places = pd.read_parquet('montreal_places.parquet', engine='auto')

edmonton_places = pd.read_parquet('edmonton_places.parquet', engine='auto')

ottawa_places = pd.read_parquet('ottawa_places.parquet', engine='auto')
#Creates a csv file for the toronto places
toronto_places.to_csv('toronto_places.csv', index=False)

montreal_places.to_csv('montreal_places.csv', index=False)

edmonton_places.to_csv('edmonton_places.csv', index=False)

ottawa_places.to_csv('ottawa_places.csv', index=False)

#Prints the transposed version of the table which allows for better printing
print(montreal_places.head().T)
 
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


#Creates a new dataframe from the different categories and their respective counts
catAndCountTable = pd.DataFrame.from_dict(categoryAndCount, orient='index', columns=['Count'])
catAndCountTable.index.name = 'Category'
catAndCountTable = catAndCountTable.reset_index()

#Adds a new column for the percentage that the category shows up
catAndCountTable = catAndCountTable.assign(Percentage= lambda counts: (counts['Count']/sum(categoryAndCount.values()) * 100))

#Prints first few rows of dataframe
print(catAndCountTable.head())

#Export to csv
catAndCountTable.to_csv('toronto_category_summary.csv', index=False)

