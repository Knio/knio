# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/ftrace/irq.proto
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
    'protos/perfetto/trace/ftrace/irq.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&protos/perfetto/trace/ftrace/irq.proto\x12\x0fperfetto.protos\"&\n\x17SoftirqEntryFtraceEvent\x12\x0b\n\x03vec\x18\x01 \x01(\r\"%\n\x16SoftirqExitFtraceEvent\x12\x0b\n\x03vec\x18\x01 \x01(\r\"&\n\x17SoftirqRaiseFtraceEvent\x12\x0b\n\x03vec\x18\x01 \x01(\r\"H\n\x1aIrqHandlerEntryFtraceEvent\x12\x0b\n\x03irq\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07handler\x18\x03 \x01(\r\"5\n\x19IrqHandlerExitFtraceEvent\x12\x0b\n\x03irq\x18\x01 \x01(\x05\x12\x0b\n\x03ret\x18\x02 \x01(\x05')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.ftrace.irq_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SOFTIRQENTRYFTRACEEVENT']._serialized_start=59
  _globals['_SOFTIRQENTRYFTRACEEVENT']._serialized_end=97
  _globals['_SOFTIRQEXITFTRACEEVENT']._serialized_start=99
  _globals['_SOFTIRQEXITFTRACEEVENT']._serialized_end=136
  _globals['_SOFTIRQRAISEFTRACEEVENT']._serialized_start=138
  _globals['_SOFTIRQRAISEFTRACEEVENT']._serialized_end=176
  _globals['_IRQHANDLERENTRYFTRACEEVENT']._serialized_start=178
  _globals['_IRQHANDLERENTRYFTRACEEVENT']._serialized_end=250
  _globals['_IRQHANDLEREXITFTRACEEVENT']._serialized_start=252
  _globals['_IRQHANDLEREXITFTRACEEVENT']._serialized_end=305
# @@protoc_insertion_point(module_scope)
