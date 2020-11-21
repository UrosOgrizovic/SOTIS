from django.test import TestCase
from nose.tools import eq_
from ..serializers import CreateUserSerializer


class TestCreateUserSerializer(TestCase):
    def setUp(self):
        self.user_data = {'username': 'test', 'password': 'test'}

    def test_serializer_with_empty_data(self):
        serializer = CreateUserSerializer(data={})
        eq_(serializer.is_valid(), False)
