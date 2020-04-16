from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.contrib.auth.models import User
from .models import Question
from .serializers import QuestionSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins


# Create your views here.
# without wrapper for API view

# @csrf_exempt
# def questions_list(request):
#
#     try:
#         question_queryset = Question.objects.all()
#     except Question.DoesNotExist:
#         return JsonResponse({"error": "Instance not found"}, status=404)
#
#     if request.method == 'GET':
#         # serializer instance holds the queryset data that is serialized in a python datatype
#         serializer = QuestionSerializer(question_queryset, many=True)
#         # in order to serialize non-dict (here tuple) objects we set safe=False
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == "POST":
#         # parsing post data from user to JSON
#         data = JSONParser().parse(request)
#         # for creation of new object we have to pass the data as data=data
#         serializer = QuestionSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         else:
#             return JsonResponse(serializer.errors, status=400)
#
# # getting , updating & deleting a single instance
# # wrapping API views @api view decorator for function based views
# # Response comprises of all responses like HTTP or JSON response
#
# # WITH @API VIEW DECORATOR (Wrapper)

# @csrf_exempt
# @api_view(['GET', 'PUT', 'DELETE'])
# def question_detail(request, id):
#
#     try:
#         single_queryset = Question.objects.get(pk=id)
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     # GET for single instance
#     if request.method == "GET":
#         serializer = QuestionSerializer(single_queryset)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         data = request.data
#         # takes in instance as a para by which it knows to edit an existing object & not to create new one
#         serializer = QuestionSerializer(instance=single_queryset, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "DELETE":
#         single_queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Class Based API views in REST
# using the API View wrapper

class QuestionAPIView(APIView):

    """
    API View is the wrapper that make sure this view receives request,
    context is passed to the response object which will help in content type negotiation

    list all the questions objects, or create a new one
    """

    # listing all question objects
    def get(self, request):
        question_queryset = Question.objects.all()
        serializer = QuestionSerializer(question_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        #temporary
        account = User.objects.get(pk=1)
        # assigning question object with user ie account instance, as it is not defined inside Serializer class
        # and to create a new question object User field is required
        # kinda ORM from shell for creating a new user instance
        question = Question(user=account)

        # user entering data, that request is passed
        data = request.data
        serializer = QuestionSerializer(question, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIView(APIView):
    """
    Lists, edits, deletes a single question instance
    """
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404
    # GET
    def get(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    # UPDATE/PUT
    def put(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, pk, request):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Using Generic API View & Mixins
# generic class provides the core functionality
# mixins provides the .list() & .create() actions, get & post method we explicitly bind these actions to it

# class QuestionListGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#     # this fnc overrides the serializer.save(), thus by allowing the logged in user to be able to Create new instance
#     # takes in user as an argument
#     #def perform_create(self, serializer):
#         #serializer.save(user=self.request.user)
#
#
# class QuestionDetailGenericView(generics.GenericAPIView,
#                                 mixins.RetrieveModelMixin,
#                                 mixins.UpdateModelMixin,
#                                 mixins.DestroyModelMixin):
#
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     lookup_field = 'id'
#
#     def get(self, request):
#         return self.retrieve(request)
#
#     def put(self, request):
#         return self.update(request)
#
#     def delete(self, request):
#         return self.delete(request)
#
#
