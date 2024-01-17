from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse, HttpResponse
import os
# Create your views here.

def hello(request):
    return HttpResponse("Hello world")

def predict(request):
    if request.method == "GET":
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'movies_new.csv')
            df = pd.read_csv(data_path)
            head = df.head()
            data_json = head.to_json()
            return JsonResponse({"data": data_json})
        except Exception as e:
            return JsonResponse({"error": str(e)})
            