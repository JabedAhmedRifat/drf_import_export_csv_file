from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import uuid
from .models import *
from .serializers import *
from django.conf import settings
import os
import time


@api_view(['POST'])
def createStudent(request):
    data = request.data 
    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)



@api_view(['GET', 'POST'])
def export_import_excel(request):
    if request.method == 'GET':
        stu_obj = Student.objects.all()
        serializer = StudentSerializer(stu_obj, many=True)
        df = pd.DataFrame(serializer.data)
        print(df)
        file_path = f'public/static/excel/{uuid.uuid4()}.csv'
        df.to_csv(file_path, encoding='UTF-8')
        
        
        time.sleep(60)  
        
        if os.path.exists(file_path):
            os.remove(file_path)
        return Response({'status': 200})
        
        

    elif request.method == 'POST':
        excel_file = request.FILES.get('files')
        if excel_file:
            exceled_upload_obj = ExcelFileUpload.objects.create(excel_file_upload=excel_file)
            file_path = f'{settings.BASE_DIR}/public/static/{exceled_upload_obj.excel_file_upload}'
            df = pd.read_csv(file_path)
            print(df.values.tolist())
            # os.delete(file_path)
            return Response({'status': 200})
        else:
            return Response({'status': 400})
