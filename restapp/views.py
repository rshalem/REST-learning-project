from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Question
from .serializers import QuestionSerializer

# Create your views here.
# without wrapper for API view
@csrf_exempt
def questions_list(request):

    try:
        question_queryset = Question.objects.all()
    except Question.DoesNotExist:
        return JsonResponse({"error": "Instance not found"}, status=404)

    if request.method == 'GET':
        # serializer instance holds the queryset data that is serialized in a python datatype
        serializer = QuestionSerializer(question_queryset, many=True)
        # in order to serialize non-dict (here tuple) objects we set safe=False
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        # parsing post data from user to JSON
        data = JSONParser().parse(request)
        # for creation of new object we have to pass the data as data=data
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

# getting , updating & deleting a single instance
# wrapping API views @api view decorator for function based views
# Response comprises of all responses like HTTP or JSON response

# WITH @API VIEW DECORATOR (Wrapper)
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request, id):

    try:
        single_queryset = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET for single instance
    if request.method == "GET":
        serializer = QuestionSerializer(single_queryset)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = request.data
        # takes in instance as a para by which it knows to edit an existing object & not to create new one
        serializer = QuestionSerializer(instance=single_queryset, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        single_queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


