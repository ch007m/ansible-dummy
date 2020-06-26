#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def main():

    module_args = dict(
        cluster_name=dict(type='str', required=True),
        version=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
    )

    result = dict(
        changed=False
    )

    module.exit_json(**result)

if __name__ == '__main__':
    main()