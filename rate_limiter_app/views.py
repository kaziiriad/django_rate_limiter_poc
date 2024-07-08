from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

def test_api(request):
    return JsonResponse({"status": "success"})
    
