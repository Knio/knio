# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/ftrace/dpu.proto
# Protobuf Python Version: 5.28.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    3,
    '',
    'protos/perfetto/trace/ftrace/dpu.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&protos/perfetto/trace/ftrace/dpu.proto\x12\x0fperfetto.protos\"\x81\x01\n\x1e\x44puTracingMarkWriteFtraceEvent\x12\x0b\n\x03pid\x18\x01 \x01(\x05\x12\x12\n\ntrace_name\x18\x02 \x01(\t\x12\x13\n\x0btrace_begin\x18\x03 \x01(\r\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0c\n\x04type\x18\x05 \x01(\r\x12\r\n\x05value\x18\x06 \x01(\x05\"A\n\x1e\x44puDsiCmdFifoStatusFtraceEvent\x12\x0e\n\x06header\x18\x01 \x01(\r\x12\x0f\n\x07payload\x18\x02 \x01(\r\"2\n\x13\x44puDsiRxFtraceEvent\x12\x0b\n\x03\x63md\x18\x01 \x01(\r\x12\x0e\n\x06rx_buf\x18\x02 \x01(\r\"S\n\x13\x44puDsiTxFtraceEvent\x12\x0c\n\x04type\x18\x01 \x01(\r\x12\x0e\n\x06tx_buf\x18\x02 \x01(\r\x12\x0c\n\x04last\x18\x03 \x01(\r\x12\x10\n\x08\x64\x65lay_ms\x18\x04 \x01(\r')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.ftrace.dpu_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DPUTRACINGMARKWRITEFTRACEEVENT']._serialized_start=60
  _globals['_DPUTRACINGMARKWRITEFTRACEEVENT']._serialized_end=189
  _globals['_DPUDSICMDFIFOSTATUSFTRACEEVENT']._serialized_start=191
  _globals['_DPUDSICMDFIFOSTATUSFTRACEEVENT']._serialized_end=256
  _globals['_DPUDSIRXFTRACEEVENT']._serialized_start=258
  _globals['_DPUDSIRXFTRACEEVENT']._serialized_end=308
  _globals['_DPUDSITXFTRACEEVENT']._serialized_start=310
  _globals['_DPUDSITXFTRACEEVENT']._serialized_end=393
# @@protoc_insertion_point(module_scope)
