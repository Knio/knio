# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/android/monitor_contention_agg_metric.proto
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
    'protos/perfetto/metrics/android/monitor_contention_agg_metric.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nCprotos/perfetto/metrics/android/monitor_contention_agg_metric.proto\x12\x0fperfetto.protos\"\xb4\x02\n!AndroidMonitorContentionAggMetric\x12\x62\n\x13process_aggregation\x18\x01 \x03(\x0b\x32\x45.perfetto.protos.AndroidMonitorContentionAggMetric.ProcessAggregation\x1a\xaa\x01\n\x12ProcessAggregation\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1e\n\x16total_contention_count\x18\x02 \x01(\x03\x12\x1c\n\x14total_contention_dur\x18\x03 \x01(\x03\x12$\n\x1cmain_thread_contention_count\x18\x04 \x01(\x03\x12\"\n\x1amain_thread_contention_dur\x18\x05 \x01(\x03')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.android.monitor_contention_agg_metric_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANDROIDMONITORCONTENTIONAGGMETRIC']._serialized_start=89
  _globals['_ANDROIDMONITORCONTENTIONAGGMETRIC']._serialized_end=397
  _globals['_ANDROIDMONITORCONTENTIONAGGMETRIC_PROCESSAGGREGATION']._serialized_start=227
  _globals['_ANDROIDMONITORCONTENTIONAGGMETRIC_PROCESSAGGREGATION']._serialized_end=397
# @@protoc_insertion_point(module_scope)