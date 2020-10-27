# cs5229-hw4

LI YIN

A0085686L

## Automonitor.py

- Automonitor will be called by PolicyX.py at 1 second time intervals to compute bps for all (switch, protocal, src_ip, dst_ip) tuples using the byteCount field of flowget.
- The result will be stored in a hierachial dictionary to be used by the policies to determine whether to switch route for UDP packets



## Policy1

- Added udpForwarding() which does exactly the same thing as staticForwarding, except for additional paramter "ip_proto":"0x11" to check for UDP packets. This allows Automonitor.py to differentiate byteCount between TCP and UDP packets.
- In AutoRouting() function, I query automonitor once every 1 second to get the following information:
  - bps of TPC packets transferred at switch 1 from h1 to h3
  - bps of UDP packets transferred at switch 1 from h1 to h4
- If the sum of the above two values >= 95 Mbps, I enable the alternative route h1->S1->S2->S3->h4 for UDP packets. This is because all inter-switch links has maximum bandwidth 100Mbps, hence before all bandwidth are utilized, I route 80Mbps of UDP traffic to the alternative route which has 0 utilization at the moment. After the switch:
  - UDP traffic gets to enjoy 100Mbps bandwidth at S1->S2->S3 
  - TCP traffic gets to enjoy 100Mbps bandwidth at S1->S3
- Since UDP traffic only require 80Mbps bandwidth, no packet loss will occur



## Policy2

- Added udpForwarding() same as Policy1
- In AutoRouting() function, I query automonitor once every 1 second to get the following information:
  - bps of TPC packets transferred at switch 1 from h1 to h3
  - bps of UDP packets transferred at switch 1 from h1 to h4
  - bps of UDP packets transferred at switch 1 from h1 to h5
- If the sum of the above 3 values >= 95 Mbps, I enable the alternative route h1->S1->S2->S3->h4 and h1->S1->S2->S3->h5 for UDP packets. After the switch:
  - UDP traffic gets to enjoy 100Mbps bandwidth at S1->S2->S3 
  - TCP traffic gets to enjoy 100Mbps bandwidth at S1->S3
- Since the combined UDP traffic only require 45+45=90Mbps bandwidth, no packet loss will occur



## Policy3

- Added udpForwarding() same as Policy1
- In AutoRouting() function, I query automonitor once every 1 second to get the following information:
  - bps of TPC packets transferred at switch 2 from h2 to h3
  - bps of UDP packets transferred at switch 2 from h2 to h5
- If the sum of the above 2 values >= 95 Mbps, I enable the alternative route h2->S2->S1->S3->h5 for h2toh5 UDP packets. After the switch:
  - h1toh4 UDP traffic gets to enjoy 100-60=40Mbps bandwidth at S1->S3, which is sufficient for the required 30Mbps.
  - h2toh5 UDP traffic gets to enjoy 100Mbps bandwidth at S2->S1, but only 100-30=70Mbps bandwidth at S1->S3, which is still sufficient for the required 60Mbps.
  - TCP traffic gets to enjoy 100Mbps bandwidth at S2->S3
- Since the combined UDP traffic bandwidth requirements are all satisfied, no packet loss will occur
