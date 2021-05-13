from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.db.models import Count, Case, When, IntegerField, Prefetch, BooleanField, Value

from .models import User

from interact.models import Like, Follow
from post.models import Post
from post.form import PostCreateForm

# def index(request):
#     return render(request, "network/index.html")


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
        followed = Follow.objects.filter(follower=self.request.user).values_list('followed', flat=True)
        if not self.request.user.is_authenticated:
            return Post.objects.all()
        return Post.objects.select_related('owner').prefetch_related(
            Prefetch('like', queryset=Like.objects.select_related('owner'))
        ).annotate(like_count=Count(Case(
            When(like__is_like=True, then=Value(1)),
            output_field=IntegerField)
        ), dislike_count=Count(Case(
            When(like__is_like=False, then=Value(1)),
            output_field=IntegerField)
        ), follow_already=Case(
            When(owner__in=followed, then=Value(True)),
            default=Value(False),
            output_field=BooleanField())).order_by('-created_time')  # improve: do we need query all?

        # if followed:
        #     return x.annotate(follow_already=Case(
        #         When(owner__in=followed, then=Value(True)),
        #         default=Value(False),
        #         output_field=BooleanField()))





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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
