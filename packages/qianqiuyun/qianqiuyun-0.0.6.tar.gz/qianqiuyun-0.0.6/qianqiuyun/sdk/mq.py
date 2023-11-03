import nats
from qianqiuyun.sdk.util import get_env_ns

def get_mq(ns=None):
    ns = get_env_ns(ns)
    nc = nats.connect('nats://nats-server.%s.svc.cluster.local:4222' % ns)
    return nc