from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Question
from .serializers import QuestionSerializer

# Create your views here.

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
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

# getting , updating & deleting a single instance
@csrf_exempt

def question_detail(request, id):

    try:
        single_queryset = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return JsonResponse({"error": "Instance not found"}, status=404)

    # GET for single instance
    if request.method == "GET":
        serializer = QuestionSerializer(single_queryset)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        # takes in instance as a para by which it knows to edit an existing object & not to create new one
        serializer = QuestionSerializer(instance=single_queryset, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        single_queryset.delete()
        return HttpResponse(status=204)


