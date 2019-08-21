import logging
from manager import Manager


manager = Manager()


@manager.command
def init_main():
    from services.main import run
    init_logger()
    run()


@manager.command
def init_cli():
    from services.cli import DrawScreen, start_log_monitor
    init_logger()
    drawer = DrawScreen()
    start_log_monitor('sample.log', drawer)
    drawer.main()


def init_logger():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename='sample.log',
        filemode='w',
        format='%(name)s - %(levelname)s : %(message)s',
        level=logging.DEBUG,
    )
    logging.info('logger initiated')


if __name__ == '__main__':
    manager.main()
