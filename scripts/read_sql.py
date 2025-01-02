import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float
from sqlalchemy.orm import sessionmaker

def read_opensees_results(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            node_id = int(parts[0])
            displacements = list(map(float, parts[1:]))
            data.append((node_id, *displacements))
    return data

def export_to_sqlite(data, sqlite_db_url, table_name):
    # Create a new SQLite engine
    engine = create_engine(sqlite_db_url)
    metadata = MetaData()

    # Define the columns for the table
    columns = [Column('id', Integer, primary_key=True)]
    for i in range(1, len(data[0])):
        columns.append(Column(f'disp_{i}', Float))

    # Define the table
    results_table = Table(
        table_name, metadata, *columns
    )

    # Create the table in the SQLite database
    metadata.create_all(engine)

    # Insert data into the SQLite table
    with engine.connect() as conn:
        conn.execute(results_table.insert(), [
            {f'disp_{i}': value for i, value in enumerate(row, start=1)}
            for row in data
        ])

    print(f"Exported {len(data)} rows to the SQLite table '{table_name}'.")

# Example usage
if __name__ == "__main__":
    results_file = "/Users/frankie/code/FEA2/examples/temp/stacked_boxes/SLS/results.txt"
    sqlite_db_url = 'sqlite:///opensees_results.db'
    table_name = 'node_displacements'

    # Read OpenSees results
    results = read_opensees_results(results_file)

    # Export results to SQLite
    export_to_sqlite(results, sqlite_db_url, table_name)
