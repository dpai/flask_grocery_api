import sys
import os
from pathlib import Path
import run_config

sys.path.append('./grocery_api') ## I put this so that json flask_config params does not need it.

if len(sys.argv) != 2:
    run_config_file = Path('config/') / run_config.DEVELOPMENT_PARAM_FILE
else:
    run_config_file = Path(sys.argv[1])

if run_config.set_run_config_map(run_config_file) == 1:
    print(f"Error reading configuration file {run_config_file}.. exiting")
    exit(1)

db_con_str = run_config.generate_database_string()
#print(db_con_str)
os.environ['DATABASE_URI'] = db_con_str

from grocery_api.app import create_app

application = create_app(
    config_object=run_config.run_conf_data['FLASK_CONFIG'])


if __name__ == '__main__':
    application.run()


# import platform


# from pathlib import Path
# import logging.config

# import main_config
# from flask_server_template import create_app

# # Global Variable Initialization - BEGIN

# # Global Variable Initialization - END

# # Main - START
# print('platform.python_version(): ', platform.python_version())

# if len(sys.argv) != 2:
#     run_config_file = Path('config/') / main_config.RUN_PARAMS_DEFAULT_FILENM
# else:
#     run_config_file = Path(sys.argv[1])

# if main_config.set_run_config_map(run_config_file) == 1:
#     print('unable to read configuration file, exiting')
#     exit(1)
# db_con_str = main_config.get_db_con_str()


# # initialize the logger
# logging.config.fileConfig(main_config.run_conf_data['LOGGER_CONFIG'])
# log = logging.getLogger('pythonLogger') # This handler comes from config>logger.conf
# log.debug('sys.version: ' + sys.version)
# log.info('__name__: ' + __name__)
# log.info('sys.path: ' + str(sys.path))
# # Flask Code - BEGIN
# """App entry point."""
# try:
#     app = create_app(main_config.run_conf_data['FLASK_CONFIG'])
#     if __name__ == "__main__":
#         app.run(host='0.0.0.0')
# except RuntimeError as err:
#     log.error(str(err))
#     exit(1)
# # Flask Code - END

# # Main - END