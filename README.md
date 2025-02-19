# Interview Scheduler API

This project is a Django-based API for managing availability and scheduling interviews for candidates and interviewers.

## Features
- Register availability for candidates and interviewers.
- Check for overlapping interview slots between candidates and interviewers.
- Support for CRUD operations on user availability.

## Requirements
- Python 3.9+
- Django 5.1.3
- Django REST Framework
- SQLite database (default, can be changed to PostgreSQL or MySQL)

## Improvements
- Buffer Times: Introduce buffer times between interviews to prevent back-to-back scheduling, ensuring a smooth transition between interviews.
- Advanced Conflict Resolution: Implement more sophisticated scheduling algorithms that can handle overlapping slots better, such as prioritizing certain interviewers or candidates.
- Real-Time Availability: Integrate with external calendaring systems (like Google Calendar) to get real-time updates on interview availability.

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your local machine:

git clone https://github.com/Muktharayappalli/interview-scheduler-backend.git
cd interview_scheduler


### 2. Create and Activate Virtual Environment
It is recommended to use a virtual environment for managing dependencies.

#### On macOS and Linux:
'python3 -m venv venv'
'source venv/bin/activate'


#### On Windows:

'python -m venv venv'
'venv\Scripts\activate'


### 3. Install Dependencies
Install the required Python packages:


"pip install -r requirements.txt"

### 4. Apply Migrations
Since the project uses SQLite by default, you just need to run migrations:

'python manage.py migrate'

### 5. Run the Development Server
Start the Django development server:


python manage.py runserver

The API will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

### 1. User Availability
#### Register Availability (POST)

POST `http://127.0.0.1:8000/register/availability/`

**Payload:**
```json
{
  "user_id": "123",
  "role": "candidate",
  "start_time": "2025-02-20T09:00:00Z",
  "end_time": "2025-02-20T17:00:00Z",
  "name": "mukthar"
},
{
  "user_id": "456",
  "role": "interviewer",
  "start_time": "2025-02-20T10:00:00Z",
  "end_time": "2025-02-20T16:00:00Z",
  "name": "John"
}

```

### 2. Check Overlapping Slots
#### Get Overlapping Slots (GET)


GET `http://127.0.0.1:8000/get/interview_slots/?candidate_id=123&interviewer_id=456`

params = {
    "candidate_id": 123,
    "interviewer_id": 456
}

**Response:**
```json
{"available_slots":[[10,11],[11,12],[12,13],[13,14],[14,15],[15,16]]}
```

## Database Configuration
By default, the project uses SQLite, and the database file (`db.sqlite3`) is automatically created when migrations are applied. If you want to switch to PostgreSQL or MySQL, update the `DATABASES` setting in `settings.py`.

