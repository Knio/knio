# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/common/observable_events.proto
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
    'protos/perfetto/common/observable_events.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.protos/perfetto/common/observable_events.proto\x12\x0fperfetto.protos\"\xf2\x05\n\x10ObservableEvents\x12_\n\x16instance_state_changes\x18\x01 \x03(\x0b\x32?.perfetto.protos.ObservableEvents.DataSourceInstanceStateChange\x12 \n\x18\x61ll_data_sources_started\x18\x02 \x01(\x08\x12L\n\x11\x63lone_trigger_hit\x18\x03 \x01(\x0b\x32\x31.perfetto.protos.ObservableEvents.CloneTriggerHit\x1a\x9a\x01\n\x1d\x44\x61taSourceInstanceStateChange\x12\x15\n\rproducer_name\x18\x01 \x01(\t\x12\x18\n\x10\x64\x61ta_source_name\x18\x02 \x01(\t\x12H\n\x05state\x18\x03 \x01(\x0e\x32\x39.perfetto.protos.ObservableEvents.DataSourceInstanceState\x1a\x86\x01\n\x0f\x43loneTriggerHit\x12\x1a\n\x12tracing_session_id\x18\x01 \x01(\x03\x12\x14\n\x0ctrigger_name\x18\x02 \x01(\t\x12\x15\n\rproducer_name\x18\x03 \x01(\t\x12\x14\n\x0cproducer_uid\x18\x04 \x01(\r\x12\x14\n\x0c\x62oot_time_ns\x18\x05 \x01(\x04\"|\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x1f\n\x1bTYPE_DATA_SOURCES_INSTANCES\x10\x01\x12!\n\x1dTYPE_ALL_DATA_SOURCES_STARTED\x10\x02\x12\x1a\n\x16TYPE_CLONE_TRIGGER_HIT\x10\x04\"i\n\x17\x44\x61taSourceInstanceState\x12&\n\"DATA_SOURCE_INSTANCE_STATE_STOPPED\x10\x01\x12&\n\"DATA_SOURCE_INSTANCE_STATE_STARTED\x10\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.common.observable_events_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_OBSERVABLEEVENTS']._serialized_start=68
  _globals['_OBSERVABLEEVENTS']._serialized_end=822
  _globals['_OBSERVABLEEVENTS_DATASOURCEINSTANCESTATECHANGE']._serialized_start=298
  _globals['_OBSERVABLEEVENTS_DATASOURCEINSTANCESTATECHANGE']._serialized_end=452
  _globals['_OBSERVABLEEVENTS_CLONETRIGGERHIT']._serialized_start=455
  _globals['_OBSERVABLEEVENTS_CLONETRIGGERHIT']._serialized_end=589
  _globals['_OBSERVABLEEVENTS_TYPE']._serialized_start=591
  _globals['_OBSERVABLEEVENTS_TYPE']._serialized_end=715
  _globals['_OBSERVABLEEVENTS_DATASOURCEINSTANCESTATE']._serialized_start=717
  _globals['_OBSERVABLEEVENTS_DATASOURCEINSTANCESTATE']._serialized_end=822
# @@protoc_insertion_point(module_scope)
