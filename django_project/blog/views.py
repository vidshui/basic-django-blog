from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import NewCommentForm

def home(request):
	context = {
	'posts':Post.objects.all()
	}
	return render(request,'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name='blog/home.html'
	context_object_name='posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name='blog/user_posts.html'
	context_object_name='posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')
	

from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import NewCommentForm

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get all approved comments for the post
        comments = post.comments.filter(status=True)
        
        context['comments'] = comments
        context['comment_form'] = NewCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        comment_form = NewCommentForm(request.POST)

        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)  # Don't save to DB yet
            user_comment.post = post  # Associate comment with the current post
            user_comment.user = request.user  # Set the user to the currently logged-in user
            user_comment.save()  # Now save the comment

           
            return redirect('post-detail', pk=post.pk)

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)

class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields=['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	fields=['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post= self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	success_url='/'
	def test_func(self):
		post= self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False


def about(request):
	return render(request,'blog/about.html', {'title':'About'})


from .models import Comment  

def delete_comment(request, comment_id):
    # Get the comment by its ID
    comment = get_object_or_404(Comment, id=comment_id)
    
    
    if request.user == comment.user:
    	post = comment.post
    	comment.delete()
    	return redirect('post-detail', pk=post.pk)  