# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/profiling/deobfuscation.proto
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
    'protos/perfetto/trace/profiling/deobfuscation.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3protos/perfetto/trace/profiling/deobfuscation.proto\x12\x0fperfetto.protos\"F\n\x10ObfuscatedMember\x12\x17\n\x0fobfuscated_name\x18\x01 \x01(\t\x12\x19\n\x11\x64\x65obfuscated_name\x18\x02 \x01(\t\"\xc3\x01\n\x0fObfuscatedClass\x12\x17\n\x0fobfuscated_name\x18\x01 \x01(\t\x12\x19\n\x11\x64\x65obfuscated_name\x18\x02 \x01(\t\x12=\n\x12obfuscated_members\x18\x03 \x03(\x0b\x32!.perfetto.protos.ObfuscatedMember\x12=\n\x12obfuscated_methods\x18\x04 \x03(\x0b\x32!.perfetto.protos.ObfuscatedMember\"\x80\x01\n\x14\x44\x65obfuscationMapping\x12\x14\n\x0cpackage_name\x18\x01 \x01(\t\x12\x14\n\x0cversion_code\x18\x02 \x01(\x03\x12<\n\x12obfuscated_classes\x18\x03 \x03(\x0b\x32 .perfetto.protos.ObfuscatedClass')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.profiling.deobfuscation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_OBFUSCATEDMEMBER']._serialized_start=72
  _globals['_OBFUSCATEDMEMBER']._serialized_end=142
  _globals['_OBFUSCATEDCLASS']._serialized_start=145
  _globals['_OBFUSCATEDCLASS']._serialized_end=340
  _globals['_DEOBFUSCATIONMAPPING']._serialized_start=343
  _globals['_DEOBFUSCATIONMAPPING']._serialized_end=471
# @@protoc_insertion_point(module_scope)