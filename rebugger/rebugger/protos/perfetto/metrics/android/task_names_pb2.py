# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/android/task_names.proto
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
    'protos/perfetto/metrics/android/task_names.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0protos/perfetto/metrics/android/task_names.proto\x12\x0fperfetto.protos\"\xc4\x01\n\x10\x41ndroidTaskNames\x12:\n\x07process\x18\x01 \x03(\x0b\x32).perfetto.protos.AndroidTaskNames.Process\x1at\n\x07Process\x12\x0b\n\x03pid\x18\x01 \x01(\x03\x12\x14\n\x0cprocess_name\x18\x02 \x01(\t\x12\x13\n\x0bthread_name\x18\x03 \x03(\t\x12\x0b\n\x03uid\x18\x04 \x01(\x03\x12\x18\n\x10uid_package_name\x18\x05 \x03(\tJ\x04\x08\x06\x10\x07J\x04\x08\x07\x10\x08')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.android.task_names_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANDROIDTASKNAMES']._serialized_start=70
  _globals['_ANDROIDTASKNAMES']._serialized_end=266
  _globals['_ANDROIDTASKNAMES_PROCESS']._serialized_start=150
  _globals['_ANDROIDTASKNAMES_PROCESS']._serialized_end=266
# @@protoc_insertion_point(module_scope)
