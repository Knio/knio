# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/chrome/media_metric.proto
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
    'protos/perfetto/metrics/chrome/media_metric.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.metrics import custom_options_pb2 as protos_dot_perfetto_dot_metrics_dot_custom__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1protos/perfetto/metrics/chrome/media_metric.proto\x12\x0fperfetto.protos\x1a,protos/perfetto/metrics/custom_options.proto\"\x94\x03\n\x0bMediaMetric\x12\x32\n\x12time_to_video_play\x18\x01 \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter\x12\x32\n\x12time_to_audio_play\x18\x02 \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter\x12\x36\n\x13\x64ropped_frame_count\x18\x03 \x03(\x03\x42\x19\x8a\xb5\x18\x15\x63ount_smallerIsBetter\x12.\n\x0e\x62uffering_time\x18\x04 \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter\x12,\n\troughness\x18\x05 \x03(\x01\x42\x19\x8a\xb5\x18\x15\x63ount_smallerIsBetter\x12(\n\x08\x66reezing\x18\x06 \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter\x12)\n\tseek_time\x18\x08 \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter\x12\x32\n\x12pipeline_seek_time\x18\t \x03(\x01\x42\x16\x8a\xb5\x18\x12ms_smallerIsBetter')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.chrome.media_metric_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['time_to_video_play']._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['time_to_video_play']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_MEDIAMETRIC'].fields_by_name['time_to_audio_play']._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['time_to_audio_play']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_MEDIAMETRIC'].fields_by_name['dropped_frame_count']._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['dropped_frame_count']._serialized_options = b'\212\265\030\025count_smallerIsBetter'
  _globals['_MEDIAMETRIC'].fields_by_name['buffering_time']._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['buffering_time']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_MEDIAMETRIC'].fields_by_name['roughness']._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['roughness']._serialized_options = b'\212\265\030\025count_smallerIsBetter'
  _globals['_MEDIAMETRIC'].fields_by_name['freezing']._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['freezing']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_MEDIAMETRIC'].fields_by_name['seek_time']._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['seek_time']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_MEDIAMETRIC'].fields_by_name['pipeline_seek_time']._loaded_options = None
  _globals['_MEDIAMETRIC'].fields_by_name['pipeline_seek_time']._serialized_options = b'\212\265\030\022ms_smallerIsBetter'
  _globals['_MEDIAMETRIC']._serialized_start=117
  _globals['_MEDIAMETRIC']._serialized_end=521
# @@protoc_insertion_point(module_scope)