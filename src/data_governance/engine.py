
import duckdb
import pandas as pd
from typing import Optional, Dict, Any

class DataEngine:
    """
    Handles data loading and querying using DuckDB for high performance on large files.
    """
    def __init__(self):
        self.conn = duckdb.connect(database=':memory:')

    def query(self, query: str) -> pd.DataFrame:
        """Executes a SQL query and returns the result as a Pandas DataFrame."""
        return self.conn.execute(query).df()

    def load_csv(self, file_path: str, table_name: str = "dataset"):
        """
        Loads a CSV file into DuckDB. 
        Note: DuckDB can query CSVs directly without loading, but creating a view/table is often cleaner.
        """
        # Create a view directly on the CSV file (Zero-Copy)
        query = f"CREATE OR REPLACE VIEW {table_name} AS SELECT * FROM read_csv_auto('{file_path}')"
        self.conn.execute(query)

    def get_summary_stats(self, table_name: str = "dataset") -> Dict[str, Any]:
        """
        Computes summary statistics entirely within DuckDB (avoiding Pandas OOM).
        """
        # Get column names and types
        schema = self.conn.execute(f"DESCRIBE {table_name}").fetchall()
        stats = {}
        
        count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        stats["row_count"] = count

        for col_name, col_type, _, _, _, _ in schema:
            if col_type in ['BIGINT', 'DOUBLE', 'INTEGER']:
                # Compute numeric stats
                q = f"""
                SELECT 
                    MIN({col_name}), 
                    MAX({col_name}), 
                    AVG({col_name})
                FROM {table_name}
                """
                res = self.conn.execute(q).fetchone()
                stats[col_name] = {
                    "min": res[0],
                    "max": res[1],
                    "avg": res[2]
                }
        return stats

# Global instance
engine = DataEngine()
