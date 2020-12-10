from rest_framework import serializers


class PyxbDateField(serializers.DateField):
    """Override DRF DateField to work with pyxb date types."""

    def to_representation(self, value):
        if not value:  # pragma: no cover
            return None
        return super().to_representation(value.date())


class ConstructionProjectsListSerializer(serializers.Serializer):
    EPROID = serializers.IntegerField(read_only=True, min_value=1, max_value=900000000)
    officialConstructionProjectFileNo = serializers.CharField(
        read_only=True, min_length=1, max_length=15
    )
    constructionSurveyDept = serializers.IntegerField(
        read_only=True, min_value=100, max_value=999999
    )
    constructionProjectDescription = serializers.CharField(
        read_only=True, min_length=3, max_length=1000
    )
    projectStatus = serializers.IntegerField(read_only=True)


class SwissMunicipalitySerializer(serializers.Serializer):
    municipalityId = serializers.IntegerField(min_value=1, max_value=9999)
    municipalityName = serializers.CharField(max_length=40)
    cantonAbbreviation = serializers.CharField(min_length=2, max_length=2)


class BuildingDateSerializer(serializers.Serializer):
    yearMonthDay = PyxbDateField()
    yearMonth = serializers.CharField(min_length=7, max_length=7)
    year = serializers.IntegerField(min_value=1000, max_value=9999)
    periodOfConstruction = serializers.IntegerField(min_value=8011, max_value=8023)


class RealestateIdentificationSerializer(serializers.Serializer):
    EGRID = serializers.CharField(max_length=14)
    number = serializers.CharField(min_length=1, max_length=12)
    numberSuffix = serializers.CharField(min_length=1, max_length=12)
    subDistrict = serializers.CharField(min_length=1, max_length=15)
    lot = serializers.CharField(min_length=1, max_length=15)


class BuildingWithEntranceWithDwellingSerializer(serializers.Serializer):
    EGID = serializers.IntegerField(min_value=1, max_value=900000000)
    realestateIdentification = RealestateIdentificationSerializer(many=True)
    dateOfConstruction = BuildingDateSerializer()


class KindOfConstructionWorkWithBuildingSerializer(serializers.Serializer):
    ARBID = serializers.IntegerField(min_value=1, max_value=999999999999)
    building = BuildingWithEntranceWithDwellingSerializer()


class ConstructionProjectsSerializer(serializers.Serializer):
    EPROID = serializers.IntegerField(min_value=1, max_value=900000000)
    officialConstructionProjectFileNo = serializers.CharField(
        min_length=1, max_length=15
    )
    extensionOfOfficialConstructionProjectFileNo = serializers.IntegerField(
        min_value=0, max_value=99
    )
    constructionSurveyDept = serializers.IntegerField(min_value=100, max_value=999999)
    totalCostsOfProject = serializers.IntegerField(
        min_value=1000, max_value=999999999000
    )
    typeOfPermit = serializers.IntegerField(min_value=5000, max_value=5071)
    constructionLocalisation = SwissMunicipalitySerializer()
    typeOfConstructionProject = serializers.IntegerField(min_value=6010, max_value=6012)
    typeOfConstruction = serializers.IntegerField(min_value=6211, max_value=6299)
    constructionProjectDescription = serializers.CharField(
        min_length=3, max_length=1000
    )
    projectAnnouncementDate = PyxbDateField()
    buildingPermitIssueDate = PyxbDateField()
    projectStartDate = PyxbDateField()
    buildingProjectLink = KindOfConstructionWorkWithBuildingSerializer(many=True)


class PlausibilityRuleSerializer(serializers.Serializer):
    ruleID = serializers.CharField(max_length=6)
    ruleCategory = serializers.ChoiceField(choices=("BAU", "G+W", "ADR", "MISS", "DB"))
    action = serializers.ChoiceField(
        choices=("Refused", "Cleaner", "Blocking", "Listed", "Auto")
    )
    messageOfError = serializers.CharField(max_length=1000)


class ConstructionProjectsCompleteSerializer(serializers.Serializer):
    constructionProject = ConstructionProjectsSerializer(read_only=True)
    errorList = PlausibilityRuleSerializer(many=True, read_only=True)
