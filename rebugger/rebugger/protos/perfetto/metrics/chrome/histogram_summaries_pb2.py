# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/chrome/histogram_summaries.proto
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
    'protos/perfetto/metrics/chrome/histogram_summaries.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8protos/perfetto/metrics/chrome/histogram_summaries.proto\x12\x0fperfetto.protos\"q\n\x10HistogramSummary\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04mean\x18\x02 \x01(\x03\x12\r\n\x05\x63ount\x18\x03 \x01(\r\x12\x0b\n\x03sum\x18\x04 \x01(\x03\x12\x0b\n\x03max\x18\x05 \x01(\x03\x12\x0b\n\x03p90\x18\x06 \x01(\x03\x12\x0b\n\x03p50\x18\x07 \x01(\x03\"X\n\x18\x43hromeHistogramSummaries\x12<\n\x11histogram_summary\x18\x01 \x03(\x0b\x32!.perfetto.protos.HistogramSummary')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.chrome.histogram_summaries_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HISTOGRAMSUMMARY']._serialized_start=77
  _globals['_HISTOGRAMSUMMARY']._serialized_end=190
  _globals['_CHROMEHISTOGRAMSUMMARIES']._serialized_start=192
  _globals['_CHROMEHISTOGRAMSUMMARIES']._serialized_end=280
# @@protoc_insertion_point(module_scope)
