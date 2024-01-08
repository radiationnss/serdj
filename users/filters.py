import django_filters

from users.models import UserAccount


class BaseUserFilter(django_filters.FilterSet):
    class Meta:
        model = UserAccount
        fields = ("id", "email")