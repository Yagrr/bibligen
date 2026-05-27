import os

def _debug_log_fn_decorator(fn):
    """
    Function wrapper for logging when a function is called.
    Usage: Decorate function with @_debug_log and pass logging level from the
    `logging` module (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    def _debug_log_fn_wrapper(*args, **kwargs):
        import inspect
        import logging

        PATH_SRC = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        PATH_LOG = os.path.join(PATH_SRC, ".debug.log")
        logging.basicConfig(
            filename=PATH_LOG,
            filemode="a",
            format="%(asctime)s %(message)s",
            datefmt="%m/%d%Y %I:%M:%S %p",
            encoding="utf-8",
            level=logging.DEBUG,
        )
        logging.info(f"Calling {fn.__name__}\n args: {args}\n kwargs: {kwargs}\n members:{inspect.getmembers(fn)}")
        fn_result = fn(*args, **kwargs)
        logging.info(f"return: {fn_result}")
        return fn_result
    return _debug_log_fn_wrapper
