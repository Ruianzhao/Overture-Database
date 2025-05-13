import pandas as pd

#Loads each csv file into a dataframe
torontoCat = pd.read_csv('toronto_category_summary.csv')
ottawaCat = pd.read_csv('ottawa_category_summary.csv')
montrealCat = pd.read_csv('montreal_category_summary.csv')
edmontonCat = pd.read_csv('edmonton_category_summary.csv')

#Converts each dataframe into sets for easy comparison
torontoSet = set(torontoCat['Category'])
ottawaSet = set(ottawaCat['Category'])
montrealSet = set(montrealCat['Category'])
edmontonSet = set(edmontonCat['Category'])

#This finds all the categories that are unique to each city
torontoUnique = torontoSet - (ottawaSet | montrealSet | edmontonSet)
ottawaUnique = ottawaSet - (torontoSet | montrealSet | edmontonSet)
montrealUnique = montrealSet - (ottawaSet | torontoSet | edmontonSet)
edmontonUnique =  edmontonSet - (ottawaSet | montrealSet | torontoSet)

pd.DataFrame({'Unique_Category': sorted(torontoUnique)}).to_csv('toronto_unique_categories.csv', index=False)
pd.DataFrame({'Unique_Category': sorted(ottawaUnique)}).to_csv('ottawa_unique_categories.csv', index=False)
pd.DataFrame({'Unique_Category': sorted(montrealUnique)}).to_csv('montreal_unique_categories.csv', index=False)
pd.DataFrame({'Unique_Category': sorted(edmontonUnique)}).to_csv('edmonton_unique_categories.csv', index=False)

#Combines all the tables together
combinedTable = pd.concat([torontoCat, ottawaCat, montrealCat, edmontonCat], ignore_index=True)

#Changes the table so that the categories are used to index the table and the columns
#display the count and percentage of each category for each city
pivotTable = combinedTable.pivot_table(index='Category', columns='City', values='Percentage')

#This removes any categories that are present in one city which can mess with the 
#comparison
filteredTable = pivotTable[pivotTable.notna().sum(axis=1)>=2]

#Creates a new column called Max Deviation, which compares the percentages
#in each row and determines the max deviation between the cities for each category
filteredTable = filteredTable.copy()
filteredTable['Max Deviation'] = filteredTable.max(axis=1) - filteredTable.min(axis=1)

#Sorts the table based on descending order
filteredTable = filteredTable.sort_values(by='Max Deviation', ascending=False)

filteredTable.to_csv("max_deviation_category_comparison.csv", index=True)
    