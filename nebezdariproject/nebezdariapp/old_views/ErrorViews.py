from django.shortcuts import render


def error_400(request, exception):
    data = {}
    return render(request, 'errors/400.html', data)

def error_403(request, exception):
    data = {}
    return render(request, 'errors/403.html', data)

def error_404(request, exception):
    data = {}
    return render(request, 'errors/404.html', data)

def error_500(request):
    data = {}
    return render(request, 'errors/500.html', data)