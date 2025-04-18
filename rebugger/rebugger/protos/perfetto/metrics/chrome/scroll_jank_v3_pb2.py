# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/chrome/scroll_jank_v3.proto
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
    'protos/perfetto/metrics/chrome/scroll_jank_v3.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.metrics import custom_options_pb2 as protos_dot_perfetto_dot_metrics_dot_custom__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3protos/perfetto/metrics/chrome/scroll_jank_v3.proto\x12\x0fperfetto.protos\x1a,protos/perfetto/metrics/custom_options.proto\"\xe3\x05\n\x12\x43hromeScrollJankV3\x12\x32\n\x10trace_num_frames\x18\x01 \x01(\x03\x42\x18\x8a\xb5\x18\x14\x63ount_biggerIsBetter\x12\x39\n\x16trace_num_janky_frames\x18\x02 \x01(\x03\x42\x19\x8a\xb5\x18\x15\x63ount_smallerIsBetter\x12<\n\x1ctrace_scroll_jank_percentage\x18\x03 \x01(\x01\x42\x16\x8a\xb5\x18\x12n%_smallerIsBetter\x12\x30\n\x11vsync_interval_ms\x18\x04 \x01(\x01\x42\x15\x8a\xb5\x18\x11ms_biggerIsBetter\x12;\n\x07scrolls\x18\x05 \x03(\x0b\x32*.perfetto.protos.ChromeScrollJankV3.Scroll\x1a\xb0\x03\n\x06Scroll\x12,\n\nnum_frames\x18\x01 \x01(\x03\x42\x18\x8a\xb5\x18\x14\x63ount_biggerIsBetter\x12\x33\n\x10num_janky_frames\x18\x02 \x01(\x03\x42\x19\x8a\xb5\x18\x15\x63ount_smallerIsBetter\x12\x36\n\x16scroll_jank_percentage\x18\x03 \x01(\x01\x42\x16\x8a\xb5\x18\x12n%_smallerIsBetter\x12@\n\x1amax_delay_since_last_frame\x18\x04 \x01(\x01\x42\x1c\x8a\xb5\x18\x18unitless_smallerIsBetter\x12V\n\x12scroll_jank_causes\x18\x05 \x03(\x0b\x32:.perfetto.protos.ChromeScrollJankV3.Scroll.ScrollJankCause\x1aq\n\x0fScrollJankCause\x12\r\n\x05\x63\x61use\x18\x01 \x01(\t\x12\x11\n\tsub_cause\x18\x02 \x01(\t\x12<\n\x16\x64\x65lay_since_last_frame\x18\x03 \x01(\x01\x42\x1c\x8a\xb5\x18\x18unitless_smallerIsBetter')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.chrome.scroll_jank_v3_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CHROMESCROLLJANKV3_SCROLL_SCROLLJANKCAUSE'].fields_by_name['delay_since_last_frame']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3_SCROLL_SCROLLJANKCAUSE'].fields_by_name['delay_since_last_frame']._serialized_options = b'\212\265\030\030unitless_smallerIsBetter'
  _globals['_CHROMESCROLLJANKV3_SCROLL'].fields_by_name['num_frames']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3_SCROLL'].fields_by_name['num_frames']._serialized_options = b'\212\265\030\024count_biggerIsBetter'
  _globals['_CHROMESCROLLJANKV3_SCROLL'].fields_by_name['num_janky_frames']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3_SCROLL'].fields_by_name['num_janky_frames']._serialized_options = b'\212\265\030\025count_smallerIsBetter'
  _globals['_CHROMESCROLLJANKV3_SCROLL'].fields_by_name['scroll_jank_percentage']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3_SCROLL'].fields_by_name['scroll_jank_percentage']._serialized_options = b'\212\265\030\022n%_smallerIsBetter'
  _globals['_CHROMESCROLLJANKV3_SCROLL'].fields_by_name['max_delay_since_last_frame']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3_SCROLL'].fields_by_name['max_delay_since_last_frame']._serialized_options = b'\212\265\030\030unitless_smallerIsBetter'
  _globals['_CHROMESCROLLJANKV3'].fields_by_name['trace_num_frames']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3'].fields_by_name['trace_num_frames']._serialized_options = b'\212\265\030\024count_biggerIsBetter'
  _globals['_CHROMESCROLLJANKV3'].fields_by_name['trace_num_janky_frames']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3'].fields_by_name['trace_num_janky_frames']._serialized_options = b'\212\265\030\025count_smallerIsBetter'
  _globals['_CHROMESCROLLJANKV3'].fields_by_name['trace_scroll_jank_percentage']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3'].fields_by_name['trace_scroll_jank_percentage']._serialized_options = b'\212\265\030\022n%_smallerIsBetter'
  _globals['_CHROMESCROLLJANKV3'].fields_by_name['vsync_interval_ms']._loaded_options = None
  _globals['_CHROMESCROLLJANKV3'].fields_by_name['vsync_interval_ms']._serialized_options = b'\212\265\030\021ms_biggerIsBetter'
  _globals['_CHROMESCROLLJANKV3']._serialized_start=119
  _globals['_CHROMESCROLLJANKV3']._serialized_end=858
  _globals['_CHROMESCROLLJANKV3_SCROLL']._serialized_start=426
  _globals['_CHROMESCROLLJANKV3_SCROLL']._serialized_end=858
  _globals['_CHROMESCROLLJANKV3_SCROLL_SCROLLJANKCAUSE']._serialized_start=745
  _globals['_CHROMESCROLLJANKV3_SCROLL_SCROLLJANKCAUSE']._serialized_end=858
# @@protoc_insertion_point(module_scope)
