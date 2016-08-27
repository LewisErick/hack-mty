# -*- coding: utf-8 -*-
"""Este módulo define las vistas de la aplicación

Las vistas funcionan como un controlador que envía ciertos datos a una
plantilla (documento HTML) y están asociadas con un enlace gracias al módulo
urls.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, date
from django.core.urlresolvers import reverse
from django.contrib import messages

@login_required  # El usuario debe estar identificado para acceder a la vista.
def dashboard(request):
    """Redirecciona a la plantilla de dashboard"""
    return render(request, 'empleado/dashboard.html')


@login_required
def agregarEmpleado(request):
    """Agrega a un empleado a la base de datos

    En un inicio crea una forma vacía para luego rellenarla con los datos de
    POST. Si son válidos, guarda al empleado registrando también la hora actual
    dentro de la base.
    """
    if request.method == 'POST':
        formaEmpleado = FormaEmpleado(request.POST)

        if formaEmpleado.is_valid():
            empleado = formaEmpleado.instance
            empleado.fecha_registro = datetime.now()
            empleado.salario_calculado = empleado.salario
            empleado.save()

            return HttpResponseRedirect(reverse('empleado:dashboard'))

    else:
        formaEmpleado = FormaEmpleado()

    return render(request, 'empleado/agregarEmpleado.html', {
            'formaEmpleado': formaEmpleado,
    })


def procesarEmpleados(listaEmpleados):
    """Procesa una lista de empleados (retorna sus atributos en una lista)

    Se deben procesar a los empleados porque no se puede mandar al objeto como
    tal a los templates"""
    empleadosProcesados = []

    for empleado in listaEmpleados:
        atributosEmpleado = []
        for atributo in empleado._meta.get_fields():
            try:
                atributosEmpleado.append(getattr(empleado, atributo.name))
            except AttributeError:
                atributosEmpleado.append("")

        empleadosProcesados.append(atributosEmpleado)

    return empleadosProcesados


def getHeadersEmpleado():
    """Retorna los headers de empleado en una lista"""
    headers = []
    for header in Empleado._meta.get_fields():
        headers.append(header)

    return headers


@login_required
def verEmpleados(request):
    """Muestra a los empleados registrados

    Regresa una lista que contiene listas de atributos para cada empleado y
    otra que contiene el nombre de cada atributo.
    """
    return render(request, 'empleado/verEmpleados.html', {
            'empleados': procesarEmpleados(Empleado.objects.all()),
            'headers': getHeadersEmpleado(),
    })


@login_required
def modificarEmpleado(request):
    """Permite modificar el empleado especificado por id

    Primero crea una forma con el empleado y la manda a renderizar. Después
    recibe al empleado, le añade la fecha de registro que tiene en la base
    y lo guarda para finalmente redireccionar a verEmpleados.
    """
    id = None

    if request.method == 'POST':
        formaEmpleado = FormaEmpleado(request.POST)

        if formaEmpleado.is_valid():
            empleado = formaEmpleado.instance
            empleado.id = request.POST.get('id')
            empleado.fecha_registro = Empleado.objects.get(
                id=request.POST.get('id')).fecha_registro
            empleado.save(force_update=True)

            return HttpResponseRedirect(reverse('empleado:verEmpleados'))

    else:
        id = int(request.GET.get('id'))
        empleadoEncontrado = Empleado.objects.get(id=id)

        formaEmpleado = FormaEmpleado(instance=empleadoEncontrado)

    return render(request, 'empleado/modificarEmpleado.html', {
            'formaEmpleado': formaEmpleado,
            'id': id,
    })


@login_required
def pasarLista(request):
    """Pasa lista al empleado seleccionado en su plantilla

    Primero envía una lista con todos los empleados a la plantilla. Luego
    obtiene el id del empleado a modificar, le pasa lista y lo guarda para
    redireccionar a pasarLista como último paso.
    """
    if request.method == 'POST':
        id = request.POST.get("id")
        empleado = Empleado.objects.get(id=id)
        pasaLista(empleado, request)
        empleado.save(force_update=True)

        return HttpResponseRedirect(reverse('empleado:pasarLista'))

    else:
        empleados = Empleado.objects.all()

        return render(request, 'empleado/pasarLista.html', {
                'empleados': empleados,
        })


def pasaLista(empleado, request):
    """Pasa lista al empleado enviado por pasarLista"""
    horaActual = datetime.now()
    hoy = date.today()
    entrada = datetime.combine(hoy, empleado.horaEntrada)
    salida = datetime.combine(hoy, empleado.horaSalida)
    tolerancia = timedelta(minutes=5)

    if(entrada - tolerancia <= horaActual <= entrada + tolerancia):
        # Si el empleado está en su hora de entrada, registra la entrada si
        # no la había pasado.
        if empleado.pasoEntrada:
            messages.error(request, "¡Usted ya registró entrada!")
        else:
            empleado.pasoEntrada = True
            messages.success(request, "Entrada registrada")
    elif(salida - tolerancia <= horaActual <= salida + tolerancia):
        # Si el empleado está en su hora de salida, registra la salida si
        # no la había pasado.
        if empleado.pasoSalida:
            messages.error(request, "¡Usted ya registró salida!")
        else:
            empleado.pasoSalida = True
            messages.success(request, "Salida registrada")
    elif(entrada < horaActual < salida):
        # Si el empleado está entre su entrada y salida, registra un retardo
        # si no había pasado entrada.
        if not Falta.objects.filter(empleado=empleado, fecha=hoy):
            if empleado.pasoEntrada:
                messages.error(request, "¡Usted ya registró entrada!")
            else:
                falta = Falta(empleado=empleado, es_falta=False,
                              es_activo=True,
                              fecha=horaActual.strftime("%Y-%m-%d"))
                falta.save()
                empleado.pasoEntrada = True
                messages.warning(request, "¡Advertencia! Entrada con retardo")
        else:
            messages.error(request, "¡Usted ya pasó entrada con retardo hoy!")
    else:
        # Si no es una hora válida ni de entrada ni de salida y tampoco se está
        # en retardo, se informa del error.
        messages.error(request, "Esta no es su hora de pase de lista. \
        Intente más tarde, por favor")

    # Se muestra la hora en que se procesó esta petición.
    messages.info(request, horaActual.strftime("Último intento registrado a las \
    %H:%M:%S"))


@login_required
def verAsistencias(request):
    """Hace listas de empleados que entraron/no entraron y salieron no
    salieron para mandarlas a los templates"""

    # Hace una lista de los empeados que llegaron a tiempo en la ENTRADA
    empleadosEntrada = Empleado.objects.filter(pasoEntrada=True)
    # Hace una lista de los empeados que NO llegaron a tiempo en la ENTRADA
    empleadosNoEntrada = Empleado.objects.filter(pasoEntrada=False)
    # Hace una lista de los empeados que llegaron a tiempo en la SALIDA
    empleadosSalida = Empleado.objects.filter(pasoSalida=True)
    # Hace una lista de los empeados que NO llegaron a tiempo en la SALIDA
    empleadosNoSalida = Empleado.objects.filter(pasoSalida=False)

    return render(request, 'empleado/verAsistencias.html', {
        'empleadosEntrada': procesarEmpleados(empleadosEntrada),
        'empleadosNoEntrada': procesarEmpleados(empleadosNoEntrada),
        'empleadosSalida': procesarEmpleados(empleadosSalida),
        'empleadosNoSalida': procesarEmpleados(empleadosNoSalida),
        'headers': getHeadersEmpleado(),
    })


@login_required
def verSalarios(request):
    """Muestra una lista de los salarios base y los calculados

    Itera sobre cada empleado y añade a la lista un diccionario con sus faltas
    y su nombre si tiene tanto salario base como calculado.
    """
    empleadosFaltas = []

    for empleado in Empleado.objects.all():
        if empleado.salario and empleado.salario_calculado:
            empleadoFaltas = {}
            empleadoFaltas['empleado'] = empleado
            empleadoFaltas['faltas'] = []

            for falta in Falta.objects.filter(empleado=empleado):
                if falta.es_activo:
                    empleadoFaltas['faltas'].append(falta)

            empleadosFaltas.append(empleadoFaltas)

    return render(request, 'empleado/verSalarios.html', {
        'empleadosFaltas': empleadosFaltas,
    })


@login_required
def modificarFalta(request):
    """Permite modificar una falta

    Primero crea una forma usando el id de la falta y la manda a renderizar.
    Posteriormente recibe los nuevos atributos y la guarda, regresando a la
    vista de verSalarios.
    """
    if request.method == "POST":
        formaFalta = FormaFalta(request.POST)

        if formaFalta.is_valid():
            falta = formaFalta.instance
            falta.id = request.POST.get("id")
            falta.save(force_update=True)  # Para que no se inserte una nueva.

            return HttpResponseRedirect(reverse('empleado:verSalarios'))
    else:
        id = request.GET.get('id')
        falta = Falta.objects.get(id=id)
        formaFalta = FormaFalta(instance=falta)

        return render(request, 'empleado/modificarFalta.html', {
            'formaFalta': formaFalta,
            'id': id,
        })
