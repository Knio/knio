# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/android/inputmethodeditor.proto
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
    'protos/perfetto/trace/android/inputmethodeditor.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.trace.android.inputmethodservice import inputmethodservice_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_inputmethodservice_dot_inputmethodservice__pb2
from protos.perfetto.trace.android.server.inputmethod import inputmethodmanagerservice_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_server_dot_inputmethod_dot_inputmethodmanagerservice__pb2
from protos.perfetto.trace.android.view.inputmethod import inputmethodmanager_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_view_dot_inputmethod_dot_inputmethodmanager__pb2
from protos.perfetto.trace.android.view import viewrootimpl_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_view_dot_viewrootimpl__pb2
from protos.perfetto.trace.android.view import insetscontroller_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_view_dot_insetscontroller__pb2
from protos.perfetto.trace.android.view import imeinsetssourceconsumer_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_view_dot_imeinsetssourceconsumer__pb2
from protos.perfetto.trace.android.view.inputmethod import editorinfo_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_view_dot_inputmethod_dot_editorinfo__pb2
from protos.perfetto.trace.android.view.inputmethod import inputconnection_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_view_dot_inputmethod_dot_inputconnection__pb2
from protos.perfetto.trace.android.view import imefocuscontroller_pb2 as protos_dot_perfetto_dot_trace_dot_android_dot_view_dot_imefocuscontroller__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5protos/perfetto/trace/android/inputmethodeditor.proto\x12\x0fperfetto.protos\x1aIprotos/perfetto/trace/android/inputmethodservice/inputmethodservice.proto\x1aPprotos/perfetto/trace/android/server/inputmethod/inputmethodmanagerservice.proto\x1aGprotos/perfetto/trace/android/view/inputmethod/inputmethodmanager.proto\x1a\x35protos/perfetto/trace/android/view/viewrootimpl.proto\x1a\x39protos/perfetto/trace/android/view/insetscontroller.proto\x1a@protos/perfetto/trace/android/view/imeinsetssourceconsumer.proto\x1a?protos/perfetto/trace/android/view/inputmethod/editorinfo.proto\x1a\x44protos/perfetto/trace/android/view/inputmethod/inputconnection.proto\x1a;protos/perfetto/trace/android/view/imefocuscontroller.proto\"\xe8\x05\n\x1cInputMethodClientsTraceProto\x12\x1e\n\x16\x65lapsed_realtime_nanos\x18\x01 \x01(\x06\x12\r\n\x05where\x18\x02 \x01(\t\x12M\n\x06\x63lient\x18\x03 \x01(\x0b\x32=.perfetto.protos.InputMethodClientsTraceProto.ClientSideProto\x1a\xc9\x04\n\x0f\x43lientSideProto\x12\x12\n\ndisplay_id\x18\x01 \x01(\x05\x12\x46\n\x14input_method_manager\x18\x02 \x01(\x0b\x32(.perfetto.protos.InputMethodManagerProto\x12:\n\x0eview_root_impl\x18\x03 \x01(\x0b\x32\".perfetto.protos.ViewRootImplProto\x12\x41\n\x11insets_controller\x18\x04 \x01(\x0b\x32&.perfetto.protos.InsetsControllerProto\x12Q\n\x1aime_insets_source_consumer\x18\x05 \x01(\x0b\x32-.perfetto.protos.ImeInsetsSourceConsumerProto\x12\x35\n\x0b\x65\x64itor_info\x18\x06 \x01(\x0b\x32 .perfetto.protos.EditorInfoProto\x12\x46\n\x14ime_focus_controller\x18\x07 \x01(\x0b\x32(.perfetto.protos.ImeFocusControllerProto\x12?\n\x10input_connection\x18\x08 \x01(\x0b\x32%.perfetto.protos.InputConnectionProto\x12H\n\x15input_connection_call\x18\t \x01(\x0b\x32).perfetto.protos.InputConnectionCallProto\"\x95\x01\n\x1cInputMethodServiceTraceProto\x12\x1e\n\x16\x65lapsed_realtime_nanos\x18\x01 \x01(\x06\x12\r\n\x05where\x18\x02 \x01(\t\x12\x46\n\x14input_method_service\x18\x03 \x01(\x0b\x32(.perfetto.protos.InputMethodServiceProto\"\xab\x01\n#InputMethodManagerServiceTraceProto\x12\x1e\n\x16\x65lapsed_realtime_nanos\x18\x01 \x01(\x06\x12\r\n\x05where\x18\x02 \x01(\t\x12U\n\x1cinput_method_manager_service\x18\x03 \x01(\x0b\x32/.perfetto.protos.InputMethodManagerServiceProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.android.inputmethodeditor_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_INPUTMETHODCLIENTSTRACEPROTO']._serialized_start=681
  _globals['_INPUTMETHODCLIENTSTRACEPROTO']._serialized_end=1425
  _globals['_INPUTMETHODCLIENTSTRACEPROTO_CLIENTSIDEPROTO']._serialized_start=840
  _globals['_INPUTMETHODCLIENTSTRACEPROTO_CLIENTSIDEPROTO']._serialized_end=1425
  _globals['_INPUTMETHODSERVICETRACEPROTO']._serialized_start=1428
  _globals['_INPUTMETHODSERVICETRACEPROTO']._serialized_end=1577
  _globals['_INPUTMETHODMANAGERSERVICETRACEPROTO']._serialized_start=1580
  _globals['_INPUTMETHODMANAGERSERVICETRACEPROTO']._serialized_end=1751
# @@protoc_insertion_point(module_scope)
