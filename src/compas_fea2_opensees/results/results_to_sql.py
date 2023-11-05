import os
from math import sqrt
from compas_fea2.results.sql_wrapper import (
    create_connection_sqlite3,
    create_field_description_table_sqlite3,
    create_field_table_sqlite3,
    insert_field_description_sqlite3,
    insert_field_results_sqlite3,
)


def read_results_file(database_path, database_name, field_output):
    """Read the .out results file and convert it to an SQLite db.

    Parameters
    ----------
    database_path : path
        Path to the folder where the sqlite database will be created
    database_name : str
        Name of the database
    field_output : :class:`compas_fea2.problem.FieldOutput`
        FieldOutput object containing the nodes and/or elemente outputs to extract.
    """
    results = {}

    field_info = {
        "u": {"num_of_comp": 3,
              "description_table": [['Spatial displacement', 'U1 U2 U3'], ['magnitude']],
              "field_table": ['U1', 'U2', 'U3', 'magnitude']},
        "rf": {"num_of_comp": 3,
              "description_table": [['Reaction forces', 'RF1 RF2 RF3'], ['magnitude']],
              "field_table": ['RF1', 'RF2', 'RF3', 'magnitude']},
        "rm": {"num_of_comp": 3,
              "description_table": [['Reaction moments', 'M1 M2 M3'], ['magnitude']],
              "field_table": ['RM1', 'RM2', 'RM3', 'magnitude']},
        "s": {"num_of_comp": 6,
              "description_table": [['Stresses', 'S11 S22 S12 M11 M22 M12'], [None]],
              "field_table": ['S11', 'S22', 'S12', 'M11', 'M22', 'M12', 'None']},
        "sf": {"num_of_comp": 6,
              "description_table": [['Section Forces', 'F11 F22 F33 M11 M22 M33'], [None]],
              "field_table": ['F11', 'F22', 'F33', 'M11', 'M22', 'M33', 'None']},
    }

    if not field_output.node_outputs and not field_output.element_outputs:
        print('WARNING - No field outputs found! Did you add an output request before running the analysis?')

    if not field_output.node_outputs:
        field_output._node_outputs = []
    if not field_output.element_outputs:
        field_output._element_outputs = []

    for field in field_output.node_outputs+field_output.element_outputs:
        field = field.lower()
        if field not in field_info:
            print(f'WARNING - the output request {field.upper()} is either not implemented or not available.')
            continue
        number_of_components = field_info[field]["num_of_comp"]
        results.setdefault(field, {})

        if field.upper() in field_output.node_outputs:
            output_set = field_output.nodes_set or range(0, list(field_output.model.parts)[0].nodes_count+1)
        else:
            output_set = field_output.elements_set or range(0, list(field_output.model.parts)[0].elements_count+1)

        filepath = os.path.join(database_path, '{}.out'.format(field.lower()))
        if not os.path.exists(filepath):
            print(f"file {filepath} not found. Results not extracted.")
            continue
        with open(filepath, 'r') as f:
            lines = f.readlines()
            # take the last analysis step and ignore the time stamp (first value)
            data = [float(i) for i in lines[-1].split(' ')[1:]]

        results[field]=[]
        for c, value in enumerate(output_set):
            part = list(field_output.model.parts)[0]
            step = field_output.step

            if field in field_output.node_outputs:
                #fea2_object = part.find_node_by_key(value)
                object_properties = [step.name, part.name, 'node', 'nodal', value]
            else:
                #fea2_object = part.find_element_by_key(value)
                object_properties = [step.name, part.name, 'element', 'nodal', value]

            components_results = data[c*number_of_components:c*number_of_components+number_of_components]

            #TODO change this to account for different invariants (Mieses, PSmax/min, etc)
            invariants=[]
            if not field_info[field]['description_table'][1][0]:
                invariants=[0]
            elif 'magnitude' in field_info[field]['description_table'][1]:
                u, v, w = components_results
                magnitude = sqrt(u**2 + v**2 + w**2)
                invariants.append(magnitude)
            else:
                raise ValueError('Invariant not supported')


            results[field].append(object_properties+components_results+invariants)

        print('***** {0}.out data loaded *****'.format(filepath))



    database = os.path.join(database_path, f'{database_name}-results.db')

    if os.path.exists(database):
        os.remove(database)

    with create_connection_sqlite3(database) as conn:
        create_field_description_table_sqlite3(conn)
        for field_name, field_data in results.items():
            insert_field_description_sqlite3(
                conn,
                field_name.upper(),
                *field_info[field_name]['description_table'][0],
                *field_info[field_name]['description_table'][1]
                )
            create_field_table_sqlite3(
                conn,
                field_name.upper(),
                field_info[field_name]['field_table']
                )
            for result_data in field_data:
                insert_field_results_sqlite3(conn, field_name.upper(), result_data)
        conn.commit()

