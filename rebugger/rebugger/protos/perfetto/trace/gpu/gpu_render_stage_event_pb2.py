# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/gpu/gpu_render_stage_event.proto
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
    'protos/perfetto/trace/gpu/gpu_render_stage_event.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6protos/perfetto/trace/gpu/gpu_render_stage_event.proto\x12\x0fperfetto.protos\"\xf6\x06\n\x13GpuRenderStageEvent\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\x04\x12\x10\n\x08\x64uration\x18\x02 \x01(\x04\x12\x14\n\x0chw_queue_iid\x18\r \x01(\x04\x12\x11\n\tstage_iid\x18\x0e \x01(\x04\x12\x0e\n\x06gpu_id\x18\x0b \x01(\x05\x12\x0f\n\x07\x63ontext\x18\x05 \x01(\x04\x12\x1c\n\x14render_target_handle\x18\x08 \x01(\x04\x12\x15\n\rsubmission_id\x18\n \x01(\r\x12\x42\n\nextra_data\x18\x06 \x03(\x0b\x32..perfetto.protos.GpuRenderStageEvent.ExtraData\x12\x1a\n\x12render_pass_handle\x18\t \x01(\x04\x12!\n\x19render_subpass_index_mask\x18\x0f \x03(\x04\x12\x1d\n\x15\x63ommand_buffer_handle\x18\x0c \x01(\x04\x12O\n\x0especifications\x18\x07 \x01(\x0b\x32\x33.perfetto.protos.GpuRenderStageEvent.SpecificationsB\x02\x18\x01\x12\x17\n\x0bhw_queue_id\x18\x03 \x01(\x05\x42\x02\x18\x01\x12\x14\n\x08stage_id\x18\x04 \x01(\x05\x42\x02\x18\x01\x1a(\n\tExtraData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x1a\xe9\x02\n\x0eSpecifications\x12U\n\x0c\x63ontext_spec\x18\x01 \x01(\x0b\x32?.perfetto.protos.GpuRenderStageEvent.Specifications.ContextSpec\x12Q\n\x08hw_queue\x18\x02 \x03(\x0b\x32?.perfetto.protos.GpuRenderStageEvent.Specifications.Description\x12N\n\x05stage\x18\x03 \x03(\x0b\x32?.perfetto.protos.GpuRenderStageEvent.Specifications.Description\x1a+\n\x0b\x43ontextSpec\x12\x0f\n\x07\x63ontext\x18\x01 \x01(\x04\x12\x0b\n\x03pid\x18\x02 \x01(\x05\x1a\x30\n\x0b\x44\x65scription\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t*\x04\x08\x64\x10\x65\"\xaa\x01\n\x17InternedGraphicsContext\x12\x0b\n\x03iid\x18\x01 \x01(\x04\x12\x0b\n\x03pid\x18\x02 \x01(\x05\x12\x39\n\x03\x61pi\x18\x03 \x01(\x0e\x32,.perfetto.protos.InternedGraphicsContext.Api\":\n\x03\x41pi\x12\r\n\tUNDEFINED\x10\x00\x12\x0b\n\x07OPEN_GL\x10\x01\x12\n\n\x06VULKAN\x10\x02\x12\x0b\n\x07OPEN_CL\x10\x03\"\xee\x01\n#InternedGpuRenderStageSpecification\x12\x0b\n\x03iid\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12Z\n\x08\x63\x61tegory\x18\x04 \x01(\x0e\x32H.perfetto.protos.InternedGpuRenderStageSpecification.RenderStageCategory\";\n\x13RenderStageCategory\x12\t\n\x05OTHER\x10\x00\x12\x0c\n\x08GRAPHICS\x10\x01\x12\x0b\n\x07\x43OMPUTE\x10\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.gpu.gpu_render_stage_event_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GPURENDERSTAGEEVENT'].fields_by_name['specifications']._loaded_options = None
  _globals['_GPURENDERSTAGEEVENT'].fields_by_name['specifications']._serialized_options = b'\030\001'
  _globals['_GPURENDERSTAGEEVENT'].fields_by_name['hw_queue_id']._loaded_options = None
  _globals['_GPURENDERSTAGEEVENT'].fields_by_name['hw_queue_id']._serialized_options = b'\030\001'
  _globals['_GPURENDERSTAGEEVENT'].fields_by_name['stage_id']._loaded_options = None
  _globals['_GPURENDERSTAGEEVENT'].fields_by_name['stage_id']._serialized_options = b'\030\001'
  _globals['_GPURENDERSTAGEEVENT']._serialized_start=76
  _globals['_GPURENDERSTAGEEVENT']._serialized_end=962
  _globals['_GPURENDERSTAGEEVENT_EXTRADATA']._serialized_start=552
  _globals['_GPURENDERSTAGEEVENT_EXTRADATA']._serialized_end=592
  _globals['_GPURENDERSTAGEEVENT_SPECIFICATIONS']._serialized_start=595
  _globals['_GPURENDERSTAGEEVENT_SPECIFICATIONS']._serialized_end=956
  _globals['_GPURENDERSTAGEEVENT_SPECIFICATIONS_CONTEXTSPEC']._serialized_start=863
  _globals['_GPURENDERSTAGEEVENT_SPECIFICATIONS_CONTEXTSPEC']._serialized_end=906
  _globals['_GPURENDERSTAGEEVENT_SPECIFICATIONS_DESCRIPTION']._serialized_start=908
  _globals['_GPURENDERSTAGEEVENT_SPECIFICATIONS_DESCRIPTION']._serialized_end=956
  _globals['_INTERNEDGRAPHICSCONTEXT']._serialized_start=965
  _globals['_INTERNEDGRAPHICSCONTEXT']._serialized_end=1135
  _globals['_INTERNEDGRAPHICSCONTEXT_API']._serialized_start=1077
  _globals['_INTERNEDGRAPHICSCONTEXT_API']._serialized_end=1135
  _globals['_INTERNEDGPURENDERSTAGESPECIFICATION']._serialized_start=1138
  _globals['_INTERNEDGPURENDERSTAGESPECIFICATION']._serialized_end=1376
  _globals['_INTERNEDGPURENDERSTAGESPECIFICATION_RENDERSTAGECATEGORY']._serialized_start=1317
  _globals['_INTERNEDGPURENDERSTAGESPECIFICATION_RENDERSTAGECATEGORY']._serialized_end=1376
# @@protoc_insertion_point(module_scope)
