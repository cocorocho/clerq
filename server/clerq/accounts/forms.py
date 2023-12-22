from allauth.account.forms import LoginForm as AllauthLoginForm


class LoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Auto populate with showcase accounts
        login_field = self.fields["login"]
        login_field.help_text = "appointer or appointee"
        login_field.widget.attrs.update(
            {
                "class": "w-full",
                "value": "appointer",
            }
        )

        password_field = self.fields["password"]
        password_field.help_text = "appointer or appointee"
        password_field.widget.attrs.update(
            {
                "class": "w-full",
                "value": "appointer",
            }
        )

    class Meta:
        help_texts = {"login": "wowo"}
