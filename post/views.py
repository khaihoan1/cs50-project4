from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post
from .form import PostCreateForm
# Create your views here.


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    # success_url = reverse('network:index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('network:index'))

    def get(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('network:index'))


class PostDetailView(DetailView):
    model = Post
    template_name = "post/detail.jinja"
    context_object_name = "post"


class PostEditView(UpdateView):
    model = Post
    template_name = "post/create.jinja"
    form_class = PostCreateForm


class PostDeleteView(DeleteView):
    model = Post

    def get(self):
        # return HttpResponseRedirect(reverse("post_detail", kwargs=({"pk": self.get_object().id})))
        return HttpResponseRedirect(reverse("post_detail"))
    # check permission
