# This program allows you to input a parquet file of a city and it will
# convert it into a .csv file, then it creates a table with the different categories
# and the amount they show up and exports it as a .csv file.

#Use pandas to read parquet files
import pandas as pd

from collections import Counter


#Function that will create a table with the number and percentage that each
#category shows up, and exports it as a .csv file
def generateCategoryTable(df, cityName):
    categories = []
    #Goes through ever place in the parquet and determines what category they are
    for curr in df['categories']:
        #If the dictionary isnt empty, and the primary tag exists, then add the category
        # into the categories list
        if isinstance(curr, dict) and 'primary' in curr:
            categories.append(curr['primary'])
    
    #Counts and creates a dictionary with each category and the amount they show up
    categoriesAndCount = Counter(categories)
    
    #Creates a new dataframe with the different categories and their respective counts
    outputTable = pd.DataFrame.from_dict(categoriesAndCount, orient='index', columns=['Count'])
    outputTable.index.name = 'Category'
    outputTable = outputTable.reset_index()
    outputTable = outputTable.assign(Percentage= lambda counts: (counts['Count']/sum(categoriesAndCount.values()) * 100))
    
    #Orders the tables so the categories with the highest counts are at the top
    outputTable = outputTable.sort_values(by='Count', ascending=False)
    
    #Export to .csv
    outputTable.to_csv(f"{cityName.lower()}_category_summary.csv", index=False)

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

generateCategoryTable(toronto_places, "toronto")
generateCategoryTable(edmonton_places, "edmonton")
generateCategoryTable(montreal_places, "montreal")
generateCategoryTable(ottawa_places, "ottawa")