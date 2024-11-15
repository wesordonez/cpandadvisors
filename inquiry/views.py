from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from django_ratelimit.decorators import ratelimit

from django.utils.translation import get_language

from .models import Inquiry
from .forms import InquiryForm


@require_http_methods(['GET', 'POST'])
def inquiry_view(request):  

    if request.method == 'GET':
        language_code = get_language()

        return render(request, 'inquiry/inquiry-create.html', {'language_code': language_code})
    
    elif request.method == 'POST':

        form = InquiryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("contact-success")

        return render(request, 'inquiry/inquiry-create.html', {
                'errors': form.errors,
                'data': request.POST,
        })
    

@require_http_methods(['POST'])
@ratelimit(key='ip', rate='10/min', method=ratelimit.ALL, block=True)
def inquiry_api_view(request):
    

    form = InquiryForm(request.POST)

    if form.is_valid():
        form.save(commit=False)
        
        return JsonResponse({'success': 'inquiry submitted'}, status=200)

    else:
        # print("errors: ", form.errors, form.non_field_errors)
        return JsonResponse({'error': 'invalid data error'}, status=400)


@require_http_methods(['GET'])
def inquiry_success(request):

    return render(request, "components/pages/success.html", {
        'title': 'Consulta Enviada', 
        'description': 'Gracias por tomarse el tiempo para enviar una consulta, nuestro equipo se pondrá en contacto con usted en breve.'
    })