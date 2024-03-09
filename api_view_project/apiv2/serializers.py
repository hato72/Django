from rest_framework import serializers
from api.models import Item,Product
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email','username','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user = get_user_model()
        return user.objects.create_user(
            validated_data['username'],
            email=validated_data['email'],
            password = validated_data['password']
        )


def check_divide(value):
    if value % 10 != 0:
        raise serializers.ValidationError("10で割り切れる値にして下さい")

class ItemModelSerializer(serializers.ModelSerializer):
    discounted_price = serializers.IntegerField(min_value=0,validators=[check_divide])

    class Meta:
        model = Item
        #fields = '__all__'
        fields = ['name','price','discounted_price']
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=['name','price'],
                message = 'nameとpriceの組み合わせは同じ値を入れないでください'
            )
        ]

    #アンダーバー以下の値のバリデーションを行える

    def validate_price(self,value): #priceに対するバリデーション
        if self.partial and value is None:
            return value
        # 1行目が0以外をはじく
        if value % 10 != 0:
            raise serializers.ValidationError("1桁目は0としてください")
        return value
    
    def validate_name(self,value):
        if self.partial and value is None:
            return value
        if value[0].islower():
            raise serializers.ValidationError("最初の文字は大文字にして下さい")
        return value
    
    #追加の値のバリデーション
    def validate(self,data):
        price = data.get('price',self.instance.price if self.instance is not None else None) #値が取得できなかった場合に元々ある値を取得する
        discounted_price = data.get('discounted_price',self.instance.discounted_price if self.instance is not None else None)
        if price < discounted_price:
            raise serializers.ValidationError("割引価格は本来の価格以下にして下さい")
        return data