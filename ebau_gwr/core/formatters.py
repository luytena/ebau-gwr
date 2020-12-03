import logging

import pyxb

from .schema import ech_0129_5_0, ech_0216_2_0 as ns_gwr

logger = logging.getLogger(__name__)


def get_date_range_type(data, prefix):
    if data.get(f"{prefix}DateFrom") and data.get(f"{prefix}DateTo"):
        return ns_gwr.dateIntervalType(
            dateFrom=data[f"{prefix}DateFrom"], dateTo=data[f"{prefix}DateTo"],
        )


def getConstructionProject(dept_no: int, search_data: dict):
    def get_realestateIdentification():
        for i in ("EGRID", "number", "numberSuffix", "subDistrict", "lot"):
            if search_data.get(i):
                return ech_0129_5_0.realestateIdentificationType(
                    EGRID=search_data.get("EGRID"),
                    number=str(search_data.get("number")),
                    numberSuffix=str(search_data.get("numberSuffix")),
                    subDistrict=search_data.get("subDistrict"),
                    lot=search_data.get("lot"),
                )
        return None

    return ns_gwr.getConstructionProjectRequestType(
        constructionSurveyDept=dept_no,
        realestateIdentification=get_realestateIdentification(),
        projectStatus=search_data.get("projectStatus"),
        hasError=search_data.get("hasError"),
        createDate=get_date_range_type(search_data, "create"),
        modifyDate=get_date_range_type(search_data, "modify"),
    )


def delivery(**args):
    """
    Generate delivery XML.

    General calling convention:
    >>> delivery(*delivery_type=delivery_data)
    """
    assert len(args) == 1, "Exactly one delivery param required"

    try:
        return ns_gwr.delivery(**args)
    except (
        pyxb.IncompleteElementContentError,
        pyxb.UnprocessedElementContentError,
    ) as e:  # pragma: no cover
        logger.error(e.details())
        raise
