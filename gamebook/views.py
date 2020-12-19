from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import PageForm, StoryForm
from .models import Page, Story

def home(request):
    return render(request, "core/home.html", {
        "stories": Story.objects.filter(is_active=True)
    })

def user_login(request):
    return render(request, "core/login.html")

@login_required
def user_logout(request):
	logout(request)
	return redirect('home')

@login_required
def edit_story(request, story_id=None):
	story = None

	if story_id:
		story = get_object_or_404(Story, pk=story_id)

		if story.user != request.user:
			return redirect('story/archive')

	if request.method == "POST":
		form = StoryForm(request.POST)

		if form.is_valid():
			if story_id is None:
				story = Story(user = request.user)

			story.title = form.cleaned_data['title']
			#story.template = form.cleaned_data['template']
			story.save()

			return redirect(reverse('story/edit', args=[story.id]) + "?status=" + ("updated" if story_id else "created"))

	elif story_id:
		form = StoryForm(initial={
			'title': story.title
		})
	else:
		form = StoryForm()

	return render(request, 'gamebook/story/edit.html', {
		'form': form,
		'button': ('Modifier' if story_id else 'Ajouter'),
		'title': ('Modifier une histoire existante' if story_id else 'Créer une nouvelle histoire'),
	})

@login_required
def edit_library(request, library_id=None):
	library = None

	if library_id:
		library = get_object_or_404(Library, pk=library_id)

		if library.user != request.user:
			return redirect('library/archive')

	if request.method == "POST":
		form = LibraryForm(request.POST)

		if form.is_valid():
			if library_id is None:
				library = Library(user = request.user)

			library.name = form.cleaned_data['name']
			# library.template = form.cleaned_data['template']
			library.save()

			return redirect(reverse('library/edit', args=[library.id]) + "?status=" + ("updated" if library_id else "created"))

	elif library_id:
		form = LibraryForm(initial={
			'title': library.title,
		})
	else:
		form = LibraryForm()

	return render(request, 'book/library/edit.html', {
		'form': form,
		'button': ('Modifier' if library_id else 'Ajouter'),
		'title': ('Modifier une bibliothèque existante' if library_id else 'Ajouter une nouvelle bibliothèque'),
	})

@login_required
def story_archive(request):
	return render(request, 'gamebook/story/index.html', {
		'stories': Story.objects.filter(user=request.user),
	})

@login_required
def page_archive(request, story_id):
    story = get_object_or_404(Story, pk=story_id, user=request.user)

    return render(request, 'gamebook/page/index.html', {
        'story': story,
        'pages': Page.objects.filter(story=story),
	})

@login_required
def edit_page(request, story_id, page_id=None):
    story = get_object_or_404(Story, pk=story_id, user=request.user)

    page = None

    if page_id:
        page = get_object_or_404(Page, pk=page_id)

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if page_id is None:
                page = Page(story=story)

            page.content = form.cleaned_data['content']
            page.save()

            return redirect(reverse('page/edit', args=[story.id, page.id]) + "?status=" + ("updated" if page_id else "created"))

    elif page_id:
        form = PageForm(initial={
            'content': page.content
        })
    else:
        form = PageForm()

    return render(request, 'gamebook/page/edit.html', {
        'story': story,
        'form': form,
        'button': ('Modifier' if page_id else 'Ajouter'),
        'title': ('Modifier une page existante' if page_id else 'Créer une nouvelle page'),
    })
