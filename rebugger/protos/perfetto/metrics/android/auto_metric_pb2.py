# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/android/auto_metric.proto
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
    'protos/perfetto/metrics/android/auto_metric.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1protos/perfetto/metrics/android/auto_metric.proto\x12\x0fperfetto.protos\"\xf7\x02\n\x1a\x41ndroidAutoMultiuserMetric\x12J\n\x0buser_switch\x18\x01 \x03(\x0b\x32\x35.perfetto.protos.AndroidAutoMultiuserMetric.EventData\x1a\x8c\x02\n\tEventData\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x13\n\x0bstart_event\x18\x02 \x01(\t\x12\x11\n\tend_event\x18\x03 \x01(\t\x12\x13\n\x0b\x64uration_ms\x18\x04 \x01(\x03\x12Z\n\x12previous_user_info\x18\x05 \x01(\x0b\x32>.perfetto.protos.AndroidAutoMultiuserMetric.EventData.UserData\x1aU\n\x08UserData\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x19\n\x11total_cpu_time_ms\x18\x02 \x01(\x03\x12\x1d\n\x15total_memory_usage_kb\x18\x03 \x01(\x03')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.android.auto_metric_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANDROIDAUTOMULTIUSERMETRIC']._serialized_start=71
  _globals['_ANDROIDAUTOMULTIUSERMETRIC']._serialized_end=446
  _globals['_ANDROIDAUTOMULTIUSERMETRIC_EVENTDATA']._serialized_start=178
  _globals['_ANDROIDAUTOMULTIUSERMETRIC_EVENTDATA']._serialized_end=446
  _globals['_ANDROIDAUTOMULTIUSERMETRIC_EVENTDATA_USERDATA']._serialized_start=361
  _globals['_ANDROIDAUTOMULTIUSERMETRIC_EVENTDATA_USERDATA']._serialized_end=446
# @@protoc_insertion_point(module_scope)