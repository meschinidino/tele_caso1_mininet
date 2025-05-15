from mininet.net import Mininet
from mininet.node import Host
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

NUM_SUCURSALES = 2

def networkTopology(num_sucursales=NUM_SUCURSALES, net=None, start_cli=True):
    # ... rest of your function ...
    "Creates a WAN topology with up to 6 branches."
    from mininet.net import Mininet
    from mininet.node import Host
    from mininet.cli import CLI
    from mininet.link import TCLink
    from mininet.log import info

    if net is None:
        net = Mininet(controller=None, link=TCLink, host=Host)

    info('*** Adding central router\n')
    r_central = net.addHost('r_central', ip=None)

    routers = []
    hosts = []

    for i in range(1, num_sucursales + 1):
        # Routers and hosts names
        r_name = f"r_suc{i}"
        h_name = f"h_suc{i}"

        # WAN subnet base for this branch
        wan_subnet_base = 8 * (i - 1)
        wan_router_ip = f"192.168.100.{wan_subnet_base + 1}/29"
        wan_central_ip = f"192.168.100.{wan_subnet_base + 6}/29"

        # LAN subnet base for this branch
        lan_router_ip = f"10.0.{i}.1/24"
        host_ip = f"10.0.{i}.254/24"
        host_gw = f"10.0.{i}.1"

        # Add branch router and host
        r_suc = net.addHost(r_name, ip=None)
        h_suc = net.addHost(h_name, ip=host_ip, defaultRoute=f"via {host_gw}")
        routers.append(r_suc)
        hosts.append(h_suc)

        # WAN link between central and branch router
        net.addLink(r_central, r_suc,
                    intfName1=f"r_central-eth{i-1}", params1={'ip': wan_central_ip},
                    intfName2=f"{r_name}-eth0", params2={'ip': wan_router_ip})

        # LAN link between branch router and host
        net.addLink(r_suc, h_suc,
                    intfName1=f"{r_name}-eth1", params1={'ip': lan_router_ip},
                    intfName2=f"{h_name}-eth0")

    info('*** Starting network\n')
    net.build()

    info('*** Enabling IP forwarding on routers\n')
    r_central.cmd('sysctl -w net.ipv4.ip_forward=1')
    for r in routers:
        r.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Configuring static routes\n')
    for i, r_suc in enumerate(routers, 1):
        wan_subnet_base = 8 * (i - 1)
        wan_router_ip = f"192.168.100.{wan_subnet_base + 1}"
        wan_central_ip = f"192.168.100.{wan_subnet_base + 6}"
        lan_subnet = f"10.0.{i}.0/24"

        # Central router: route to each branch LAN via branch WAN IP
        r_central.cmd(f"ip route add {lan_subnet} via {wan_router_ip} dev r_central-eth{i-1}")
        # Branch router: default route via central WAN IP
        r_suc.cmd(f"ip route add default via {wan_central_ip} dev {r_suc.name}-eth0")

    info('*** Network is ready. Starting CLI...\n')
    if start_cli:
        CLI(net)
        net.stop()
    return net