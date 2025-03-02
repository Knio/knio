# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/android/wattson_in_time_period.proto
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
    'protos/perfetto/metrics/android/wattson_in_time_period.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<protos/perfetto/metrics/android/wattson_in_time_period.proto\x12\x0fperfetto.protos\"\x97\x01\n\x1e\x41ndroidWattsonTimePeriodMetric\x12\x16\n\x0emetric_version\x18\x01 \x01(\x05\x12\x1b\n\x13power_model_version\x18\x02 \x01(\x05\x12@\n\x0bperiod_info\x18\x03 \x03(\x0b\x32+.perfetto.protos.AndroidWattsonEstimateInfo\"\x8f\x01\n\x1a\x41ndroidWattsonEstimateInfo\x12\x11\n\tperiod_id\x18\x01 \x01(\x05\x12\x12\n\nperiod_dur\x18\x02 \x01(\x03\x12J\n\rcpu_subsystem\x18\x03 \x01(\x0b\x32\x33.perfetto.protos.AndroidWattsonCpuSubsystemEstimate\"\x91\x05\n\"AndroidWattsonCpuSubsystemEstimate\x12\x14\n\x0c\x65stimated_mw\x18\x01 \x01(\x02\x12\x15\n\restimated_mws\x18\x02 \x01(\x02\x12>\n\x07policy0\x18\x03 \x01(\x0b\x32-.perfetto.protos.AndroidWattsonPolicyEstimate\x12>\n\x07policy1\x18\x04 \x01(\x0b\x32-.perfetto.protos.AndroidWattsonPolicyEstimate\x12>\n\x07policy2\x18\x05 \x01(\x0b\x32-.perfetto.protos.AndroidWattsonPolicyEstimate\x12>\n\x07policy3\x18\x06 \x01(\x0b\x32-.perfetto.protos.AndroidWattsonPolicyEstimate\x12>\n\x07policy4\x18\x07 \x01(\x0b\x32-.perfetto.protos.AndroidWattsonPolicyEstimate\x12>\n\x07policy5\x18\x08 \x01(\x0b\x32-.perfetto.protos.AndroidWattsonPolicyEstimate\x12>\n\x07policy6\x18\t \x01(\x0b\x32-.perfetto.protos.AndroidWattsonPolicyEstimate\x12>\n\x07policy7\x18\n \x01(\x0b\x32-.perfetto.protos.AndroidWattsonPolicyEstimate\x12>\n\x07\x64su_scu\x18\x0b \x01(\x0b\x32-.perfetto.protos.AndroidWattsonDsuScuEstimate\"\x9b\x04\n\x1c\x41ndroidWattsonPolicyEstimate\x12\x14\n\x0c\x65stimated_mw\x18\x01 \x01(\x02\x12\x15\n\restimated_mws\x18\x02 \x01(\x02\x12\x38\n\x04\x63pu0\x18\x03 \x01(\x0b\x32*.perfetto.protos.AndroidWattsonCpuEstimate\x12\x38\n\x04\x63pu1\x18\x04 \x01(\x0b\x32*.perfetto.protos.AndroidWattsonCpuEstimate\x12\x38\n\x04\x63pu2\x18\x05 \x01(\x0b\x32*.perfetto.protos.AndroidWattsonCpuEstimate\x12\x38\n\x04\x63pu3\x18\x06 \x01(\x0b\x32*.perfetto.protos.AndroidWattsonCpuEstimate\x12\x38\n\x04\x63pu4\x18\x07 \x01(\x0b\x32*.perfetto.protos.AndroidWattsonCpuEstimate\x12\x38\n\x04\x63pu5\x18\x08 \x01(\x0b\x32*.perfetto.protos.AndroidWattsonCpuEstimate\x12\x38\n\x04\x63pu6\x18\t \x01(\x0b\x32*.perfetto.protos.AndroidWattsonCpuEstimate\x12\x38\n\x04\x63pu7\x18\n \x01(\x0b\x32*.perfetto.protos.AndroidWattsonCpuEstimate\"H\n\x19\x41ndroidWattsonCpuEstimate\x12\x14\n\x0c\x65stimated_mw\x18\x01 \x01(\x02\x12\x15\n\restimated_mws\x18\x02 \x01(\x02\"K\n\x1c\x41ndroidWattsonDsuScuEstimate\x12\x14\n\x0c\x65stimated_mw\x18\x01 \x01(\x02\x12\x15\n\restimated_mws\x18\x02 \x01(\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.android.wattson_in_time_period_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANDROIDWATTSONTIMEPERIODMETRIC']._serialized_start=82
  _globals['_ANDROIDWATTSONTIMEPERIODMETRIC']._serialized_end=233
  _globals['_ANDROIDWATTSONESTIMATEINFO']._serialized_start=236
  _globals['_ANDROIDWATTSONESTIMATEINFO']._serialized_end=379
  _globals['_ANDROIDWATTSONCPUSUBSYSTEMESTIMATE']._serialized_start=382
  _globals['_ANDROIDWATTSONCPUSUBSYSTEMESTIMATE']._serialized_end=1039
  _globals['_ANDROIDWATTSONPOLICYESTIMATE']._serialized_start=1042
  _globals['_ANDROIDWATTSONPOLICYESTIMATE']._serialized_end=1581
  _globals['_ANDROIDWATTSONCPUESTIMATE']._serialized_start=1583
  _globals['_ANDROIDWATTSONCPUESTIMATE']._serialized_end=1655
  _globals['_ANDROIDWATTSONDSUSCUESTIMATE']._serialized_start=1657
  _globals['_ANDROIDWATTSONDSUSCUESTIMATE']._serialized_end=1732
# @@protoc_insertion_point(module_scope)
