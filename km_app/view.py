from django.shortcuts import redirect

def start(request):
    return redirect('clients:view')