from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import ujson
from api.Serilizers import PeopleSimpleSerializer, PeopleDetailSerializer
from api.helper import CustomPagePagination


# load data from people.json
with open('people.json') as f_people:
    people_list = ujson.load(f_people)


# load data from companies.json
with open('companies.json') as f_companies:
    companies_list = ujson.load(f_companies)


class CompanyEmployee(APIView):

    def get(self, request, pk):
        data_dict = {
            # we can predefine this code to give frontend engineer more information
            # I use 10000 as an example.
            'code': 100000,
            'msg': 'success',
            'results': [],
        }

        # return extra information when index matches no company
        if not any(pk == item['index'] for item in companies_list):
            data_dict['code'] = 100001
            data_dict['msg'] = 'no such company'
            return Response(data_dict, status=status.HTTP_204_NO_CONTENT)
        else:
            res = [item for item in people_list if int(pk) == item['company_id']]

            # return extra information when the company does not have any employees
            if len(res) == 0:
                data_dict['code'] = 100002
                data_dict['msg'] = 'no employee in this company'
                return Response(data_dict, status=status.HTTP_204_NO_CONTENT)
            else:
                # return all company's employees with pagination
                paginated_obj = CustomPagePagination()
                data_dict['result'] = paginated_obj.paginate_queryset(queryset=res, request=request, view=self)
                return paginated_obj.get_paginated_response(data_dict)


class CompanyEmployeeWithoutPagination(APIView):

    def get(self, request, pk):
        data_dict = {
            # we can predefine this code to give frontend engineer more information
            # I use 10000 as an example.
            'code': 100000,
            'msg': 'success',
            'results': [],
        }

        # return extra information when index matches no company
        if not any(pk == item['index'] for item in companies_list):
            data_dict['code'] = 100001
            data_dict['msg'] = 'no such company'
            return Response(data_dict, status=status.HTTP_204_NO_CONTENT)
        else:
            res = [item for item in people_list if int(pk) == item['company_id']]

            # return extra information when the company does not have any employees
            if len(res) == 0:
                data_dict['code'] = 100002
                data_dict['msg'] = 'no employee in this company'
            else:
                # return all company's employees
                data_dict['results'] = res
            return Response(data_dict)


class PeopleInfo(APIView):

    def get(self, request, pk):
        query_set = {}
        for item in people_list:
            if pk == item['_id']:
                query_set = item
                break
        # when empty, status code is 204
        if len(query_set) == 0:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        serializer = PeopleSimpleSerializer(query_set)
        return Response(serializer.data)


class Relations(APIView):

    def get(self, request, id1, id2):
        data_dict = {
            'code': 100000,
            'msg': 'success',
            'results': {},
        }
        two_person_list = []

        for item in people_list:
            if item['index'] == int(id1) or item['index'] == int(id2):
                two_person_list.append(item)
                if len(two_person_list) == 2:
                    break

        if len(two_person_list) != 2:
            data_dict['code'] = 100003
            data_dict['msg'] = "can't find two people with these inputs"
            return Response(data_dict, status=status.HTTP_204_NO_CONTENT)

        person1 = two_person_list[0]
        person2 = two_person_list[1]
        common_friends_set = set(item['index'] for item in person1['friends']) \
                             & set(item['index'] for item in person2['friends'])
        common_friends_list = [item for item in people_list if item['index'] in common_friends_set
                               and not item['has_died'] and item['eyeColor'] == 'brown']

        serializer1 = PeopleDetailSerializer(person1)
        serializer2 = PeopleDetailSerializer(person2)
        data_dict['results'] = {'person1': serializer1.data, 'person2': serializer2.data,
                                'common_friends': common_friends_list}

        return Response(data_dict)
