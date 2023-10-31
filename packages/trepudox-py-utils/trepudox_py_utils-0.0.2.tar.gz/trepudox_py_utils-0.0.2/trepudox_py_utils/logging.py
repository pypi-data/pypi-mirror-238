"""
trepudox_py_utils
Copyright (C) 2023  Marco Aurelio Queiroz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import colorama
import copy
import os
from datetime import datetime
from logging import LogRecord


class ConsoleLogFormatter(logging.Formatter):
    LOG_COLORS = {
        logging.ERROR: colorama.Fore.RED,
        logging.WARN: colorama.Fore.YELLOW,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.INFO: colorama.Fore.GREEN,
        logging.DEBUG: colorama.Fore.CYAN,
    }

    def format(self, record: LogRecord, *args, **kwargs):
        new_record: LogRecord = copy.copy(record)

        if new_record.levelno in self.LOG_COLORS:
            new_record.levelname = "{colorbegin}{levelname}{colorend}".format(
                colorbegin=self.LOG_COLORS[new_record.levelno],
                levelname=new_record.levelname,
                colorend=colorama.Style.RESET_ALL,
            )

        return super(ConsoleLogFormatter, self).format(new_record, *args, **kwargs)


def configure_logger(level_name: str = "INFO", add_file_handler: bool = False) -> None:
    log_fmt = "[%(asctime)s.%(msecs)03d] %(levelname)s @ %(name)s - (%(threadName)s): %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"

    console_formatter = ConsoleLogFormatter(fmt=log_fmt, datefmt=date_fmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger()
    logger.setLevel(level_name)

    logger.addHandler(console_handler)
    logger.info("ConsoleHandler configurado com sucesso")

    logger.info("Iniciando configuracao do FileHandler")
    if add_file_handler:
        dirpath = "logs/"
        try:
            os.mkdir(dirpath)
        except FileExistsError:
            logger.info("Diretorio 'logs' ja existe, prosseguindo")
        except Exception as e:
            logger.exception("Nao foi possivel configurar o FileHandler", e)
            return

        now = datetime.now()
        filename_date_fmt = date_fmt.replace(" ", "T").replace(":", "-")

        filename = dirpath + now.strftime(filename_date_fmt) + "_log.log"

        with open(filename, "x"):
            file_handler = logging.FileHandler(filename=filename)

            file_handler.setFormatter(logging.Formatter(fmt=log_fmt, datefmt=date_fmt))
            logger.addHandler(file_handler)

            logger.info("FileHandler configurado com sucesso")
