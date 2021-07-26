from django.shortcuts import render


def is_staff(view_func):
    def wrapper_func(request, id=None):
        user = request.user
        if user.is_staff:
            if id == None:
                return view_func(request)
            else:
                return view_func(request, id)
        else:
            return render(request, 'invalidCredentials.html')

    return wrapper_func
