from django.core import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.utils.timezone import now
from django.utils import timezone
from .models import (
    Organization,
    System,
    Functionality,
    TestCase,
    TestStep,
    TestExecution,
    Defect,
    User,
    UserOrganization,
)
from .serializers import (
    OrganizationSerializer,
    SystemSerializer,
    FunctionalitySerializer,
    TestCaseSerializer,
    TestStepSerializer,
    TestExecutionSerializer,
    DefectSerializer,
    UserSerializer,
)
import pyotp
import requests
import random
import logging
import time
from django.db import transaction

User = get_user_model()
otp_store = {}  # Temporary OTP storage with expiration


class DefectOptionsView(APIView):
    """
    API View to fetch options for Defect fields (severity and status).
    """

    def get(self, request):
        # Get severity choices from Defect model
        severity_choices = Defect._meta.get_field("severity").choices
        severity_options = [
            {"value": choice[0], "label": choice[1]} for choice in severity_choices
        ]

        # Get status choices from Defect model
        status_choices = Defect._meta.get_field("status").choices
        status_options = [
            {"value": choice[0], "label": choice[1]} for choice in status_choices
        ]

        return Response(
            {"severity_options": severity_options, "status_options": status_options}
        )


class StatusChoicesView(APIView):
    """
    API View to fetch status choices for TestExecution.
    """

    def get(self, request):
        # Fetch status choices from the TestExecution model
        status_choices = TestExecution._meta.get_field("status").choices
        # Format the choices as a list of dictionaries
        formatted_choices = [
            {"value": choice[0], "label": choice[1]} for choice in status_choices
        ]
        return Response(formatted_choices)


class RolesView(APIView):
    def get(self, request):
        # Fetch roles from User.ROLE_CHOICES
        roles = [{"value": role[0], "label": role[1]} for role in User.ROLE_CHOICES]
        # Return the roles as a JSON response
        return Response(roles)


class DashboardView(APIView):
    def get(self, request):
        # Calculate totals
        total_organizations = Organization.objects.count()
        total_systems = System.objects.count()
        total_functionalities = Functionality.objects.count()
        total_test_cases = TestCase.objects.count()
        total_active_users = User.objects.filter(is_active=True).count()
        total_open_defects = Defect.objects.filter(
            status="open"
        ).count()  # Use 'status' field

        # Prepare response
        stats = {
            "organizations": total_organizations,
            "systems": total_systems,
            "functionalities": total_functionalities,
            "test_cases": total_test_cases,
            "active_users": total_active_users,
            "open_defects": total_open_defects,
        }

        return Response({"stats": stats}, status=status.HTTP_200_OK)
class TesterDashboardView(APIView):
    """
    API View to fetch dashboard statistics for testers.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Check if user is a tester
        if user.role != 'tester':
            return Response(
                {"error": "Only testers can access this dashboard."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            # Get test cases assigned to this tester
            assigned_tests_count = TestCase.objects.filter(assigned_user=user).count()
            
            # Get test executions by this tester
            executions = TestExecution.objects.filter(tester=user)
            executed_tests_count = executions.count()
            
            # Calculate pending tests (assigned but not executed)
            executed_test_case_ids = executions.values_list('test_case_id', flat=True)
            pending_tests_count = TestCase.objects.filter(
                assigned_user=user
            ).exclude(
                id__in=executed_test_case_ids
            ).count()
            
            # Count passed, failed, and other status tests
            passed_tests_count = executions.filter(
                status__in=['pass', 'passed']
            ).count()
            
            failed_tests_count = executions.filter(
                status__in=['fail', 'failed']
            ).count()
            
            blocked_tests_count = executions.filter(
                status__in=['blocked', 'on_hold']
            ).count()
            
            # Get defects reported by this tester
            reported_defects_count = Defect.objects.filter(
                reported_by=user
            ).count()
            
            # Get recent activities for this tester
            recent_executions = TestExecution.objects.filter(
                tester=user
            ).select_related('test_case').order_by('-started_at')[:10]
            
            recent_activities = []
            for execution in recent_executions:
                try:
                    test_case_title = execution.test_case.title if execution.test_case else "Unknown Test Case"
                    
                    recent_activities.append({
                        'id': execution.id,
                        'description': f"Test Execution: {test_case_title}",
                        'status': execution.status,
                        'date': execution.started_at.strftime('%Y-%m-%d %H:%M') if execution.started_at else 'N/A'
                    })
                except Exception as e:
                    print(f"Error processing execution {execution.id}: {str(e)}")
            
            # Prepare response data
            stats = {
                'assigned_tests': assigned_tests_count,
                'executed_tests': executed_tests_count,
                'pending_tests': pending_tests_count,
                'passed_tests': passed_tests_count,
                'failed_tests': failed_tests_count,
                'blocked_tests': blocked_tests_count,
                'reported_defects': reported_defects_count
            }
            
            return Response({
                'stats': stats,
                'recent_activities': recent_activities
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Log the error
            import traceback
            print(f"Error in tester dashboard: {str(e)}")
            print(traceback.format_exc())
            
            # Return error response
            return Response(
                {"error": "Failed to fetch dashboard data.", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    


class TestCaseViewSet(viewsets.ModelViewSet):
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = TestCase.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = (
            super().get_queryset().order_by("functionality", "sort_order")
        )  # Order by functionality and then sort_order

        # Apply organization filter if provided
        organization_id = self.request.query_params.get("organization_id")
        if organization_id:
            queryset = queryset.filter(
                functionality__system__organization_id=organization_id
            )
        
        # Add functionality filter
        functionality_id = self.request.query_params.get("functionality_id")
        if functionality_id:
            queryset = queryset.filter(functionality_id=functionality_id)

        # Role-based filtering
        if user.role == "admin":
            return queryset
        elif user.role == "tester":
            return queryset.filter(assigned_user=user)
        elif user.role == "viewer":
            return queryset.filter(
                models.Q(created_by=user) | models.Q(assigned_user=user)
            )
        return TestCase.objects.none()

    def perform_create(self, serializer):
        """
        Ensure created_by is set and handle functionality validation
        """
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError(
                {"detail": "Authentication credentials were not provided."},
                code=status.HTTP_401_UNAUTHORIZED,
            )

        # Validate functionality_id exists if provided
        functionality_id = self.request.data.get("functionality_id")
        if functionality_id:
            try:
                Functionality.objects.get(id=functionality_id)
            except Functionality.DoesNotExist:
                raise serializers.ValidationError(
                    {"functionality_id": "Functionality with this ID does not exist."},
                    code=status.HTTP_400_BAD_REQUEST,
                )

        # Save with the current user as created_by
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        """
        Custom action to assign a test case to a user
        """
        test_case = self.get_object()
        user_id = request.data.get("userId")

        if not user_id:
            return Response(
                {"error": "userId is required in the request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        test_case.assigned_user = user
        test_case.save()

        return Response(
            {"message": "User assigned successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def change_status(self, request, pk=None):
        """
        Custom action to change test case status
        """
        test_case = self.get_object()
        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"error": "status is required in the request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_status not in dict(TestCase._meta.get_field("status").choices):
            return Response(
                {"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST
            )

        test_case.status = new_status
        test_case.save()

        return Response(
            {"message": f"Status changed to {new_status}"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        """
        Custom action to reorder test cases within a functionality

        Request format:
        {
            "functionality_id": 123,
            "testcase_id": 456,
            "new_position": 2
        }
        """
        functionality_id = request.data.get("functionality_id")
        testcase_id = request.data.get("testcase_id")
        new_position = request.data.get("new_position")

        # Validate input
        if not all([functionality_id, testcase_id, new_position is not None]):
            return Response(
                {
                    "error": "functionality_id, testcase_id, and new_position are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify functionality exists
            functionality = Functionality.objects.get(id=functionality_id)

            # Get the test case to move
            testcase_to_move = TestCase.objects.get(
                id=testcase_id, functionality_id=functionality_id
            )

            # Get all test cases for this functionality, ordered by sort_order
            testcases = list(
                TestCase.objects.filter(functionality_id=functionality_id).order_by(
                    "sort_order"
                )
            )

            # Remove the test case from the list and reinsert at new position
            current_position = next(
                (i for i, tc in enumerate(testcases) if tc.id == testcase_id), None
            )
            if current_position is None:
                return Response(
                    {"error": "Test case not found in the specified functionality"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            testcase_obj = testcases.pop(current_position)
            testcases.insert(min(new_position, len(testcases)), testcase_obj)

            # Update sort_order values with a gap of 1000
            # Inside the reorder method
            with transaction.atomic():
                TestCase.objects.bulk_update(
                    [
                        TestCase(id=tc.id, sort_order=(i + 1) * 1000)
                        for i, tc in enumerate(testcases)
                    ],
                    ["sort_order"],
                )

            return Response(
                {"message": "Test cases reordered successfully"},
                status=status.HTTP_200_OK,
            )

        except Functionality.DoesNotExist:
            return Response(
                {"error": "Functionality not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except TestCase.DoesNotExist:
            return Response(
                {"error": "Test case not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
    @action(detail=False, methods=['post'])
    def bulk_reorder(self, request):
        """
        Reorder multiple test cases at once
        
        Request format:
        {
            "functionality_id": 123,
            "order": [789, 456, 123]  # List of test case IDs in desired order
        }
        """
        functionality_id = request.data.get('functionality_id')
        order = request.data.get('order', [])
        
        if not functionality_id or not order:
            return Response(
                {'error': 'functionality_id and order array are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                for index, testcase_id in enumerate(order):
                    TestCase.objects.filter(
                        id=testcase_id, 
                        functionality_id=functionality_id
                    ).update(sort_order=(index + 1) * 1000)
            
            return Response(
                {'message': 'Test cases reordered successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer


class FunctionalityViewSet(viewsets.ModelViewSet):
    queryset = Functionality.objects.all()
    serializer_class = FunctionalitySerializer


class TestStepViewSet(viewsets.ModelViewSet):
    queryset = TestStep.objects.all()
    serializer_class = TestStepSerializer

# Replace your TestExecutionViewSet in views.py with this:

class TestExecutionViewSet(viewsets.ModelViewSet):
    serializer_class = TestExecutionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optimize queryset with select_related and prefetch_related
        """
        return TestExecution.objects.select_related(
            'test_case',
            'test_case__functionality',
            'tester'
        ).prefetch_related(
            'test_case__steps'
        ).all()

    def perform_create(self, serializer):
        serializer.save(tester=self.request.user)
        
    @action(detail=False, methods=['get'])
    def executions(self, request):
        """
        Custom action to get all test executions.
        This can be accessed at /uat/test-executions/executions/
        """
        executions = self.get_queryset()
        serializer = self.get_serializer(executions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """
        Execute a test with step results
        """
        execution = self.get_object()
        steps = request.data.get('steps', [])
        
        if not steps:
            return Response(
                {'error': 'steps data is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Update execution status based on step results
            all_passed = all(step.get('status') == 'passed' for step in steps)
            any_failed = any(step.get('status') == 'failed' for step in steps)
            
            if all_passed:
                execution.status = 'passed'
            elif any_failed:
                execution.status = 'failed'
            else:
                execution.status = 'in_progress'
            
            execution.completed_at = now()
            execution.save()
            
            # Log the step results for debugging
            print(f"Execution {execution.id} completed with status: {execution.status}")
            print(f"Steps processed: {len(steps)}")
            
            return Response(
                {
                    'message': 'Test execution completed successfully', 
                    'status': execution.status,
                    'execution_id': execution.id,
                    'completed_at': execution.completed_at
                }, 
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            print(f"Error in execute method: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class DefectViewSet(viewsets.ModelViewSet):
#     queryset = Defect.objects.all().order_by("-created_at")
#     serializer_class = DefectSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         """
#         Minimal validation - just save with current user as reporter
#         """
#         serializer.save(reported_by=self.request.user)

#     def get_queryset(self):
#         """
#         Basic queryset filtering without strict permissions
#         """
#         return super().get_queryset()
class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all().order_by("-created_at")
    serializer_class = DefectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Handle defect creation - convert test_case_id to execution_id
        """
        print("=== DEFECT CREATE METHOD CALLED ===")
        print(f"Raw request.data: {dict(request.data)}")
        print(f"User: {request.user}")
        
        # Step 1: Fix multipart form data (convert lists to single values)
        processed_data = {}
        for key, value in request.data.items():
            if isinstance(value, list) and len(value) > 0:
                processed_data[key] = value[0]
                print(f"Fixed {key}: {value} -> {value[0]}")
            else:
                processed_data[key] = value
        
        print(f"After fixing multipart data: {processed_data}")
        
        # Step 2: Handle test_case_id -> execution_id conversion (required by your model)
        if 'test_case_id' in processed_data:
            try:
                test_case_id = int(processed_data.pop('test_case_id'))
                print(f"Converting test_case_id {test_case_id} to execution_id")
                
                # Get the test case
                test_case = TestCase.objects.get(id=test_case_id)
                print(f"Found test case: {test_case.title}")
                
                # Find existing execution or create new one
                execution = TestExecution.objects.filter(
                    test_case=test_case,
                    tester=request.user
                ).order_by('-started_at').first()
                
                if not execution:
                    print("No existing execution found, creating new one")
                    execution = TestExecution.objects.create(
                        test_case=test_case,
                        tester=request.user,
                        status='in_progress',
                        started_at=timezone.now()
                    )
                    print(f"Created new execution: {execution.id}")
                else:
                    print(f"Using existing execution: {execution.id}")
                
                # Add execution_id to the data (required by your model)
                processed_data['execution_id'] = execution.id
                
            except TestCase.DoesNotExist:
                print(f"Test case {test_case_id} not found")
                return Response({
                    'error': f'Test case with ID {test_case_id} does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                print(f"Invalid test_case_id: {e}")
                return Response({
                    'error': 'Invalid test_case_id format'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"Unexpected error: {e}")
                return Response({
                    'error': f'Error processing request: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print(f"Final data for serializer: {processed_data}")
        
        # Step 3: Create the defect using your existing serializer
        serializer = self.get_serializer(data=processed_data)
        
        if serializer.is_valid():
            print("Serializer is valid, creating defect...")
            defect = serializer.save(reported_by=request.user)
            print(f"✅ Defect created successfully: ID {defect.id}")
            
            # Return the created defect data
            response_data = self.get_serializer(defect).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print(f"❌ Serializer validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        Basic queryset - can be enhanced later for role-based filtering
        """
        return super().get_queryset()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related("user_organizations__organization")
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Changed from IsAdminUser to IsAuthenticated

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["create", "destroy"]:
            # Only superusers can create or delete users
            permission_classes = [IsAdminUser]
        else:
            # For other actions, check our custom permission logic in get_queryset
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        organization_id = self.request.query_params.get("organization_id")

        # Filter by organization if specified
        if organization_id:
            queryset = queryset.filter(
                user_organizations__organization_id=organization_id
            ).distinct()

        # Role-based filtering
        if user.is_superuser:
            # Superusers can see all users
            return queryset
        elif user.role == "admin":
            # Admins can see all users except superusers
            return queryset.filter(is_superuser=False)
        elif user.role == "tester":
            # Testers can only see themselves
            return queryset.filter(id=user.id)
        elif user.role == "viewer":
            # Viewers can see themselves and users in their organizations
            return queryset.filter(
                models.Q(id=user.id)
                | models.Q(
                    user_organizations__organization__in=user.user_organizations.values(
                        "organization"
                    )
                )
            )

        # Default fallback - only see yourself
        return queryset.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        # Make data mutable
        data = request.data.copy()

        # Ensure organizations is always a list
        organizations = data.get("organizations", [])
        if isinstance(organizations, (int, str)):
            organizations = [organizations]
            data["organizations"] = organizations

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            # Create user with serializer (includes organization validation)
            user = serializer.save()

            # If serializer didn't handle organizations (fallback)
            if not user.user_organizations.exists() and organizations:
                for org_id in organizations:
                    try:
                        org = Organization.objects.get(id=org_id)
                        UserOrganization.objects.create(user=user, organization=org)
                    except Organization.DoesNotExist:
                        # Shouldn't happen since serializer validates
                        continue

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data.copy()

        # Handle organizations if provided
        if "organizations" in data:
            organizations = data.pop("organizations", [])
            if isinstance(organizations, (int, str)):
                organizations = [organizations]

            # Let serializer handle validation
            data["organizations"] = organizations

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            self.perform_update(serializer)

            # If serializer didn't handle organizations (fallback)
            if "organizations" in data:
                current_orgs = set(
                    instance.user_organizations.values_list(
                        "organization_id", flat=True
                    )
                )
                new_orgs = set(map(int, organizations))

                # Only make changes if needed
                if current_orgs != new_orgs:
                    # Clear existing organizations
                    instance.user_organizations.all().delete()
                    # Add new organizations
                    for org_id in new_orgs:
                        try:
                            org = Organization.objects.get(id=org_id)
                            UserOrganization.objects.create(
                                user=instance, organization=org
                            )
                        except Organization.DoesNotExist:
                            # Shouldn't happen since serializer validates
                            continue

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()

        # Set default empty list if organizations not provided
        if "organizations" not in data:
            data["organizations"] = []

        # Convert single organization ID to list if needed
        if isinstance(data["organizations"], (int, str)):
            data["organizations"] = [data["organizations"]]

        # Validate organizations if any are provided
        if data["organizations"]:
            for org_id in data["organizations"]:
                try:
                    Organization.objects.get(id=org_id)
                except (Organization.DoesNotExist, ValueError):
                    return Response(
                        {
                            "organizations": [
                                f"Organization with ID {org_id} does not exist."
                            ]
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # Create UserOrganization relationships if organizations were provided
            if data["organizations"]:
                for org_id in data["organizations"]:
                    organization = Organization.objects.get(id=org_id)
                    UserOrganization.objects.create(
                        user=user, organization=organization
                    )

            return Response(
                {
                    "message": "User registered successfully!",
                    "user_id": user.id,
                    "organizations": data["organizations"] or None,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        whatsapp_number = request.data.get("whatsapp_number")
        org_id = request.data.get("org_id")

        if not whatsapp_number:
            return Response(
                {"error": "WhatsApp number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Clean the whatsapp number (remove any non-digit characters)
        whatsapp_number = "".join(filter(str.isdigit, whatsapp_number))

        try:
            user = User.objects.get(whatsapp_number=whatsapp_number)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found. Please register first."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))
        # Store OTP with timestamp (valid for 5 minutes)
        otp_store[whatsapp_number] = {
            "otp": otp,
            "timestamp": time.time(),
            "verified": False,
        }

        # Log the OTP for debugging (remove in production)
        logging.info(f"Generated OTP for {whatsapp_number}: {otp}")

        try:
            response = requests.post(
                "https://backend.bitz-itc.com/api/webhook/whatsapp/",
                json={
                    "direction": "outgoing",
                    "data": {
                        "recipient": whatsapp_number,
                        "message_type": "text",
                        "content": f"Your verification code is: {otp}",
                    },
                },
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                return Response(
                    {"message": "OTP sent successfully!"}, status=status.HTTP_200_OK
                )
            else:
                logging.error(f"Failed to send OTP: {response.text}")
                return Response(
                    {"error": "Failed to send OTP."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except requests.RequestException as e:
            logging.error(f"Request error while sending OTP: {e}")
            return Response(
                {"error": "Failed to send OTP."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        whatsapp_number = request.data.get("whatsapp_number")
        otp = request.data.get("otp")

        if not whatsapp_number or not otp:
            return Response(
                {"error": "WhatsApp number and OTP are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Clean the whatsapp number (remove any non-digit characters)
        whatsapp_number = "".join(filter(str.isdigit, whatsapp_number))

        # Get stored OTP data
        otp_data = otp_store.get(whatsapp_number)

        if not otp_data:
            return Response(
                {"error": "OTP not found or expired. Please request a new OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if OTP is correct
        if otp_data["otp"] != otp:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if OTP is expired (5 minutes = 300 seconds)
        if time.time() - otp_data["timestamp"] > 300:
            return Response(
                {"error": "OTP expired. Please request a new OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(whatsapp_number=whatsapp_number)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Mark OTP as verified
        otp_data["verified"] = True
        otp_store[whatsapp_number] = otp_data

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Clean up (optional - you might want to keep it for a while)
        # del otp_store[whatsapp_number]

        return Response(
            {
                "access": access_token,
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class StaffAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        whatsapp_number = request.data.get("whatsapp_number")
        password = request.data.get("password")

        if not whatsapp_number or not password:
            return Response(
                {"error": "WhatsApp number and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(whatsapp_number=whatsapp_number, is_staff=True)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials."}, status=status.HTTP_403_FORBIDDEN
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials."}, status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"access": access_token}, status=status.HTTP_200_OK)