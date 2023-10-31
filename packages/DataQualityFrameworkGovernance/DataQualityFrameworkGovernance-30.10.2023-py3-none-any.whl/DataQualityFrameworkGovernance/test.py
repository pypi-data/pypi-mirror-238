print('hello')

dfLocation = "https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv"


from Completeness import *
missing_values(dfLocation)
completeness_percentage(dfLocation)
