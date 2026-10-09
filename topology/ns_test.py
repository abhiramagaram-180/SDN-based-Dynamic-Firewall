#!/usr/bin/env python3
"""Single-switch test topology with a root-namespace node for the controller side.

Run in the VM (controller must already be listening on 127.0.0.1:6653):
    sudo python3 topology/ns_test.py
"""
from mininet.cli import CLI
from mininet.link import Link
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, RemoteController
from mininet.topo import SingleSwitchTopo


def run():
    topo = SingleSwitchTopo(k=2)
    net = Mininet(
        topo=topo,
        switch=lambda name, **kw: OVSSwitch(name, protocols="OpenFlow13", **kw),
        controller=None,
        autoSetMacs=True,
    )
    net.addController(
        "c0", controller=RemoteController, ip="127.0.0.1", port=6653
    )

    # Node that lives in the VM's root network namespace (not isolated like h1, h2)
    root = Node("root", inNamespace=False)
    s1 = net.get("s1")
    Link(root, s1)

    net.start()

    # Give the root side of the new link an address in the host subnet
    root.setIP("10.0.0.254/24", intf="root-eth0")

    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()
