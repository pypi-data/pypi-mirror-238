print('hello')

dfLocation = "https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv"

import DataQualityFrameworkGovernance.Completeness as ct
import pandas as pd

ct.completeness_percentage(dfLocation)
df = ct.missing_values(dfLocation)

print(df)