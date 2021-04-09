from rest_framework import serializers
import ujson

with open('food.json') as f_food:
    food_list = ujson.load(f_food)


class PeopleSimpleSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField('get_alternate_name')
    age = serializers.IntegerField()
    fruits = serializers.SerializerMethodField()
    vegetables = serializers.SerializerMethodField()

    def get_alternate_name(self, people):
        return people['name']

    def get_fruits(self, people):
        for item in food_list:
            if item['type'] == 'fruits':
                fruits_category = item['names']
                break
        return [food for food in people['favouriteFood'] if food in fruits_category]

    def get_vegetables(self, people):
        for item in food_list:
            if item['type'] == 'vegetables':
                vegetables_category = item['names']
                break
        return [food for food in people['favouriteFood'] if food in vegetables_category]


class PeopleDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    address = serializers.CharField()
    phone = serializers.CharField()
