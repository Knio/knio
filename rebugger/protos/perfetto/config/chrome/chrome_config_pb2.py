# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/config/chrome/chrome_config.proto
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
    'protos/perfetto/config/chrome/chrome_config.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1protos/perfetto/config/chrome/chrome_config.proto\x12\x0fperfetto.protos\"\x92\x02\n\x0c\x43hromeConfig\x12\x14\n\x0ctrace_config\x18\x01 \x01(\t\x12!\n\x19privacy_filtering_enabled\x18\x02 \x01(\x08\x12\x1e\n\x16\x63onvert_to_legacy_json\x18\x03 \x01(\x08\x12\x45\n\x0f\x63lient_priority\x18\x04 \x01(\x0e\x32,.perfetto.protos.ChromeConfig.ClientPriority\x12\x1f\n\x17json_agent_label_filter\x18\x05 \x01(\t\"A\n\x0e\x43lientPriority\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0e\n\nBACKGROUND\x10\x01\x12\x12\n\x0eUSER_INITIATED\x10\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.config.chrome.chrome_config_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CHROMECONFIG']._serialized_start=71
  _globals['_CHROMECONFIG']._serialized_end=345
  _globals['_CHROMECONFIG_CLIENTPRIORITY']._serialized_start=280
  _globals['_CHROMECONFIG_CLIENTPRIORITY']._serialized_end=345
# @@protoc_insertion_point(module_scope)