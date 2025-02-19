from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from .models import Candidate, Interviewer, CandidateAvailability, InterviewerAvailability
from .serializers import CandidateAvailabilitySerializer, InterviewerAvailabilitySerializer
from rest_framework import status

@api_view(['POST'])
def register_availability(request):
    """
    API for registering availability for candidates or interviewers.
    If the user doesn't exist, a new user is created.
    """
    try:
        data = request.data
        user_id = data.get("user_id")
        role = data.get("role")
        start_time = parse_datetime(data.get("start_time"))
        end_time = parse_datetime(data.get("end_time"))

        if not (user_id and role and start_time and end_time):
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        if role not in ['candidate', 'interviewer']:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if role == "candidate":
            user, created = Candidate.objects.get_or_create(id=user_id, defaults={'name': data.get("name", "Unknown Candidate")})
            availability_data = {'candidate': user.id, 'start_time': start_time, 'end_time': end_time}
            serializer = CandidateAvailabilitySerializer(data=availability_data)
        elif role == "interviewer":
            user, created = Interviewer.objects.get_or_create(id=user_id, defaults={'name': data.get("name", "Unknown Interviewer")})
            availability_data = {'interviewer': user.id, 'start_time': start_time, 'end_time': end_time}
            serializer = InterviewerAvailabilitySerializer(data=availability_data)

        if serializer.is_valid():
            serializer.save()
            message = "New user created" if created else "Existing user found"
            return Response({"message": f"{message}. Availability registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_interview_slots(request):
    """
    API for getting possible interview slots between a candidate and an interviewer.
    Returns only the overlapping one-hour slots that do not exceed either candidate's or interviewer's availability.
    """
    candidate_id = request.GET.get("candidate_id")
    interviewer_id = request.GET.get("interviewer_id")

    if not candidate_id or not interviewer_id:
        return Response({"error": "Missing candidate_id or interviewer_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        candidate = Candidate.objects.get(id=candidate_id)
        interviewer = Interviewer.objects.get(id=interviewer_id)
    except (Candidate.DoesNotExist, Interviewer.DoesNotExist):
        return Response({"error": "Candidate or Interviewer not found"}, status=status.HTTP_404_NOT_FOUND)

    candidate_slots = CandidateAvailability.objects.filter(candidate=candidate)
    interviewer_slots = InterviewerAvailability.objects.filter(interviewer=interviewer)

    interviewable_slots = []
    for candidate_slot in candidate_slots:
        for interviewer_slot in interviewer_slots:
            start = max(candidate_slot.start_time, interviewer_slot.start_time)
            end = min(candidate_slot.end_time, interviewer_slot.end_time)

            if start < end:
                current_time = start
                while current_time + timedelta(hours=1) <= end:
                    start_hour = current_time.hour
                    end_hour = (current_time + timedelta(hours=1)).hour
                    interviewable_slots.append((start_hour, end_hour))
                    current_time += timedelta(hours=1)

    return Response({"available_slots": interviewable_slots}, status=status.HTTP_200_OK)