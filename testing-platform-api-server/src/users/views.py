from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from src.users.models import User
from src.users.permissions import IsUserOrReadOnly
from src.users.serializers import CreateUserSerializer, UserSerializer
from src.common.constants import USER_GROUP_STUDENT
from src.users.permissions import IsTeacherUser
from src.exams.models import ExamResult

class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates, Updates and Retrieves - User Accounts
    """
    queryset = User.objects.all()
    serializers = {
        'default': UserSerializer,
        'create': CreateUserSerializer
    }
    permissions = {
        'default': (IsUserOrReadOnly,),
        'create': (AllowAny,)
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def get_user_data(self, instance):
        try:
            return Response(UserSerializer(self.request.user, context={'request': self.request}).data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Wrong auth token' + e}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='students', url_name='students',
            permission_classes=[IsAuthenticated, IsTeacherUser])
    def get_students(self, instance):
        return Response(UserSerializer(self.get_queryset().filter(groups__name=USER_GROUP_STUDENT), many=True).data)

    @action(detail=False, methods=['get'], url_path=r'getCurrentKnowledgeState/(?P<user_id>.*)/(?P<exam_id>\d+)',
            url_name='getCurrentKnowledgeState',
            permission_classes=[IsAuthenticated])
    def get_current_knowledge_state(self, request, user_id, exam_id):
        print(user_id, exam_id)
        exam_results = list(ExamResult.objects.filter(exam=exam_id, user=user_id).values())
        current_state = exam_results[-1]["state"]
        return Response({"state": current_state}, status=status.HTTP_200_OK)
