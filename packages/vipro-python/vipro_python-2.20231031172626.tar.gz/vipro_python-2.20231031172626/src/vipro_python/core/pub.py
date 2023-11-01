from google.cloud import pubsub_v1
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_structured

class Publisher:
  def __init__(self, p: pubsub_v1.PublisherClient, topic: str):
    self.p = p
    self.topic = topic

  # re-usable publish method for sending extract records to ips ingress
  def publish(self, attrs: dict, e: CloudEvent):
      # make row specific changes to IPS
      attrs['source'] = e['source']
      attrs['subject'] = e['subject']
      attrs['type'] = e['type']
      _, body = to_structured(e)
      # then publish
      self.p.publish(self.topic, body, **attrs)


def ips_topic(location: str = 'london', gcp_project: str = 'vipro-core-services') -> Publisher:
  p = pubsub_v1.PublisherClient()
  topic_name = p.topic_path(gcp_project, f"ips-{location}-ingress")
  return Publisher(p, topic_name)
