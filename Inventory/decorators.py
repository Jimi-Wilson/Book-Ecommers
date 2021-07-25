from django.shortcuts import render


def isStaff(view_func):
    def wrapper_func(request):
        user = request.user
        if user.is_staff:
            return view_func(request)
        else:
            return render(request, 'invalidCredentials.html')
    return wrapper_func

