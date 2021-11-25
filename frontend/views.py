from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from frontend.forms import LoginForm
from frontend.helpers import change_chain, check_codon_in_chain
from frontend.models import Chain


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'back_url' in request.POST:
                        return redirect(request.POST['back_url'])
                    return redirect(reverse('home'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid registration')


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['chain_title'] = Chain.load()
        return context


class ChainActionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ChainActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        action = post_request.get('action', None)
        actions = {
            'change_chain': change_chain,
            'check_codon_in_chain': check_codon_in_chain
        }
        response = actions[action](post_request)
        back_url = response['back_url']
        if action == 'change_chain' or action == 'check_codon_in_chain':
            return JsonResponse(response, safe=False)
        else:
            return redirect(back_url)
