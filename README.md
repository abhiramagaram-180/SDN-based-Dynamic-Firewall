# SDN-based-Dynamic-Firewall
# Dynamic Firewall with Security Event Logger

An SDN-based dynamic firewall that monitors TCP application traffic, dynamically applies firewall rules, and records security events through a centralized logging server.

## Project Overview


The system will simulate a network using **Mininet**, with an **SDN-controlled switch** and a **Ryu SDN controller**. TCP client and server applications will generate network traffic, while the firewall will monitor and classify the traffic and dynamically allow, deny, or block connections.

Security-related events will be sent to a centralized logging server for recording and analysis.

### Planned Architecture

```text
TCP Clients
    |
    v
Mininet Network
    |
    v
SDN Switch (Open vSwitch)
    |
    v
Ryu SDN Controller
    |
    +----> Dynamic Firewall
    |
    +----> Security Event Logger
    |
    v
TCP Application Server
