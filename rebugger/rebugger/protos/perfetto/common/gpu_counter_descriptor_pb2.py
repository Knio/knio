# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/common/gpu_counter_descriptor.proto
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
    'protos/perfetto/common/gpu_counter_descriptor.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3protos/perfetto/common/gpu_counter_descriptor.proto\x12\x0fperfetto.protos\"\xb6\x0b\n\x14GpuCounterDescriptor\x12\x43\n\x05specs\x18\x01 \x03(\x0b\x32\x34.perfetto.protos.GpuCounterDescriptor.GpuCounterSpec\x12\x45\n\x06\x62locks\x18\x02 \x03(\x0b\x32\x35.perfetto.protos.GpuCounterDescriptor.GpuCounterBlock\x12\x1e\n\x16min_sampling_period_ns\x18\x03 \x01(\x04\x12\x1e\n\x16max_sampling_period_ns\x18\x04 \x01(\x04\x12&\n\x1esupports_instrumented_sampling\x18\x05 \x01(\x08\x1a\x8e\x03\n\x0eGpuCounterSpec\x12\x12\n\ncounter_id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x18\n\x0eint_peak_value\x18\x05 \x01(\x03H\x00\x12\x1b\n\x11\x64ouble_peak_value\x18\x06 \x01(\x01H\x00\x12J\n\x0fnumerator_units\x18\x07 \x03(\x0e\x32\x31.perfetto.protos.GpuCounterDescriptor.MeasureUnit\x12L\n\x11\x64\x65nominator_units\x18\x08 \x03(\x0e\x32\x31.perfetto.protos.GpuCounterDescriptor.MeasureUnit\x12\x19\n\x11select_by_default\x18\t \x01(\x08\x12\x45\n\x06groups\x18\n \x03(\x0e\x32\x35.perfetto.protos.GpuCounterDescriptor.GpuCounterGroupB\x0c\n\npeak_valueJ\x04\x08\x04\x10\x05\x1as\n\x0fGpuCounterBlock\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\r\x12\x16\n\x0e\x62lock_capacity\x18\x02 \x01(\r\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x13\n\x0b\x63ounter_ids\x18\x05 \x03(\r\"u\n\x0fGpuCounterGroup\x12\x10\n\x0cUNCLASSIFIED\x10\x00\x12\n\n\x06SYSTEM\x10\x01\x12\x0c\n\x08VERTICES\x10\x02\x12\r\n\tFRAGMENTS\x10\x03\x12\x0e\n\nPRIMITIVES\x10\x04\x12\n\n\x06MEMORY\x10\x05\x12\x0b\n\x07\x43OMPUTE\x10\x06\"\xac\x04\n\x0bMeasureUnit\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03\x42IT\x10\x01\x12\x0b\n\x07KILOBIT\x10\x02\x12\x0b\n\x07MEGABIT\x10\x03\x12\x0b\n\x07GIGABIT\x10\x04\x12\x0b\n\x07TERABIT\x10\x05\x12\x0b\n\x07PETABIT\x10\x06\x12\x08\n\x04\x42YTE\x10\x07\x12\x0c\n\x08KILOBYTE\x10\x08\x12\x0c\n\x08MEGABYTE\x10\t\x12\x0c\n\x08GIGABYTE\x10\n\x12\x0c\n\x08TERABYTE\x10\x0b\x12\x0c\n\x08PETABYTE\x10\x0c\x12\t\n\x05HERTZ\x10\r\x12\r\n\tKILOHERTZ\x10\x0e\x12\r\n\tMEGAHERTZ\x10\x0f\x12\r\n\tGIGAHERTZ\x10\x10\x12\r\n\tTERAHERTZ\x10\x11\x12\r\n\tPETAHERTZ\x10\x12\x12\x0e\n\nNANOSECOND\x10\x13\x12\x0f\n\x0bMICROSECOND\x10\x14\x12\x0f\n\x0bMILLISECOND\x10\x15\x12\n\n\x06SECOND\x10\x16\x12\n\n\x06MINUTE\x10\x17\x12\x08\n\x04HOUR\x10\x18\x12\n\n\x06VERTEX\x10\x19\x12\t\n\x05PIXEL\x10\x1a\x12\x0c\n\x08TRIANGLE\x10\x1b\x12\r\n\tPRIMITIVE\x10&\x12\x0c\n\x08\x46RAGMENT\x10\'\x12\r\n\tMILLIWATT\x10\x1c\x12\x08\n\x04WATT\x10\x1d\x12\x0c\n\x08KILOWATT\x10\x1e\x12\t\n\x05JOULE\x10\x1f\x12\x08\n\x04VOLT\x10 \x12\n\n\x06\x41MPERE\x10!\x12\x0b\n\x07\x43\x45LSIUS\x10\"\x12\x0e\n\nFAHRENHEIT\x10#\x12\n\n\x06KELVIN\x10$\x12\x0b\n\x07PERCENT\x10%\x12\x0f\n\x0bINSTRUCTION\x10(')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.common.gpu_counter_descriptor_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GPUCOUNTERDESCRIPTOR']._serialized_start=73
  _globals['_GPUCOUNTERDESCRIPTOR']._serialized_end=1535
  _globals['_GPUCOUNTERDESCRIPTOR_GPUCOUNTERSPEC']._serialized_start=342
  _globals['_GPUCOUNTERDESCRIPTOR_GPUCOUNTERSPEC']._serialized_end=740
  _globals['_GPUCOUNTERDESCRIPTOR_GPUCOUNTERBLOCK']._serialized_start=742
  _globals['_GPUCOUNTERDESCRIPTOR_GPUCOUNTERBLOCK']._serialized_end=857
  _globals['_GPUCOUNTERDESCRIPTOR_GPUCOUNTERGROUP']._serialized_start=859
  _globals['_GPUCOUNTERDESCRIPTOR_GPUCOUNTERGROUP']._serialized_end=976
  _globals['_GPUCOUNTERDESCRIPTOR_MEASUREUNIT']._serialized_start=979
  _globals['_GPUCOUNTERDESCRIPTOR_MEASUREUNIT']._serialized_end=1535
# @@protoc_insertion_point(module_scope)
