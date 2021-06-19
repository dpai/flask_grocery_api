import json

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
                     f'pai123@' \
                     f'{run_conf_data["DB_SERVER"]}/' \
                     f'{run_conf_data["DB_NAME"]}'

    return db_con_str