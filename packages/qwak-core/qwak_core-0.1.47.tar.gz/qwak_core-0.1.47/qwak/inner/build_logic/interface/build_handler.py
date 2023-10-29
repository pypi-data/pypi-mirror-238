from abc import abstractmethod, ABC

from qwak.inner.build_logic.constants.step_description import BuildPhase


class BuildRunHandler(ABC):
    @abstractmethod
    def handle_phase_in_progress(self, phase_id: str):
        pass

    @abstractmethod
    def handle_phase_finished_successfully(
        self, phase_id: str, duration_in_seconds: int
    ):
        pass

    @abstractmethod
    def handle_contact_support_error(
        self, build_id: str, phase_id: str, ex: BaseException, duration_in_seconds: int
    ):
        pass

    @abstractmethod
    def handle_remote_build_error(
        self, build_id: str, phase_id: str, ex: BaseException, duration_in_seconds: int
    ):
        pass

    @abstractmethod
    def handle_keyboard_interrupt(
        self, build_id: str, phase_id: str, duration_in_seconds: int
    ):
        pass

    @abstractmethod
    def handle_pipeline_exception(
        self, build_id: str, phase_id: str, ex: BaseException, duration_in_seconds: int
    ):
        pass

    @abstractmethod
    def handle_pipeline_quiet_exception(
        self, build_id: str, phase_id: str, ex: BaseException, duration_in_seconds: int
    ):
        pass

    @staticmethod
    def build_phase_to_human_readable_string(phase_id: str):
        prefix_length = len(f"{BuildPhase.__name__}.")
        return phase_id[prefix_length:].replace("_", " ").capitalize()
