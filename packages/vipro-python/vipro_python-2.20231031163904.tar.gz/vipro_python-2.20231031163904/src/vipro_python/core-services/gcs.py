from google.cloud import storage

def bucket(payload: dict = None, ips: dict = None):
  if payload is not None:
    return _bucket_for_ips(payload['ips'])
  elif ips is not None:
    return _bucket_for_ips(ips)
  return None

def _bucket_for_ips(ips: dict):
  gcs = storage.Client()
  return gcs.get_bucket(ips['bucketId'])

def download_extract(bucket: storage.Bucket, remote_path: str, local_file: str):
  print(f"downloading file <{remote_path}> to local file {local_file}")
  bucket.blob(remote_path).download_to_filename(local_file)
