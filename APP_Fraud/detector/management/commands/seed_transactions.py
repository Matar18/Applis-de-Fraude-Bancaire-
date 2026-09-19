import joblib
import numpy as np
from django.conf import settings
from django.core.management.base import BaseCommand

from detector.models import Transaction

EXAMPLES = [
    dict(
        reference="DEMO-001",
        montant=42.90,
        heure=13,
        nb_transactions_24h=2,
        distance_domicile=1.5,
        pays_etranger=False,
        nouvelle_carte=False,
    ),
    dict(
        reference="DEMO-002",
        montant=2850.00,
        heure=3,
        nb_transactions_24h=6,
        distance_domicile=980.0,
        pays_etranger=True,
        nouvelle_carte=True,
    ),
    dict(
        reference="DEMO-003",
        montant=89.50,
        heure=18,
        nb_transactions_24h=1,
        distance_domicile=3.2,
        pays_etranger=False,
        nouvelle_carte=False,
    ),
    dict(
        reference="DEMO-004",
        montant=1200.00,
        heure=2,
        nb_transactions_24h=8,
        distance_domicile=650.0,
        pays_etranger=True,
        nouvelle_carte=False,
    ),
    dict(
        reference="DEMO-005",
        montant=25.00,
        heure=9,
        nb_transactions_24h=1,
        distance_domicile=0.8,
        pays_etranger=False,
        nouvelle_carte=False,
    ),
    dict(
        reference="DEMO-006",
        montant=610.00,
        heure=23,
        nb_transactions_24h=5,
        distance_domicile=210.0,
        pays_etranger=False,
        nouvelle_carte=True,
    ),
]


class Command(BaseCommand):
    help = "Seed a fixed set of example transactions so the demo dashboard is never empty."

    def handle(self, *args, **options):
        try:
            pipeline = joblib.load(settings.ML_MODEL_PATH)
        except FileNotFoundError:
            self.stderr.write("ML model not found, skipping seed.")
            return

        for example in EXAMPLES:
            features = np.array([[
                example["montant"],
                example["heure"],
                example["nb_transactions_24h"],
                example["distance_domicile"],
                float(example["pays_etranger"]),
                float(example["nouvelle_carte"]),
            ]])
            probabilite_fraude = float(pipeline.predict_proba(features)[0][1])

            Transaction.objects.update_or_create(
                reference=example["reference"],
                defaults=dict(
                    montant=example["montant"],
                    heure=example["heure"],
                    nb_transactions_24h=example["nb_transactions_24h"],
                    distance_domicile=example["distance_domicile"],
                    pays_etranger=example["pays_etranger"],
                    nouvelle_carte=example["nouvelle_carte"],
                    est_fraud=probabilite_fraude >= 0.5,
                    probabilite_fraude=probabilite_fraude,
                ),
            )

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(EXAMPLES)} example transactions."))
