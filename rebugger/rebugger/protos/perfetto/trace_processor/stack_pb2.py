# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace_processor/stack.proto
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
    'protos/perfetto/trace_processor/stack.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+protos/perfetto/trace_processor/stack.proto\x12\x0fperfetto.protos\"\xa4\x01\n\x05Stack\x12-\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x1c.perfetto.protos.Stack.Entry\x1al\n\x05\x45ntry\x12\x0e\n\x04name\x18\x01 \x01(\tH\x00\x12\x15\n\x0b\x63\x61llsite_id\x18\x02 \x01(\rH\x00\x12\x1f\n\x15\x61nnotated_callsite_id\x18\x03 \x01(\rH\x00\x12\x12\n\x08\x66rame_id\x18\x04 \x01(\rH\x00\x42\x07\n\x05\x65ntry')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace_processor.stack_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STACK']._serialized_start=65
  _globals['_STACK']._serialized_end=229
  _globals['_STACK_ENTRY']._serialized_start=121
  _globals['_STACK_ENTRY']._serialized_end=229
# @@protoc_insertion_point(module_scope)
