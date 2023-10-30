from classiq._internals.enum_utils import StrEnum


class ErrorMitigationMethod(StrEnum):
    COMPLETE_CALIBRATION = "Complete Calibration"
    TENSORED_CALIBRATION = "Tensored Calibration"
