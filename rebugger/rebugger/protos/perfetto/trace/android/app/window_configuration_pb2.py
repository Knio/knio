# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/android/app/window_configuration.proto
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
    'protos/perfetto/trace/android/app/window_configuration.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.trace.android.graphics import rect_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_graphics_dot_rect__pb2
from protos.perfetto.trace.android import typedef_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_typedef__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<protos/perfetto/trace/android/app/window_configuration.proto\x12\x0fperfetto.protos\x1a\x31protos/perfetto/trace/android/graphics/rect.proto\x1a+protos/perfetto/trace/android/typedef.proto\"\xba\x02\n\x18WindowConfigurationProto\x12.\n\napp_bounds\x18\x01 \x01(\x0b\x32\x1a.perfetto.protos.RectProto\x12I\n\x0ewindowing_mode\x18\x02 \x01(\x05\x42\x31\x8a\xa6\x1d-android.app.WindowConfiguration.WindowingMode\x12G\n\ractivity_type\x18\x03 \x01(\x05\x42\x30\x8a\xa6\x1d,android.app.WindowConfiguration.ActivityType\x12*\n\x06\x62ounds\x18\x04 \x01(\x0b\x32\x1a.perfetto.protos.RectProto\x12.\n\nmax_bounds\x18\x05 \x01(\x0b\x32\x1a.perfetto.protos.RectProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.android.app.window_configuration_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_WINDOWCONFIGURATIONPROTO'].fields_by_name['windowing_mode']._loaded_options = None
  _globals['_WINDOWCONFIGURATIONPROTO'].fields_by_name['windowing_mode']._serialized_options = b'\212\246\035-android.app.WindowConfiguration.WindowingMode'
  _globals['_WINDOWCONFIGURATIONPROTO'].fields_by_name['activity_type']._loaded_options = None
  _globals['_WINDOWCONFIGURATIONPROTO'].fields_by_name['activity_type']._serialized_options = b'\212\246\035,android.app.WindowConfiguration.ActivityType'
  _globals['_WINDOWCONFIGURATIONPROTO']._serialized_start=178
  _globals['_WINDOWCONFIGURATIONPROTO']._serialized_end=492
# @@protoc_insertion_point(module_scope)
