# -*- coding: utf-8 -*-
"""Este módulo define las vistas de la aplicación

Las vistas funcionan como un controlador que envía ciertos datos a una
plantilla (documento HTML) y están asociadas con un enlace gracias al módulo
urls.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def test(request):
    """Redirecciona a la plantilla de dashboard"""
    return HttpResponse('Ush')
