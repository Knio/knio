# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/chrome/reported_by_page.proto
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
    'protos/perfetto/metrics/chrome/reported_by_page.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.metrics import custom_options_pb2 as protos_dot_perfetto_dot_metrics_dot_custom__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5protos/perfetto/metrics/chrome/reported_by_page.proto\x12\x0fperfetto.protos\x1a,protos/perfetto/metrics/custom_options.proto\"\xa7\x01\n\x0eReportedByPage\x12\x30\n\x10time_to_viewable\x18\x01 \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter\x12\x33\n\x13time_to_interactive\x18\x02 \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter\x12.\n\x0e\x62\x65nchmark_time\x18\x03 \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.chrome.reported_by_page_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REPORTEDBYPAGE'].fields_by_name['time_to_viewable']._loaded_options = None
  _globals['_REPORTEDBYPAGE'].fields_by_name['time_to_viewable']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_REPORTEDBYPAGE'].fields_by_name['time_to_interactive']._loaded_options = None
  _globals['_REPORTEDBYPAGE'].fields_by_name['time_to_interactive']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_REPORTEDBYPAGE'].fields_by_name['benchmark_time']._loaded_options = None
  _globals['_REPORTEDBYPAGE'].fields_by_name['benchmark_time']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_REPORTEDBYPAGE']._serialized_start=121
  _globals['_REPORTEDBYPAGE']._serialized_end=288
# @@protoc_insertion_point(module_scope)
