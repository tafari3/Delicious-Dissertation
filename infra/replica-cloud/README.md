# Controlled Replica Cloud Contract
Stage 1 uses XCP-ng as the hypervisor and Xen Orchestra as management/orchestration.

Required logical roles:
- scanner VM;
- synthetic `government-permit-service-fastapi` target VM;
- database/supporting service, separate where resources permit;
- Xen Orchestra management/orchestration;
- management and service/test network roles separated where feasible.

This directory intentionally contains no guessed IP addresses, VLAN IDs, storage repositories, credentials or production details. Environment-specific values are recorded only after the controlled lab is provisioned and verified.
