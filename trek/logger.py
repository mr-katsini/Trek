import structlog

import datetime


def timestamper(_, __, event_dict):
    # event_dict["time"] = datetime.datetime.now().isoformat()
    return event_dict


structlog.configure(
    processors=[
        timestamper,
        # structlog.processors.KeyValueRenderer(),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.BoundLogger,
    # or OrderedDict if the runtime's dict is unordered (e.g. Python <3.6)
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False
)

logger = structlog.get_logger()
