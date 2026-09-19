from django.db import models

class Transaction(models.Model):
    #### Input / Features
    montant =models.FloatField()
    heure= models.FloatField()
    nb_transactions_24h=models.FloatField()
    distance_domicile=models.FloatField()
    pays_etranger=models.BooleanField(default=False)
    nouvelle_carte=models.BooleanField(default=False)

    ##### Resultats 
    est_fraud=models.BooleanField(default=False)
    probabilite_fraude=models.FloatField(default=0.0)

    date_analyse=models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        statut='FRAUDE' if self.est_fraud else 'Légitime'
        return f"Transaction - {self.montant} - {statut}"
    
    ####### Methode des kpis de risques

    def get_niveau_risque(self):
        p=self.probabilite_fraude
        if p>=0.8: return("Tres elevé", "danger")
        if p>=0.5: return("Elevé", "warning")
        if p>=0.3: return("Modere", "info")
        return ("Faible", "success")
    
    class Meta :
        ordering =['-date_analyse']

