from django.shortcuts import reverse, render, get_object_or_404, render_to_response, redirect
from blog.models import Post
from users.models import Profile
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, View, UpdateView
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.forms import ModelForm
from users.forms import SignupForm, UpdateProfileForm, LoginForm
from django.urls import reverse_lazy
from django.http import Http404

class LoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('blog:index'), request)
            else:
                context = {}
                context['form'] = form
                return render(request=request, template_name=self.template_name, context=context)
        else:
            context = {'form': form}
            return render(request=request, template_name=self.template_name, context=context)

class ProfileView(DetailView):
    model = Profile
    template_name = 'profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user__id = self.kwargs['user_id'])

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("picturas:index"))


class SignupView(View):
    template_name = 'registration/signup.html'
    registration_form = SignupForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.registration_form}
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user_form = SignupForm(data=request.POST)
        registered = False
        if user_form.is_valid():
            user = user_form.save(commit=True)
            user.email = user_form.cleaned_data['email']
            user.save()
            registered = True
            return render(request,'registration/signup.html',
                                    {'registered':registered})
        else:
            return render(request,'registration/signup.html',
                          {'form':user_form,
                           'registered':registered})


class EditProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'edit_profile.html'
    slug_field = "user_id"
    slug_url_kwarg = "user_id"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("It is not your profile!")
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        user_id=self.kwargs['user_id']
        return reverse('users:profile', args=(user_id, ))


class AddRemoveFriend(View):

    def post(self, request, user_id, *args, **kwargs):
        profile = get_object_or_404(Profile, user__id=user_id)
        if profile.friends.filter(user__id=request.user.id).exists():
            friend = profile.friends.get(user__id=request.user.id)
            profile.friends.remove(friend)
            request.user.user_profile.friends.remove(profile)
        else:
            profile.friends.add(request.user.user_profile)
            request.user.user_profile.friends.add(profile)
        return redirect(request.META.get('HTTP_REFERER'), request)

