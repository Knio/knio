# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/android/startup_metric.proto
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
    'protos/perfetto/metrics/android/startup_metric.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.perfetto.metrics.android import process_metadata_pb2 as protos_dot_perfetto_dot_metrics_dot_android_dot_process__metadata__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4protos/perfetto/metrics/android/startup_metric.proto\x12\x0fperfetto.protos\x1a\x36protos/perfetto/metrics/android/process_metadata.proto\"\xd0\x39\n\x14\x41ndroidStartupMetric\x12>\n\x07startup\x18\x01 \x03(\x0b\x32-.perfetto.protos.AndroidStartupMetric.Startup\x1a\xe5\x01\n\x12TaskStateBreakdown\x12\x16\n\x0erunning_dur_ns\x18\x01 \x01(\x03\x12\x17\n\x0frunnable_dur_ns\x18\x02 \x01(\x03\x12$\n\x1cuninterruptible_sleep_dur_ns\x18\x03 \x01(\x03\x12\"\n\x1ainterruptible_sleep_dur_ns\x18\x04 \x01(\x03\x12\'\n\x1funinterruptible_io_sleep_dur_ns\x18\x05 \x01(\x03\x12+\n#uninterruptible_non_io_sleep_dur_ns\x18\x06 \x01(\x03\x1aQ\n\x11McyclesByCoreType\x12\x0e\n\x06little\x18\x01 \x01(\x03\x12\x0b\n\x03\x62ig\x18\x02 \x01(\x03\x12\x0e\n\x06\x62igger\x18\x03 \x01(\x03\x12\x0f\n\x07unknown\x18\x04 \x01(\x03\x1a\'\n\x05Slice\x12\x0e\n\x06\x64ur_ns\x18\x01 \x01(\x03\x12\x0e\n\x06\x64ur_ms\x18\x02 \x01(\x01\x1a\x93\x12\n\x0cToFirstFrame\x12\x0e\n\x06\x64ur_ns\x18\x01 \x01(\x03\x12\x0e\n\x06\x64ur_ms\x18\x11 \x01(\x01\x12[\n\x19main_thread_by_task_state\x18\x02 \x01(\x0b\x32\x38.perfetto.protos.AndroidStartupMetric.TaskStateBreakdown\x12U\n\x14mcycles_by_core_type\x18\x1a \x01(\x0b\x32\x37.perfetto.protos.AndroidStartupMetric.McyclesByCoreType\x12%\n\x1dother_processes_spawned_count\x18\x03 \x01(\r\x12J\n\x15time_activity_manager\x18\x04 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12N\n\x19time_activity_thread_main\x18\x05 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12J\n\x15time_bind_application\x18\x06 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12H\n\x13time_activity_start\x18\x07 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12I\n\x14time_activity_resume\x18\x08 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12J\n\x15time_activity_restart\x18\x15 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12G\n\x12time_choreographer\x18\t \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x41\n\x0ctime_inflate\x18\x16 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12G\n\x12time_get_resources\x18\x17 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12N\n\x19time_before_start_process\x18\n \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12N\n\x19time_during_start_process\x18\x0b \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12J\n\x15time_to_running_state\x18# \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x41\n\x0cto_post_fork\x18\x12 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12L\n\x17to_activity_thread_main\x18\x13 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12H\n\x13to_bind_application\x18\x14 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x43\n\x0etime_post_fork\x18\x10 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12N\n\x19time_class_initialization\x18$ \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x42\n\rtime_dex_open\x18\x18 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x46\n\x11time_verify_class\x18\x19 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x1c\n\x14jit_compiled_methods\x18\x1b \x01(\r\x12\"\n\x1a\x63lass_initialization_count\x18% \x01(\r\x12P\n\x1btime_jit_thread_pool_on_cpu\x18\x1c \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x42\n\rtime_gc_total\x18\x1d \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x43\n\x0etime_gc_on_cpu\x18\x1e \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12U\n time_lock_contention_thread_main\x18\x1f \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12X\n#time_monitor_contention_thread_main\x18  \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12N\n\x19time_dex_open_thread_main\x18! \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12L\n\x17time_dlopen_thread_main\x18\" \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.SliceJ\x04\x08\x0c\x10\rJ\x04\x08\r\x10\x0eJ\x04\x08\x0e\x10\x0fJ\x04\x08\x0f\x10\x10\x1aO\n\nHscMetrics\x12\x41\n\x0c\x66ull_startup\x18\x01 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x1aG\n\x08\x41\x63tivity\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x02 \x01(\t\x12\x17\n\x0fts_method_start\x18\x04 \x01(\x03J\x04\x08\x03\x10\x04\x1a\xcb\x01\n\x11\x42inderTransaction\x12=\n\x08\x64uration\x18\x01 \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12\x0e\n\x06thread\x18\x02 \x01(\t\x12\x1a\n\x12\x64\x65stination_thread\x18\x03 \x01(\t\x12\x1b\n\x13\x64\x65stination_process\x18\x04 \x01(\t\x12\r\n\x05\x66lags\x18\x05 \x01(\t\x12\x0c\n\x04\x63ode\x18\x06 \x01(\t\x12\x11\n\tdata_size\x18\x07 \x01(\x03\x1a\x84\x01\n\x12OptimizationStatus\x12\x13\n\x0bodex_status\x18\x01 \x01(\t\x12\x1a\n\x12\x63ompilation_filter\x18\x02 \x01(\t\x12\x1a\n\x12\x63ompilation_reason\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0f\n\x07summary\x18\x05 \x01(\t\x1a+\n\x0bVerifyClass\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x64ur_ns\x18\x02 \x01(\x03\x1a?\n\x0f\x45ventTimestamps\x12\x17\n\x0fintent_received\x18\x01 \x01(\x03\x12\x13\n\x0b\x66irst_frame\x18\x02 \x01(\x03\x1a\xe9\x01\n\x0bSystemState\x12\x1b\n\x0f\x64\x65x2oat_running\x18\x01 \x01(\x08\x42\x02\x18\x01\x12\x1c\n\x10installd_running\x18\x02 \x01(\x08\x42\x02\x18\x01\x12\"\n\x1a\x62roadcast_dispatched_count\x18\x03 \x01(\x03\x12 \n\x18\x62roadcast_received_count\x18\x04 \x01(\x03\x12(\n most_active_non_launch_processes\x18\x05 \x03(\t\x12\x17\n\x0finstalld_dur_ns\x18\x06 \x01(\x03\x12\x16\n\x0e\x64\x65x2oat_dur_ns\x18\x07 \x01(\x03\x1a:\n\x17SlowStartReasonDetailed\x12\x0e\n\x06reason\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\x1a\xf6\x0b\n\x0fSlowStartReason\x12Q\n\treason_id\x18\x01 \x01(\x0e\x32>.perfetto.protos.AndroidStartupMetric.SlowStartReason.ReasonId\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12U\n\x08severity\x18\n \x01(\x0e\x32\x43.perfetto.protos.AndroidStartupMetric.SlowStartReason.SeverityLevel\x12L\n\x0e\x65xpected_value\x18\x03 \x01(\x0b\x32\x34.perfetto.protos.AndroidStartupMetric.ThresholdValue\x12G\n\x0c\x61\x63tual_value\x18\x04 \x01(\x0b\x32\x31.perfetto.protos.AndroidStartupMetric.ActualValue\x12\x12\n\nlaunch_dur\x18\x05 \x01(\x03\x12\x10\n\x08\x64uration\x18\x06 \x01(\x03\x12Y\n\x14trace_slice_sections\x18\x07 \x01(\x0b\x32;.perfetto.protos.AndroidStartupMetric.TraceSliceSectionInfo\x12[\n\x15trace_thread_sections\x18\x08 \x01(\x0b\x32<.perfetto.protos.AndroidStartupMetric.TraceThreadSectionInfo\x12\x17\n\x0f\x61\x64\x64itional_info\x18\t \x01(\t\"\xcd\x06\n\x08ReasonId\x12\x19\n\x15REASON_ID_UNSPECIFIED\x10\x00\x12!\n\x1dNO_BASELINE_OR_CLOUD_PROFILES\x10\x01\x12\x10\n\x0cRUN_FROM_APK\x10\x02\x12\x12\n\x0eUNLOCK_RUNNING\x10\x03\x12\x1a\n\x16\x41PP_IN_DEBUGGABLE_MODE\x10\x04\x12\x0f\n\x0bGC_ACTIVITY\x10\x05\x12\x13\n\x0f\x44\x45X2OAT_RUNNING\x10\x06\x12\x14\n\x10INSTALLD_RUNNING\x10\x07\x12&\n\"MAIN_THREAD_TIME_SPENT_IN_RUNNABLE\x10\x08\x12\x31\n-MAIN_THREAD_TIME_SPENT_IN_INTERRUPTIBLE_SLEEP\x10\t\x12)\n%MAIN_THREAD_TIME_SPENT_IN_BLOCKING_IO\x10\n\x12\x35\n1MAIN_THREAD_TIME_SPENT_IN_OPEN_DEX_FILES_FROM_OAT\x10\x0b\x12\"\n\x1eTIME_SPENT_IN_BIND_APPLICATION\x10\x0c\x12 \n\x1cTIME_SPENT_IN_VIEW_INFLATION\x10\r\x12\x31\n-TIME_SPENT_IN_RESOURCES_MANAGER_GET_RESOURCES\x10\x0e\x12 \n\x1cTIME_SPENT_VERIFYING_CLASSES\x10\x0f\x12\x31\n-POTENTIAL_CPU_CONTENTION_WITH_ANOTHER_PROCESS\x10\x10\x12\x10\n\x0cJIT_ACTIVITY\x10\x11\x12\x1f\n\x1bMAIN_THREAD_LOCK_CONTENTION\x10\x12\x12\"\n\x1eMAIN_THREAD_MONITOR_CONTENTION\x10\x13\x12\x18\n\x14JIT_COMPILED_METHODS\x10\x14\x12\x1e\n\x1a\x42ROADCAST_DISPATCHED_COUNT\x10\x15\x12\x1c\n\x18\x42ROADCAST_RECEIVED_COUNT\x10\x16\x12\x1e\n\x1aSTARTUP_RUNNING_CONCURRENT\x10\x17\x12+\n\'MAIN_THREAD_BINDER_TRANSCATIONS_BLOCKED\x10\x18\"K\n\rSeverityLevel\x12\x18\n\x14SEVERITY_UNSPECIFIED\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x12\x0b\n\x07WARNING\x10\x02\x12\x08\n\x04INFO\x10\x03\x1a\xf1\x01\n\x0eThresholdValue\x12\r\n\x05value\x18\x01 \x01(\x03\x12P\n\x04unit\x18\x02 \x01(\x0e\x32\x42.perfetto.protos.AndroidStartupMetric.ThresholdValue.ThresholdUnit\x12\x17\n\x0fhigher_expected\x18\x03 \x01(\x08\"e\n\rThresholdUnit\x12\x1e\n\x1aTHRESHOLD_UNIT_UNSPECIFIED\x10\x00\x12\x06\n\x02NS\x10\x01\x12\x0e\n\nPERCENTAGE\x10\x02\x12\x11\n\rTRUE_OR_FALSE\x10\x03\x12\t\n\x05\x43OUNT\x10\x04\x1a)\n\x0b\x41\x63tualValue\x12\r\n\x05value\x18\x01 \x01(\x03\x12\x0b\n\x03\x64ur\x18\x02 \x01(\x03\x1a\x92\x01\n\x11TraceSliceSection\x12\x17\n\x0fstart_timestamp\x18\x01 \x01(\x03\x12\x15\n\rend_timestamp\x18\x02 \x01(\x03\x12\x10\n\x08slice_id\x18\x03 \x01(\r\x12\x12\n\nslice_name\x18\x04 \x01(\t\x12\x13\n\x0bprocess_pid\x18\x05 \x01(\r\x12\x12\n\nthread_tid\x18\x06 \x01(\r\x1a\x97\x01\n\x15TraceSliceSectionInfo\x12N\n\rslice_section\x18\x01 \x03(\x0b\x32\x37.perfetto.protos.AndroidStartupMetric.TraceSliceSection\x12\x17\n\x0fstart_timestamp\x18\x02 \x01(\x03\x12\x15\n\rend_timestamp\x18\x03 \x01(\x03\x1a\x97\x01\n\x12TraceThreadSection\x12\x17\n\x0fstart_timestamp\x18\x01 \x01(\x03\x12\x15\n\rend_timestamp\x18\x02 \x01(\x03\x12\x13\n\x0bthread_utid\x18\x03 \x01(\r\x12\x13\n\x0bthread_name\x18\x04 \x01(\t\x12\x13\n\x0bprocess_pid\x18\x05 \x01(\r\x12\x12\n\nthread_tid\x18\x06 \x01(\r\x1a\x9a\x01\n\x16TraceThreadSectionInfo\x12P\n\x0ethread_section\x18\x01 \x03(\x0b\x32\x38.perfetto.protos.AndroidStartupMetric.TraceThreadSection\x12\x17\n\x0fstart_timestamp\x18\x02 \x01(\x03\x12\x15\n\rend_timestamp\x18\x03 \x01(\x03\x1a\xfa\t\n\x07Startup\x12\x12\n\nstartup_id\x18\x01 \x01(\r\x12\x14\n\x0cstartup_type\x18\x10 \x01(\t\x12\x11\n\tcpu_count\x18\x19 \x01(\r\x12\x14\n\x0cpackage_name\x18\x02 \x01(\t\x12\x14\n\x0cprocess_name\x18\x03 \x01(\t\x12\x42\n\nactivities\x18\x0b \x03(\x0b\x32..perfetto.protos.AndroidStartupMetric.Activity\x12Y\n\x18long_binder_transactions\x18\x0e \x03(\x0b\x32\x37.perfetto.protos.AndroidStartupMetric.BinderTransaction\x12\x1a\n\x12zygote_new_process\x18\x04 \x01(\x08\x12&\n\x1e\x61\x63tivity_hosting_process_count\x18\x06 \x01(\r\x12\x1f\n\x17time_to_initial_display\x18\x16 \x01(\x03\x12\x1c\n\x14time_to_full_display\x18\x17 \x01(\x03\x12O\n\x10\x65vent_timestamps\x18\r \x01(\x0b\x32\x35.perfetto.protos.AndroidStartupMetric.EventTimestamps\x12J\n\x0eto_first_frame\x18\x05 \x01(\x0b\x32\x32.perfetto.protos.AndroidStartupMetric.ToFirstFrame\x12\x38\n\x07process\x18\x07 \x01(\x0b\x32\'.perfetto.protos.AndroidProcessMetadata\x12=\n\x03hsc\x18\x08 \x01(\x0b\x32\x30.perfetto.protos.AndroidStartupMetric.HscMetrics\x12G\n\x12report_fully_drawn\x18\t \x01(\x0b\x32+.perfetto.protos.AndroidStartupMetric.Slice\x12U\n\x13optimization_status\x18\x0c \x03(\x0b\x32\x38.perfetto.protos.AndroidStartupMetric.OptimizationStatus\x12G\n\x0cverify_class\x18\x13 \x03(\x0b\x32\x31.perfetto.protos.AndroidStartupMetric.VerifyClass\x12\x13\n\x0b\x64lopen_file\x18\x14 \x03(\t\x12$\n\x1cstartup_concurrent_to_launch\x18\x12 \x03(\t\x12G\n\x0csystem_state\x18\x0f \x01(\x0b\x32\x31.perfetto.protos.AndroidStartupMetric.SystemState\x12\x19\n\x11slow_start_reason\x18\x11 \x03(\t\x12\x61\n\x1aslow_start_reason_detailed\x18\x15 \x03(\x0b\x32=.perfetto.protos.AndroidStartupMetric.SlowStartReasonDetailed\x12]\n\x1eslow_start_reason_with_details\x18\x18 \x03(\x0b\x32\x35.perfetto.protos.AndroidStartupMetric.SlowStartReasonJ\x04\x08\n\x10\x0b')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.android.startup_metric_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANDROIDSTARTUPMETRIC_SYSTEMSTATE'].fields_by_name['dex2oat_running']._loaded_options = None
  _globals['_ANDROIDSTARTUPMETRIC_SYSTEMSTATE'].fields_by_name['dex2oat_running']._serialized_options = b'\030\001'
  _globals['_ANDROIDSTARTUPMETRIC_SYSTEMSTATE'].fields_by_name['installd_running']._loaded_options = None
  _globals['_ANDROIDSTARTUPMETRIC_SYSTEMSTATE'].fields_by_name['installd_running']._serialized_options = b'\030\001'
  _globals['_ANDROIDSTARTUPMETRIC']._serialized_start=130
  _globals['_ANDROIDSTARTUPMETRIC']._serialized_end=7506
  _globals['_ANDROIDSTARTUPMETRIC_TASKSTATEBREAKDOWN']._serialized_start=219
  _globals['_ANDROIDSTARTUPMETRIC_TASKSTATEBREAKDOWN']._serialized_end=448
  _globals['_ANDROIDSTARTUPMETRIC_MCYCLESBYCORETYPE']._serialized_start=450
  _globals['_ANDROIDSTARTUPMETRIC_MCYCLESBYCORETYPE']._serialized_end=531
  _globals['_ANDROIDSTARTUPMETRIC_SLICE']._serialized_start=533
  _globals['_ANDROIDSTARTUPMETRIC_SLICE']._serialized_end=572
  _globals['_ANDROIDSTARTUPMETRIC_TOFIRSTFRAME']._serialized_start=575
  _globals['_ANDROIDSTARTUPMETRIC_TOFIRSTFRAME']._serialized_end=2898
  _globals['_ANDROIDSTARTUPMETRIC_HSCMETRICS']._serialized_start=2900
  _globals['_ANDROIDSTARTUPMETRIC_HSCMETRICS']._serialized_end=2979
  _globals['_ANDROIDSTARTUPMETRIC_ACTIVITY']._serialized_start=2981
  _globals['_ANDROIDSTARTUPMETRIC_ACTIVITY']._serialized_end=3052
  _globals['_ANDROIDSTARTUPMETRIC_BINDERTRANSACTION']._serialized_start=3055
  _globals['_ANDROIDSTARTUPMETRIC_BINDERTRANSACTION']._serialized_end=3258
  _globals['_ANDROIDSTARTUPMETRIC_OPTIMIZATIONSTATUS']._serialized_start=3261
  _globals['_ANDROIDSTARTUPMETRIC_OPTIMIZATIONSTATUS']._serialized_end=3393
  _globals['_ANDROIDSTARTUPMETRIC_VERIFYCLASS']._serialized_start=3395
  _globals['_ANDROIDSTARTUPMETRIC_VERIFYCLASS']._serialized_end=3438
  _globals['_ANDROIDSTARTUPMETRIC_EVENTTIMESTAMPS']._serialized_start=3440
  _globals['_ANDROIDSTARTUPMETRIC_EVENTTIMESTAMPS']._serialized_end=3503
  _globals['_ANDROIDSTARTUPMETRIC_SYSTEMSTATE']._serialized_start=3506
  _globals['_ANDROIDSTARTUPMETRIC_SYSTEMSTATE']._serialized_end=3739
  _globals['_ANDROIDSTARTUPMETRIC_SLOWSTARTREASONDETAILED']._serialized_start=3741
  _globals['_ANDROIDSTARTUPMETRIC_SLOWSTARTREASONDETAILED']._serialized_end=3799
  _globals['_ANDROIDSTARTUPMETRIC_SLOWSTARTREASON']._serialized_start=3802
  _globals['_ANDROIDSTARTUPMETRIC_SLOWSTARTREASON']._serialized_end=5328
  _globals['_ANDROIDSTARTUPMETRIC_SLOWSTARTREASON_REASONID']._serialized_start=4406
  _globals['_ANDROIDSTARTUPMETRIC_SLOWSTARTREASON_REASONID']._serialized_end=5251
  _globals['_ANDROIDSTARTUPMETRIC_SLOWSTARTREASON_SEVERITYLEVEL']._serialized_start=5253
  _globals['_ANDROIDSTARTUPMETRIC_SLOWSTARTREASON_SEVERITYLEVEL']._serialized_end=5328
  _globals['_ANDROIDSTARTUPMETRIC_THRESHOLDVALUE']._serialized_start=5331
  _globals['_ANDROIDSTARTUPMETRIC_THRESHOLDVALUE']._serialized_end=5572
  _globals['_ANDROIDSTARTUPMETRIC_THRESHOLDVALUE_THRESHOLDUNIT']._serialized_start=5471
  _globals['_ANDROIDSTARTUPMETRIC_THRESHOLDVALUE_THRESHOLDUNIT']._serialized_end=5572
  _globals['_ANDROIDSTARTUPMETRIC_ACTUALVALUE']._serialized_start=5574
  _globals['_ANDROIDSTARTUPMETRIC_ACTUALVALUE']._serialized_end=5615
  _globals['_ANDROIDSTARTUPMETRIC_TRACESLICESECTION']._serialized_start=5618
  _globals['_ANDROIDSTARTUPMETRIC_TRACESLICESECTION']._serialized_end=5764
  _globals['_ANDROIDSTARTUPMETRIC_TRACESLICESECTIONINFO']._serialized_start=5767
  _globals['_ANDROIDSTARTUPMETRIC_TRACESLICESECTIONINFO']._serialized_end=5918
  _globals['_ANDROIDSTARTUPMETRIC_TRACETHREADSECTION']._serialized_start=5921
  _globals['_ANDROIDSTARTUPMETRIC_TRACETHREADSECTION']._serialized_end=6072
  _globals['_ANDROIDSTARTUPMETRIC_TRACETHREADSECTIONINFO']._serialized_start=6075
  _globals['_ANDROIDSTARTUPMETRIC_TRACETHREADSECTIONINFO']._serialized_end=6229
  _globals['_ANDROIDSTARTUPMETRIC_STARTUP']._serialized_start=6232
  _globals['_ANDROIDSTARTUPMETRIC_STARTUP']._serialized_end=7506
# @@protoc_insertion_point(module_scope)
