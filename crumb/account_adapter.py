from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):

        redirect_to = request.session.pop(
            "after_signup_redirect",
            None,
        )

        if redirect_to:
            return resolve_url(redirect_to)

        return super().get_login_redirect_url(request)