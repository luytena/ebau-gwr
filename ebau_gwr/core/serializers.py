from rest_framework import serializers


class ConstructionProjectsListSerializer(serializers.Serializer):
    EPROID = serializers.IntegerField(read_only=True)
    officialConstructionProjectFileNo = serializers.CharField(read_only=True)
    constructionSurveyDept = serializers.IntegerField(read_only=True)
    constructionProjectDescription = serializers.CharField(read_only=True)
    projectStatus = serializers.IntegerField(read_only=True)
