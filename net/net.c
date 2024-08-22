#include <linux/if_ether.h>
#include <linux/inet.h>
#include <linux/ip.h>


struct Flow {
  u32 ip_a;
  u32 ip_b;
};


BPF_HASH(flows, struct Flow, u32, 1024);

static void log_packet(const struct iphdr* ip) {
  struct Flow flow;
  u32 z = 0;
  flow.ip_a = ntohl(ip->saddr);
  flow.ip_b = ntohl(ip->daddr);

  u32 *bytes = flows.lookup_or_try_init(&flow, &z);
  if (bytes) {
      *bytes += ntohs(ip->tot_len);
  } else {
    bpf_trace_printk("no map entry");
  }
}


int sock_peek_packet(struct __sk_buff *skb) {
  bpf_trace_printk("protocol: %x", skb->protocol);
  bpf_trace_printk("pkt_type: %x", skb->pkt_type);
  struct ethhdr e_hdr;
  u32 off = 0;
  if (bpf_skb_load_bytes(skb, off, &e_hdr, sizeof(e_hdr))) {
     bpf_trace_printk("no eth header");
    return 1;
  }
  u8 ipproto = *((u8*)(&e_hdr)) & 0xf0;
  if (e_hdr.h_proto == htons(ETH_P_IP)) {
    off += sizeof(e_hdr);
  }
  else if (ipproto == 0x40) {
    // ipv4
    bpf_trace_printk("lol idk");
  } else {
    bpf_trace_printk("not an ip packet: %x", e_hdr.h_proto);
    return 1;
  }
  struct iphdr ip_hdr;
  if (bpf_skb_load_bytes(skb, off, &ip_hdr, sizeof(ip_hdr))) {
     bpf_trace_printk("no ip header");
    return 1;
  }
  bpf_trace_printk("socket packet 3 %x %x", ip_hdr.saddr, ip_hdr.daddr);
  log_packet(&ip_hdr);
  return 1;
}


int xdp_peek_packet(struct xdp_md *ctx) {
  bpf_trace_printk("packet");

  void *data = (void *)(long)ctx->data;
  void *data_end = (void *)(long)ctx->data_end;

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

  log_packet(ip);

  return XDP_PASS;
}
