from google.cloud import firestore

def db(auth_instance: str, gcp_project: str = 'vipro-core-services'):
  db = firestore.Client(project=gcp_project)
  return db.collection("scriptengine").document(auth_instance)
