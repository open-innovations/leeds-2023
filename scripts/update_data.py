from util.logger import logging

import metrics.volunteers.process


def main():
    try:
        metrics.volunteers.process.update()
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    main()
