# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/chrome/chrome_benchmark_metadata.proto
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
    'protos/perfetto/trace/chrome/chrome_benchmark_metadata.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<protos/perfetto/trace/chrome/chrome_benchmark_metadata.proto\x12\x0fperfetto.protos\"\xf2\x01\n\x17\x43hromeBenchmarkMetadata\x12\x1f\n\x17\x62\x65nchmark_start_time_us\x18\x01 \x01(\x03\x12\x19\n\x11story_run_time_us\x18\x02 \x01(\x03\x12\x16\n\x0e\x62\x65nchmark_name\x18\x03 \x01(\t\x12\x1d\n\x15\x62\x65nchmark_description\x18\x04 \x01(\t\x12\r\n\x05label\x18\x05 \x01(\t\x12\x12\n\nstory_name\x18\x06 \x01(\t\x12\x12\n\nstory_tags\x18\x07 \x03(\t\x12\x17\n\x0fstory_run_index\x18\x08 \x01(\x05\x12\x14\n\x0chad_failures\x18\t \x01(\x08')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.chrome.chrome_benchmark_metadata_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CHROMEBENCHMARKMETADATA']._serialized_start=82
  _globals['_CHROMEBENCHMARKMETADATA']._serialized_end=324
# @@protoc_insertion_point(module_scope)
