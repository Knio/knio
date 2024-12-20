# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/sys_stats/sys_stats.proto
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
    'protos/perfetto/trace/sys_stats/sys_stats.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.common import sys_stats_counters_pb2 as protos_dot_perfetto_dot_common_dot_sys__stats__counters__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/protos/perfetto/trace/sys_stats/sys_stats.proto\x12\x0fperfetto.protos\x1a/protos/perfetto/common/sys_stats_counters.proto\"\xd6\x0f\n\x08SysStats\x12\x37\n\x07meminfo\x18\x01 \x03(\x0b\x32&.perfetto.protos.SysStats.MeminfoValue\x12\x35\n\x06vmstat\x18\x02 \x03(\x0b\x32%.perfetto.protos.SysStats.VmstatValue\x12\x34\n\x08\x63pu_stat\x18\x03 \x03(\x0b\x32\".perfetto.protos.SysStats.CpuTimes\x12\x11\n\tnum_forks\x18\x04 \x01(\x04\x12\x15\n\rnum_irq_total\x18\x05 \x01(\x04\x12\x39\n\x07num_irq\x18\x06 \x03(\x0b\x32(.perfetto.protos.SysStats.InterruptCount\x12\x19\n\x11num_softirq_total\x18\x07 \x01(\x04\x12=\n\x0bnum_softirq\x18\x08 \x03(\x0b\x32(.perfetto.protos.SysStats.InterruptCount\x12 \n\x18\x63ollection_end_timestamp\x18\t \x01(\x04\x12\x37\n\x07\x64\x65vfreq\x18\n \x03(\x0b\x32&.perfetto.protos.SysStats.DevfreqValue\x12\x13\n\x0b\x63pufreq_khz\x18\x0b \x03(\r\x12\x37\n\nbuddy_info\x18\x0c \x03(\x0b\x32#.perfetto.protos.SysStats.BuddyInfo\x12\x35\n\tdisk_stat\x18\r \x03(\x0b\x32\".perfetto.protos.SysStats.DiskStat\x12\x30\n\x03psi\x18\x0e \x03(\x0b\x32#.perfetto.protos.SysStats.PsiSample\x12;\n\x0cthermal_zone\x18\x0f \x03(\x0b\x32%.perfetto.protos.SysStats.ThermalZone\x12=\n\rcpuidle_state\x18\x10 \x03(\x0b\x32&.perfetto.protos.SysStats.CpuIdleState\x12\x13\n\x0bgpufreq_mhz\x18\x11 \x03(\x04\x1aL\n\x0cMeminfoValue\x12-\n\x03key\x18\x01 \x01(\x0e\x32 .perfetto.protos.MeminfoCounters\x12\r\n\x05value\x18\x02 \x01(\x04\x1aJ\n\x0bVmstatValue\x12,\n\x03key\x18\x01 \x01(\x0e\x32\x1f.perfetto.protos.VmstatCounters\x12\r\n\x05value\x18\x02 \x01(\x04\x1a\xa2\x01\n\x08\x43puTimes\x12\x0e\n\x06\x63pu_id\x18\x01 \x01(\r\x12\x0f\n\x07user_ns\x18\x02 \x01(\x04\x12\x14\n\x0cuser_nice_ns\x18\x03 \x01(\x04\x12\x16\n\x0esystem_mode_ns\x18\x04 \x01(\x04\x12\x0f\n\x07idle_ns\x18\x05 \x01(\x04\x12\x12\n\nio_wait_ns\x18\x06 \x01(\x04\x12\x0e\n\x06irq_ns\x18\x07 \x01(\x04\x12\x12\n\nsoftirq_ns\x18\x08 \x01(\x04\x1a,\n\x0eInterruptCount\x12\x0b\n\x03irq\x18\x01 \x01(\x05\x12\r\n\x05\x63ount\x18\x02 \x01(\x04\x1a*\n\x0c\x44\x65vfreqValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x04\x1a<\n\tBuddyInfo\x12\x0c\n\x04node\x18\x01 \x01(\t\x12\x0c\n\x04zone\x18\x02 \x01(\t\x12\x13\n\x0border_pages\x18\x03 \x03(\r\x1a\xd7\x01\n\x08\x44iskStat\x12\x13\n\x0b\x64\x65vice_name\x18\x01 \x01(\t\x12\x14\n\x0cread_sectors\x18\x02 \x01(\x04\x12\x14\n\x0cread_time_ms\x18\x03 \x01(\x04\x12\x15\n\rwrite_sectors\x18\x04 \x01(\x04\x12\x15\n\rwrite_time_ms\x18\x05 \x01(\x04\x12\x17\n\x0f\x64iscard_sectors\x18\x06 \x01(\x04\x12\x17\n\x0f\x64iscard_time_ms\x18\x07 \x01(\x04\x12\x13\n\x0b\x66lush_count\x18\x08 \x01(\x04\x12\x15\n\rflush_time_ms\x18\t \x01(\x04\x1a\xb4\x02\n\tPsiSample\x12\x41\n\x08resource\x18\x01 \x01(\x0e\x32/.perfetto.protos.SysStats.PsiSample.PsiResource\x12\x10\n\x08total_ns\x18\x02 \x01(\x04\"\xd1\x01\n\x0bPsiResource\x12\x1c\n\x18PSI_RESOURCE_UNSPECIFIED\x10\x00\x12\x19\n\x15PSI_RESOURCE_CPU_SOME\x10\x01\x12\x19\n\x15PSI_RESOURCE_CPU_FULL\x10\x02\x12\x18\n\x14PSI_RESOURCE_IO_SOME\x10\x03\x12\x18\n\x14PSI_RESOURCE_IO_FULL\x10\x04\x12\x1c\n\x18PSI_RESOURCE_MEMORY_SOME\x10\x05\x12\x1c\n\x18PSI_RESOURCE_MEMORY_FULL\x10\x06\x1a\x37\n\x0bThermalZone\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04temp\x18\x02 \x01(\x04\x12\x0c\n\x04type\x18\x03 \x01(\t\x1a\x37\n\x11\x43puIdleStateEntry\x12\r\n\x05state\x18\x01 \x01(\t\x12\x13\n\x0b\x64uration_us\x18\x02 \x01(\x04\x1ah\n\x0c\x43puIdleState\x12\x0e\n\x06\x63pu_id\x18\x01 \x01(\r\x12H\n\x13\x63puidle_state_entry\x18\x02 \x03(\x0b\x32+.perfetto.protos.SysStats.CpuIdleStateEntry')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.sys_stats.sys_stats_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SYSSTATS']._serialized_start=118
  _globals['_SYSSTATS']._serialized_end=2124
  _globals['_SYSSTATS_MEMINFOVALUE']._serialized_start=906
  _globals['_SYSSTATS_MEMINFOVALUE']._serialized_end=982
  _globals['_SYSSTATS_VMSTATVALUE']._serialized_start=984
  _globals['_SYSSTATS_VMSTATVALUE']._serialized_end=1058
  _globals['_SYSSTATS_CPUTIMES']._serialized_start=1061
  _globals['_SYSSTATS_CPUTIMES']._serialized_end=1223
  _globals['_SYSSTATS_INTERRUPTCOUNT']._serialized_start=1225
  _globals['_SYSSTATS_INTERRUPTCOUNT']._serialized_end=1269
  _globals['_SYSSTATS_DEVFREQVALUE']._serialized_start=1271
  _globals['_SYSSTATS_DEVFREQVALUE']._serialized_end=1313
  _globals['_SYSSTATS_BUDDYINFO']._serialized_start=1315
  _globals['_SYSSTATS_BUDDYINFO']._serialized_end=1375
  _globals['_SYSSTATS_DISKSTAT']._serialized_start=1378
  _globals['_SYSSTATS_DISKSTAT']._serialized_end=1593
  _globals['_SYSSTATS_PSISAMPLE']._serialized_start=1596
  _globals['_SYSSTATS_PSISAMPLE']._serialized_end=1904
  _globals['_SYSSTATS_PSISAMPLE_PSIRESOURCE']._serialized_start=1695
  _globals['_SYSSTATS_PSISAMPLE_PSIRESOURCE']._serialized_end=1904
  _globals['_SYSSTATS_THERMALZONE']._serialized_start=1906
  _globals['_SYSSTATS_THERMALZONE']._serialized_end=1961
  _globals['_SYSSTATS_CPUIDLESTATEENTRY']._serialized_start=1963
  _globals['_SYSSTATS_CPUIDLESTATEENTRY']._serialized_end=2018
  _globals['_SYSSTATS_CPUIDLESTATE']._serialized_start=2020
  _globals['_SYSSTATS_CPUIDLESTATE']._serialized_end=2124
# @@protoc_insertion_point(module_scope)
