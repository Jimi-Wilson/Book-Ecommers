from django.shortcuts import render


def is_staff(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'invalidCredentials.html')

    return wrapper_func
