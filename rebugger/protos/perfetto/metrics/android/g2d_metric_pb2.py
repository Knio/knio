# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/android/g2d_metric.proto
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
    'protos/perfetto/metrics/android/g2d_metric.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0protos/perfetto/metrics/android/g2d_metric.proto\x12\x0fperfetto.protos\"\xba\x03\n\nG2dMetrics\x12\x35\n\x06g2d_hw\x18\x01 \x01(\x0b\x32%.perfetto.protos.G2dMetrics.G2dMetric\x12\x35\n\x06g2d_sw\x18\x02 \x01(\x0b\x32%.perfetto.protos.G2dMetrics.G2dMetric\x1a\x87\x01\n\x0bG2dInstance\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x66rame_count\x18\x05 \x01(\r\x12\x13\n\x0b\x65rror_count\x18\x06 \x01(\r\x12\x12\n\nmax_dur_ms\x18\x07 \x01(\x01\x12\x12\n\nmin_dur_ms\x18\x08 \x01(\x01\x12\x12\n\navg_dur_ms\x18\t \x01(\x01J\x04\x08\x02\x10\x05\x1a\xb3\x01\n\tG2dMetric\x12:\n\tinstances\x18\x01 \x03(\x0b\x32\'.perfetto.protos.G2dMetrics.G2dInstance\x12\x13\n\x0b\x66rame_count\x18\x05 \x01(\r\x12\x13\n\x0b\x65rror_count\x18\x06 \x01(\r\x12\x12\n\nmax_dur_ms\x18\x07 \x01(\x01\x12\x12\n\nmin_dur_ms\x18\x08 \x01(\x01\x12\x12\n\navg_dur_ms\x18\t \x01(\x01J\x04\x08\x02\x10\x05')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.android.g2d_metric_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_G2DMETRICS']._serialized_start=70
  _globals['_G2DMETRICS']._serialized_end=512
  _globals['_G2DMETRICS_G2DINSTANCE']._serialized_start=195
  _globals['_G2DMETRICS_G2DINSTANCE']._serialized_end=330
  _globals['_G2DMETRICS_G2DMETRIC']._serialized_start=333
  _globals['_G2DMETRICS_G2DMETRIC']._serialized_end=512
# @@protoc_insertion_point(module_scope)