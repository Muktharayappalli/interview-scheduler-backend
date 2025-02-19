from rest_framework import serializers
from .models import Candidate, Interviewer, CandidateAvailability, InterviewerAvailability

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name']

class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = ['id', 'name']

class CandidateAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateAvailability
        fields = ['id', 'candidate', 'start_time', 'end_time']

class InterviewerAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewerAvailability
        fields = ['id', 'interviewer', 'start_time', 'end_time']