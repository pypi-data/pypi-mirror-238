import os
import shutil
from functools import wraps

from qwak.exceptions import QuietError
from qwak.inner.build_logic.interface.build_logger_interface import BuildLogger
from qwak.inner.build_logic.interface.step_inteface import Step


def build_failure_handler(should_fail_build: bool = True):
    def _exception_handler(func):
        @wraps(func)
        def inner_function(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except BaseException as e:
                if should_fail_build and not isinstance(e, QuietError):
                    build_logger: BuildLogger = args[0].build_logger
                    build_logger.error(
                        "Build failed with Exception. See the stack trace above."
                    )
                    cleaning_up_after_build(args[0])
                raise e

        return inner_function

    return _exception_handler


def cleaning_up_after_build(step: Step):
    if os.getenv("QWAK_DEBUG") != "true":
        step.build_logger.debug("Removing Qwak temp artifacts directory")
        shutil.rmtree(step.context.host_temp_local_build_dir, ignore_errors=True)
