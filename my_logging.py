from global_settings import LOGS_FILE_LOCATION

from datetime import datetime

def write_logs(func):
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        start_time = datetime.now()
        result = func(*args, **kwargs)
        exec_time = datetime.now() - start_time
        if issubclass(type(result), Exception):
            with open(f"{LOGS_FILE_LOCATION}/logs.txt", 'a') as logs_file:
                logs_file.write(f'{function_name} | {exec_time} | {datetime.now()}| {result} \n')
        return result
    return wrapper




