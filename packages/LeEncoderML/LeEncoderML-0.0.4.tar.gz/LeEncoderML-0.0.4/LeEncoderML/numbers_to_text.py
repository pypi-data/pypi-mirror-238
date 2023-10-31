def numbers_to_text(df, le_dict): 
    """
    Decode previously encoded categorical columns using label encoders.

    Parameters:
    - df (DataFrame): The input DataFrame containing the data with encoded categorical columns.
    - le_dict (dict): A dictionary storing label encoders for each encoded column.

    Returns:
    - DataFrame: The updated DataFrame with categorical columns decoded to their original values.
    """
    for i in le_dict.keys(): 
        df[i] = le_dict[i].inverse_transform(df[i]) 
    return df
