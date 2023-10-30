import logging
from typing import List

_logger = logging.getLogger(__name__)

CLASSIQ_SLACK_COMMUNITY_LINK = (
    "\nIf you need further assistance, please reach out on our Community Slack channel at: https://short.classiq.io/join-slack"
    "\nIf the error persists feel free to open a ticket at: https://short.classiq.io/support"
)


class ClassiqError(Exception):
    def __init__(self, message: str) -> None:
        message_with_link = message + CLASSIQ_SLACK_COMMUNITY_LINK
        super().__init__(message_with_link)


class ClassiqExecutionError(ClassiqError):
    pass


class ClassiqMissingOutputFormatError(ClassiqError):
    def __init__(self, missing_formats: List[str]) -> None:
        msg = (
            f"Cannot create program because output format is missing. "
            f"Expected one of the following formats: {missing_formats}"
        )
        super().__init__(message=msg)


class ClassiqCombinatorialOptimizationError(ClassiqError):
    pass


class ClassiqOracleError(ClassiqError):
    pass


class ClassiqAnalyzerError(ClassiqError):
    pass


class ClassiqAnalyzerGraphError(ClassiqError):
    pass


class ClassiqAPIError(ClassiqError):
    pass


class ClassiqVersionError(ClassiqError):
    pass


class ClassiqValueError(ClassiqError, ValueError):
    pass


class ClassiqArithmeticError(ClassiqValueError):
    pass


class ClassiqIndexError(ClassiqError, IndexError):
    pass


class ClassiqWiringError(ClassiqValueError):
    pass


class ClassiqControlError(ClassiqError):
    def __init__(self) -> None:
        message = "Repeated control names, please rename the control states"
        super().__init__(message=message)


class ClassiqQRegError(ClassiqValueError):
    pass


class ClassiqQFuncError(ClassiqValueError):
    pass


class ClassiqQSVMError(ClassiqValueError):
    pass


class ClassiqQNNError(ClassiqValueError):
    pass


class ClassiqTorchError(ClassiqQNNError):
    pass


class ClassiqChemistryError(ClassiqError):
    pass


class ClassiqAuthenticationError(ClassiqError):
    pass


class ClassiqExpiredTokenError(ClassiqAuthenticationError):
    pass


class ClassiqFileNotFoundError(FileNotFoundError):
    pass


class ClassiqStateInitializationError(ClassiqError):
    pass


class ClassiqPasswordManagerSelectionError(ClassiqError):
    pass


class ClassiqMismatchIOsError(ClassiqError):
    pass


class ClassiqNotImplementedError(ClassiqError, NotImplementedError):
    pass
