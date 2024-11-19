import pickle
import sys
import os
import pathlib
import time


# thanks again, google
_proto_path = str(pathlib.Path(__file__).parent.parent)
sys.path.append(_proto_path)
from protos.perfetto.trace import trace_pb2
from protos.perfetto.trace.track_event.track_event_pb2 import TrackEvent
sys.path.remove(_proto_path)


_uuid = 0
def uuid():
  global _uuid
  _uuid += 1
  return _uuid


def pickles(f):
  while 1:
    try:
       yield pickle.load(f)
    except EOFError:
      break


def perfetto_file_from_tracep(tracep_fn: pathlib.Path):
  input = tracep_fn.with_suffix('.tracep').open('rb')
  threads = {}
  output = trace_pb2.Trace()

  process = output.packet.add()
  td = process.track_descriptor
  td.uuid = uuid()
  td.process.pid = os.getpid()
  td.process.process_name = "process name"

  offset = time.time_ns() - time.perf_counter_ns()

  for el in pickles(input):
    ts, tid, event, *a = el
    if tid not in threads:
      thread = output.packet.add()
      td = thread.track_descriptor
      td.uuid = uuid()
      td.parent_uuid = process.track_descriptor.uuid
      td.thread.pid = process.track_descriptor.process.pid
      td.thread.tid = tid
      td.thread.thread_name = f"thread {tid}"
      threads[tid] = td

    if event == 'line':
      pkt = output.packet.add()
      pkt.timestamp = ts + offset
      pkt.track_event.type = TrackEvent.Type.TYPE_INSTANT
      pkt.track_event.track_uuid = threads[tid].uuid
      pkt.track_event.name = 'line'
      sl = pkt.track_event.source_location
      sl.file_name,\
      sl.function_name,\
      sl.line_number = a
      pkt.trusted_packet_sequence_id = tid

    elif event == 'call':
      pkt = output.packet.add()
      pkt.timestamp = ts + offset
      pkt.track_event.type = TrackEvent.Type.TYPE_SLICE_BEGIN
      pkt.track_event.track_uuid = threads[tid].uuid
      pkt.track_event.name = f'{a[0]}'
      pkt.trusted_packet_sequence_id = tid
      sl = pkt.track_event.source_location
      sl.file_name = a[2]
      sl.function_name = a[0]
      sl.line_number = a[3]
      args = pkt.track_event.debug_annotations
      for k, v in a[1].items():
        x = args.add()
        x.name = k
        x.string_value = v

    elif event == 'return':
      pkt = output.packet.add()
      pkt.timestamp = ts + offset
      pkt.track_event.type = TrackEvent.Type.TYPE_SLICE_END
      pkt.track_event.track_uuid = threads[tid].uuid
      pkt.trusted_packet_sequence_id = tid
      ret = pkt.track_event.debug_annotations.add()
      ret.name = 'return'
      ret.string_value = a[0]

    elif event == 'exception':
      pkt = output.packet.add()
      pkt.timestamp = ts + offset
      pkt.track_event.type = TrackEvent.Type.TYPE_INSTANT
      pkt.track_event.track_uuid = threads[tid].uuid
      pkt.track_event.name = a[0]
      pkt.trusted_packet_sequence_id = tid

    elif event == 'log':
      pkt = output.packet.add()
      pkt.timestamp = ts + offset
      pkt.track_event.type = TrackEvent.Type.TYPE_INSTANT
      pkt.track_event.track_uuid = threads[tid].uuid
      pkt.track_event.name = a[0]
      pkt.trusted_packet_sequence_id = tid
      args = pkt.track_event.debug_annotations
      for k, v in a[1].items():
        x = args.add()
        x.name = k
        x.string_value = v

    else:
      print(el)


  def parse_time(st: str):
    s, ns = st.strip('<>').split('.')
    return int(s) * 1000000000 + int(ns)

  strace_file = tracep_fn.with_suffix('.strace')
  if strace_file.is_file():
    for strace in strace_file.open('r'):
      tokens = strace.split()
      if tokens[0] == 'strace:':
        continue
      if tokens[-1] == 'detached':
        continue
      start = parse_time(tokens[0])
      dur = parse_time(tokens[-1])
      pkt = output.packet.add()
      pkt.timestamp = start
      pkt.track_event.type = TrackEvent.Type.TYPE_SLICE_BEGIN
      pkt.track_event.track_uuid = threads[tid].uuid
      pkt.track_event.name = ' '.join(tokens[1:-1])
      pkt.trusted_packet_sequence_id = tid
      pkt = output.packet.add()
      pkt.timestamp = start + dur
      pkt.track_event.type = TrackEvent.Type.TYPE_SLICE_END
      pkt.track_event.track_uuid = threads[tid].uuid
      pkt.trusted_packet_sequence_id = tid

  tracep_fn.with_suffix('.perfetto').write_bytes(
    output.SerializeToString())


