from django.shortcuts import render, redirect


# Create your views here.
def main(request):
    """The main view,
    redirect user to other url.
    """
    return redirect('login')
