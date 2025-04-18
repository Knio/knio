# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/android/content/configuration.proto
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
    'protos/perfetto/trace/android/content/configuration.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.trace.android.app import window_configuration_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_app_dot_window__configuration__pb2
from protos.perfetto.trace.android.content import locale_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_content_dot_locale__pb2
from protos.perfetto.trace.android import privacy_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_privacy__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9protos/perfetto/trace/android/content/configuration.proto\x12\x0fperfetto.protos\x1a<protos/perfetto/trace/android/app/window_configuration.proto\x1a\x32protos/perfetto/trace/android/content/locale.proto\x1a+protos/perfetto/trace/android/privacy.proto\"\xe1\x04\n\x12\x43onfigurationProto\x12\x12\n\nfont_scale\x18\x01 \x01(\x02\x12\x0b\n\x03mcc\x18\x02 \x01(\r\x12\x15\n\x03mnc\x18\x03 \x01(\rB\x08\x9a\x9f\xd5\x87\x03\x02\x08\x64\x12\x31\n\x07locales\x18\x04 \x03(\x0b\x32\x1c.perfetto.protos.LocaleProtoB\x02\x18\x01\x12\x15\n\rscreen_layout\x18\x05 \x01(\r\x12\x12\n\ncolor_mode\x18\x06 \x01(\r\x12\x13\n\x0btouchscreen\x18\x07 \x01(\r\x12\x10\n\x08keyboard\x18\x08 \x01(\r\x12\x17\n\x0fkeyboard_hidden\x18\t \x01(\r\x12\x1c\n\x14hard_keyboard_hidden\x18\n \x01(\r\x12\x12\n\nnavigation\x18\x0b \x01(\r\x12\x19\n\x11navigation_hidden\x18\x0c \x01(\r\x12\x13\n\x0borientation\x18\r \x01(\r\x12\x0f\n\x07ui_mode\x18\x0e \x01(\r\x12\x17\n\x0fscreen_width_dp\x18\x0f \x01(\r\x12\x18\n\x10screen_height_dp\x18\x10 \x01(\r\x12 \n\x18smallest_screen_width_dp\x18\x11 \x01(\r\x12\x13\n\x0b\x64\x65nsity_dpi\x18\x12 \x01(\r\x12G\n\x14window_configuration\x18\x13 \x01(\x0b\x32).perfetto.protos.WindowConfigurationProto\x12\x13\n\x0blocale_list\x18\x14 \x01(\t\x12\x1e\n\x16\x66ont_weight_adjustment\x18\x15 \x01(\r\x12\x1a\n\x12grammatical_gender\x18\x16 \x01(\r\"\xa1\x01\n\x1bResourcesConfigurationProto\x12:\n\rconfiguration\x18\x01 \x01(\x0b\x32#.perfetto.protos.ConfigurationProto\x12\x13\n\x0bsdk_version\x18\x02 \x01(\r\x12\x17\n\x0fscreen_width_px\x18\x03 \x01(\r\x12\x18\n\x10screen_height_px\x18\x04 \x01(\r\"\xc8\x02\n\x18\x44\x65viceConfigurationProto\x12\x1e\n\x16stable_screen_width_px\x18\x01 \x01(\r\x12\x1f\n\x17stable_screen_height_px\x18\x02 \x01(\r\x12\x1a\n\x12stable_density_dpi\x18\x03 \x01(\r\x12\x11\n\ttotal_ram\x18\x04 \x01(\x04\x12\x0f\n\x07low_ram\x18\x05 \x01(\x08\x12\x11\n\tmax_cores\x18\x06 \x01(\r\x12\x1e\n\x16has_secure_screen_lock\x18\x07 \x01(\x08\x12\x16\n\x0eopengl_version\x18\x08 \x01(\r\x12\x19\n\x11opengl_extensions\x18\t \x03(\t\x12\x18\n\x10shared_libraries\x18\n \x03(\t\x12\x10\n\x08\x66\x65\x61tures\x18\x0b \x03(\t\x12\x19\n\x11\x63pu_architectures\x18\x0c \x03(\t\"\x96\x01\n\x18GlobalConfigurationProto\x12?\n\tresources\x18\x01 \x01(\x0b\x32,.perfetto.protos.ResourcesConfigurationProto\x12\x39\n\x06\x64\x65vice\x18\x02 \x01(\x0b\x32).perfetto.protos.DeviceConfigurationProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.android.content.configuration_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CONFIGURATIONPROTO'].fields_by_name['mnc']._loaded_options = None
  _globals['_CONFIGURATIONPROTO'].fields_by_name['mnc']._serialized_options = b'\232\237\325\207\003\002\010d'
  _globals['_CONFIGURATIONPROTO'].fields_by_name['locales']._loaded_options = None
  _globals['_CONFIGURATIONPROTO'].fields_by_name['locales']._serialized_options = b'\030\001'
  _globals['_CONFIGURATIONPROTO']._serialized_start=238
  _globals['_CONFIGURATIONPROTO']._serialized_end=847
  _globals['_RESOURCESCONFIGURATIONPROTO']._serialized_start=850
  _globals['_RESOURCESCONFIGURATIONPROTO']._serialized_end=1011
  _globals['_DEVICECONFIGURATIONPROTO']._serialized_start=1014
  _globals['_DEVICECONFIGURATIONPROTO']._serialized_end=1342
  _globals['_GLOBALCONFIGURATIONPROTO']._serialized_start=1345
  _globals['_GLOBALCONFIGURATIONPROTO']._serialized_end=1495
# @@protoc_insertion_point(module_scope)
