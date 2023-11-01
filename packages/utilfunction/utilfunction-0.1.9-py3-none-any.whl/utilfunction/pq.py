import secrets
import os
import pandas as pd

def gen_hex(length: int) -> str:
    """
    Generate a random hexadecimal string.

    Args:
        length (int): The length of the hexadecimal string to generate.

    Returns:
        str: A random hexadecimal string of the specified length.
    """
    random_hex = secrets.token_hex(length // 2)
    return random_hex

def df_to_pq(df: pd.DataFrame, output_folder: str, output_file_name: str) -> None:
    """
    Save a DataFrame as a Parquet file.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
        output_folder (str): The folder where the Parquet file will be saved.
        output_file_name (str): The name of the output Parquet file.

    Returns:
        None

    Example:
    ```
    example_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    output_folder = 'output'
    output_file_name = 'example.parquet'
    df_to_pq(example_df, output_folder, output_file_name)
    ```

    This function saves the DataFrame as a Parquet file in the specified folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file_path = os.path.join(output_folder, output_file_name)
    df.to_parquet(output_file_path, index=False, engine='pyarrow', compression='snappy')

    print(f'DataFrame saved as Parquet file: {output_file_path}')