from prometheus_client import Counter, Histogram, Info
import time

# Metrics
http_requests_total = Counter(
    'http_requests_total', 
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration_seconds = Histogram(
    'request_duration_seconds',
    'HTTP request duration in seconds',
    ['endpoint']
)

student_attendance_marked = Counter(
    'student_attendance_marked_total',
    'Total number of attendance records marked'
)

app_info = Info('flask_app_info', 'Application information')
app_info.info({'version': '1.0.0'})
