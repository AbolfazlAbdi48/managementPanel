from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def test(request):
    return render(request, 'base/_Base.html')
