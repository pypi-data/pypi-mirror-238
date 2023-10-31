# Completeness

def missing_values(location):
    import pandas as pd
    # Load dataset
    df = pd.read_csv(location)

    missing_values = df.isnull().sum()
    print(missing_values)

def completeness_percentage(location):
    import pandas as pd
    # Load dataset
    df = pd.read_csv(location)
    
    total_entries = df.shape[0]
    complete_entries = df.dropna().shape[0]
    completeness_percentage = (complete_entries / total_entries) * 100
    completeness_percentage = f"Data completeness: {completeness_percentage:.2f}%"
    print(completeness_percentage)

def count_dataset(location):
    num_rows, num_cols = location.shape
    print("Number of rows:", num_rows)
    print("Number of columns:", num_cols)

def duplicate_rows(location):
    import pandas as pd
    duplicate_rows = location.duplicated()
    print("Duplicate rows:\n", duplicate_rows)