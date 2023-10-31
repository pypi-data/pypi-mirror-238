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