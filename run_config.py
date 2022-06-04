import os
import json
import secrets1

DEVELOPMENT_PARAM_FILE = 'development_params.json' 

def set_run_config_map(run_config_file):
    global run_conf_data
    try:
        with open(run_config_file) as fp:
            run_conf_data = json.load(fp)
    except IOError as err:
        print(err)
        return (1)
    return (0)

def generate_database_string():
    if run_conf_data["ID"] == "Development":
        db_con_str = f'mysql+pymysql://' \
                     f'{run_conf_data["DB_USER"]}:' \
                     f'{secrets1.dbpass}@' \
                     f'{run_conf_data["DB_SERVER"]}/' \
                     f'{run_conf_data["DB_NAME"]}'
    elif run_conf_data["ID"] == "Production":
        db_con_str = secrets1.dburi
    return db_con_str