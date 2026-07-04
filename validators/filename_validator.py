import re

APP_DEV_PATTERN = r"^RM_APP_DEV_ASSESSM_RITM\d+\.docm$"
UAT_PATTERN = r"^RM_UAT_EVIDENCE_RITM\d+\.docm$"


def validate_filename(filename: str):

    if re.match(APP_DEV_PATTERN, filename):
        return {
            "status": "PASS",
            "documentType": "APP_DEV",
            "message": "Valid App Development Assessment filename."
        }

    if re.match(UAT_PATTERN, filename):
        return {
            "status": "PASS",
            "documentType": "UAT",
            "message": "Valid UAT Evidence filename."
        }

    return {
        "status": "FAIL",
        "documentType": "UNKNOWN",
        "message": "Incorrect file naming convention."
    }