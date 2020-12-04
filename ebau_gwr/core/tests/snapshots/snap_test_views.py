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
