from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.expressions import OuterRef
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.db.models import Count, Case, When, IntegerField, BooleanField, Value, Exists
from django.contrib.auth.decorators import login_required

from .models import User

from interact.models import Like, Follow
from post.models import Post
from post.form import PostCreateForm
from network.form import PersonalInfoForm


class PostListView(FormMixin, ListView):
    model = Post
    paginate_by = 5
    template_name = "network/newsfeed.jinja"
    body_title = "All Posts"
    context_object_name = "posts"
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['body_title'] = self.body_title
        return context

    def get_queryset(self):
        queryset = Post.objects.select_related('owner').annotate(
            comment_count=Count('comments', distinct=True),
            like_count=Count(
                Case(
                    When(likes__is_like=True, then=Value(1)),
                    output_field=IntegerField()
                ),
                distinct=True
            ),
            dislike_count=Count(
                Case(
                    When(likes__is_like=False, then=Value(1)),
                    output_field=IntegerField()
                ),
                distinct=True
            ),
        ).order_by('-created_time')  # improve: do we need query all?
        if self.request.user.is_authenticated:
            return queryset.annotate(
                follow_already=Exists(
                    Follow.objects.filter(followed=OuterRef('owner'), follower=self.request.user)
                ),
                like_already=Exists(
                    Like.objects.filter(owner=self.request.user, post_parent=OuterRef('pk'), is_like=True)
                ),
                dislike_already=Exists(
                    Like.objects.filter(owner=self.request.user, post_parent=OuterRef('pk'), is_like=False)
                )
            )
        return queryset.annotate(
            follow_already=Value(False, output_field=BooleanField()),
            like_already=Value(False, output_field=BooleanField())
        )


@login_required
def edit_personal_info(request):
    form = PersonalInfoForm(instance=request.user)
    if request.method == "POST":
        form = PersonalInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    context = {
        'form': form
    }
    return render(request, 'network/edit_personal_info.jinja', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.jinja", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.jinja")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.jinja", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.jinja", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.jinja")
