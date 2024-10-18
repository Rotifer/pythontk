import duckdb
import os
import json
from datetime import datetime as dt
from excel_info import ExcelInfo
from duckdb_info import DuckDBInfo

"""
Uses the DuckDB SPATIAL library to upload sheet contents to a DuckDB database.

"""
class ExcelSheetLoader:
    def __init__(self, duckdb_filepath, excel_filepath):
        self.duckdb_filepath = duckdb_filepath
        self.excel_filepath = excel_filepath
        self._conn = duckdb.connect(self.duckdb_filepath)
        self.duckdb_info = DuckDBInfo(duckdb_filepath)
        self._prep_conn()
        self._excel_info = ExcelInfo(excel_filepath)

    def _prep_conn(self):
        """Load the extension required for Excel interaction.
        """
        self._conn.install_extension("spatial")
        self._conn.load_extension("spatial")
    
    @property
    def sheet_names(self):
        return self._excel_info.sheet_names
    
    @property
    def wb_properties(self):
        return self._excel_info.extract_workbook_properties()

    def make_and_load_new_table(self, table_name, load_sheet_name):
        """Given a database table name and an Excel sheet name, create a new database table of
        that name and load the sheet data into it using the first row of the sheet data as column names.
        """
        sql = f"""CREATE TABLE {table_name} AS
            SELECT * 
            FROM st_read('{self.excel_filepath}',
                        layer = '{load_sheet_name}',
                        open_options = ['HEADERS=FORCE', 'FIELD_TYPES=AUTO'])"""
        self._conn.execute(sql)

    def load_sheet_to_ddb(self, load_sheet_name, description, table_name=None):
        """Load the sheet into a table and return the inserted row count for the table. 
        
        If no table name is given, the new table is given the sheet name.
        If the table already exists, an error is thrown.
        """
        if not table_name:
            table_name = load_sheet_name
        try:
            self.make_and_load_new_table(table_name, load_sheet_name)
            table_creation_date = dt.today().strftime("%Y-%m-%d")
            comment_dict = self.wb_properties.copy()
            comment_dict["sheet_name"] = load_sheet_name
            comment_dict["filepath"] = self.excel_filepath
            comment_dict["description"] = description
            comment_dict["table_creation_date"] = table_creation_date
            comment_dict["updates"] = []
            table_comment = json.dumps(comment_dict)
            self.duckdb_info.add_json_comment_to_table(table_name, table_comment)
        except Exception as ex:
            raise ex
        loaded_row_count = self.duckdb_info.get_table_row_count(table_name)
        return loaded_row_count  
        
    def append_sheet_data_to_table(self, append_sheet_name, target_table_name):
        """Append sheet data to a given table if the table exists and if the columns types and 
        their order in the sheet to upload are compatible with those of the target table"""
        if not self.duckdb_info.table_exists(target_table_name):
            raise Exception(f"Table name {target_table_name} does not exist!")
        tmp_table_name = f"tmp_{append_sheet_name}_"
        self.make_and_load_new_table(tmp_table_name, append_sheet_name)
        append_row_count = self.duckdb_info.get_table_row_count(tmp_table_name)
        column_types_tmp = self.duckdb_info.get_table_column_types(tmp_table_name)
        column_types_target = self.duckdb_info.get_table_column_types(target_table_name)
        sql_append = f"INSERT INTO {target_table_name} SELECT * FROM {tmp_table_name}"
        append_date = dt.today().strftime("%Y-%m-%d")
        comment_update_dict = {"operation": "append",
                               "row_count": append_row_count,
                               "operation_date": append_date}
        comment_update_json = json.dumps(comment_update_dict)
        if column_types_tmp == column_types_target:
            try:
                self._conn.execute(sql_append)
                self.duckdb_info.update_table_json_comment(target_table_name, comment_update_json)
            finally:
                self.duckdb_info.drop_table_if_exists(tmp_table_name)
        else:
            raise Exception("Unable to append due to to incompatible column types!")
        return append_row_count

    
if __name__ == "__main__":
    parent_dirpath = os.path.join(os.getcwd(), "docs")
    duckdb_filepath = os.path.join(parent_dirpath, "WC2022.ddb")
    excel_filepath = os.path.join(parent_dirpath, "WC2022.xlsx")
    sheet_name = "country_managers"
    xl_sh_ldr = ExcelSheetLoader(duckdb_filepath, excel_filepath)
    loaded_row_count = xl_sh_ldr.load_sheet_to_ddb(sheet_name,"The names of the managers of each country taking part in the WC2022 finals.")
    print(loaded_row_count)
    append_row_count = xl_sh_ldr.append_sheet_data_to_table(sheet_name, sheet_name)
    print(append_row_count)
