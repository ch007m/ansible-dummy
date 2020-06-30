# Ansible Collection - snowdrop.kubernetes

Documentation for the collection.

## Role

- To install the `kind` binary using the releases published on github under `kubernetes-sigs/kind`, use the following command
  ```bash
  $ ANSIBLE_ROLES_PATH=$(pwd)/roles ansible-playbook ./playbooks/role.yml -e kind_version=v0.8.0
  ```
- You can install the latest release
  ```bash
  $ ANSIBLE_ROLES_PATH=$(pwd)/roles ansible-playbook ./playbooks/role.yml
  ```  
- Or force to reinstall `kind`
  ```bash 
  $ ANSIBLE_ROLES_PATH=$(pwd)/roles ansible-playbook ./playbooks/role.yml \
                           -e kind_version=v0.8.0 \
                           -e kind_force_client_install=true
  ```
  
## Collection

- To use the role packaged as a collection, execute the following commands:
  ```bash
  ansible-galaxy collection build       
  Created collection for snowdrop.kubernetes at $HOME/yoour/path/ansible-kind/snowdrop-kubernetes-1.0.0.tar.gz
  
  ansible-galaxy collection install $HOME/yoour/path/ansible-kind/snowdrop-kubernetes-1.0.0.tar.gz
  Process install dependency map
  Starting collection install process
  Installing 'snowdrop.kubernetes:1.0.0' to '$HOME/.ansible/collections/ansible_collections/snowdrop/kubernetes'
  ```
- Next, create a playbook using this collection:
  ```yaml
  ---
  - hosts: localhost
    connection: local
    collections:
    - snowdrop.kubernetes
    tasks:
    - include_role:
        name: "kind"
  ```
  
- Finally, call it
  ```bash
  ansible-playbook ./playbooks/collection.yml
  ```