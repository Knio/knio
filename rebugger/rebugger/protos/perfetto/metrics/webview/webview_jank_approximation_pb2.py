# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/webview/webview_jank_approximation.proto
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
    'protos/perfetto/metrics/webview/webview_jank_approximation.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n@protos/perfetto/metrics/webview/webview_jank_approximation.proto\x12\x0fperfetto.protos\"\xa5\x01\n\x18WebViewJankApproximation\x12\x15\n\rwebview_janks\x18\x01 \x01(\x05\x12%\n\x1dwebview_janks_without_startup\x18\x02 \x01(\x05\x12\x19\n\x11webview_app_janks\x18\x03 \x01(\x05\x12\x1b\n\x13webview_total_janks\x18\x04 \x01(\x05\x12\x13\n\x0btotal_janks\x18\x05 \x01(\x05')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.webview.webview_jank_approximation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_WEBVIEWJANKAPPROXIMATION']._serialized_start=86
  _globals['_WEBVIEWJANKAPPROXIMATION']._serialized_end=251
# @@protoc_insertion_point(module_scope)