#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.k8s.common import K8sAnsibleMixin
from kubernetes.client import ApiClient

class FakeKubeResponse:
    def __init__(self, obj):
        import json
        self.data = json.dumps(obj)

def main():
    module_args = dict(
        # cluster_name=dict(type='str', required=True),
        # version=dict(type='str', required=True),
        pod_namespace=dict(type='str'),
        label_selectors=dict(type='list', elements='str', default=[]),
    )

    module = AnsibleModule(
        argument_spec=module_args,
    )

    k8s = K8sAnsibleMixin()
    k8s.client = k8s.get_api_client()

    type = {'kind': 'Pod', 'apiVersion': 'v1'}
    result = k8s.kubernetes_facts(
        type['kind'],
        type['apiVersion'],
        "",
        module.params['pod_namespace'],
        module.params['label_selectors'],
        "")

    pods = result['resources']
    for i in pods:
        jsonPod = i

    api_client = ApiClient()
    fake_kube_response = FakeKubeResponse(jsonPod)
    v1pod = api_client.deserialize(fake_kube_response, 'V1Pod')
    response = "Pod : name %s, running under namespace: %s, status is : %s" % (v1pod.metadata.name,
                v1pod.metadata.namespace,
                v1pod.status.conditions)

    result = {'changed': True, 'result': response}
    module.exit_json(**result)

if __name__ == '__main__':
    main()
