from django.urls import path

from sdk.apis import (
    GoogleLoginApi,
    GoogleLoginRedirectApi,
)

urlpatterns = [
    path("callback/", GoogleLoginApi.as_view(), name="callback-sdk"),
    path("redirect/", GoogleLoginRedirectApi.as_view(), name="redirect-sdk"),
]
