# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/metrics/android/android_garbage_collection_unagg_metric.proto
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
    'protos/perfetto/metrics/android/android_garbage_collection_unagg_metric.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nMprotos/perfetto/metrics/android/android_garbage_collection_unagg_metric.proto\x12\x0fperfetto.protos\"\xc2\x04\n#AndroidGarbageCollectionUnaggMetric\x12^\n\tgc_events\x18\x01 \x03(\x0b\x32K.perfetto.protos.AndroidGarbageCollectionUnaggMetric.GarbageCollectionEvent\x1a\xba\x03\n\x16GarbageCollectionEvent\x12\x13\n\x0bthread_name\x18\x01 \x01(\t\x12\x14\n\x0cprocess_name\x18\x02 \x01(\t\x12\x0f\n\x07gc_type\x18\x03 \x01(\t\x12\x17\n\x0fis_mark_compact\x18\x04 \x01(\x03\x12\x14\n\x0creclaimed_mb\x18\x05 \x01(\x01\x12\x13\n\x0bmin_heap_mb\x18\x06 \x01(\x01\x12\x13\n\x0bmax_heap_mb\x18\x07 \x01(\x01\x12\x1f\n\x17mb_per_ms_of_running_gc\x18\x08 \x01(\x01\x12\x1c\n\x14mb_per_ms_of_wall_gc\x18\t \x01(\x01\x12\x0e\n\x06gc_dur\x18\n \x01(\x03\x12\x16\n\x0egc_running_dur\x18\x0b \x01(\x03\x12\x17\n\x0fgc_runnable_dur\x18\x0c \x01(\x03\x12\x17\n\x0fgc_unint_io_dur\x18\r \x01(\x03\x12\x1b\n\x13gc_unint_non_io_dur\x18\x0e \x01(\x03\x12\x12\n\ngc_int_dur\x18\x0f \x01(\x03\x12\r\n\x05gc_ts\x18\x10 \x01(\x03\x12\x0b\n\x03pid\x18\x11 \x01(\x03\x12\x0b\n\x03tid\x18\x12 \x01(\x03\x12\x18\n\x10gc_monotonic_dur\x18\x13 \x01(\x03')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.metrics.android.android_garbage_collection_unagg_metric_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANDROIDGARBAGECOLLECTIONUNAGGMETRIC']._serialized_start=99
  _globals['_ANDROIDGARBAGECOLLECTIONUNAGGMETRIC']._serialized_end=677
  _globals['_ANDROIDGARBAGECOLLECTIONUNAGGMETRIC_GARBAGECOLLECTIONEVENT']._serialized_start=235
  _globals['_ANDROIDGARBAGECOLLECTIONUNAGGMETRIC_GARBAGECOLLECTIONEVENT']._serialized_end=677
# @@protoc_insertion_point(module_scope)