from django.shortcuts import render
import joblib
from django.conf import settings
from .models import Transaction
from .forms import TransactionForm
from django.db.models import Avg
import numpy as np
from django.http import JsonResponse



try:
    ML_PIPELINE=joblib.load(settings.ML_MODEL_PATH)
    print("Modele de machine learning chargé")
except FileNotFoundError:
    ML_PIPELINE=None
    print("Model is not found")

def predict_view(request):
    result=None
    form=TransactionForm(request.POST or None)

    if request.method=='POST' and form.is_valid():

        df=form.cleaned_data

        #### Creation du vecteur de features
        features = np.array([[
            df['montant'],
            df['heure'],
            df['nb_transactions_24h'],
            df['distance_domicile'],
            float(df['pays_etranger']),
            float(df['nouvelle_carte']),
        ]])
        proba=ML_PIPELINE.predict_proba(features)[0]
        probabilite_fraude=float(proba[1])
        est_fraud=probabilite_fraude>=0.5

        transaction=form.save(commit=False)
        transaction.est_fraud=est_fraud
        transaction.probabilite_fraude=probabilite_fraude
        transaction.save()

        niveau, badge = transaction.get_niveau_risque()

        result = {
            'transaction':transaction,
            'probabilite_pct':round(probabilite_fraude*100, 1),
            'niveau_risque':niveau,
            'badge':badge,
            'est_fraud':est_fraud,
        }

    return render(request, 'detector/predict.html', {
        'form':form,
        'result':result,
    })

def history_views(request):
    transactions=Transaction.objects.all()

    filtre = request.GET.get("filtre", "toutes")
    if filtre=='fraudes':
        transactions = transactions.filter(est_fraud=True)
    elif filtre=='legitimes':
        transactions = transactions.filter(est_fraud=False)

    total = transactions.count()
    nb_fraud= transactions.filter(est_fraud=True).count()
    nb_legitimes= transactions.filter(est_fraud=False).count()

    return render(request, 'detector/history.html', {
        'transactions':transactions,
        'total':total,
        'nb_fraud':nb_fraud,
        'nb_legitimes':nb_legitimes,
        'filtre':filtre,
    })

def dashboard(request):
    all_trans=Transaction.objects.all()
    total_trans=all_trans.count()

    if total_trans==0 :
        return render(request, 'detector/dashboard.html', {'no_data':True})

    nb_fraudes= all_trans.filter(est_fraud=True).count()
    nb_legitime= all_trans.filter(est_fraud=False).count()

    taux_fraude=round(nb_fraudes/total_trans *100, 1)

    moy_fraud=all_trans.filter(est_fraud=True).aggregate(m=Avg('montant'))['m'] or 0
    moy_legitime=all_trans.filter(est_fraud=False).aggregate(m=Avg('montant'))['m'] or 0

    return render(request, 'detector/dashboard.html', {
        'total_trans':total_trans,
        'nb_fraudes':nb_fraudes,
        'nb_legitime':nb_legitime,
        'taux_fraude':taux_fraude,
        'moy_legitime':moy_legitime,
        'moy_fraud':moy_fraud
    })
