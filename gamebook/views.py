from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import ActionForm, PageForm, StoryForm
from .models import Action, Page, Story


def home(request):
    stories = []

    for story in Story.objects.filter(is_active=True):
        stories.append({
            "title": story.title,
            "first_page": Page.objects.filter(
                is_first_page=True, story=story
            ).first()
        })

    return render(request, "core/home.html", {
        "stories": stories,
    })


def user_login(request):
    return render(request, "core/login.html")


def play(request, page_id):
    page = get_object_or_404(Page, id=page_id)

    actions = []
    for action in Action.objects.filter(page=page):
        actions.append({
            "label": action.label,
            "destination": Page.objects.filter(
                id=action.extra['destination']
            ).first()
        })

    return render(request, "gamebook/play.html", {
        "page": page,
        "actions": actions,
    })


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
                story = Story(user=request.user)

            story.title = form.cleaned_data['title']
            # story.template = form.cleaned_data['template']
            story.save()

            return redirect(
                reverse(
                    'story/edit',
                    args=[story.id]) + "?status=" + ("updated" if story_id else "created")  # nopep8
            )

    elif story_id:
        form = StoryForm(initial={
            'title': story.title
        })
    else:
        form = StoryForm()

    return render(request, 'gamebook/story/edit.html', {
        'form': form,
        'button': ('Modifier' if story_id else 'Ajouter'),
        'title': ('Modifier une histoire existante' if story_id else 'Créer une nouvelle histoire'),  # nopep8
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
                library = Library(user=request.user)

            library.name = form.cleaned_data['name']
            # library.template = form.cleaned_data['template']
            library.save()

            return redirect(
                reverse(
                    'library/edit',
                    args=[library.id]) + "?status=" + ("updated" if library_id else "created")  # nopep8
            )

    elif library_id:
        form = LibraryForm(initial={
            'title': library.title,
        })
    else:
        form = LibraryForm()

    return render(request, 'book/library/edit.html', {
        'form': form,
        'button': ('Modifier' if library_id else 'Ajouter'),
        'title': ('Modifier une bibliothèque existante' if library_id else 'Ajouter une nouvelle bibliothèque'),  # nopep8
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
            # If this is the new First Page, be sure it's the only one
            Page.objects.filter(story=story).update(is_first_page=False)

            if page_id is None:
                page = Page(story=story)

            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.is_first_page = form.cleaned_data['is_first_page']
            page.save()

            return redirect(
                reverse(
                    'page/edit',
                    args=[story.id, page.id]) + "?status=" + ("updated" if page_id else "created")  # nopep8
            )

    elif page_id:
        form = PageForm(initial={
            'title': page.title,
            'content': page.content,
            "is_first_page": page.is_first_page,
        })
    else:
        form = PageForm()

    actions = []
    for action in Action.objects.filter(page=page):
        actions.append({
            "label": action.label,
            "id": action.id,
            "destination": Page.objects.filter(
                id=action.extra['destination']
            ).first()
        })

    return render(request, 'gamebook/page/edit.html', {
        'story': story,
        'page': page,
        'page_id': page_id,
        'form': form,
        'action': ('edit' if page_id else 'add'),
        "actions": actions,
        'button': ('Modifier' if page_id else 'Ajouter'),
        'title': ('Modifier une page existante' if page_id else 'Créer une nouvelle page'),  # nopep8
    })


@login_required
def edit_action(request, page_id, action_id=None):
    page = get_object_or_404(Page, pk=page_id)
    story = get_object_or_404(Story, pk=page.story.pk, user=request.user)

    action = None

    if action_id:
        action = get_object_or_404(Action, pk=action_id)

    if request.method == "POST":
        form = ActionForm(request.POST, story=story)

        if form.is_valid():
            if action_id is None:
                action = Action(page=page)

            action.label = form.cleaned_data['label']
            action.extra = {
                "destination": str(form.cleaned_data['destination'].pk)
            }
            action.save()

            return redirect(
                reverse(
                    'action/edit',
                    args=[page.id, action.id]) + "?status=" + ("updated" if action_id else "created")  # nopep8
            )

    elif action_id:
        destination = None
        if "destination" in action.extra:
            destination = Page.objects.filter(
                pk=action.extra['destination']
            ).first()

        form = ActionForm(initial={
            'label': action.label,
            'destination': destination,
        }, story=story)
    else:
        form = ActionForm(story=story)

    return render(request, 'gamebook/action/edit.html', {
        'story': story,
        'page': page,
        'form': form,
        'action': action,
        'button': ('Modifier' if action_id else 'Ajouter'),
        'title': ('Modifier une action existante' if action_id else 'Créer une nouvelle action'),  # nopep8
    })
