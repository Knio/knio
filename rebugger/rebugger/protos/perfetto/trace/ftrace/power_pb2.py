# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/ftrace/power.proto
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
    'protos/perfetto/trace/ftrace/power.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(protos/perfetto/trace/ftrace/power.proto\x12\x0fperfetto.protos\"8\n\x17\x43puFrequencyFtraceEvent\x12\r\n\x05state\x18\x01 \x01(\r\x12\x0e\n\x06\x63pu_id\x18\x02 \x01(\r\"S\n\x1d\x43puFrequencyLimitsFtraceEvent\x12\x10\n\x08min_freq\x18\x01 \x01(\r\x12\x10\n\x08max_freq\x18\x02 \x01(\r\x12\x0e\n\x06\x63pu_id\x18\x03 \x01(\r\"3\n\x12\x43puIdleFtraceEvent\x12\r\n\x05state\x18\x01 \x01(\r\x12\x0e\n\x06\x63pu_id\x18\x02 \x01(\r\"E\n\x16\x43lockEnableFtraceEvent\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05state\x18\x02 \x01(\x04\x12\x0e\n\x06\x63pu_id\x18\x03 \x01(\x04\"F\n\x17\x43lockDisableFtraceEvent\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05state\x18\x02 \x01(\x04\x12\x0e\n\x06\x63pu_id\x18\x03 \x01(\x04\"F\n\x17\x43lockSetRateFtraceEvent\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05state\x18\x02 \x01(\x04\x12\x0e\n\x06\x63pu_id\x18\x03 \x01(\x04\"F\n\x18SuspendResumeFtraceEvent\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\x0b\n\x03val\x18\x02 \x01(\x05\x12\r\n\x05start\x18\x03 \x01(\r\"8\n\x17GpuFrequencyFtraceEvent\x12\x0e\n\x06gpu_id\x18\x01 \x01(\r\x12\r\n\x05state\x18\x02 \x01(\r\">\n\x1fWakeupSourceActivateFtraceEvent\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05state\x18\x02 \x01(\x04\"@\n!WakeupSourceDeactivateFtraceEvent\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05state\x18\x02 \x01(\x04\"\x85\x01\n\x18GpuWorkPeriodFtraceEvent\x12\x0e\n\x06gpu_id\x18\x01 \x01(\r\x12\x0b\n\x03uid\x18\x02 \x01(\r\x12\x15\n\rstart_time_ns\x18\x03 \x01(\x04\x12\x13\n\x0b\x65nd_time_ns\x18\x04 \x01(\x04\x12 \n\x18total_active_duration_ns\x18\x05 \x01(\x04\"q\n DevicePmCallbackStartFtraceEvent\x12\x0e\n\x06\x64\x65vice\x18\x01 \x01(\t\x12\x0e\n\x06\x64river\x18\x02 \x01(\t\x12\x0e\n\x06parent\x18\x03 \x01(\t\x12\x0e\n\x06pm_ops\x18\x04 \x01(\t\x12\r\n\x05\x65vent\x18\x05 \x01(\x05\"O\n\x1e\x44\x65vicePmCallbackEndFtraceEvent\x12\x0e\n\x06\x64\x65vice\x18\x01 \x01(\t\x12\x0e\n\x06\x64river\x18\x02 \x01(\t\x12\r\n\x05\x65rror\x18\x03 \x01(\x05')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.ftrace.power_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CPUFREQUENCYFTRACEEVENT']._serialized_start=61
  _globals['_CPUFREQUENCYFTRACEEVENT']._serialized_end=117
  _globals['_CPUFREQUENCYLIMITSFTRACEEVENT']._serialized_start=119
  _globals['_CPUFREQUENCYLIMITSFTRACEEVENT']._serialized_end=202
  _globals['_CPUIDLEFTRACEEVENT']._serialized_start=204
  _globals['_CPUIDLEFTRACEEVENT']._serialized_end=255
  _globals['_CLOCKENABLEFTRACEEVENT']._serialized_start=257
  _globals['_CLOCKENABLEFTRACEEVENT']._serialized_end=326
  _globals['_CLOCKDISABLEFTRACEEVENT']._serialized_start=328
  _globals['_CLOCKDISABLEFTRACEEVENT']._serialized_end=398
  _globals['_CLOCKSETRATEFTRACEEVENT']._serialized_start=400
  _globals['_CLOCKSETRATEFTRACEEVENT']._serialized_end=470
  _globals['_SUSPENDRESUMEFTRACEEVENT']._serialized_start=472
  _globals['_SUSPENDRESUMEFTRACEEVENT']._serialized_end=542
  _globals['_GPUFREQUENCYFTRACEEVENT']._serialized_start=544
  _globals['_GPUFREQUENCYFTRACEEVENT']._serialized_end=600
  _globals['_WAKEUPSOURCEACTIVATEFTRACEEVENT']._serialized_start=602
  _globals['_WAKEUPSOURCEACTIVATEFTRACEEVENT']._serialized_end=664
  _globals['_WAKEUPSOURCEDEACTIVATEFTRACEEVENT']._serialized_start=666
  _globals['_WAKEUPSOURCEDEACTIVATEFTRACEEVENT']._serialized_end=730
  _globals['_GPUWORKPERIODFTRACEEVENT']._serialized_start=733
  _globals['_GPUWORKPERIODFTRACEEVENT']._serialized_end=866
  _globals['_DEVICEPMCALLBACKSTARTFTRACEEVENT']._serialized_start=868
  _globals['_DEVICEPMCALLBACKSTARTFTRACEEVENT']._serialized_end=981
  _globals['_DEVICEPMCALLBACKENDFTRACEEVENT']._serialized_start=983
  _globals['_DEVICEPMCALLBACKENDFTRACEEVENT']._serialized_end=1062
# @@protoc_insertion_point(module_scope)
