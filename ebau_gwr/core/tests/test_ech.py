import os.path

import pytest
import xmlschema

from ebau_gwr.core import formatters


@pytest.mark.parametrize("set_number", [True, False])
def test_generate_delivery(set_number):
    data = {
        "createDateFrom": "2020-01-01",
        "createDateTo": "2020-02-01",
    }
    if set_number:
        data["number"] = 2323
    xml_data = formatters.delivery(
        getConstructionProject=formatters.getConstructionProject(351388, data),
    ).toxml()

    my_dir = os.path.dirname(__file__)
    my_schema = xmlschema.XMLSchema(my_dir + "/../xsd/ech_0216_2_0.xsd")
    my_schema.validate(xml_data)
