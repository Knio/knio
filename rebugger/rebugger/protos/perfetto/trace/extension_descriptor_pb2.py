# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/extension_descriptor.proto
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
    'protos/perfetto/trace/extension_descriptor.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.common import descriptor_pb2 as protos_dot_perfetto_dot_common_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0protos/perfetto/trace/extension_descriptor.proto\x12\x0fperfetto.protos\x1a\'protos/perfetto/common/descriptor.proto\"P\n\x13\x45xtensionDescriptor\x12\x39\n\rextension_set\x18\x01 \x01(\x0b\x32\".perfetto.protos.FileDescriptorSet')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.extension_descriptor_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EXTENSIONDESCRIPTOR']._serialized_start=110
  _globals['_EXTENSIONDESCRIPTOR']._serialized_end=190
# @@protoc_insertion_point(module_scope)
