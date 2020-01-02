import json

from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib import messages

from bestbonus import models


# class allBonusesView(View)
    # def get(*args, **kwargs)
    # def post(*args, **kwargs)


# Returns main page. Returns paginated bonuses via AJAX
# Paginates all bonuses, shows sweet bonuses(no dep).
def bonusRating(request):
    bonuses = models.Bonus.objects.all()

    #? Paginator paginates 6 bonuses
    paginator = Paginator(bonuses, 6)
    page = request.GET.get('page', 1)

    paginated_bonuses = paginator.get_page(page)
    
# Executes if an user clicks a paginaton button
# Checks if request is AJAX. If so returns JSON response with next paginated page
    if request.is_ajax():
        data = {}

        # When paginated bonuses are over it is hiding the paginator button
        if int(page) >= paginator.num_pages:
            data['paginator_hiding'] = True
                
        # Renders a string with html code of 'cardblock.html' template.
        data["html_from_view"] = render_to_string(
            template_name="cardblock.html", 
            context={
                'bonuses': paginated_bonuses,
        
                'bonuses_meta' : {
                    'count': paginator.count,
                    'title' : "Все бонусы",
                    'description' : 'В разделе расположены бесплатные и выгодные бонусы для пользователя......блабла',
                },
                }
        )
        # messages.info(request, 'Pagination works!!')
        return JsonResponse(data=data)
    
# If request is not AJAX(event was not triggered)
# Just returns first all bonuses paginator page 

#! Think about adding a paginaotr to sweet bonuses
# And returns all sweet bonuses
# Sweet bonuses = no dep bonuses
    sweet_bonuses = models.Bonus.objects.filter(dep_bool=False)

    context = {
        'bonuses' : paginated_bonuses,
        'bonuses_meta' : {
            'count': paginator.count,
            'title' : 'Все бонусы',
            'description' : 'В разделе расположены все бонусы бла бла бла......блабла',
        },

        'sweet_bonuses' : sweet_bonuses,
        'sweet_bonuses_meta': {
            'count' : sweet_bonuses.count,
            'title' : "Самые выгодные бонусы",
            'description' : 'В разделе расположены бесплатные и выгодные бонусы для пользователя......блабла',
        },

        'filter_box_meta': models.filterbox_meta_count(), 
    } 

    return render(request, 'base.html', context=context)


# Calls when user types some query text into search input. Works using AJAX
# Looks up bonuses comparing the query and return result JSON 
def ajaxSearch(request):
# Search input data
    search_query = request.GET.get('q', False)

# Marker variable
# Shows filter is called from filter-box
# Why do we use this var instead of 'form-data'??
# 'form-data' provides a non-empty object. So we cannot capture when when we have to work with it 
    filter_ = request.GET.get('filter', False)
    data = {}

    # AJAX can work with filter or search
    # Checks if filter is triggered. So if it returns JSON response with a template what contains filtered bonus queryset
    # If not, it returns JSON response filtered by search input query           
    if request.is_ajax():
        # Filtering
        if filter_:
            # Deserialization JSON object
            # 'form_data' contains different filter params what we need to apply to Filter Mechanism
            form_data = json.loads(request.GET.get('form_data'))

            # mainFilterWay - rendering function of Filter Mechanism for filter-box
            # Returns bonus queryset what fits filter params('form_data'))
            bonuses = models.Bonus.get_filtered_bonuses(form_data)
 
            data['html_from_view'] = render_to_string(
                template_name="cardblock.html", 
                context={
                    'bonuses': bonuses,
                    
                    'bonuses_meta' : {
                        'count': bonuses.count,
                        'title' : "Бонусы по вашему запросу",
                        'description' : 'Бонусы по вашему запросу, самые прикольные......блабла',
                    },
                    }
            )
            return JsonResponse(data=data)
        
        # Searching
        # Returns bonus queryset what fits search input
        bonuses = models.Bonus.get_searched_bonuses(search_query)

        data['html_from_view'] = render_to_string(
            template_name="cardblock.html", 
            context={
                'bonuses': bonuses,
                'bonuses_meta' : {
                        'count': bonuses.count,
                        'title' : "Бонусы по вашему поиску",
                        'description' : 'Обнаруженые бонусы по вашему запросу!!!........',
                    },
                }
        )
        return JsonResponse(data=data)
