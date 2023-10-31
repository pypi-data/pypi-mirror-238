from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext_lazy as _

from accrete.shortcuts import save_form
from accrete.contrib.ui import FormContext, DetailContext, ClientAction
from .forms import UserForm


class LoginView(views.LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        user = form.get_user()
        if user is not None and not user.is_active:
            ctx = {'to_confirm': True}
            if self.extra_context:
                self.extra_context.update(ctx)
            else:
                self.extra_context = ctx
        return super().form_invalid(form)


class LogoutView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        return redirect('user:login')


@login_required()
def user_detail(request):
    ctx = DetailContext(
        request.user, request.GET.dict(), paginate_by=0, breadcrumbs=[],
        actions=[
            ClientAction(_('Edit'), url=reverse('user:edit'))
        ]
    )
    return render(request, 'user/user_detail.html', ctx.get_context())


@login_required()
def user_edit(request):
    form = UserForm(
        initial={'language_code': request.user.language_code},
        instance=request.user
    )
    if request.method == 'POST':
        form = save_form(UserForm(request.POST, instance=request.user))
        if form.is_saved:
            return redirect('user:detail')
    ctx = FormContext(request.user, request.GET.dict(), context={'form': form}).get_context()
    return render(request, 'user/user_form.html', ctx)
