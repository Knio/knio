# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/track_event/chrome_process_descriptor.proto
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
    'protos/perfetto/trace/track_event/chrome_process_descriptor.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nAprotos/perfetto/trace/track_event/chrome_process_descriptor.proto\x12\x0fperfetto.protos\"\xe5\x0b\n\x17\x43hromeProcessDescriptor\x12J\n\x0cprocess_type\x18\x01 \x01(\x0e\x32\x34.perfetto.protos.ChromeProcessDescriptor.ProcessType\x12\x18\n\x10process_priority\x18\x02 \x01(\x05\x12\x19\n\x11legacy_sort_index\x18\x03 \x01(\x05\x12\x1d\n\x15host_app_package_name\x18\x04 \x01(\t\x12\x16\n\x0e\x63rash_trace_id\x18\x05 \x01(\x04\"\x91\n\n\x0bProcessType\x12\x17\n\x13PROCESS_UNSPECIFIED\x10\x00\x12\x13\n\x0fPROCESS_BROWSER\x10\x01\x12\x14\n\x10PROCESS_RENDERER\x10\x02\x12\x13\n\x0fPROCESS_UTILITY\x10\x03\x12\x12\n\x0ePROCESS_ZYGOTE\x10\x04\x12\x1a\n\x16PROCESS_SANDBOX_HELPER\x10\x05\x12\x0f\n\x0bPROCESS_GPU\x10\x06\x12\x18\n\x14PROCESS_PPAPI_PLUGIN\x10\x07\x12\x18\n\x14PROCESS_PPAPI_BROKER\x10\x08\x12\x1b\n\x17PROCESS_SERVICE_NETWORK\x10\t\x12\x1b\n\x17PROCESS_SERVICE_TRACING\x10\n\x12\x1b\n\x17PROCESS_SERVICE_STORAGE\x10\x0b\x12\x19\n\x15PROCESS_SERVICE_AUDIO\x10\x0c\x12 \n\x1cPROCESS_SERVICE_DATA_DECODER\x10\r\x12\x1c\n\x18PROCESS_SERVICE_UTIL_WIN\x10\x0e\x12\"\n\x1ePROCESS_SERVICE_PROXY_RESOLVER\x10\x0f\x12\x17\n\x13PROCESS_SERVICE_CDM\x10\x10\x12!\n\x1dPROCESS_SERVICE_VIDEO_CAPTURE\x10\x11\x12\x1c\n\x18PROCESS_SERVICE_UNZIPPER\x10\x12\x12\x1d\n\x19PROCESS_SERVICE_MIRRORING\x10\x13\x12\x1f\n\x1bPROCESS_SERVICE_FILEPATCHER\x10\x14\x12\x17\n\x13PROCESS_SERVICE_TTS\x10\x15\x12\x1c\n\x18PROCESS_SERVICE_PRINTING\x10\x16\x12\x1e\n\x1aPROCESS_SERVICE_QUARANTINE\x10\x17\x12$\n PROCESS_SERVICE_CROS_LOCALSEARCH\x10\x18\x12\x30\n,PROCESS_SERVICE_CROS_ASSISTANT_AUDIO_DECODER\x10\x19\x12\x1c\n\x18PROCESS_SERVICE_FILEUTIL\x10\x1a\x12#\n\x1fPROCESS_SERVICE_PRINTCOMPOSITOR\x10\x1b\x12 \n\x1cPROCESS_SERVICE_PAINTPREVIEW\x10\x1c\x12%\n!PROCESS_SERVICE_SPEECHRECOGNITION\x10\x1d\x12\x1c\n\x18PROCESS_SERVICE_XRDEVICE\x10\x1e\x12\x1c\n\x18PROCESS_SERVICE_READICON\x10\x1f\x12%\n!PROCESS_SERVICE_LANGUAGEDETECTION\x10 \x12\x1b\n\x17PROCESS_SERVICE_SHARING\x10!\x12\x1f\n\x1bPROCESS_SERVICE_MEDIAPARSER\x10\"\x12#\n\x1fPROCESS_SERVICE_QRCODEGENERATOR\x10#\x12!\n\x1dPROCESS_SERVICE_PROFILEIMPORT\x10$\x12\x17\n\x13PROCESS_SERVICE_IME\x10%\x12\x1d\n\x19PROCESS_SERVICE_RECORDING\x10&\x12\"\n\x1ePROCESS_SERVICE_SHAPEDETECTION\x10\'\x12\x1e\n\x1aPROCESS_RENDERER_EXTENSION\x10(\x12$\n PROCESS_SERVICE_MEDIA_FOUNDATION\x10)')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.track_event.chrome_process_descriptor_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CHROMEPROCESSDESCRIPTOR']._serialized_start=87
  _globals['_CHROMEPROCESSDESCRIPTOR']._serialized_end=1596
  _globals['_CHROMEPROCESSDESCRIPTOR_PROCESSTYPE']._serialized_start=299
  _globals['_CHROMEPROCESSDESCRIPTOR_PROCESSTYPE']._serialized_end=1596
# @@protoc_insertion_point(module_scope)
