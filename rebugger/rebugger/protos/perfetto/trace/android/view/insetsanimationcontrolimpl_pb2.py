# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/android/view/insetsanimationcontrolimpl.proto
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
    'protos/perfetto/trace/android/view/insetsanimationcontrolimpl.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nCprotos/perfetto/trace/android/view/insetsanimationcontrolimpl.proto\x12\x0fperfetto.protos\"\xd9\x01\n\x1fInsetsAnimationControlImplProto\x12\x14\n\x0cis_cancelled\x18\x01 \x01(\x08\x12\x13\n\x0bis_finished\x18\x02 \x01(\x08\x12\x12\n\ntmp_matrix\x18\x03 \x01(\t\x12\x16\n\x0epending_insets\x18\x04 \x01(\t\x12\x18\n\x10pending_fraction\x18\x05 \x01(\x02\x12\x17\n\x0fshown_on_finish\x18\x06 \x01(\x08\x12\x15\n\rcurrent_alpha\x18\x07 \x01(\x02\x12\x15\n\rpending_alpha\x18\x08 \x01(\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.android.view.insetsanimationcontrolimpl_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_INSETSANIMATIONCONTROLIMPLPROTO']._serialized_start=89
  _globals['_INSETSANIMATIONCONTROLIMPLPROTO']._serialized_end=306
# @@protoc_insertion_point(module_scope)
