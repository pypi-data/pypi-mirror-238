import os

import logbook
from logbook.more import ColorizedStderrHandler


def sys_log_format(record, handler):
    log = "[{date}][{level}][{filename}][{lineno}]{msg}".format(
        date=record.time,  # 日志时间
        level=record.level_name,  # 日志等级
        filename=os.path.split(record.filename)[-1],  # 文件名
        func_name=record.func_name,  # 函数名
        lineno=record.lineno,  # 行号
        msg=str(record.message)  # 日志内容
    )
    return log


class ShareLogger:
    logbook.set_datetime_format("local")
    logger = logbook.Logger("algo_bus", level=logbook.DEBUG)
    log_std = ColorizedStderrHandler(bubble=False)
    log_std.formatter = sys_log_format
    logger.handlers.append(log_std)


def get_algo_bus_logger():
    return ShareLogger.logger
