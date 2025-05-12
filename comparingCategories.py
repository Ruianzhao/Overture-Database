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

#This finds all the categories that are unique to toronto
torontoUnique = torontoSet - (ottawaSet | montrealSet | edmontonSet)
ottawaUnique = ottawaSet - (torontoSet | montrealSet | edmontonSet)
montrealUnique = montrealSet - (ottawaSet | torontoSet | edmontonSet)
edmontonUnique =  edmontonSet - (ottawaSet | montrealSet | torontoSet)

pd.DataFrame({'Unique_Category': sorted(torontoUnique)}).to_csv('toronto_unique_categories.csv', index=False)
pd.DataFrame({'Unique_Category': sorted(ottawaUnique)}).to_csv('ottawa_unique_categories.csv', index=False)
pd.DataFrame({'Unique_Category': sorted(montrealUnique)}).to_csv('montreal_unique_categories.csv', index=False)
pd.DataFrame({'Unique_Category': sorted(edmontonUnique)}).to_csv('edmonton_unique_categories.csv', index=False)
