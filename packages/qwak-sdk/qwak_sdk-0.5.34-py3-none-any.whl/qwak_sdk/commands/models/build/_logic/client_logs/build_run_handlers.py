from contextlib import contextmanager
from logging import Logger
from pathlib import Path

from qwak.exceptions import QwakException
from qwak.inner.build_logic.interface.build_phase import BuildPhase
from qwak.inner.build_logic.interface.phase_run_handler import PhaseRunHandler
from qwak.inner.build_logic.phases.phases_pipeline import PhasesPipeline
from yaspin import yaspin

from qwak_sdk.tools.colors import Color
from .messages import (
    FAILED_CONTACT_QWAK_SUPPORT,
    FAILED_CONTACT_QWAK_SUPPORT_PROGRAMMATIC,
)
from .trigger_build_logger import TriggerBuildLogger
from .utils import zip_logs


class CLIPhaseRunHandler(PhaseRunHandler):

    def __init__(self, python_logger: Logger, log_path: Path, verbose: int, json_logs: bool):
        self.sp = None
        self.build_logger = None
        self.log_path = str(log_path)
        self.python_logger = python_logger
        self.json_logs = json_logs
        self.verbose = verbose

    @contextmanager
    def handle_current_phase(self, phase: PhasesPipeline):
        self.build_logger = TriggerBuildLogger(
            self.python_logger,
            prefix="" if self.json_logs else phase.build_phase.description,
            build_phase=phase.build_phase,
        )
        show = (self.verbose == 0 and not self.json_logs)
        text = phase.build_phase.description
        if show:
            try:
                with yaspin(text=text, color="blue", timer=True).bold as sp:
                    self.sp = sp
                    self.build_logger.set_spinner(sp)
                    yield
            finally:
                pass
        else:
            yield

    def handle_phase_in_progress(self, build_phase: BuildPhase):
        logger = self.build_logger or self.python_logger
        logger.debug(
            f"Build phase in progress: {build_phase.name}"
        )

    def handle_phase_finished_successfully(
        self, build_phase: BuildPhase, duration_in_seconds: int
    ):
        if self.sp:
            self.sp.ok("✅")

        logger = self.build_logger or self.python_logger
        logger.debug(
            f"Phase successfully finished: {build_phase.name} after {duration_in_seconds} seconds"
        )

    def __report_failure(self, build_phase: BuildPhase, duration_in_seconds: int):
        logger = self.build_logger or self.python_logger
        logger.debug(
            f"Build phase failed: {build_phase.name} after {duration_in_seconds} seconds"
        )

    def handle_contact_support_error(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        print(f"\n{ex}")
        print(
            FAILED_CONTACT_QWAK_SUPPORT.format(
                build_id=build_id,
                log_file=Path(self.log_path).parent / build_id,
            )
        )
        zip_logs(log_path=self.log_path, build_id=build_id)
        self.__report_failure(build_phase, duration_in_seconds)
        exit(1)

    def handle_remote_build_error(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        if self.sp:
            self.sp.fail("💥")
            print(f"\n{Color.RED}{ex}")
        else:
            print(f"\n{ex}")
        self.__report_failure(build_phase, duration_in_seconds)
        exit(1)

    def handle_keyboard_interrupt(
        self, build_id: str, build_phase: BuildPhase, duration_in_seconds: int
    ):
        print(f"\n{Color.RED}Stopping Qwak build (ctrl-c)")
        zip_logs(log_path=self.log_path, build_id=build_id)
        self.__report_failure(build_phase, duration_in_seconds)
        exit(1)

    def handle_pipeline_exception(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        if self.sp:
            self.sp.fail("💥")
            print(f"\n{Color.RED}{ex}")
        zip_logs(
            log_path=self.log_path,
            build_id=build_id,
        )
        self.__report_failure(build_phase, duration_in_seconds)
        exit(1)

    def handle_pipeline_quiet_exception(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        if self.sp:
            self.sp.ok("‼️")
            print(f"\n{Color.RED}{ex}")
        self.__report_failure(build_phase, duration_in_seconds)
        exit(1)


class ProgrammaticPhaseRunHandler(PhaseRunHandler):
    def __init__(self, python_logger: Logger, verbose: int, json_logs: bool):
        self.build_logger = None
        self.python_logger = python_logger
        self.json_logs = json_logs
        self.verbose = verbose

    @contextmanager
    def handle_current_phase(self, phase: PhasesPipeline):
        self.build_logger = TriggerBuildLogger(
            self.python_logger,
            prefix="" if self.json_logs else phase.build_phase.description,
            build_phase=phase.build_phase,
        )
        yield

    def handle_phase_in_progress(self, build_phase: BuildPhase):
        logger = self.build_logger or self.python_logger
        logger.debug(
            f"Build phase in progress: {build_phase.name}"
        )

    def handle_phase_finished_successfully(
        self, build_phase: BuildPhase, duration_in_seconds: int
    ):
        logger = self.build_logger or self.python_logger
        logger.debug(
            f"Phase successfully finished: {build_phase.name} after {duration_in_seconds} seconds"
        )

    def __report_failure(self, build_phase: BuildPhase, duration_in_seconds: int):
        logger = self.build_logger or self.python_logger
        logger.debug(
            f"Build phase failed: {build_phase.name} after {duration_in_seconds} seconds"
        )

    def handle_contact_support_error(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        print(
            FAILED_CONTACT_QWAK_SUPPORT_PROGRAMMATIC.format(
                build_id=build_id,
            )
        )
        self.__report_failure(build_phase, duration_in_seconds)
        raise QwakException(str(ex))

    def handle_keyboard_interrupt(
        self, build_id: str, build_phase: BuildPhase, duration_in_seconds: int
    ):
        self.__report_failure(build_phase, duration_in_seconds)

    def handle_pipeline_exception(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        self.__report_failure(build_phase, duration_in_seconds)
        raise QwakException(str(ex))

    def handle_pipeline_quiet_exception(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        self.__report_failure(build_phase, duration_in_seconds)

    def handle_remote_build_error(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        self.handle_pipeline_exception(build_id, build_phase, ex, duration_in_seconds)
