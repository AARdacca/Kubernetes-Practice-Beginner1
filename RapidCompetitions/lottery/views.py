from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Lottery
from .serializers import LotterySerializer


def view_lottery(request,pk):

    try:
        lottery = Lottery.objects.get(id=pk)
    except(ObjectDoesNotExist):
        return redirect('/')
    
    return render(request,'single_product.html', context={'lottery':lottery})




def single_lottery_view(request,pk):
    try:
        category = Category.objects.get(id=pk)
    except(ObjectDoesNotExist):
        return redirect('/')
    return render(request,'competitions.html',context={'category':category})




class GetLotteryDetails(APIView):
    permission_classes = []
    def post(self,request):
        data = request.data 
        if 'id_list' not in data:
            return Response({"msg":"Please Provide id_list"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        print(data['id_list'])

        ids = [d.get('id', None) for d in data['id_list']]
        print(ids)
        print(type(ids))
        lottery = Lottery.objects.filter(id__in = ids)
        ser = LotterySerializer(lottery,many = True, context={'request':request})
        return Response(ser.data, status=status.HTTP_200_OK)
    

def custom_lottery_view(request):

    return render(request,'draw.html')
