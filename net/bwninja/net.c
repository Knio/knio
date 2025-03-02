#include <linux/if_ether.h>
#include <linux/inet.h>
#include <linux/ip.h>
#include <linux/ipv6.h>

// TODO: bpf_get_socket_cookie
// (same as inode?)

struct __attribute__((packed)) Ports {
  u16 protocol;
  u16 sport;
  u16 dport;
};

struct __attribute__((packed)) Flow4 {
  u32 src;
  u32 dst;
  struct Ports ports;
};

struct __attribute__((packed)) Flow6 {
  struct	in6_addr src;
  struct	in6_addr dst;
  struct Ports ports;
};

struct __attribute__((packed)) Stat {
  u32 bytes;
  u32 packets;
};

struct ParseState {
  struct __sk_buff *const skb;
  u16 offset;
  u16 protocol;
  struct iphdr    ip4;
  struct ipv6hdr  ip6;
  struct tcphdr tcp;
  struct udphdr udp;
  struct Ports ports;
};

// /*
static void get_ports4(struct ParseState* state) {
  // state->ports.protocol = 0;
  state->ports.sport = 0;
  state->ports.dport = 0;
  // return;
  const u8 ihl = state->ip4.ihl * 4;
  if (state->ip4.protocol == IPPROTO_TCP) {
    if (bpf_skb_load_bytes(state->skb, state->offset + ihl, &state->tcp, sizeof(state->tcp))) {
      bpf_trace_printk("could not load tcp header");
      state->ports.protocol = 1;
      return;
    }
    state->ports.protocol = 2;
    state->ports.sport = ntohs(state->tcp.source);
    state->ports.dport = ntohs(state->tcp.dest);
    return;
  }
  else if (state->ip4.protocol == IPPROTO_UDP) {
    if (bpf_skb_load_bytes(state->skb, state->offset + ihl, &state->udp, sizeof(state->udp))) {
      bpf_trace_printk("could not load udp header");
      state->ports.protocol = 1;
      return;
    }
    state->ports.protocol = 3;
    state->ports.sport = ntohs(state->udp.source);
    state->ports.dport = ntohs(state->udp.dest);
    return;
  }
  else {
    // not UDP or TCP.
    // TODO: ICMP, etc
    state->ports.protocol = 0;
    return;
  }
}
// */

BPF_HASH(flows4, struct Flow4, struct Stat, 1024);
BPF_HASH(flows6, struct Flow6, struct Stat, 1024);

static void log_packet4(struct ParseState* state) {
  struct Flow4 flow;
  struct Stat z = {0,0};
  flow.src = ntohl(state->ip4.saddr);
  flow.dst = ntohl(state->ip4.daddr);
  get_ports4(state);
  flow.ports = state->ports;

  struct Stat *stat = flows4.lookup_or_try_init(&flow, &z);
  if (stat) {
      stat->bytes += ntohs(state->ip4.tot_len);
      stat->packets ++;
  } else {
    bpf_trace_printk("no map entry");
  }
}

static void log_packet6(struct ParseState* state) {
  struct Flow6 flow;
  struct Stat z = {0,0};
  flow.src = state->ip6.saddr;
  flow.dst = state->ip6.daddr;
  flow.ports.protocol = 0;
  flow.ports.sport = 0;
  flow.ports.dport = 0;

  struct Stat *stat = flows6.lookup_or_try_init(&flow, &z);
  if (stat) {
      stat->bytes += ntohs(state->ip6.payload_len);
      stat->packets ++;
  } else {
    bpf_trace_printk("no map entry");
  }
}


static void handle_ip(struct ParseState *state) {

  // Cannot do direct packets access for "socket"
  // https://stackoverflow.com/a/61726788/132076
  // So we use bpf_skb_load_bytes

  if (bpf_skb_load_bytes(state->skb, state->offset, &state->ip4, sizeof(state->ip4))) {
    bpf_trace_printk("could not load ip4 bytes");
    return;
  }
  if (state->ip4.version == 4) {
    log_packet4(state);
    return;
  }
  else if (state->ip4.version == 6) {
    if (bpf_skb_load_bytes(state->skb, state->offset, &state->ip6, sizeof(state->ip6))) {
      bpf_trace_printk("could not load ip6 bytes");
      return;
    }
    log_packet6(state);
    return;
  }
  else {
    // TODO: likely ARP. should actually read the ethhdr.h_proto
    // if we have it.
    bpf_trace_printk("unknown ip version %x", state->ip4.version);
    return;
  }

}

// Example: https://elixir.bootlin.com/linux/v6.1/source/samples/bpf/parse_varlen.c#L113
int sock_peek_packet_eth(struct __sk_buff *skb) {
  struct ParseState state = {
    .skb = skb,
    .offset = sizeof(struct ethhdr)
  };
  handle_ip(&state);
  return 0;
}

int sock_peek_packet_ip(struct __sk_buff *skb) {
  // On wireguard interfaces, sk_buff is L3 and not L2,
  // so there is no ethernet header and just an IP header.
  // handle_ip(skb, 0);
  struct ParseState state = {
    .skb = skb,
    .offset = 0
  };
  handle_ip(&state);
  return 0;
}
