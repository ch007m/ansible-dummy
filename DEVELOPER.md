Table of Contents
=================

  * [Instructions](#instructions)
  * [Testing](#testing)

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
  ansible-galaxy collection build -f
  Created collection for snowdrop.kubernetes at /Users/cmoullia/code/ch007m/ansible-kind/snowdrop-kubernetes-1.0.0.tar.gz 
  
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
- Uncomment the line of the `play.yml` playbook to include the role and test it
  ```bash
  ansible-playbook ./play.yml
  ...
  TASK [snowdrop.kubernetes.kind : debug] ********************************************************************************************************************************************************************************************
  ok: [localhost] => {
      "msg": "Hello world!"
  }
  ```
## Testing

- Install the module dependency
  ```bash
  pip3 install molecule
  ```
- Instantiate the `molecule testing` project
  ```bash
  molecule init scenario --role-name kind
  ``` 
- Create a new folder containing the resources needed to run the tests using playbooks, templates, vars ...
  ```bash
  mkdir -p molecule/resources
  ``` 
- Move under the `resources` folder, the yml files of the scenario to play except the file `molecule.yml`
  ```bash
  mv ./molecule/default/^molecule.yml* ./molecule/resources
  ```
- Reconfigure the molecule.yml file to point to the resource files
  ```bash
  ---
  dependency:
    name: galaxy
  driver:
    name: docker
  platforms:
    - name: instance
      image: docker.io/pycontribs/centos:7
      pre_build_image: true
  provisioner:
    name: ansible
    playbooks:
        converge: ../resources/converge.yml
        # prepare: ../resources/prepare.yml
        verify: ../resources/verify.yml
  verifier:
    name: ansible
  ``` 
        
- Launch docker and test it
  ```bash
  molecule test
  ``` 
- TODO: Expand this section when more stuff will be ready to test     
  
