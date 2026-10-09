# Dynamic Firewall with Security Event Logger

A Computer Networks mini-project exploring socket programming,
Software-Defined Networking (SDN), dynamic traffic filtering, and
centralized security-event logging.

> **Current status:** The development environment and basic SDN
> forwarding test have been verified. The complete TCP application,
> security logger, dynamic firewall, recovery logic, and performance
> experiments are still to be implemented.

## 1. Project overview

The project aims to demonstrate how an SDN controller can dynamically
manage network traffic while a socket-based application communicates
across hosts and security events are recorded.

The planned project will include these functional areas:

-   TCP client/server communication using Python sockets.
-   Traffic classification using information such as source,
    destination, and port.
-   An SDN controller that communicates with Open vSwitch over OpenFlow.
-   Dynamic blocking of selected traffic and subsequent
    recovery/unblocking.
-   Centralized logging of relevant security events.
-   Multiple-client testing.
-   Experiments measuring blocking response time and network impact.
-   Documentation and a repeatable demonstration.

The exact implementation and module boundaries will be refined during
development.

## 2. Tested environment

The following versions and configuration have been tested in the current
development environment:

  -----------------------------------------------------------------------
  Component                           Tested configuration
  ----------------------------------- -----------------------------------
  Host operating system               Windows

  Virtualization                      Oracle VirtualBox

  VM name                             `CN-Project-Ubuntu`

  Guest operating system              Ubuntu 22.04.5 LTS Desktop

  VM resources                        4 CPUs, approximately 6 GB RAM, 40
                                      GB virtual disk

  Python                              3.10.12

  Git                                 2.34.1

  Mininet                             2.3.0

  Open vSwitch                        2.17.12

  SDN controller library              OS-Ken 3.1.1, installed in a Python
                                      virtual environment

  Southbound protocol                 OpenFlow 1.3

  Editor                              Visual Studio Code on Windows with
                                      Remote - SSH
  -----------------------------------------------------------------------

The VM uses VirtualBox NAT networking. SSH port forwarding maps Windows
`127.0.0.1:2222` to port `22` inside Ubuntu.

These are the versions used for the successful test. Teammates should
record their versions and test their own environment rather than
assuming every system will behave identically.

## 3. Prerequisites

### Required software

1.  **Oracle VirtualBox** --- runs the Ubuntu VM on a Windows host.
2.  **Ubuntu 22.04 LTS** --- provides the Linux environment needed by
    Mininet and Open vSwitch.
3.  **Git** --- repository and version-control operations.
4.  **Python 3, pip, and venv** --- Python development and isolated
    dependencies.
5.  **Mininet** --- creates virtual hosts, links, and network
    topologies.
6.  **Open vSwitch** --- provides the virtual switch used by Mininet.
7.  **OS-Ken** --- SDN controller framework used in this environment.
8.  **Visual Studio Code and Remote - SSH** --- optional but recommended
    for editing and running code from Windows while it executes inside
    Ubuntu.

A Windows host with enough free disk space and memory is required to run
the VM comfortably. The tested VM configuration used 4 CPUs, about 6 GB
RAM, and a 40 GB virtual disk.

## 4. Install the Ubuntu environment

### 4.1 Create the VM

In VirtualBox:

1.  Create a VM named `CN-Project-Ubuntu`.
2.  Install Ubuntu 22.04 LTS Desktop from an official Ubuntu image.
3.  Allocate around 4 CPUs, 6 GB RAM, and a 40 GB virtual disk if your
    computer can comfortably support these settings.
4.  Configure the VM's network adapter to use **NAT**.
5.  Start Ubuntu and complete its initial setup.

These resource settings match the development VM; adjust them to suit
the host computer if necessary.

### 4.2 Update Ubuntu and install base packages

Open a terminal inside Ubuntu and run:

``` bash
sudo apt update
sudo apt upgrade -y
sudo apt install git mininet openvswitch-switch python3-pip python3-venv openssh-server build-essential libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev -y
```

Check the installed versions:

``` bash
python3 --version
git --version
mn --version
ovs-vsctl --version
```

The current development VM reported Python 3.10.12, Git 2.34.1, Mininet
2.3.0, and Open vSwitch 2.17.12.

### 4.3 Install OS-Ken in an isolated virtual environment

The original Ryu 4.34 installation encountered dependency compatibility
errors in this environment. We therefore switched to OS-Ken and verified
that it could run a controller and communicate with Mininet.

Create and activate the virtual environment:

``` bash
python3 -m venv ~/osken/venv
source ~/osken/venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "os-ken<4.0"
```

Verify that the controller command is available:

``` bash
which python
osken-manager --help
```

The Python path should point to:

``` text
/home/<your-ubuntu-username>/osken/venv/bin/python
```

The tested environment used OS-Ken 3.1.1. The virtual environment must
be activated in each new terminal where OS-Ken commands are run:

``` bash
source ~/osken/venv/bin/activate
```

Do not assume that activating a virtual environment in one terminal
activates it in other terminal tabs.

## 5. Connect Windows VS Code to Ubuntu using SSH

This lets teammates edit files using VS Code on Windows while commands
and project code run inside the Ubuntu VM.

### 5.1 Enable SSH inside Ubuntu

In an Ubuntu terminal:

``` bash
sudo systemctl enable --now ssh
systemctl status ssh
```

The SSH service should show as active.

### 5.2 Configure VirtualBox port forwarding

With the VM powered on or off as supported by the VirtualBox settings
UI, open the VM's **Settings → Network → Adapter 1 → Advanced → Port
Forwarding**.

Add a rule with these values:

  Field        Value
  ------------ -------------
  Name         `SSH`
  Protocol     `TCP`
  Host IP      `127.0.0.1`
  Host Port    `2222`
  Guest IP     Leave blank
  Guest Port   `22`

Save the rule. The host port `2222` is used to avoid needing to expose
SSH directly on the host's standard port.

### 5.3 Test the connection from Windows

Open PowerShell on Windows and run:

``` powershell
ssh -p 2222 <ubuntu-username>@127.0.0.1
```

Replace `<ubuntu-username>` with the username created in Ubuntu. For the
original development VM, the username is `vboxuser`.

The first connection may ask you to confirm the host key. Confirm it
only if you expect to be connecting to your own VM, then enter the
Ubuntu account password when prompted.

### 5.4 Connect through VS Code

1.  Install Visual Studio Code on Windows.

2.  Install Microsoft's **Remote - SSH** extension.

3.  Open the Command Palette (`Ctrl+Shift+P`).

4.  Choose **Remote-SSH: Connect to Host...**.

5.  Enter or select:

    ``` text
    ssh -p 2222 <ubuntu-username>@127.0.0.1
    ```

6.  Once connected, open the project folder inside Ubuntu:

    ``` text
    /home/<ubuntu-username>/sdn-dynamic-firewall
    ```

The VS Code status bar should indicate an SSH connection. Use a VS Code
terminal in that remote window to run Linux commands.

**Important:** The Ubuntu VM must be running, and the SSH service must
be active, for Remote - SSH to connect. If the VM is shut down, start it
before reconnecting.

## 6. Create or open the project workspace

Inside Ubuntu, create the workspace if it does not already exist:

``` bash
mkdir -p ~/sdn-dynamic-firewall
cd ~/sdn-dynamic-firewall
```

If the team already has a GitHub repository, clone it into an
appropriate location instead of creating a duplicate project directory.
Follow the repository's existing README and branch conventions.

For the original development machine, the workspace is:

``` text
/home/vboxuser/sdn-dynamic-firewall
```

## 7. Verify Mininet and Open vSwitch

### 7.1 Basic Mininet check

Run:

``` bash
sudo mn
```

At the `mininet>` prompt:

``` text
nodes
net
pingall
exit
```

This checks that Mininet can start a basic topology and that its hosts
can communicate in the basic setup.

### 7.2 Test the SDN controller connection and forwarding

Activate the OS-Ken environment in one VS Code remote terminal:

``` bash
source ~/osken/venv/bin/activate
cd ~/sdn-dynamic-firewall
osken-manager --verbose ./controller_test.py
```

Keep this terminal open while the controller runs.

In a **second** remote terminal, start a two-host Mininet topology:

``` bash
sudo mn --topo single,2 --controller remote,ip=127.0.0.1,port=6653 --switch ovsk,protocols=OpenFlow13
```

At the `mininet>` prompt, run:

``` text
pingall
```

In the tested environment, the learning-switch controller and Mininet
reported:

``` text
*** Results: 0% dropped (2/2 received)
```

This is a basic SDN connectivity test. It does **not** verify the
dynamic firewall, TCP application, event logger, or automatic recovery
functionality.

To stop the test, type `exit` in Mininet, then press `Ctrl+C` in the
controller terminal.

If `controller_test.py` is not present in the repository, this test
cannot be run until the file is obtained from the development version or
recreated. Do not treat this temporary test controller as the final
firewall controller.

## 8. Planned implementation areas

The project requirements call for these broad areas of work:

1.  **TCP communication:** clients and a server exchange messages over
    sockets.
2.  **Traffic classification:** identify relevant traffic using source,
    destination, and port information.
3.  **SDN control:** communicate with Open vSwitch using the controller
    and OpenFlow.
4.  **Dynamic firewall behavior:** block selected traffic and
    demonstrate recovery or unblocking.
5.  **Security-event logging:** centrally record relevant events and
    firewall actions.
6.  **Multi-client tests:** verify behavior with more than one client.
7.  **Performance experiments:** measure blocking response time and
    network impact using a documented, repeatable method.
8.  **Documentation and demonstration:** provide setup, usage, test
    results, and material for the project demo and viva.

The exact architecture, file layout, rule-management design, and
integration sequence are development decisions to be finalized by the
team.

## 9. Current progress and known limitations

### Verified

-   Ubuntu VM is running.
-   Base packages are installed.
-   Mininet and Open vSwitch are installed.
-   OS-Ken is installed in an isolated Python environment.
-   SSH access from Windows to Ubuntu works.
-   VS Code Remote - SSH works.
-   A temporary OS-Ken learning-switch controller was tested with
    Mininet using OpenFlow 1.3.
-   `pingall` passed with 0% packet loss in the basic two-host topology.

### Still to implement or validate

-   TCP client/server application.
-   Centralized security-event logger.
-   Final SDN controller and firewall rules.
-   Dynamic blocking and recovery.
-   Multiple-client and end-to-end integration tests.
-   Performance measurements, result files, and final project
    documentation.

### Known compatibility note

Ryu 4.34 was attempted but failed due to dependency compatibility
problems in this environment. OS-Ken is the working alternative
currently used. Keep controller dependencies isolated in the
`~/osken/venv` environment, and test dependency/version changes before
adopting them across the team.

## 10. Safe shutdown and resuming work

Before shutting down:

1.  Save all edited files in VS Code.

2.  Type `exit` in the Mininet terminal.

3.  Press `Ctrl+C` in the controller terminal.

4.  Shut down Ubuntu normally using its desktop power menu or:

    ``` bash
    sudo poweroff
    ```

5.  Wait for Ubuntu to shut down, then shut down Windows normally.

The installed packages, virtual environment, VM settings, and saved
project files remain on the VM's virtual disk. After restarting, start
the VM and reconnect through VS Code Remote - SSH. You do not need to
reinstall everything. You will need to restart Mininet and the
controller when you want to run the tests again.

## 11. Team setup checklist

-   [ ] Ubuntu 22.04 LTS VM installed and internet access working.
-   [ ] Git, Mininet, Open vSwitch, Python `pip`/`venv`, and required
    build libraries installed.
-   [ ] OS-Ken installed in `~/osken/venv`.
-   [ ] Mininet basic test completed.
-   [ ] SSH service and VirtualBox port forwarding configured if using
    Windows Remote - SSH.
-   [ ] VS Code Remote - SSH connection verified if using that workflow.
-   [ ] Basic OpenFlow 1.3 learning-switch test completed when
    `controller_test.py` is available.
-   [ ] Actual project components and tests tracked separately from the
    environment setup.

------------------------------------------------------------------------

**Reminder:** A successful environment test is not the same as a
completed project. Keep the README updated as implementation, test
coverage, and measured results evolve.
