# Tests

Manual test cases for the project. Each test lists its purpose, the exact
commands, the expected result, and the result actually observed in the VM.

Test environment: Ubuntu 22.04, Mininet 2.3.0, Open vSwitch 2.17.12
(OpenFlow 1.3), OS-Ken 3.1.1.

| ID | Name                         | Status |
|----|------------------------------|--------|
| T0 | Namespace connectivity test  | Passed |

---

## T0 – Namespace connectivity test

Topology script: `topology/ns_test.py` (one switch `s1`, hosts `h1` and `h2`,
plus a `root` node placed in the VM's root namespace).

### Purpose

Prove that the root network namespace, where the OS-Ken controller will run,
can exchange TCP traffic with the Mininet hosts. The connection goes through
an extra link from `s1` to the root namespace. The root side of that link is
`10.0.0.254/24` and the switch side is port `s1-eth3`.

### Why the root link is needed

Mininet hosts each live in their own network namespace, so they cannot reach
programs running in the VM's root namespace. The controller (and later the
report listener on port 7000) runs in the root namespace. The `root` node is
attached to `s1` with a real link, so it becomes one more port on the switch
with an address in the host subnet. Hosts can then send packets to
`10.0.0.254`, for example the app server's reports to the controller. The
OpenFlow control channel is separate and stays on `127.0.0.1:6653`.

### Why /24 and not /8

Mininet hosts default to `10.0.0.x/8`. A /8 covers `10.0.0.0` to
`10.255.255.255`, which overlaps the VM's NAT network `10.0.2.0/24`. The root
namespace would then have two routes covering the same addresses and could
lose its connection to the outside (for example `apt` or `git`). Using
`10.0.0.254/24` limits the root side to `10.0.0.0/24` and leaves `10.0.2.0/24`
untouched.

### Setup

Terminal 1 (controller):

```bash
osken-manager --verbose controller/learning_switch.py
```

Terminal 2 (topology, leaves the Mininet CLI open):

```bash
sudo python3 topology/ns_test.py
```

Terminal 3 is a plain shell in the VM. It is in the root namespace, so it is
the "root shell" in the tests below.

Check the root interface first:

```bash
ip addr show root-eth0
```

Expected: `10.0.0.254/24` on `root-eth0`.

### Test A – Root to hosts (ICMP)

Root shell:

```bash
ping -c 3 10.0.0.1
ping -c 3 10.0.0.2
```

Expected: 0% packet loss for both.

### Test B – Root to host (TCP)

Mininet CLI, start a listener on h1:

```
mininet> h1 nc -l 6000 &
```

Root shell, send a message:

```bash
echo "hello from root" | nc -q 1 10.0.0.1 6000
```

Expected: `hello from root` appears in the Mininet CLI output from h1's
listener, and the root shell's `nc` exits after one second.

### Test C – Host to root (TCP)

Root shell, start a listener (leave it running):

```bash
nc -l 7000
```

Mininet CLI, send from h2:

```
mininet> h2 sh -c 'echo "hello from h2" | nc -q 1 10.0.0.254 7000'
```

Expected: `hello from h2` appears in the root shell where `nc -l 7000` is
running.

### Test D – Host to root (ICMP) and full reachability

Mininet CLI:

```
mininet> h1 ping -c 3 10.0.0.254
mininet> h2 ping -c 3 10.0.0.254
mininet> pingall
```

Expected: 0% packet loss. `pingall` covers `h1`, `h2` and `root`.

### Result

All four tests (A–D) passed on Ubuntu 22.04 / Mininet 2.3.0 /
Open vSwitch 2.17.12 / OS-Ken 3.1.1.

---

<!-- Add later test cases below as T1, T2, ... using the same layout:
     purpose, setup, commands, expected result, actual result. -->
