import sys
import os
from pathlib import Path
import run_config
import logging.config

# # Global Variable Initialization - BEGIN

# # Global Variable Initialization - END

# # Main
sys.path.append('./grocery_api') ## I put this so that json flask_config params [Line 31- create_app]does not need it.

if len(sys.argv) != 2:
    run_config_file = Path('config/') / run_config.DEVELOPMENT_PARAM_FILE
else:
    run_config_file = Path(sys.argv[1])

if run_config.set_run_config_map(run_config_file) == 1:
    print(f"Error reading configuration file {run_config_file}.. exiting")
    exit(1)

# # initialize the logger
logging.config.fileConfig(run_config.run_conf_data['LOGGER_CONFIG'])
log = logging.getLogger('pythonLogger') # This handler comes from config>logger.conf
log.debug('sys.version: ' + sys.version)
log.info('__name__: ' + __name__)
log.info('sys.path: ' + str(sys.path))

db_con_str = run_config.generate_database_string()
#print(db_con_str)
os.environ['DATABASE_URI'] = db_con_str

from grocery_api.app import create_app

application = create_app(
    config_object=run_config.run_conf_data['FLASK_CONFIG'])


if __name__ == '__main__':
    try:
        application.run()
    except RuntimeError as err:
        log.error(str(err))
        exit(1)

# # Main End