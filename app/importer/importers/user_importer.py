from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string


def transform_user(data):
    try:
        user = User.objects.get(username=data['name'])
    except User.DoesNotExist:
        user: User
        user = User.objects.create_user(
            username=data['name'],
            email=data['mail'],
            password=get_random_string(16),
            is_staff=True)
        user.groups.add(Group.objects.get(id=2))
        user.save()

    return user
