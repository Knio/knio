# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/ftrace/thermal.proto
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
    'protos/perfetto/trace/ftrace/thermal.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*protos/perfetto/trace/ftrace/thermal.proto\x12\x0fperfetto.protos\"b\n\x1dThermalTemperatureFtraceEvent\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04temp\x18\x02 \x01(\x05\x12\x11\n\ttemp_prev\x18\x03 \x01(\x05\x12\x14\n\x0cthermal_zone\x18\x04 \x01(\t\"5\n\x15\x43\x64\x65vUpdateFtraceEvent\x12\x0e\n\x06target\x18\x01 \x01(\x04\x12\x0c\n\x04type\x18\x02 \x01(\t')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.ftrace.thermal_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_THERMALTEMPERATUREFTRACEEVENT']._serialized_start=63
  _globals['_THERMALTEMPERATUREFTRACEEVENT']._serialized_end=161
  _globals['_CDEVUPDATEFTRACEEVENT']._serialized_start=163
  _globals['_CDEVUPDATEFTRACEEVENT']._serialized_end=216
# @@protoc_insertion_point(module_scope)
