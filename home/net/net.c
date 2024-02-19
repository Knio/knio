#include <linux/if_ether.h>
#include <linux/inet.h>
#include <linux/ip.h>


struct Flow {
  u32 ip_a;
  u32 ip_b;
};


BPF_HASH(flows, struct Flow, u32, 4096);


int tc_peek_packet(struct __sk_buff *skb) {
  bpf_trace_printk("skb");
  return 1;
}


int xdp_peek_packet(struct xdp_md *ctx) {
  bpf_trace_printk("packet");

  void *data_end = (void *)(long)ctx->data_end;
  void *data = (void *)(long)ctx->data;

  struct ethhdr *eth = data;
  struct iphdr *ip = data + sizeof(struct ethhdr);

  if ((void*)eth + sizeof(*eth) > data_end) {
    bpf_trace_printk("frame too small");
    return XDP_PASS;
  }

  u16 h_proto = ntohs(eth->h_proto);
  if (h_proto != ETH_P_IP) {
    bpf_trace_printk("eth %d skipped\n", h_proto);
    return XDP_PASS;
  }

  if ((void*)ip + sizeof(*ip) > data_end) {
    bpf_trace_printk("packet too small");
    return XDP_PASS;
  }

  u32 z = 0;

  struct Flow flow;
  flow.ip_a = ntohl(ip->saddr);
  flow.ip_b = ntohl(ip->daddr);

  u32 *bytes = flows.lookup_or_try_init(&flow, &z);
  if (bytes) {
      *bytes += ntohs(ip->tot_len);
  } else {
    bpf_trace_printk("no stats");
  }

  return XDP_PASS;
}
