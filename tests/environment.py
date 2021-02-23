from dpb1.frequencies import HaplotypeFreqs
import os
from pyard import ARD

def before_all(context):
    # Start test client
    os.environ["FLASK_ENV"] = "testing"
    # Enable Py-ard
    os.environ["ENABLE_PYARD"] = "True"
    from server import app
    app.testing = True
    context.client = app.test_client()
    context.ard = ARD()

    # Provide testing haplotype frequencies
    context.hap_freqs = HaplotypeFreqs(directory='tests/data/frequencies')
    pass