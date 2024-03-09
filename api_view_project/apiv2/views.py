from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemModelSerializer,UserModelSerializer,ProductModelSerializer
from rest_framework import status
from api.models import Item,Product
from rest_framework import permissions
from .permissions import CustomPermission
from django.contrib.auth import get_user_model

# Create your views here.

class BaseListView(APIView):
    def get(self,request):  #一覧画面を返す
        objects = self.model.objects.all()
        serializer = self.serializer_class(objects,many=True)
        # print(items)
        # print(serializer)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        #バリデーション
        # print(serializer.is_valid(raise_exception=True)) #例外を返す
        # print(serializer.errors)
        if serializer.is_valid(raise_exception=True):
            serializer.save() # 保存(create) or 更新
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.data)


class BaseDetailView(APIView):
    def get(self,request,pk):
        obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)
    
    def put(self,request,pk):
        obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(obj,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self,request,pk):
        obj = self.model.objects.get(pk=pk)
        print(request.data)
        serializer = self.serializer_class(obj,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class ItemModelView(BaseListView):

    serializer_class = ItemModelSerializer
    permission_classes = [CustomPermission]


class ProductModelView(BaseListView):
    serializer_class = ProductModelSerializer
    model = Product

class UserModelView(BaseListView):
    serializer_class = UserModelSerializer
    model = get_user_model()




class ItemModelDetailView(BaseDetailView):
    serializer_class = ItemModelSerializer
    model = Item
    permission_classes = [CustomPermission]

class ProductModelDetailView(BaseDetailView):
    serializer_class = ProductModelSerializer
    model = Product


class UserModelDetailView(BaseDetailView):
    serializer_class = UserModelSerializer
    model = get_user_model()
