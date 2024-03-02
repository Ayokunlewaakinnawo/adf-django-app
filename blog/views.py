from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import BlogPost
from .forms import BlogPostForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

#FOR PUBLIC BLOG VIEW
def bloghome(request):
    if BlogPost.objects.exists():
        # Get the most recent post
        recent_post = BlogPost.objects.latest('date_added')
        # Get all posts except the most recent one
        other_posts = BlogPost.objects.exclude(pk=recent_post.pk)
    else:
        recent_post = None
        other_posts = None

    context = {
        'recent_post': recent_post,
        'other_posts': other_posts,
    }
    return render(request, 'bloghome.html', context)

#The Main Blog Detail Page
def blog(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        raise Http404("BlogPost does not exist")
    
    post = BlogPost.objects.get(slug=slug)
    context = {
        'post':post
    }
    return render (request, 'blogviewdetails.html', context) 



#CREATE POST - USER PROFILE PAGE
@login_required(login_url='log_in')
def createpost(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        intro = request.POST.get('intro')
        body = request.POST.get('body')
        img1 = request.FILES.get('image1')
        img2 = request.FILES.get('image2')
        user=request.user 

        PostBlog = BlogPost(
            title = title,
            desc = desc,
            intro = intro,
            body = body,
            image1 = img1,
            image2 = img2,
            user=user
        )
        PostBlog.save()
        messages.success(request, 'Post successfully created!')
        return redirect('ProfilePg')
        
    context = {}
    return render(request, 'create-article.html', context)


# EDIT EXISTING BLOG POST
@login_required(login_url='log_in')
def edit_blog_post(request, slug):

    try:
        post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        raise Http404("BlogPost does not exist")
    

    if request.method == 'POST':
        if 'edit_post' in request.POST:
            form = BlogPostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes successfully applied!')
                return redirect('ProfilePg')  # Redirect to profile or post detail view
    else:
        form = BlogPostForm(instance=post)

    #USER DELETE BLOG POST
    if request.method == 'POST':
        # Check if a delete request is made
        if 'delete_post' in request.POST:
            slug = request.POST.get('slug')
            try:
                post_to_delete = BlogPost.objects.get(slug=slug)

                # Get related images associated with the post
                images_to_delete = []
                if post_to_delete.image1:
                    images_to_delete.append(post_to_delete.image1)
                if post_to_delete.image2:
                    images_to_delete.append(post_to_delete.image2)
                
                # Delete each related image
                for image in images_to_delete:
                    image.delete()

                # Delete the post
                post_to_delete.delete()
                messages.success(request, 'Post deleted successfully!')
                return redirect('ProfilePg')
            except BlogPost.DoesNotExist:
                # Handle case where post with given ID does not exist
                pass

    context = {'form': form,
               'post': post,}
    return render(request, 'edit-article.html', context)