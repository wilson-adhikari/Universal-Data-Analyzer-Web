"""
Database Queries Module - Advanced Query Builder and Executor
Supports ORM operations and raw SQL queries for data analysis
Version: 1.0.0
"""
import pandas as pd
from sqlalchemy import (
    select, insert, update, delete, text, 
    and_, or_, func, Table, MetaData
)
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Any, Tuple
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class QueryBuilder:
    """Build and execute various database queries"""
    
    def __init__(self, engine):
        """Initialize query builder with database engine"""
        self.engine = engine
        self.metadata = MetaData()
        self.metadata.reflect(bind=engine)
    
    # ==================== SELECT QUERIES ====================
    
    def select_all(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Select all rows from table
        
        Args:
            table_name: Name of the table
            limit: Maximum number of rows to return
        
        Returns:
            DataFrame with all rows
        """
        try:
            if table_name not in self.metadata.tables:
                raise ValueError(f"Unknown table: {table_name}")
            if limit is not None and not isinstance(limit, int):
                raise ValueError("limit must be an integer")
            query = select(self.metadata.tables[table_name])
            if limit:
                query = query.limit(limit)
            
            df = pd.read_sql(query, self.engine)
            logger.info(f"Selected all rows from {table_name}: {len(df)} rows")
            return df
        
        except Exception as e:
            logger.error(f"Error selecting from {table_name}: {str(e)}")
            raise
    
    def select_columns(self, table_name: str, columns: List[str], limit: Optional[int] = None) -> pd.DataFrame:
        """
        Select specific columns from table
        
        Args:
            table_name: Name of the table
            columns: List of column names
            limit: Maximum number of rows
        
        Returns:
            DataFrame with selected columns
        """
        try:
            if table_name not in self.metadata.tables:
                raise ValueError(f"Unknown table: {table_name}")
            table = self.metadata.tables[table_name]
            unknown = [c for c in columns if c not in table.c]
            if unknown:
                raise ValueError(f"Unknown columns: {unknown}")
            if limit is not None and not isinstance(limit, int):
                raise ValueError("limit must be an integer")
            query = select(*[table.c[c] for c in columns])
            if limit:
                query = query.limit(limit)
            
            df = pd.read_sql(query, self.engine)
            logger.info(f"Selected {len(columns)} columns from {table_name}")
            return df
        
        except Exception as e:
            logger.error(f"Error selecting columns: {str(e)}")
            raise
