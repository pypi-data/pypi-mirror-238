# Leostream-client-python

This is a python client for the Leostream REST API. It is a work in progress and is not yet complete.

## Installation

```bash
pip install leostream-client
```

## Usage

The client API can currently be used to query the following endpoints:
- [Centers](#centers)
Currently only the list and get methods are implemented.
- [Pools](#pools)
The create method is implemented. The list and get methods are implemented. Update is partially implemented but because the Leostream API does not support updating all fields of a pool it is not possible to update all fields of a pool in one go. The delete method is not implemented.
- [Gateways](#gateways)
The create method is implemented. The list and get methods are implemented. Update is not implemented. The delete method is not implemented.

- [Policies](#policies)
The create method is not implemented. The list and get methods are implemented. Update is not implemented. The delete method is not implemented.

- [Poolassignments](#poolassignments)
The create method is not implemented. The list and get methods are implemented. Update is not implemented. The delete method is not implemented.

### Authentication
The Leostream REST API endpoint requires authentication. The LeostreamClient class takes a username and password from the environment. The username and password are used to generate a token which is then used for all subsequent requests. See restapi.py for more details.

### Centers
Centers are the main organizational unit in Leostream. They are used to group pools and gateways. Currently only the list and get methods are implemented.
To list all centers in Leostream you can use the list method of the LeostreamCenter class.
```python
>>> from leostream import LeostreamCenter
>>> LeostreamCenter.list()
[{'flavor': 'I', 'id': 1, 'name': 'Vsphere', 'online': 0, 'os': '', 'status': 2, 'status_label': 'Offline', 'type': 'vcenter', 'type_label': 'VMware vSphere and vCenter Server'}, {'flavor': 'Z', 'id': 2, 'name': 'AWS Center', 'online': 0, 'os': 'Amazon Web Services', 'status': 2, 'status_label': 'Offline', 'type': 'amazon', 'type_label': 'Amazon Web Services'}]
```
To get a specific one you can pass the id to constructor.
```python
>>> center = LeostreamCenter(2)
>>> print(center.data['center_definition']['name'])
AWS Center
```

### Pools
To create a new pool in Leostream you need to pass a name and an array of one or more id's of centers to which the pool will belong. The center id's can be found iby [querying the centers endpoint](#centers).

```python
>>>from leostream import LeostreamPool
>>>pool = LeostreamPool(name='My Pool', center_id=[1])
>>>print(pool._id)
103
```

To get a list of all pools use the list method of the LeostreamPool class.
```python
>>>from leostream import LeostreamPool
>>>LeostreamPool.list()
[{'assigned_vm': 0, 'available_vm': 0, 'id': 1, 'name': 'All Desktops', 'parent_pool_id': 0, 'total_agent_running': 0, 'total_connected': 0, 'total_logged_in': 0, 'total_vm': 0, 'total_vm_running': 0, 'total_vm_stopped': 0, 'total_vm_suspended': 0, 'unavailable_vm': 0}, {'assigned_vm': 0, 'available_vm': 0, 'id': 4, 'name': 'All Linux Desktops', 'parent_pool_id': 1, 'total_agent_running': 0, 'total_connected': 0, 'total_logged_in': 0, 'total_vm': 0, 'total_vm_running': 0, 'total_vm_stopped': 0, 'total_vm_suspended': 0, 'unavailable_vm': 0}, {'assigned_vm': 0, 'available_vm': 0, 'id': 3, 'name': 'All Windows Desktops', 'parent_pool_id': 1, 'total_agent_running': 0, 'total_connected': 0, 'total_logged_in': 0, 'total_vm': 0, 'total_vm_running': 0, 'total_vm_stopped': 0, 'total_vm_suspended': 0, 'unavailable_vm': 0}, {'assigned_vm': 0, 'available_vm': 0, 'id': 11, 'name': 'Linux Advanced Desktop Pool', 'parent_pool_id': 4, 'total_agent_running': 0, 'total_connected': 0, 'total_logged_in': 0, 'total_vm': 0, 'total_vm_running': 0, 'total_vm_stopped': 0, 'total_vm_suspended': 0, 'unavailable_vm': 0}, {'assigned_vm': 0, 'available_vm': 0, 'id': 103, 'name': 'My Pool', 'parent_pool_id': 1, 'total_agent_running': 0, 'total_connected': 0, 'total_logged_in': 0, 'total_vm': 0, 'total_vm_running': 0, 'total_vm_stopped': 0, 'total_vm_suspended': 0, 'unavailable_vm': 0}, {'assigned_vm': 0, 'available_vm': 0, 'id': 23, 'name': 'us-dev-rhel7-g3.4xl-pool', 'parent_pool_id': 4, 'total_agent_running': 0, 'total_connected': 0, 'total_logged_in': 0, 'total_vm': 0, 'total_vm_running': 0, 'total_vm_stopped': 0, 'total_vm_suspended': 0, 'unavailable_vm': 0}]
```

To get a specific pool you can pass the id to constructor.
```python
>>>pool = LeostreamPool(23)
>>> print(pool.data['name'])
us-dev-rhel7-g3.4xl-pool
```

### Gateways
To create a gateway you need to pass a name and an address to the constructor. The address can be either an IP address or a DNS name. The address must be resolvable by the Leostream broker. The address can be a public IP address or a private IP address. If the address is a private IP address then the Leostream broker must be able to reach the address. If the address is a public IP address then the Leostream broker must be reachable from the address.

```python
>>>from leostream import LeostreamGateway
>>>gateway = LeostreamGateway(name='My Gateway', address='192.168.178.105')
>>>print(gateway.data)
{'address': '192.168.178.105', 'address_private': '', 'created': '2023-11-01 22:08:21', 'forward_to': '', 'id': 49, 'load_balancer_id': 0, 'name': 'My Gateway', 'notes': '', 'online': 1, 'signature': '', 'updated': '2023-11-01 22:08:21', 'use_src_ip': 2, 'version': ''}
```

To get a list of all gateways use the list method of the LeostreamGateway class.
```python
>>>from leostream import LeostreamGateway
>>> LeostreamGateway.list()
[{'id': 49, 'name': 'My Gateway'}]
```

To get a specific gateway you can pass the id to constructor.
```python
>>>gateway = LeostreamGateway(49)
>>>print(gateway.data['name'])
My Gateway
```

### Policies
Create is not implemented yet. To get a list of all policies use the list method of the LeostreamPolicy class.
```python
>>>from leostream import LeostreamPolicy
>>> LeostreamPolicy.list()
[{'id': 1, 'name': 'Default'}, {'id': 2, 'name': 'test'}]
```

To get a specific policy you can pass the id to constructor.
```python
>>>policy = LeostreamPolicy(2)
>>>print(policy.data['name'])
test
```

### Poolassignments
Create is not implemented yet. To get a list of all poolassignments use the list method of the LeostreamPoolassignment class and pass the id of the policy to which the poolassignments belong.
```python
>>>from leostream import LeostreamPoolAssignment
>>>LeostreamPoolAssignment.list(2)
[{'id': 2, 'pool_id': 23, 'pool_name': 'us-dev-rhel7-g3.4xl-pool'}, {'id': 3, 'pool_id': 3, 'pool_name': 'All Windows Desktops'}]
```

To get a specific poolassignment you can pass the id and policy id to constructor.
```python
>>> from leostream import LeostreamPoolAssignment
>>> poolassignment = LeostreamPoolAssignment(2,2)
>>> print(poolassignment.data)
{'adjust_timezone': 0, 'attribute_filter': [], 'attribute_join': 'a', 'auto_login': 0, 'backup_pool_criteria_agent': 0, 'backup_pool_criteria_empty': 0, 'backup_pool_criteria_viewer': 0, 'backup_pool_id': 0, 'bu_plan_power_control_data': {'id': 1, 'name': 'Default'}, 'bu_plan_power_control_id': 1, 'bu_plan_protocol_data': {'id': 1, 'name': 'Default'}, 'bu_plan_protocol_id': 1, 'bu_plan_release_data': {'id': 1, 'name': 'Default'}, 'bu_plan_release_id': 1, 'confirm_power_state': 0, 'created': '2023-11-01 16:06:23', 'display_mode': '0', 'email_decline_shadowing': 0, 'email_shadowing': 0, 'enable_power_control': 0, 'enable_shadowing': 0, 'favor_previous_assigned': 1, 'id': 2, 'kiosk': 0, 'login_as': 'R', 'logout_rogue': 0, 'offer_filter': '0', 'offer_filter_json': {}, 'offer_pending_reboot': 1, 'offer_quantity': 1, 'offer_running_without_hda': 0, 'on_assign_url': '', 'on_assign_url_cb': 0, 'on_assign_url_timeout': 5, 'plan_power_control_data': {'id': 1, 'name': 'Default'}, 'plan_power_control_id': 1, 'plan_protocol_data': {'id': 1, 'name': 'Default'}, 'plan_protocol_id': 1, 'plan_release_data': {'id': 1, 'name': 'Default'}, 'plan_release_id': 1, 'plan_script_data': {'id': 0, 'name': ''}, 'plan_script_id': 0, 'policy_id': 2, 'pool_data': {'created': '2023-06-28 17:34:19', 'display_name': 'US | DEV | RHEL7 | 16CPU | 122GB', 'id': 23, 'is_root': 0, 'name': 'us-dev-rhel7-g3.4xl-pool', 'pool_type': 'D', 'read_only': 0, 'updated': '2023-11-01 22:15:29'}, 'pool_id': 23, 'power_on': 0, 'prevent_release': 0, 'revert_to_snapshot': 0, 'shadowing_filter': '0', 'shadowing_filter_json': {}, 'start_if_stopped': 1, 'updated': '2023-11-01 19:42:56'}
```
