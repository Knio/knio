# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/android/winscope_extensions_impl.proto
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
    'protos/perfetto/trace/android/winscope_extensions_impl.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.trace.android import winscope_extensions_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_winscope__extensions__pb2
from protos.perfetto.trace.android import android_input_event_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_android__input__event__pb2
from protos.perfetto.trace.android import inputmethodeditor_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_inputmethodeditor__pb2
from protos.perfetto.trace.android import viewcapture_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_viewcapture__pb2
from protos.perfetto.trace.android import windowmanager_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_windowmanager__pb2

from protos.perfetto.trace.android.winscope_extensions_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<protos/perfetto/trace/android/winscope_extensions_impl.proto\x12\x0fperfetto.protos\x1a\x37protos/perfetto/trace/android/winscope_extensions.proto\x1a\x37protos/perfetto/trace/android/android_input_event.proto\x1a\x35protos/perfetto/trace/android/inputmethodeditor.proto\x1a/protos/perfetto/trace/android/viewcapture.proto\x1a\x31protos/perfetto/trace/android/windowmanager.proto\"\x9e\x05\n\x16WinscopeExtensionsImpl2o\n\x13inputmethod_clients\x12#.perfetto.protos.WinscopeExtensions\x18\x01 \x01(\x0b\x32-.perfetto.protos.InputMethodClientsTraceProto2o\n\x13inputmethod_service\x12#.perfetto.protos.WinscopeExtensions\x18\x02 \x01(\x0b\x32-.perfetto.protos.InputMethodServiceTraceProto2~\n\x1binputmethod_manager_service\x12#.perfetto.protos.WinscopeExtensions\x18\x03 \x01(\x0b\x32\x34.perfetto.protos.InputMethodManagerServiceTraceProto2V\n\x0bviewcapture\x12#.perfetto.protos.WinscopeExtensions\x18\x04 \x01(\x0b\x32\x1c.perfetto.protos.ViewCapture2d\n\x13\x61ndroid_input_event\x12#.perfetto.protos.WinscopeExtensions\x18\x05 \x01(\x0b\x32\".perfetto.protos.AndroidInputEvent2d\n\rwindowmanager\x12#.perfetto.protos.WinscopeExtensions\x18\x06 \x01(\x0b\x32(.perfetto.protos.WindowManagerTraceEntryP\x00')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.android.winscope_extensions_impl_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_WINSCOPEEXTENSIONSIMPL']._serialized_start=351
  _globals['_WINSCOPEEXTENSIONSIMPL']._serialized_end=1021
# @@protoc_insertion_point(module_scope)
