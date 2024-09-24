from django.shortcuts import render
from rest_framework import viewsets
from . forms import SalesForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from . models import SalesData
from . serializers import SalesDataSerializer

import joblib
import numpy as np


class SalsesDataView(viewsets.ModelViewSet):
	queryset = SalesData.objects.all()
	serializer_class = SalesDataSerializer
		
# @api_view(["POST"])
def SalesDatapredict(request):
	try:
		mdl=joblib.load("apis/model_22-09-2024-12-49-52.pkl")
		
		mydata=request.data
		unit=np.array(list(mydata.values()))
		unit=unit.reshape(1,-1)
		scalers=joblib.load("apis/preprocessing_pipeline.pkl")
		X=scalers.transform(unit)
		y_pred=mdl.predict(X)
		ans = int(y_pred)
		return JsonResponse('Your Status is {}'.format(ans), safe=False)
	except ValueError as e:
		return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
	

def salesFormView(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            form_data = {
                'Store': form.cleaned_data['Store'],
                'DayOfWeek': form.cleaned_data['DayOfWeek'],
                'Date': form.cleaned_data['Date'],
                'Open': form.cleaned_data['Open'],
                'Promo': form.cleaned_data['Promo'],
                'StateHoliday': form.cleaned_data['StateHoliday'],
                'SchoolHoliday': form.cleaned_data['SchoolHoliday'],
                'StoreType': form.cleaned_data['StoreType'],
                'Assortment': form.cleaned_data['Assortment'],
                'CompetitionDistance': form.cleaned_data['CompetitionDistance'],
                'CompetitionOpenSinceMonth': form.cleaned_data['CompetitionOpenSinceMonth'],
                'CompetitionOpenSinceYear': form.cleaned_data['CompetitionOpenSinceYear'],
                'Promo2': form.cleaned_data['Promo2'],
                'Promo2SinceWeek': form.cleaned_data['Promo2SinceWeek'],
                'Promo2SinceYear': form.cleaned_data['Promo2SinceYear'],
                'PromoInterval': form.cleaned_data['PromoInterval']
            }

            # Convert the data to the format expected by the preprocessor and model
            import pandas as pd
            input_data = pd.DataFrame([form_data])  # Convert to a DataFrame for the pipeline

            # Load your preprocessor pipeline and model
            import joblib
            preprocessor = joblib.load('C:/Users/user/Documents/Programming/Python/Django_ml/apis/preprocessing_pipeline.pkl')
            model = joblib.load('C:/Users/user/Documents/Programming/Python/Django_ml/apis/model_22-09-2024-12-49-52.pkl')

            # Apply preprocessing to the input data
            processed_data = preprocessor.transform(input_data)

            # Make prediction
            prediction = model.predict(processed_data)

            # Return the prediction as part of the response
            return JsonResponse({'status': 'success', 'prediction': prediction[0]})
    
    # For GET requests, render the form
    form = SalesForm()
    return render(request, 'myform/SalesForm.html', {'form': form})