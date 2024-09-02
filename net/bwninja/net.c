#include <linux/if_ether.h>
#include <linux/inet.h>
#include <linux/ip.h>
#include <linux/ipv6.h>

// TODO: bpf_get_socket_cookie
// (same as inode?)


struct Flow4 {
  u32 src;
  u32 dst;
};

struct Flow6 {
  struct	in6_addr src;
  struct	in6_addr dst;
};

struct Stat {
  u32 bytes;
  u32 packets;
};

BPF_HASH(flows4, struct Flow4, struct Stat, 1024);
BPF_HASH(flows6, struct Flow6, struct Stat, 1024);

static void log_packet4(const struct iphdr* ip) {
  struct Flow4 flow;
  struct Stat z = {0,0};
  flow.src = ntohl(ip->saddr);
  flow.dst = ntohl(ip->daddr);

  struct Stat *stat = flows4.lookup_or_try_init(&flow, &z);
  if (stat) {
      stat->bytes += ntohs(ip->tot_len);
      stat->packets ++;
  } else {
    bpf_trace_printk("no map entry");
  }
}

static void log_packet6(const struct ipv6hdr* ip6) {
  struct Flow6 flow;
  struct Stat z = {0,0};
  flow.src = ip6->saddr;
  flow.dst = ip6->daddr;

  struct Stat *stat = flows6.lookup_or_try_init(&flow, &z);
  if (stat) {
      stat->bytes += ntohs(ip6->payload_len);
      stat->packets ++;
  } else {
    bpf_trace_printk("no map entry");
  }
}


static void handle_ip(struct __sk_buff *skb, const u32 offset) {
  struct iphdr ip4;

  // Cannot do direct packets access for "socket"
  // https://stackoverflow.com/a/61726788/132076
  // So we use bpf_skb_load_bytes

  if (bpf_skb_load_bytes(skb, offset, &ip4, sizeof(ip4))) {
    bpf_trace_printk("could not load ip4 bytes");
    return;
  }
  if (ip4.version == 4) {
    log_packet4(&ip4);
    return;
  }
  else if (ip4.version == 6) {
    struct ipv6hdr ip6;
    if (bpf_skb_load_bytes(skb, offset, &ip6, sizeof(ip6))) {
      bpf_trace_printk("could not load ip6 bytes");
      return;
    }
    log_packet6(&ip6);
    return;
  }
  else {
    bpf_trace_printk("unknown ip version %x", ip4.version);
    return;
  }

}

// Example: https://elixir.bootlin.com/linux/v6.1/source/samples/bpf/parse_varlen.c#L113
int sock_peek_packet_eth(struct __sk_buff *skb) {
  handle_ip(skb, sizeof(struct ethhdr));
  return 0;
}

int sock_peek_packet_ip(struct __sk_buff *skb) {
  // On wireguard interfaces, sk_buff is L3 and not L2,
  // so there is no ethernet header and just an IP header.
  handle_ip(skb, 0);
  return 0;
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

  log_packet4(ip);

  return XDP_PASS;
}
