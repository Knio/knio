# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/android/view/insetssource.proto
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
    'protos/perfetto/trace/android/view/insetssource.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.trace.android.graphics import rect_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_graphics_dot_rect__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5protos/perfetto/trace/android/view/insetssource.proto\x12\x0fperfetto.protos\x1a\x31protos/perfetto/trace/android/graphics/rect.proto\"\xa9\x01\n\x11InsetsSourceProto\x12\x10\n\x04type\x18\x01 \x01(\tB\x02\x18\x01\x12)\n\x05\x66rame\x18\x02 \x01(\x0b\x32\x1a.perfetto.protos.RectProto\x12\x31\n\rvisible_frame\x18\x03 \x01(\x0b\x32\x1a.perfetto.protos.RectProto\x12\x0f\n\x07visible\x18\x04 \x01(\x08\x12\x13\n\x0btype_number\x18\x05 \x01(\x05')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.android.view.insetssource_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_INSETSSOURCEPROTO'].fields_by_name['type']._loaded_options = None
  _globals['_INSETSSOURCEPROTO'].fields_by_name['type']._serialized_options = b'\030\001'
  _globals['_INSETSSOURCEPROTO']._serialized_start=126
  _globals['_INSETSSOURCEPROTO']._serialized_end=295
# @@protoc_insertion_point(module_scope)