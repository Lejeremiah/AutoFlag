import os
import logging

log_file_name = 'submit_flag.log'
log_colors_config = {
    'DEBUG': 'green',  # cyan white
    'INFO': 'white',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'cyan',
}

def init_log_file():
    global log_file_name
    if not os.path.exists('logs'):
        os.mkdir('logs')
    log_file_name = 'logs/submit_flag.log'

def start_log_file():
    import colorlog
    global log_file_name,log_colors_config
    init_log_file()


    logging.basicConfig(level=logging.INFO,
                        filename=log_file_name,
                        format="[%(asctime)s.%(msecs)03d] %(pathname)s (%(lineno)d) - [%(levelname)s] :\n%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(colorlog.ColoredFormatter(
        fmt="%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s (%(lineno)d) - [%(levelname)s] : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=log_colors_config
    ))
    logging.getLogger().addHandler(sh)
start_log_file()