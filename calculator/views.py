import json
import math
import pdb
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'calculator/index.html')


def calc_op(request):
    if request.method == 'GET':

        arr1 = request.GET.getlist('arr1[]')
        print(arr1)
        arr2 = request.GET.getlist('arr2[]')
        # pdb.set_trace()
        print ("**get**")
        arr_len = len(arr1)
        data = int(arr1[0])
        for i in range(arr_len - 1):
            if (arr2[i] == '+'):
                qt = arr2[i]
                data = int(arr1[i + 1]) + data
                # pdb.set_trace()
            elif (arr2[i] == '-'):
                data = data - int(arr1[i + 1])
            elif (arr2[i] == '*'):
                data = data * int(arr1[i + 1])
            elif (arr2[i] == '/'):
                data = data / int(arr1[i + 1])
            elif (arr2[i] == 'log'):
                data = math.log(int(arr1[i + 1]), data)
        data = json.dumps(data)

        mimetype = 'application/json'
        # pdb.set_trace()
        return HttpResponse(data, mimetype)
