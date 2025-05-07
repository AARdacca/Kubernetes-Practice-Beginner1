from django.shortcuts import render




def cart_view(request):

    if request.user.is_authenticated:
        return render(request,'cart.html', context={'cart':'cart',})
    else:
        return render(request,'cart.html')
    
