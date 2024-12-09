from django.contrib import admin
from .models import Course, Enrollment, Activity
from django.contrib.auth.models import User, Group

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date_enrolled')  # Display these fields in the list view
    list_filter = ('course', 'user')  # Add filters for course and user
    search_fields = ('user__username', 'course__title')  # Add search functionality by user and course title

class CourseAdmin(admin.ModelAdmin):
    # Allow lecturers to manage courses
    list_display = ('title', 'description', 'instructor', 'created_at', 'credits')
    search_fields = ('title', 'description')

    def get_queryset(self, request):
        # Restrict to only show courses for the logged-in lecturer
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='Lecturer').exists():
            return queryset.filter(instructor=request.user)
        return queryset

# Register models with custom admin
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Activity)
