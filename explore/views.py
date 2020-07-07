from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# from explore.models import Corpus
from explorer.parts.main import load_layout
from explorer.parts.strings import _slug_from_name
from .forms import UploadCorpusForm

from django.conf import settings

if settings.BUZZWORD_SPECIFIC_CORPUS:
    HOME_URL = f"/{settings.BUZZWORD_SPECIFIC_CORPUS}"
else:
    HOME_URL = "/"


def _make_path(slug):
    return f"storage/{slug}"


def _store_corpus_file(corpus_file, slug):
    """
        store the corpus file sent by the user
        in the local storage. fails if a corpus with
        the same slug already exists.
    """
    path = _make_path(slug)
    with open(_make_path(slug), "xb") as storage:
        for chunk in corpus_file.chunks():
            storage.write(chunk)
    return path


def _start_parse_corpus_job(corpus):
    # todo: implement this function
    pass


#@login_required
def explore(request, slug):
    app = load_layout(slug)
    return render(request, "explore/explore.html")


@login_required
def upload(request):
    if request.method == "POST":
        form = UploadCorpusForm(request.POST, request.FILES)
        if form.is_valid():
            slug = _slug_from_name(form.cleaned_data["name"])
            try:
                path = _store_corpus_file(request.FILES["corpus_file"], slug)
            except Exception:
                # TODO: was not able to store corpus file. possibly duplicate slug.
                # handle gracefully
                raise
            corpus = form.save(commit=False)
            corpus.slug = slug
            corpus.path = path
            corpus.save()
            _start_parse_corpus_job(corpus)
            return redirect(HOME_URL)
    else:
        form = UploadCorpusForm()

    context = {"form": form, "navbar": "upload"}

    return render(request, "explore/upload.html", context)
