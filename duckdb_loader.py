import re
import duckdb
import pandas as pd
from excel_info import ExcelInfo
from duckdb_info import DuckDBInfo

"""
Older loading code for Excel.
See newer module excel_sheet_loader which uses DuckDB SPATIAL.
"""

class DuckDBLoader:
    def __init__(self, duckdb_filepath, excel_filepath, load_sheet_name, column_names_row=1):
        self.xl_info = ExcelInfo(excel_filepath)
        if load_sheet_name in self.xl_info.sheet_names:
            self.load_sheet_name = load_sheet_name
        else:
            raise ValueError(f"Sheet name {load_sheet_name} not in given Excel file!")
        self.excel_filepath = excel_filepath
        self.load_sheet_name = load_sheet_name
        self.duckdb_info = DuckDBInfo(duckdb_filepath)
        self.duckdb_conn = self.duckdb_info.duckdb_conn
        self.column_names_row = column_names_row
        self._original_column_names = self.xl_info.get_row_values(load_sheet_name, column_names_row)
        self._column_names_inferred_types = self.xl_info.get_sheet_column_types(load_sheet_name, column_names_row)
        self._data_row_count = self.xl_info.get_last_row_for_sheet(load_sheet_name) - column_names_row
        self._data_column_count = len(self._original_column_names)
        self._usedrange = self.xl_info.get_sheet_usedrange_address(load_sheet_name)

    @property
    def data_row_count(self):
        return self._data_row_count

    @property
    def data_column_count(self):
        return self._data_column_count
    
    @property
    def original_column_names(self):
        return self._original_column_names
    
    @property
    def column_names_inferred_types(self):
        return self._column_names_inferred_types
    
    @property
    def usedrange(self):
        return self._usedrange
    
    def _normalise_column_names(self):
        column_names_types_normalised = []
        for column_name_original, data_type in self._column_names_inferred_types:
            column_name_normalised = re.sub(r"[^a-z0-9_]", "_", column_name_original.strip().lower())
            column_name_normalised = re.sub(r"[_]+", "_", column_name_normalised).strip("_")
            if column_name_normalised[0].isnumeric():
                column_name_normalised = "_" + column_name_normalised
            column_names_types_normalised.append((column_name_original, 
                                                  data_type, 
                                                  column_name_normalised))
        return column_names_types_normalised
    
    def generate_create_table_ddl(self, table_name):
        column_names_types_normalised = self._normalise_column_names()
        column_names_types = [" ".join([entry[2], entry[1]]) for entry in 
                              column_names_types_normalised]
        table_body = ',\n'.join(column_names_types)
        table_head = f"CREATE TABLE {table_name}(" + "\n"
        create_table_ddl = f"{table_head}{table_body})"
        return create_table_ddl

    def load_sheet_to_typed_duckdb_table(self, table_name):
        create_table_ddl = self.generate_create_table_ddl(table_name)
        if not self.duckdb_info.table_exists(table_name):
            self.duckdb_conn.execute(create_table_ddl)
        sql = f"""INSERT INTO {table_name}
               SELECT * 
               FROM st_read('{self.excel_filepath}', 
                              layer = '{self.load_sheet_name}', 
                              open_options = ['HEADERS=FORCE'])"""
        self.duckdb_conn.execute(sql)

    def load_sheet_to_duckdb(self, new_table_name):
        sql = f"""CREATE OR REPLACE TABLE {new_table_name} AS 
                  SELECT * 
                  FROM st_read('{self.excel_filepath}', 
                              layer = '{self.load_sheet_name}', 
                              open_options = ['HEADERS=FORCE'])"""
        self.duckdb_conn.execute(sql)


if __name__ == "__main__":
    ddb_filepath = "mabs.ddb"
    xl_filepath = "TheraSAbDab_SeqStruc_OnlineDownload.xlsx"
    load_sheet_name = "TheraSAbDab_June24"
    new_table_name = "antibodies"
    ddb_ldr = DuckDBLoader(ddb_filepath, xl_filepath, load_sheet_name)
    ddb_ldr.load_sheet_to_typed_duckdb_table(new_table_name)