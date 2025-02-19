from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Candidate {self.id}: {self.name}"

class Interviewer(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Interviewer {self.id}: {self.name}"

class CandidateAvailability(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['candidate', 'start_time', 'end_time'], name='unique_candidate_availability')
        ]
    
    def __str__(self):
        return f"{self.candidate.name} - {self.start_time} to {self.end_time}"

class InterviewerAvailability(models.Model):
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['interviewer', 'start_time', 'end_time'], name='unique_interviewer_availability')
        ]
    
    def __str__(self):
        return f"{self.interviewer.name} - {self.start_time} to {self.end_time}"
