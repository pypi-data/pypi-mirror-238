import logging as _logging

_logging.addLevelName(99, 'CHARACTOR')
logger = _logging.getLogger('CHARACTOR')
file_handler = _logging.FileHandler('charactor.log', 'w')
formatter = _logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
file_handler.setLevel(99)
logger.addHandler(file_handler)
logger.setLevel(99)
logger.propagate = False

def log(message):
    import inspect
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if module.__name__ == '__main__':
        return logger.log(99, message)
    caller = frame[3]
    return logger.log(99, f'{module.__name__[-module.__name__[::-1].index('.'):]}: {caller}: \n\t\t\t\t\t{message}')
