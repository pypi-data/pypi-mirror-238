def text_to_numbers(df): 
    """
    Encode categorical columns in a DataFrame using LabelEncoder and save the encoders.

    Parameters:
    - df (DataFrame): The input DataFrame containing the data with categorical columns.

    Returns:
    - DataFrame: The updated DataFrame with categorical columns encoded.
    - dict: A dictionary storing label encoders for each encoded column.
    """
    le_dict = dict() 
    col = df.select_dtypes(include=['object']).columns 
    for i in col: 
        print(i)
        le_dict[i] = LabelEncoder() 
        df[i] = le_dict[i].fit_transform(df[i]) 
    return df, le_dict 
    
