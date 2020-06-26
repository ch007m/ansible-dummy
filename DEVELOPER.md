## Instructions

Commands executed to create a collection containing a module, role and molecule test

- Create an ansible collection hosting the role, plugins/module
  ```bash
  ansible-galaxy collection init snowdrop.kubernetes --init-path ansible-kind
  ```
- Move the content of the collection to the parent folder
  ```bash
  cd ansible-kind && mv snowdrop/kubernetes/* . && rm -rf snowdrop/kubernetes
  ``` 
- Create now the folders structure of the `role`
  ```bash
  ansible-galaxy role init --init-path roles kind
  ```
- Move to the role and instantiate the molecule project
  ```bash
  cd roles/kind && molecule init scenario --role-name kind && cd ../..
  ```  
- Finally create a dummy module
  ```bash
  mkdir plugins/modules && touch plugins/modules/kind.py
  ```  
- Develop the `kind.py` module
```bash
cat <<EOF > plugins/modules/kind.py
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
EOF
```

- Test the module locally
  ```bash
  ansible localhost -M ./plugins/modules -m kind -a "cluster_name=myk8s version=1.17"
  localhost | SUCCESS => {
      "changed": false
  }
  ```
- Build and import the collection
  ```bash
  ansible-galaxy collection build
  Created collection for snowdrop.kubernetes at /Users/cmoullia/code/ch007m/ansible-kind/snowdrop-kubernetes-1.0.0.tar.gz -f
  
  ansible-galaxy collection install snowdrop-kubernetes-1.0.0.tar.gz -f 
  Process install dependency map
  Starting collection install process
  Skipping 'snowdrop.kubernetes' as it is already installed
  ```

- Create a playbook to test the collection
```bash
cat <<EOF > play.yml
---
- hosts: localhost
  connection: local
  collections:
  - snowdrop.kubernetes
  tasks:
  - name: Create a K8s cluster
    kind:
      cluster_name: my-k8s
      version: 1.17
  # - include_role:
  #     name: "kind"
EOF
```
- Test it locally
  ```bash
  ansible-playbook ./play.yml -vvv
  TASK [Create a K8s cluster] ********************************************************************************************************************************************************************************************************
  task path: /Users/cmoullia/code/ch007m/ansible-kind/play.yml:7
  ...
  ok: [localhost] => {
      "changed": false,
      "invocation": {
          "module_args": {
              "cluster_name": "my-k8s",
              "version": "1.17"
          }
      }
  }
  ```
  
    
  
