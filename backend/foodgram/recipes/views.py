"""
View-функции.
"""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page


#from .forms import CommentForm, PostForm
from .models import Follow, Ingredient, Recipe


@cache_page(20, key_prefix='index_page')
def index(request):
    """
    Метод главной страницы, куда выводятся
    последние добавленные рецепты.
    """
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, settings.PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'recipes/index.html', context)
