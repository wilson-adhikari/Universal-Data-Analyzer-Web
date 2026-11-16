import pandas as pd
import sqlalchemy
def load_sql_table(connection_string: str, table_name: str) -> pd.DataFrame:
    """
    Load a SQL table into a pandas DataFrame.

    Parameters:
    - connection_string: str - The database connection string.
    - table_name: str - The name of the table to load.

    Returns:
    - pd.DataFrame - The loaded DataFrame.
    """
    engine = sqlalchemy.create_engine(connection_string)
    with engine.connect() as connection:
        return pd.read_sql_table(table_name, con=connection)