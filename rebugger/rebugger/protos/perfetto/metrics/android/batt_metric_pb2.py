# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/android/batt_metric.proto
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
    'protos/perfetto/metrics/android/batt_metric.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1protos/perfetto/metrics/android/batt_metric.proto\x12\x0fperfetto.protos\"\x93\x06\n\x14\x41ndroidBatteryMetric\x12O\n\x10\x62\x61ttery_counters\x18\x01 \x03(\x0b\x32\x35.perfetto.protos.AndroidBatteryMetric.BatteryCounters\x12S\n\x12\x62\x61ttery_aggregates\x18\x02 \x01(\x0b\x32\x37.perfetto.protos.AndroidBatteryMetric.BatteryAggregates\x12K\n\x0esuspend_period\x18\x03 \x03(\x0b\x32\x33.perfetto.protos.AndroidBatteryMetric.SuspendPeriod\x1a\x9d\x01\n\x0f\x42\x61tteryCounters\x12\x14\n\x0ctimestamp_ns\x18\x01 \x01(\x03\x12\x1a\n\x12\x63harge_counter_uah\x18\x02 \x01(\x01\x12\x18\n\x10\x63\x61pacity_percent\x18\x03 \x01(\x02\x12\x12\n\ncurrent_ua\x18\x04 \x01(\x01\x12\x16\n\x0e\x63urrent_avg_ua\x18\x05 \x01(\x01\x12\x12\n\nvoltage_uv\x18\x06 \x01(\x01\x1a\xab\x02\n\x11\x42\x61tteryAggregates\x12\x1b\n\x13total_screen_off_ns\x18\x01 \x01(\x03\x12\x1a\n\x12total_screen_on_ns\x18\x02 \x01(\x03\x12\x1c\n\x14total_screen_doze_ns\x18\x03 \x01(\x03\x12\x19\n\x11total_wakelock_ns\x18\x04 \x01(\x03\x12\x10\n\x08sleep_ns\x18\x05 \x01(\x03\x12\x1b\n\x13sleep_screen_off_ns\x18\x06 \x01(\x03\x12\x1a\n\x12sleep_screen_on_ns\x18\x07 \x01(\x03\x12\x1c\n\x14sleep_screen_doze_ns\x18\x08 \x01(\x03\x12\x14\n\x0c\x61vg_power_mw\x18\t \x01(\x01\x12%\n\x1d\x61vg_power_from_charge_diff_mw\x18\n \x01(\x01\x1a:\n\rSuspendPeriod\x12\x14\n\x0ctimestamp_ns\x18\x01 \x01(\x03\x12\x13\n\x0b\x64uration_ns\x18\x02 \x01(\x03')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.android.batt_metric_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANDROIDBATTERYMETRIC']._serialized_start=71
  _globals['_ANDROIDBATTERYMETRIC']._serialized_end=858
  _globals['_ANDROIDBATTERYMETRIC_BATTERYCOUNTERS']._serialized_start=339
  _globals['_ANDROIDBATTERYMETRIC_BATTERYCOUNTERS']._serialized_end=496
  _globals['_ANDROIDBATTERYMETRIC_BATTERYAGGREGATES']._serialized_start=499
  _globals['_ANDROIDBATTERYMETRIC_BATTERYAGGREGATES']._serialized_end=798
  _globals['_ANDROIDBATTERYMETRIC_SUSPENDPERIOD']._serialized_start=800
  _globals['_ANDROIDBATTERYMETRIC_SUSPENDPERIOD']._serialized_end=858
# @@protoc_insertion_point(module_scope)