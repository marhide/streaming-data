import src.main
from src.setup import set_env_vars, set_secret_env_vars

set_env_vars()
set_secret_env_vars('test', 'test_queue_name')

