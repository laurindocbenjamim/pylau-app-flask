import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('app/static/logs/logs.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler.setFormatter(file_formatter)

# Create a console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
console_handler.setFormatter(console_formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Log some messages
#logger.debug('This is a debug message')
#logger.info('This is an info message')
#logger.warning('This is a warning message')
#logger.error('This is an error message')
#logger.critical('This is a critical message')


def get_message(e, type='debug'):
    if type == 'debug':
        code = e.code
        name = e.name
        description = e.description
        logger.debug('\n===============================================================\
            \nCODE:%s NAME:%s \
            \n _________________________DESCRIPTION___________________________\n %s ', code, name, description)
    elif type == 'info':
        code = e.code
        name = e.name
        description = e.description
        logger.info('\n===============================================================\
            \nCODE:%s \nNAME:%s \
            \n _________________________DESCRIPTION___________________________\n %s ', code, name, description)
    elif type == 'warn':
        code = e.code
        name = e.name
        description = e.description
        logger.warning('\n===========================================================================================\
            \nCODE:%s \nNAME:%s \
            \n _________________________DESCRIPTION___________________________\n %s ', code, name, description)
    elif type == 'error':
        code = e.code
        name = e.name
        description = e.description
        logger.error('\n===============================================================\
            \nCODE:%s \nNAME:%s \
            \n _________________________DESCRIPTION___________________________\n %s ', code, name, description)
    elif type == 'critical':
        code = e.code
        name = e.name
        description = e.description
        logger.critical('\n===============================================================\
            \nCODE:%s \nNAME:%s \
            \n _________________________DESCRIPTION___________________________\n %s ', code, name, description)