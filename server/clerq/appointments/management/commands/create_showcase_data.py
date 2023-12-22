from typing import Any
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from appointments.models import Appointment
from appointments.utils import get_appointment_periods
from accounts.showcase import showcase_accounts


class Command(BaseCommand):
    help = "Creates appointments for showcase"

    def create_mock_data(self) -> list[dict]:
        user_model = get_user_model()

        # Create users and permissions
        for username, permissions in showcase_accounts.items():
            user = user_model.objects.create_user(
                username=username,
                password=username,  # password is same as username
            )

            for perm_string in permissions:
                permission = Permission.objects.get(codename=perm_string)
                user.user_permissions.add(permission)

        appointer = user_model.objects.get(username="appointer")
        appointee = user_model.objects.get(username="appointee")

        mock_data = [
            {
                "subject": "Meeting with John",
                "details": "Discuss project updates",
                "client_name": "John Doe",
            },
            {
                "subject": "Consultation call",
                "details": "Review legal documents",
                "client_name": "Alice Johnson",
            },
            {
                "subject": "Product demo",
                "details": "Showcasing new features",
                "client_name": "Bob Smith",
            },
            {
                "subject": "Team brainstorming",
                "details": "Generating new ideas",
                "client_name": "Emily Brown",
            },
            {
                "subject": "Training session",
                "details": "Employee onboarding",
                "client_name": "Michael Wilson",
            },
            {
                "subject": "Project kickoff",
                "details": "Introduction to new project",
                "client_name": "Sophia Lee",
            },
            {
                "subject": "Sales presentation",
                "details": "Pitching to potential client",
                "client_name": "David Taylor",
            },
            {
                "subject": "Support call",
                "details": "Assisting with technical issues",
                "client_name": "Emma Miller",
            },
            {
                "subject": "Networking event",
                "details": "Building industry connections",
                "client_name": "James Anderson",
            },
            {
                "subject": "Interview",
                "details": "Hiring process",
                "client_name": "Olivia Garcia",
            },
            {
                "subject": "Customer feedback",
                "details": "Gathering opinions on product",
                "client_name": "Daniel Martinez",
            },
            {
                "subject": "Conference call",
                "details": "Discussing quarterly goals",
                "client_name": "Ava Harris",
            },
            {
                "subject": "Task review",
                "details": "Checking progress on assignments",
                "client_name": "William Jones",
            },
            {
                "subject": "Workshop",
                "details": "Learning new skills",
                "client_name": "Mia Davis",
            },
            {
                "subject": "Health checkup",
                "details": "Routine medical examination",
                "client_name": "Jackson White",
            },
            {
                "subject": "Website redesign",
                "details": "Planning user interface changes",
                "client_name": "Sophie Robinson",
            },
            {
                "subject": "Marketing strategy",
                "details": "Reviewing campaign performance",
                "client_name": "Henry Brown",
            },
            {
                "subject": "Financial consultation",
                "details": "Planning for future investments",
                "client_name": "Lily Turner",
            },
            {
                "subject": "IT support",
                "details": "Resolving technical issues",
                "client_name": "Ethan Clark",
            },
            {
                "subject": "Community event",
                "details": "Volunteer coordination",
                "client_name": "Chloe Baker",
            },
            {
                "subject": "Birthday surprise",
                "details": "Planning a surprise party",
                "client_name": "Alexander King",
            },
            {
                "subject": "Research meeting",
                "details": "Discussing recent findings",
                "client_name": "Grace Parker",
            },
            {
                "subject": "Training workshop",
                "details": "Improving team skills",
                "client_name": "Sebastian Young",
            },
            {
                "subject": "Legal consultation",
                "details": "Reviewing contracts",
                "client_name": "Zoe Turner",
            },
            {
                "subject": "Webinar",
                "details": "Educational session",
                "client_name": "Nathan Brooks",
            },
            {
                "subject": "Team building",
                "details": "Outdoor activities",
                "client_name": "Avery Moore",
            },
            {
                "subject": "Appointment scheduling",
                "details": "System demo",
                "client_name": "Madison Reed",
            },
            {
                "subject": "Strategic planning",
                "details": "Setting long-term goals",
                "client_name": "Elijah Fisher",
            },
            {
                "subject": "Art exhibition",
                "details": "Showcasing local artists",
                "client_name": "Aria Hughes",
            },
            {
                "subject": "Customer support",
                "details": "Resolving user queries",
                "client_name": "Logan Collins",
            },
            {
                "subject": "Job interview",
                "details": "Candidate evaluation",
                "client_name": "Hannah Turner",
            },
            {
                "subject": "Travel planning",
                "details": "Organizing business trip",
                "client_name": "Caleb White",
            },
            {
                "subject": "Content creation",
                "details": "Brainstorming ideas for campaign",
                "client_name": "Leah Wood",
            },
            {
                "subject": "Fitness consultation",
                "details": "Personal training session",
                "client_name": "Samuel Davis",
            },
            {
                "subject": "Data analysis",
                "details": "Reviewing statistical reports",
                "client_name": "Scarlett Bennett",
            },
            {
                "subject": "Project status update",
                "details": "Team progress report",
                "client_name": "Liam Parker",
            },
            {
                "subject": "Charity event",
                "details": "Coordinating fundraising efforts",
                "client_name": "Victoria Hill",
            },
            {
                "subject": "Client onboarding",
                "details": "Welcoming new clients",
                "client_name": "Gabriel Turner",
            },
            {
                "subject": "Conflict resolution",
                "details": "Mediating team disputes",
                "client_name": "Avery Lopez",
            },
            {
                "subject": "Fashion show",
                "details": "Showcasing latest trends",
                "client_name": "Peyton Mitchell",
            },
            {
                "subject": "Software demo",
                "details": "Showcasing new features",
                "client_name": "Brooklyn Turner",
            },
            {
                "subject": "Book launch",
                "details": "Author book signing",
                "client_name": "Elijah Turner",
            },
            {
                "subject": "Job fair",
                "details": "Recruiting new talent",
                "client_name": "Sofia Turner",
            },
            {
                "subject": "Parent-teacher meeting",
                "details": "Discussing student progress",
                "client_name": "Lucas Turner",
            },
            {
                "subject": "Wedding planning",
                "details": "Coordinating details for the big day",
                "client_name": "Aria Turner",
            },
            {
                "subject": "Language exchange",
                "details": "Practice speaking foreign languages",
                "client_name": "Mateo Turner",
            },
            {
                "subject": "Artificial intelligence seminar",
                "details": "Exploring AI applications",
                "client_name": "Isabella Turner",
            },
            {
                "subject": "Community cleanup",
                "details": "Organizing neighborhood cleanup",
                "client_name": "Xavier Turner",
            },
            {
                "subject": "Music concert",
                "details": "Showcasing local bands",
                "client_name": "Aria Turner",
            },
            {
                "subject": "Investor meeting",
                "details": "Pitching startup ideas",
                "client_name": "Mason Turner",
            },
            {
                "subject": "Volunteer orientation",
                "details": "Onboarding new volunteers",
                "client_name": "Zoe Turner",
            },
            {
                "subject": "Scientific research presentation",
                "details": "Sharing research findings",
                "client_name": "Aria Turner",
            },
            {
                "subject": "Virtual reality demo",
                "details": "Experiencing VR technology",
                "client_name": "Elijah Turner",
            },
            {
                "subject": "Cooking class",
                "details": "Learning new culinary skills",
                "client_name": "Aria Turner",
            },
        ]

        appointments = []

        _date = now()
        times = get_appointment_periods()

        for appointment in mock_data:
            try:
                appointment_time = times.pop(0)[0]
            except IndexError:
                times = get_appointment_periods()

                # Move to next day when no more available times
                _date = _date + timedelta(days=1)
                appointment_time = times.pop(0)[0]

            appointments.append(
                Appointment(
                    appointer_staff=appointer,
                    appointed_staff=appointee,
                    appointment_date=_date.date(),
                    appointment_time=appointment_time,
                    **appointment
                )
            )

        Appointment.objects.bulk_create(appointments)

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.create_mock_data()
