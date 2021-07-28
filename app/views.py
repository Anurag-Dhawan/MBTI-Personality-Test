from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np 
import pandas as pd 
import joblib
import re
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from django.http import JsonResponse
# Create your views here.
@csrf_exempt

def home(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)

        inputstr=" "

        for element in received_json_data:
          inputstr+=element[4:]
        print(inputstr)  

        
        vectorizer = joblib.load("vectorizer.dat")
        #all_words = vectorizer.get_feature_names()
        #tfizer = TfidfTransformer()
        tfizer = joblib.load("tfizer.dat")
        all_words = joblib.load("all_words.dat")
        final_test = tfizer.transform(vectorizer.transform([inputstr])).toarray()

        test_point = pd.DataFrame.from_dict({w: final_test[:, i] for i, w in enumerate(all_words)})
        fav_classifier = joblib.load("fav_classifier.dat")
        info_classifier = joblib.load("info_classifier.dat")
        decision_classifier = joblib.load("decision_classifier.dat")
        str_classifier = joblib.load("str_classifier.dat")
        
        predper=" "
        pred = fav_classifier.predict_proba(test_point) #[I, E]
        labels = ['I','E']
        predper+= labels[np.argmax(pred)]

        pred = info_classifier.predict_proba(test_point) #[N,S]
        labels = ['N','S']
        predper+= labels[np.argmax(pred)]
        pred = decision_classifier.predict_proba(test_point) #[F, T]
        labels = ['F','T']
        predper+=labels[np.argmax(pred)]
        pred = str_classifier.predict_proba(test_point) #[P, J]
        labels = ['P','J']
        predper+= labels[np.argmax(pred)]
        print(predper)
        return JsonResponse(predper,safe=False)
        if predper == "ENFJ":
            return render(request,'ENFJ.html')
        elif predper=="ENFP":
            return render(request,'ENFP.html')
        elif predper=="ENTJ":
            return render(request,'ENTJ.html')
        elif predper=="ENTP":
            return render(request,'ENTP.html')
        elif predper=="ESFJ":
            return render(request,'ESFJ.html')
        elif predper=="ESFP":
            return render(request,'ESFP.html')
        elif predper=="ESTJ":
            return render(request,'ENFP.html')
        elif predper=="ESTP":
            return render(request,'ESTP.html')
        elif predper=="INFJ":
            return render(request,'INFJ.html')
        elif predper== " INFP":
            print("yes")
            return render(request,'INFP.html')
        elif predper=="INTJ":
            return render(request,'INTJ.html')
        elif predper=="INTP":
            return render(request,'INTP.html')
        elif predper=="ISFJ":
            return render(request,'ISFJ.html')
        elif predper=="ISFP":
            return render(request,'ISFP.html')
        elif predper=="ISTJ":
            return render(request,'ISTJ.html')
        elif predper=="ISTP":
            return render(request,'ISTP.html')
    else:
        return render(request,'index.html')

def INFP(request):
    return render(request,'INFP.html')  