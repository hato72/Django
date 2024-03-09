from rest_framework import serializers
from .models import Item

def check_divide(value):
    if value % 10 != 0:
        raise serializers.ValidationError("10で割り切れる値にして下さい")

class ItemSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=20)
    price = serializers.IntegerField(min_value=0)
    discounted_price = serializers.IntegerField(min_value=0,validators=[check_divide])

    #アンダーバー以下の値のバリデーションを行える

    def validate_price(self,value): #priceに対するバリデーション
        print(f'price:{value}')
        # 1行目が0以外をはじく
        if value % 10 != 0:
            raise serializers.ValidationError("1桁目は0としてください")
        return value
    
    def validate_name(self,value):
        if self.partial and value is None:
            return value
        print(f'name:{value}')
        if value[0].islower():
            raise serializers.ValidationError("最初の文字は大文字にして下さい")
        return value
    
    #追加の値のバリデーション
    def validate(self,data):
        print(f'data:{data}')

        price = data.get('price',self.instance.price if self.instance is not None else None) #値が取得できなかった場合に元々ある値を取得する
        discounted_price = data.get('discounted_price',self.instance.discounted_price if self.instance is not None else None)
        if price < discounted_price:
            raise serializers.ValidationError("割引価格は本来の価格以下にして下さい")
        return data
    

    def create(self,validated_data):
        print("createを実行")     
        print(validated_data)   
        return Item.objects.create(**validated_data)
        
    def update(self,instance,validated_data):
        # print("updateを実行")
        # print(instance)
        # print(validated_data)
        instance.name = validated_data.get('name',instance.name)
        instance.price = validated_data.get('price',instance.price)
        instance.discounted_price = validated_data.get('discounted_price',instance.discounted_price)
        instance.save()
        return instance