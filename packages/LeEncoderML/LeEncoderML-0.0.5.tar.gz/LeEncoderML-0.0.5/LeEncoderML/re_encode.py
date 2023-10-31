def re_encode(df,le_dict):
    """
    Re-encode categorical columns in a DataFrame and handle unseen labels.

    Parameters:
    - df (DataFrame): The input DataFrame containing the data with categorical columns.
    - le_dict (Dictionary): A dictionary storing label encoders for various columns in the DataFrame.

    Returns:
    - DataFrame: The updated DataFrame with re-encoded categorical columns and rows with unseen labels removed.
    """
    for i in le_dict.keys():
        try:
            df[i] = le_dict[i].transform(test_df[i])
        except Exception as e:
            print(e)
            df = remove_row_fit(df, le_dict, i)
    return df

def remove_row_fit(df, le_dict, i):
    """
    Remove rows with unseen labels and re-encode a specific categorical column.

    Parameters:
    df (DataFrame)      : The input DataFrame containing the data with categorical columns.
    le_dict (Dictionary): A dictionary storing label encoders for various columns in the DataFrame.
    i (String)          : Represents the name of a specific column within the DataFrame that you want to process. It is a column name.
    
    Returns:
    - DataFrame: The updated DataFrame with rows containing unseen labels removed and re-encoded values.
    """
    for j in df[i].unique():
        if j in list(le_dict[i].classes_):
            pass
        else:
            print(j, " is an Unseen label in the column ", i)
            df = df[(df[i] != j)].copy()
            df[i] = le_dict[i].transform(df[i])
    return df

