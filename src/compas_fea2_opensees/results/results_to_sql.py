"""
This script reads results from .out files generated by a finite element analysis and converts them into an SQLite database.
It supports various types of field outputs such as displacements, reaction forces, reaction moments, stresses, and section forces.
The script creates tables in the SQLite database to store these results and their descriptions.
"""

import os


def read_results_file(connection, field_output):
    """
    Read the .out results file and convert it to a dictionary.

    Parameters
    ----------
    database_path : path
        Path to the folder where the sqlite database will be created
    database_name : str
        Name of the database
    field_output : :class:`compas_fea2.problem.FieldOutput`
        FieldOutput object containing the nodes and/or element outputs to extract.
    """

    model = field_output.model
    step = field_output.step
    field_name = field_output.field_name
    database_path = field_output.problem.database_path

    results = []
    with open(os.path.join(database_path, f"{field_name}.out"), "r") as f:
        lines = f.readlines()
        for line in lines:
            columns = line.split()

            key = int(columns[0])  # Convert the first column to int
            member = getattr(model, field_output._results_func)(key)[0]

            # FIXME: this does not take into account the integration points
            # which can be different from element implementation to element implementation
            values = list(map(float, columns[1:]))
            if len(values) < len(field_output.components_names):
                values = values + [0.0] * (len(field_output.components_names) - len(values))
            elif len(values) > len(field_output.components_names):
                values = values[: len(field_output.components_names)]
            else:
                values = values

            results.append([member.key] + [step.name, member.part.name] + values)

    field_output.create_table_for_output_class(connection, results)


def process_modal_shapes(connection, step):
    database_path = step.problem.database_path
    model = step.model

    eigenvalues = []
    with open(os.path.join(database_path, "eigenvalues.out"), "r") as f:
        lines = f.readlines()
        for line in lines:
            eigenvalues.append(line.split())

    eigenvectors = []
    with open(os.path.join(database_path, "eigenvectors.out"), "r") as f:
        lines = f.readlines()
        for line in lines:
            eigenvectors.append(line.split())

    cursor = connection.cursor()

    # Create table for eigenvalues
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS eigenvalues (
        id INTEGER PRIMARY KEY,
        step TEXT,
        mode INTEGER,
        lambda REAL,
        omega REAL,
        freq REAL,
        period REAL
        )
    """
    )

    # Insert eigenvalues into the database
    for eigenvalue in eigenvalues:
        cursor.execute(
            """
        INSERT INTO eigenvalues (step, mode, lambda, omega, freq, period)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            [step.name] + eigenvalue,
        )
    connection.commit()

    for i, eigenvector in enumerate(eigenvectors):
        if len(eigenvector) < 8:
            eigenvector = eigenvector + [0.0] * (8 - len(eigenvector))
        node = model.find_node_by_inputkey(int(eigenvector[1]))[0]
        eigenvectors[i] = [eigenvector[0], step.name, node.part.name, node.input_key] + eigenvector[2:]

    # Create table for modal shapes
    cursor.execute(
        f"""
    CREATE TABLE IF NOT EXISTS eigenvectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mode INTEGER,
        step TEXT,
        part TEXT,
        input_key INTEGER,
        {",\n".join([f"dof_{c+1} REAL" for c in range(6)])}
        )
    """
    )
    # Insert modal shape data into the database
    for eigenvector in eigenvectors:
        cursor.execute(
            f"""
        INSERT INTO eigenvectors (mode, step, part, input_key, {", ".join([f"dof_{c+1}" for c in range(6)])})
        VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?, ?)
        """,
            eigenvector,
        )

    connection.commit()

    print(f"Modal shapes and eigenvalues successfully saved to {database_path}")
