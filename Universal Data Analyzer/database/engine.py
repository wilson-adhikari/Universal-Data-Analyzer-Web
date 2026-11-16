"""SQL Database Engine Module"""
from sqlalchemy import create_engine, inspect, select, Table, MetaData
from typing import Optional, List
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DatabaseEngine:
    """SQLAlchemy database engine wrapper"""
    
    def __init__(self, connection_string: str):
        """Initialize database engine"""
        try:
            self.engine = create_engine(connection_string)
            self.connection_string = connection_string
            logger.info(f"Database engine initialized")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def load_table(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Load table as dataframe"""
        try:
            if table_name not in inspect(self.engine).get_table_names():
                raise ValueError(f"Unknown table: {table_name}")
            if limit is not None and not isinstance(limit, int):
                raise ValueError("limit must be an integer")
            query = select(Table(table_name, MetaData(), autoload_with=self.engine))
            if limit:
                query = query.limit(limit)

            df = pd.read_sql(query, self.engine)
            logger.info(f"Loaded table {table_name}: {len(df)} rows")
            return df
        
        except Exception as e:
            logger.error(f"Error loading table: {str(e)}")
            raise
    
    def get_tables(self) -> List[str]:
        """Get list of available tables"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        logger.info(f"Found {len(tables)} tables")
        return tables
    
    def get_table_info(self, table_name: str) -> dict:
        """Get column information for table"""
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        
        info = {
            'table_name': table_name,
            'columns': [
                {
                    'name': col['name'],
                    'type': str(col['type']),
                    'nullable': col['nullable']
                }
                for col in columns
            ]
        }
        
        return info
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()
        logger.info("Database connection closed")
