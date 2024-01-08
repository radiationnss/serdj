from django.db.models.query import QuerySet

from users.models import UserAccount



def user_list(*, filters=None) -> QuerySet[UserAccount]:
    filters = filters or {}

    qs = UserAccount.objects.all()

    return BaseUserFilter(filters, qs).qs