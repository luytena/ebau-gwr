# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_search_view 1"] = [
    {
        "EPROID": 193052735,
        "constructionProjectDescription": 'Abbruch "alte Molkerei" und Neubau Mehrfamilienhaus mit Tiefgarage',
        "constructionSurveyDept": 134200,
        "officialConstructionProjectFileNo": "18-2015/48",
        "projectStatus": 6703,
    },
    {
        "EPROID": 193118952,
        "constructionProjectDescription": "Neubau Einfamilienhaus und Neubau Reiheneinfamilienhäuser",
        "constructionSurveyDept": 134200,
        "officialConstructionProjectFileNo": "1662-2017/49",
        "projectStatus": 6702,
    },
    {
        "EPROID": 193245350,
        "constructionProjectDescription": "Neubau Luft-/Wasser-Wärmepumpe (Aussenaufstellung)",
        "constructionSurveyDept": 134200,
        "officialConstructionProjectFileNo": "800-2018/78",
        "projectStatus": 6702,
    },
]

snapshots["test_construction_project_view 1"] = {
    "constructionProject": {
        "EPROID": 193052735,
        "buildingPermitIssueDate": "2016-12-19",
        "buildingProjectLink": [
            {
                "ARBID": 1,
                "building": {
                    "EGID": 191632131,
                    "dateOfConstruction": None,
                    "realestateIdentification": [],
                },
            },
            {
                "ARBID": 2,
                "building": {
                    "EGID": 250375,
                    "dateOfConstruction": {
                        "periodOfConstruction": 8011,
                        "year": None,
                        "yearMonth": None,
                        "yearMonthDay": None,
                    },
                    "realestateIdentification": [
                        {
                            "EGRID": "CH952453779371",
                            "lot": None,
                            "number": "18",
                            "numberSuffix": None,
                            "subDistrict": "0",
                        }
                    ],
                },
            },
        ],
        "constructionLocalisation": {
            "cantonAbbreviation": "SZ",
            "municipalityId": 1342,
            "municipalityName": "Galgenen",
        },
        "constructionProjectDescription": 'Abbruch "alte Molkerei" und Neubau Mehrfamilienhaus mit Tiefgarage',
        "constructionSurveyDept": 134200,
        "extensionOfOfficialConstructionProjectFileNo": 0,
        "officialConstructionProjectFileNo": "18-2015/48",
        "projectAnnouncementDate": "2015-07-30",
        "projectStartDate": "2018-07-02",
        "totalCostsOfProject": 5500000,
        "typeOfConstruction": 6273,
        "typeOfConstructionProject": 6011,
        "typeOfPermit": None,
    },
    "errorList": [
        {
            "action": "Blocking",
            "messageOfError": "Das Bauprojekt ist immer abgeschlossen, wenn die voraussichtliche Baudauer den Stichtag der Quartalserhebung überschreitet. Bitte korrigieren.",
            "ruleCategory": "BAU",
            "ruleID": "CQ3602",
        }
    ],
}
