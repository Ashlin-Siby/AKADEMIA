from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

# def index(request):
#     template = loader.get_template('eventsCalendar/index.html')
#     cont = {
#         'data': "hello",
#     }
#     return HttpResponse(template.render(cont, request))

class index(TemplateView):
    template_name = "index.html"
