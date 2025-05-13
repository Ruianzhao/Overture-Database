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
pivotTable1 = combinedTable.pivot_table(index='Category', columns='City', values='Percentage')
pivotTable2 = combinedTable.pivot_table(index='Category', columns='City', values='Count')

#This removes any categories that are present in one city which can mess with the 
#comparison
filteredTable = pivotTable1[pivotTable1.notna().sum(axis=1)>=2]

#Creates a new column called Max Deviation, which compares the percentages
#in each row and determines the max deviation between the cities for each category
filteredTable = filteredTable.copy()
filteredTable['Max Deviation'] = filteredTable.max(axis=1) - filteredTable.min(axis=1)

#Sorts the table based on descending order
filteredTable = filteredTable.sort_values(by='Max Deviation', ascending=False)

filteredTable.to_csv("max_deviation_category_comparison.csv", index=True)
    
    
    
#This makes it so if a category is present it will get a value of 1 and if it isnt
#present it will get a value of 0
binaryCoverageMatrix = pivotTable1.notna().astype(int)
binaryCoverageMatrix = binaryCoverageMatrix.copy()

binaryCoverageMatrix['Cities Present'] = binaryCoverageMatrix.sum(axis=1)
binaryCoverageMatrix = binaryCoverageMatrix.sort_values(
    by=['Cities Present', binaryCoverageMatrix.index.name],
    ascending=[False, True]
)

grouped = binaryCoverageMatrix.groupby('Cities Present')

group1 = grouped.get_group(1)
group2 = grouped.get_group(2)
group3 = grouped.get_group(3)
group4 = grouped.get_group(4)

binaryCoverageMatrix.to_csv("binary_coverage_matrix_of_categories.csv", index=True)

group1.to_csv("categories_in_1_city.csv", index=True)
group2.to_csv("categories_in_2_cities.csv", index=True)
group3.to_csv("categories_in_3_cities.csv", index=True)
group4.to_csv("categories_in_4_cities.csv", index=True)


#This creates a Spearman ranked correlation table based on the data
#This removes any rows that arent presnent in all 
pivotTable2Clean = pivotTable2.dropna()
rankedTable2 = pivotTable2.rank(ascending=False)
spearmanCorrelation = rankedTable2.corr(method='spearman')

spearmanCorrelation.to_csv("spearman_correlation_common_categories.csv", index=True)
