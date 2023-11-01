from google.cloud import pubsub_v1

class Publisher:
  def __init__(self, p: pubsub_v1.PublisherClient, topic: str):
    self.p = p
    self.topic = topic

def topic(location: str = 'london', gcp_project: str = 'vipro-core-services') -> Publisher:
  p = pubsub_v1.PublisherClient()
  topic_name = p.topic_path(gcp_project, f"ips-{location}-ingress")
  return Publisher(p, topic_name)
