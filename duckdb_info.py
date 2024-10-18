import os
import duckdb
import json

"""
All interaction with the DuckDB database is mediated by this module.

"""
class DuckDBInfo:
    def __init__(self, duckdb_filepath):
        self.duckdb_filepath = duckdb_filepath
        self._is_new_duckdb_file = not self._db_exists()
        self._conn = duckdb.connect(self.duckdb_filepath)
        self._prep_conn()
        self._db_name = os.path.splitext(os.path.basename(self.duckdb_filepath))[0]
        self._table_names = None
        self._view_names = None
        self._view_and_table_names = None

    def _prep_conn(self):
        """Load the extension required for Excel interaction.
        """
        self._conn.install_extension("spatial")
        self._conn.load_extension("spatial")

    @property
    def is_new_duckdb_file(self):
        """Has an empty DuckDB database been newly created?
        """
        return self._is_new_duckdb_file
    
    @property
    def db_name(self):
        return self._db_name
    
    def _db_exists(self):
        if os.path.isfile(self.duckdb_filepath):
            return True
        return False
    
    @property
    def table_names(self):
        sql = f"SELECT table_name FROM duckdb_tables WHERE database_name = '{self.db_name}'"
        self._table_names = [row[0] for row in self._conn.execute(sql).fetchall()]
        return self._table_names

    @property
    def view_names(self):
        sql = """SELECT view_name 
                  FROM duckdb_views() 
                  WHERE schema_name = 'main' and internal = false"""
        self._view_names = [row[0] for row in self._conn.execute(sql).fetchall()]
        return self._view_names
    
    @property
    def duckdb_conn(self):
        return self._conn

    @property
    def view_and_table_names(self):
        """A list of tables and views in the current database.
        """
        _view_and_table_names =self.table_names[:]
        view_names =self.view_names[:]
        _view_and_table_names.extend(view_names)
        self._view_and_table_names = _view_and_table_names
        return self._view_and_table_names
  
    def table_exists(self, table_name):
        if table_name in self.table_names:
            return True
        return False
    
    def _is_json(self, text):
        try:
            json.loads(text)
            return True
        except json.decoder.JSONDecodeError:
            return False

    def add_json_comment_to_table(self, table_name, table_comment_text):
        """Add table comment as JSON text to a table."""
        sql = f"COMMENT ON TABLE {table_name} IS $${table_comment_text}$$"
        if self._is_json(table_comment_text) and self.table_exists(table_name):
            try:
                self.duckdb_conn.execute(sql)
            except Exception as ex:
                raise ex

    def view_exists(self, view_name):
        if view_name in self.view_names:
            return True
        return False
  
    def get_table_comment(self, table_name):
        sql = f"SELECT comment FROM duckdb_tables() WHERE table_name = '{table_name}'"
        if not self.table_exists(table_name):
            return f"Table {table_name} does not exists!"
        table_comment = self._conn.execute(sql).fetchone()[0]
        if not table_comment:
            table_comment = f"No comment set for table '{table_name}'."
        return table_comment
    
    def get_view_comment(self, view_name):
        sql = f"SELECT comment FROM duckdb_views() WHERE view_name = '{view_name}'"
        if not self.view_exists(view_name):
            return f"View {view_name} does not exists!"
        view_comment = self._conn.execute(sql).fetchone()[0]
        if not (view_comment and self.table_exists(view_name)):
            view_comment = f"No comment set for view '{view_name}'."
        return view_comment
    
    def get_column_comment(self, table_name, column_name):
        """Return the user-supplied comment string for a given table column or 
        a set string indicating that no comment has been set for that table column"""
        sql = f"""SELECT comment 
                  FROM duckdb_columns 
                  WHERE table_name = '{table_name}'
                    AND column_name = '{column_name}'"""
        result = self._conn.execute(sql).fetchone()[0]
        if result:
            return result
        return f"No comment set for column '{table_name}.{column_name}'."
    
    def update_table_json_comment(self, table_name, comment_dict):
        """Add the comment as JSON to a JSON list for the given table.
        """
        table_comment_current_text = self.get_table_comment(table_name)
        table_comment_current_dict = json.loads(table_comment_current_text)
        updates = table_comment_current_dict.get("updates", [])
        updates.append(comment_dict)
        table_comment_current_dict["updates"] = updates
        table_comment_updated_text = json.dumps(table_comment_current_dict)
        self.overwrite_table_comment(table_name, table_comment_updated_text)
        return f"Table '{table_name}' comment is updated."
    
    def overwrite_table_comment(self, table_name, table_comment):
        """Set a user-supplied comment for a given table that overwrites any pre-existing
        comment for that table."""
        sql = f"COMMENT ON TABLE {table_name} IS $${table_comment}$$"
        self._conn.execute(sql)

    def update_view_comment(self, view_name, view_comment):
        """Set a user-supplied comment for a given view."""
        sql = f"COMMENT ON VIEW {view_name} IS $${view_comment}$$"
        self._conn.execute(sql)    

    def update_column_comment(self, table_name, column_name, column_comment):
        """Add the given text description comment to the specified table column."""
        sql = f"COMMENT ON COLUMN {table_name}.{column_name} IS $${column_comment}$$"
        self._conn.execute(sql)

    def get_table_columns_types(self, table_name):
        sql = f"""SELECT column_name, data_type 
                  FROM information_schema.columns 
                  WHERE table_name = '{table_name}'"""
        results = self._conn.execute(sql).fetchall()
        return results
    
    def get_table_column_names(self, table_name):
        table_columns_types = self.get_table_columns_types(table_name)
        column_names = [column_name for column_name, _ in table_columns_types]
        return column_names
    
    def get_table_column_types(self, table_name):
        """For a given table name, return a list of itss column types.
        """
        table_columns_types = self.get_table_columns_types(table_name)
        column_types = [column_type for _, column_type in table_columns_types]
        return column_types
    
    def get_view_column_names(self, view_name):
        pass

    def get_table_rows(self, table_name, row_count_limit):
        sql = f"SELECT * FROM {table_name} LIMIT {row_count_limit}"
        result_set = self._conn.execute(sql).fetchall()
        return result_set

    def get_table_type(self, table_name):
        """Given a table or view name, determine if it is a table or view.
        """
        sql = f"SELECT type FROM sqlite_master WHERE name = '{table_name}'"
        result = self._conn.execute(sql).fetchone()
        if result:
            return result[0]
        return None
    
    def get_table_row_count(self, table_name):
        """The current row count for a given table or view."""
        sql = f"SELECT COUNT(*) FROM {table_name}"
        row_count = self._conn.execute(sql).fetchone()[0]
        return row_count

    def drop_table_if_exists(self, table_name):
        """Delete a table if it exists."""
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.duckdb_conn.execute(sql)

    def get_table_info_summary(self, table_name):
        """Create an return a dictionary to summarise information on a given table or view.
        """
        table_info_summary = dict()
        table_type = self.get_table_type(table_name)
        table_comment = None
        if table_type == "table":
            table_comment = self.get_table_comment(table_name)
        elif table_type == "view":
            table_comment = self.get_view_comment(table_name)
        table_columns_types = self.get_table_columns_types(table_name)
        table_row_count = self.get_table_row_count(table_name)
        table_info_summary["table_name"] = table_name
        table_info_summary["table_type"] = table_type
        table_info_summary["table_comment"] = table_comment
        table_info_summary["table_row_count"] = table_row_count
        table_info_summary["table_columns_types"] = table_columns_types
        return table_info_summary
    
if __name__ == "__main__":
    parent_dirpath = os.path.join(os.getcwd(), "docs")
    duckdb_filepath = os.path.join(parent_dirpath, "WC2022.ddb")
    db_info = DuckDBInfo(duckdb_filepath)
    table_name = "country_managers"
    print(db_info.get_table_comment(table_name))
