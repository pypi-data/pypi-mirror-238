from loguru import logger
import sys
import os

logger.remove()
logger.add('log_{time:MMDDYY-HH_mm_ss}.log',
           format='[{time:MM/DD/YYYY HH:mm:ss}] {level: <8}| <lvl>{message}</lvl>')

logger.add(sys.stdout,
           format='[{time:MM/DD/YYYY HH:mm:ss}] {level: <8}| <lvl>{message}</lvl>')

logger.opt(colors=True)
logger.success('WELCOME TO METABODIRECT')
logger.info('Command: {}', sys.argv)
logger.info('Analysis starting on {}', 'heeeee')
logger.info('Can I do '
            'two lines?')
logger.debug(f'Results will be saved in directory: {os.getcwd()}')
logger.warning('Analysis starting on {} and {}', 5, '2')
logger.error('Analysis starting on {}', 'heeeee')
logger.critical('Analysis starting on {}', 'heeeee')
logger.level("PROCESS", no=38, color="<magenta>", icon="@")
logger.log("PROCESS", "Here we go!")
