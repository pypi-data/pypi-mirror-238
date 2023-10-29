# python-osism

[![Quay](https://img.shields.io/badge/Quay-osism%2Fosism-blue.svg)](https://quay.io/repository/osism/osism)

``python-osism`` is responsible for controlling and providing various APIs within OSISM.

## Total overview

![osism](https://raw.githubusercontent.com/osism/python-osism/main/contrib/osism.drawio.png)

### python-osism in detail

![python-osism](https://raw.githubusercontent.com/osism/python-osism/main/contrib/python-osism.drawio.png)

## Services

### API

### Beat

### Listener

### Watchdog

## Workers

### Ansible

### Ceph

### Conductor

### Kolla

### Netbox

### OpenStack

### Reconciler

## Commands

### apply

### bifrost

### netbox

### reconciler

### service

### status

### worker

## States & Transitions

The state 0 is reserved. Newly added devices are always in state 0.

The transfer of a device from a state a to a new state b takes place in 4 phases.

In phase 1 the state of a device in the Netbox is changed.

In phase 2 the new configuration is generated based on the state in the Netbox.

In phase 3, the generated configuration is deployed on the switch.

In phase 4, the configuration on the switch is compared with the state in the Netbox.

After phase 4 is completed, the device is in the new state b.

![Netbox state machine](./contrib/netbox-state-machine.png)

```
dot -Tpng contrib/netbox-state-machine.dot -o contrib/netbox-state-machine.png
```

### Pre-defined states

* State 0: new device
* State a: unprovisioned device, ready for introspection
* State b: introspected device, ready for cleaning or provisioning
* State c: provisioned device
