from mininet.net import Mininet
from mininet.node import Host
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

def networkTopology():
    "Creates the specified WAN network topology."

    net = Mininet(controller=None, link=TCLink, host=Host)

    info('*** Adding hosts and routers\n')
    r_central = net.addHost('r_central', ip=None)
    r_suc1 = net.addHost('r_suc1', ip=None)
    r_suc2 = net.addHost('r_suc2', ip=None)
    h_suc1 = net.addHost('h_suc1', ip='10.0.1.254/24', defaultRoute='via 10.0.1.1')
    h_suc2 = net.addHost('h_suc2', ip='10.0.2.254/24', defaultRoute='via 10.0.2.1')

    info('*** Creating links\n')
    net.addLink(r_central, r_suc1, intfName1='r_central-eth0', params1={'ip': '192.168.100.6/29'},
                intfName2='r_suc1-eth0', params2={'ip': '192.168.100.1/29'})
    net.addLink(r_central, r_suc2, intfName1='r_central-eth1', params1={'ip': '192.168.100.14/29'},
                intfName2='r_suc2-eth0', params2={'ip': '192.168.100.9/29'})
    net.addLink(r_suc1, h_suc1, intfName1='r_suc1-eth1', params1={'ip': '10.0.1.1/24'},
                intfName2='h_suc1-eth0')
    net.addLink(r_suc2, h_suc2, intfName1='r_suc2-eth1', params1={'ip': '10.0.2.1/24'},
                intfName2='h_suc2-eth0')

    info('*** Starting network\n')
    net.build()

    info('*** Enabling IP forwarding on routers\n')
    for router in [r_central, r_suc1, r_suc2]:
        router.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Configuring static routes\n')
    r_central.cmd('ip route add 10.0.1.0/24 via 192.168.100.1 dev r_central-eth0')
    r_central.cmd('ip route add 10.0.2.0/24 via 192.168.100.9 dev r_central-eth1')
    r_suc1.cmd('ip route add default via 192.168.100.6 dev r_suc1-eth0')
    r_suc2.cmd('ip route add default via 192.168.100.14 dev r_suc2-eth0')

    info('*** Network is ready. Starting CLI...\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    networkTopology()