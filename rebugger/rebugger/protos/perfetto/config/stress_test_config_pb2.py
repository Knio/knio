# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/config/stress_test_config.proto
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
    'protos/perfetto/config/stress_test_config.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.config import trace_config_pb2 as protos_dot_perfetto_dot_config_dot_trace__config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/protos/perfetto/config/stress_test_config.proto\x12\x0fperfetto.protos\x1a)protos/perfetto/config/trace_config.proto\"\x99\x04\n\x10StressTestConfig\x12\x32\n\x0ctrace_config\x18\x01 \x01(\x0b\x32\x1c.perfetto.protos.TraceConfig\x12\x15\n\rshmem_size_kb\x18\x02 \x01(\r\x12\x1a\n\x12shmem_page_size_kb\x18\x03 \x01(\r\x12\x15\n\rnum_processes\x18\x04 \x01(\r\x12\x13\n\x0bnum_threads\x18\x05 \x01(\r\x12\x12\n\nmax_events\x18\x06 \x01(\r\x12\x0f\n\x07nesting\x18\x07 \x01(\r\x12L\n\x14steady_state_timings\x18\x08 \x01(\x0b\x32..perfetto.protos.StressTestConfig.WriterTiming\x12\x17\n\x0f\x62urst_period_ms\x18\t \x01(\r\x12\x19\n\x11\x62urst_duration_ms\x18\n \x01(\r\x12\x45\n\rburst_timings\x18\x0b \x01(\x0b\x32..perfetto.protos.StressTestConfig.WriterTiming\x1a\x83\x01\n\x0cWriterTiming\x12\x14\n\x0cpayload_mean\x18\x01 \x01(\x01\x12\x16\n\x0epayload_stddev\x18\x02 \x01(\x01\x12\x11\n\trate_mean\x18\x03 \x01(\x01\x12\x13\n\x0brate_stddev\x18\x04 \x01(\x01\x12\x1d\n\x15payload_write_time_ms\x18\x05 \x01(\r')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.config.stress_test_config_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STRESSTESTCONFIG']._serialized_start=112
  _globals['_STRESSTESTCONFIG']._serialized_end=649
  _globals['_STRESSTESTCONFIG_WRITERTIMING']._serialized_start=518
  _globals['_STRESSTESTCONFIG_WRITERTIMING']._serialized_end=649
# @@protoc_insertion_point(module_scope)
