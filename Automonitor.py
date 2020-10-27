import time

class Automonitor(object):
    def __init__(self, update_interval=1):
        self.update_interval = float(update_interval)
        self.switches = [
            "00:00:00:00:00:00:00:01",
            "00:00:00:00:00:00:00:02",
            "00:00:00:00:00:00:00:03",
        ]
        self.hosts = [
            "10.0.0.1",
            "10.0.0.2",
            "10.0.0.3",
            "10.0.0.4",
            "10.0.0.5",
        ]
        self.stats = {}

    def get_stats(self, switch, protocol, src, dst):
        switch_stat = self.stats.get(switch, None)
        if switch_stat is None:
            switch_stat = {}
            self.stats[switch]=switch_stat
        proto_stat = switch_stat.get(protocol, None)
        if proto_stat is None:
            proto_stat = {}
            switch_stat[protocol]=proto_stat
        src_stat = proto_stat.get(src, None)
        if src_stat is None:
            src_stat = {}
            proto_stat[src]=src_stat
        dst_stat = src_stat.get(dst, None)
        if dst_stat is None:
            dst_stat = {
                'last_bytes':0,
                'curr_bytes':0,
                'throughput':0,
            }
            src_stat[dst]=dst_stat
        return dst_stat
    
    def update_all_stats(self, flowget):

        for switch in self.switches:
            retData = flowget.get(switch)
            myFlows = retData['flows']
            for myFlow in myFlows:
                myMatch = myFlow['match']
                if 'ipv4_src' not in myMatch or 'ipv4_dst' not in myMatch:
                    continue
                ipSrc = myMatch['ipv4_src']
                ipDst = myMatch['ipv4_dst'] 
                protocol = 'tcp'
                if 'ip_proto' in myMatch and myMatch['ip_proto']=='0x11':
                    protocol = 'udp'
                stat = self.get_stats(switch, protocol, ipSrc, ipDst)
                # print (self.stats)
                stat['curr_bytes']+=int(myFlow['byteCount'])

        for switch,switch_stat in self.stats.items():
            for protocol, proto_stat in switch_stat.items():
                for src, src_stat in proto_stat.items():
                    for dst, stat in src_stat.items():
                        stat['throughput']=(stat['curr_bytes']-stat['last_bytes'])*8/self.update_interval
                        stat['last_bytes']=stat['curr_bytes']
                        stat['curr_bytes']=0

    def print_stats(self):
        print("=======")
        for switch,switch_stat in self.stats.items():
            for protocol, proto_stat in switch_stat.items():
                for src, src_stat in proto_stat.items():
                    for dst, stat in src_stat.items():
                        if stat['throughput']>0:
                            print (switch[-1], protocol, src[-1], dst[-1], stat['throughput'])
