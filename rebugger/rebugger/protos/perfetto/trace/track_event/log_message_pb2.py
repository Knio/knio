# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/track_event/log_message.proto
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
    'protos/perfetto/trace/track_event/log_message.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3protos/perfetto/trace/track_event/log_message.proto\x12\x0fperfetto.protos\"\x83\x02\n\nLogMessage\x12\x1b\n\x13source_location_iid\x18\x01 \x01(\x04\x12\x10\n\x08\x62ody_iid\x18\x02 \x01(\x04\x12\x32\n\x04prio\x18\x03 \x01(\x0e\x32$.perfetto.protos.LogMessage.Priority\"\x91\x01\n\x08Priority\x12\x14\n\x10PRIO_UNSPECIFIED\x10\x00\x12\x0f\n\x0bPRIO_UNUSED\x10\x01\x12\x10\n\x0cPRIO_VERBOSE\x10\x02\x12\x0e\n\nPRIO_DEBUG\x10\x03\x12\r\n\tPRIO_INFO\x10\x04\x12\r\n\tPRIO_WARN\x10\x05\x12\x0e\n\nPRIO_ERROR\x10\x06\x12\x0e\n\nPRIO_FATAL\x10\x07\"+\n\x0eLogMessageBody\x12\x0b\n\x03iid\x18\x01 \x01(\x04\x12\x0c\n\x04\x62ody\x18\x02 \x01(\t')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.track_event.log_message_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LOGMESSAGE']._serialized_start=73
  _globals['_LOGMESSAGE']._serialized_end=332
  _globals['_LOGMESSAGE_PRIORITY']._serialized_start=187
  _globals['_LOGMESSAGE_PRIORITY']._serialized_end=332
  _globals['_LOGMESSAGEBODY']._serialized_start=334
  _globals['_LOGMESSAGEBODY']._serialized_end=377
# @@protoc_insertion_point(module_scope)
