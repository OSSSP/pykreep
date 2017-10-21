import logging



class KreepConfig:
    ''' Environment '''
    debug_level = 1

    ''' Paths '''
    exploits_path = 'exploits'
    log_path = '.'
    log_name = 'pykreep.log'


logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}".format(KreepConfig.log_path, KreepConfig.log_name)),
        #logging.StreamHandler()
    ],
    level=logging.DEBUG)
