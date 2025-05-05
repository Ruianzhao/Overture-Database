#Use pandas to read parquet files
import pandas as pd

#Load the parquet file
toronto_places = pd.read_parquet('toronto_places.parquet', engine='auto')

#Prints the transposed version of the table which allows for better printing
print(toronto_places.head().T)

