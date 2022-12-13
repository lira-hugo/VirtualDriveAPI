"""Google Cloud Storage Configuration."""
from os import environ
from google.cloud import storage
from GoogleCloud_Storage.authenticate_implicit_with_adc import authenticate_implicit_with_adc

# Google Cloud Storage
bucketURL = environ.get('https://storage.googleapis.com')
bucketName = environ.get('turma_mtres2022_2_next')
bucketFolder = environ.get('gs://turmam03next20022/')

# Data
localFolder = environ.get('/home/sonny/Documentos/NExT/ExperienciadeTrabalho/googlecloud-storage/googlecloud-storage-tutorial-master/')

#Autentication
authenticate_implicit_with_adc(project_id="global-incline-369522")