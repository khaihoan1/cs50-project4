from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post
from . form import PostCreateForm
# Create your views here.


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    # template_name="post/create.jinja"
    template_name = "post/layout.jinja"

    # def get_context_data(self, *args, **kwargs):
    #     print(super().get_context_data(*args,**kwargs))
    #     print(self)
    #     return super().get_context_data(*args,**kwargs)
    # context = super().get_context_data(*args, **kwargs)
    # context['userrr'] = self.request.user
    # return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get(self, *args, **kwargs):
        print(self.request)
        return super().get(*args, **kwargs)

        # print(self.object, self.object.created_time)
        # ahihi = form.save()
        # ahihi.owner = self.request.user
        # ahihi.save()
    # def post(self, request, *args, **kwargs):
    #     print("sdfjj"*100,(self.get_form()).is_valid())
    #     return super().post(request, *args, **kwargs)
    # @login_required
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


def detail(request, pk):
    print(pk)


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
