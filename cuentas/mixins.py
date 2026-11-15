from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
class RolRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    roles_permitidos = ()
    def test_func(self):
        return self.request.user.rol in self.roles_permitidos
