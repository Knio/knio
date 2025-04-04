# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/trace/track_event/chrome_latency_info.proto
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
    'protos/perfetto/trace/track_event/chrome_latency_info.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;protos/perfetto/trace/track_event/chrome_latency_info.proto\x12\x0fperfetto.protos\"\xf6\r\n\x11\x43hromeLatencyInfo\x12\x10\n\x08trace_id\x18\x01 \x01(\x03\x12\x35\n\x04step\x18\x02 \x01(\x0e\x32\'.perfetto.protos.ChromeLatencyInfo.Step\x12\x1a\n\x12\x66rame_tree_node_id\x18\x03 \x01(\x05\x12H\n\x0e\x63omponent_info\x18\x04 \x03(\x0b\x32\x30.perfetto.protos.ChromeLatencyInfo.ComponentInfo\x12\x14\n\x0cis_coalesced\x18\x05 \x01(\x08\x12\x19\n\x11gesture_scroll_id\x18\x06 \x01(\x03\x12\x10\n\x08touch_id\x18\x07 \x01(\x03\x12@\n\ninput_type\x18\x08 \x01(\x0e\x32,.perfetto.protos.ChromeLatencyInfo.InputType\x1aq\n\rComponentInfo\x12O\n\x0e\x63omponent_type\x18\x01 \x01(\x0e\x32\x37.perfetto.protos.ChromeLatencyInfo.LatencyComponentType\x12\x0f\n\x07time_us\x18\x02 \x01(\x04\"\x92\x03\n\x04Step\x12\x14\n\x10STEP_UNSPECIFIED\x10\x00\x12\x1c\n\x18STEP_SEND_INPUT_EVENT_UI\x10\x03\x12 \n\x1cSTEP_HANDLE_INPUT_EVENT_IMPL\x10\x05\x12(\n$STEP_DID_HANDLE_INPUT_AND_OVERSCROLL\x10\x08\x12 \n\x1cSTEP_HANDLE_INPUT_EVENT_MAIN\x10\x04\x12\"\n\x1eSTEP_MAIN_THREAD_SCROLL_UPDATE\x10\x02\x12\'\n#STEP_HANDLE_INPUT_EVENT_MAIN_COMMIT\x10\x01\x12)\n%STEP_HANDLED_INPUT_EVENT_MAIN_OR_IMPL\x10\t\x12!\n\x1dSTEP_HANDLED_INPUT_EVENT_IMPL\x10\n\x12\x15\n\x11STEP_SWAP_BUFFERS\x10\x06\x12\x16\n\x12STEP_DRAW_AND_SWAP\x10\x07\x12\x1e\n\x1aSTEP_FINISHED_SWAP_BUFFERS\x10\x0b\"\xf5\x05\n\x14LatencyComponentType\x12\x19\n\x15\x43OMPONENT_UNSPECIFIED\x10\x00\x12+\n\'COMPONENT_INPUT_EVENT_LATENCY_BEGIN_RWH\x10\x01\x12\x38\n4COMPONENT_INPUT_EVENT_LATENCY_SCROLL_UPDATE_ORIGINAL\x10\x02\x12>\n:COMPONENT_INPUT_EVENT_LATENCY_FIRST_SCROLL_UPDATE_ORIGINAL\x10\x03\x12*\n&COMPONENT_INPUT_EVENT_LATENCY_ORIGINAL\x10\x04\x12$\n COMPONENT_INPUT_EVENT_LATENCY_UI\x10\x05\x12/\n+COMPONENT_INPUT_EVENT_LATENCY_RENDERER_MAIN\x10\x06\x12:\n6COMPONENT_INPUT_EVENT_LATENCY_RENDERING_SCHEDULED_MAIN\x10\x07\x12:\n6COMPONENT_INPUT_EVENT_LATENCY_RENDERING_SCHEDULED_IMPL\x10\x08\x12:\n6COMPONENT_INPUT_EVENT_LATENCY_SCROLL_UPDATE_LAST_EVENT\x10\t\x12)\n%COMPONENT_INPUT_EVENT_LATENCY_ACK_RWH\x10\n\x12/\n+COMPONENT_INPUT_EVENT_LATENCY_RENDERER_SWAP\x10\x0b\x12/\n+COMPONENT_DISPLAY_COMPOSITOR_RECEIVED_FRAME\x10\x0c\x12)\n%COMPONENT_INPUT_EVENT_GPU_SWAP_BUFFER\x10\r\x12,\n(COMPONENT_INPUT_EVENT_LATENCY_FRAME_SWAP\x10\x0e\"\xac\x01\n\tInputType\x12\x18\n\x14UNSPECIFIED_OR_OTHER\x10\x00\x12\x0f\n\x0bTOUCH_MOVED\x10\x01\x12\x18\n\x14GESTURE_SCROLL_BEGIN\x10\x02\x12\x19\n\x15GESTURE_SCROLL_UPDATE\x10\x03\x12\x16\n\x12GESTURE_SCROLL_END\x10\x04\x12\x0f\n\x0bGESTURE_TAP\x10\x05\x12\x16\n\x12GESTURE_TAP_CANCEL\x10\x06')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.trace.track_event.chrome_latency_info_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CHROMELATENCYINFO']._serialized_start=81
  _globals['_CHROMELATENCYINFO']._serialized_end=1863
  _globals['_CHROMELATENCYINFO_COMPONENTINFO']._serialized_start=410
  _globals['_CHROMELATENCYINFO_COMPONENTINFO']._serialized_end=523
  _globals['_CHROMELATENCYINFO_STEP']._serialized_start=526
  _globals['_CHROMELATENCYINFO_STEP']._serialized_end=928
  _globals['_CHROMELATENCYINFO_LATENCYCOMPONENTTYPE']._serialized_start=931
  _globals['_CHROMELATENCYINFO_LATENCYCOMPONENTTYPE']._serialized_end=1688
  _globals['_CHROMELATENCYINFO_INPUTTYPE']._serialized_start=1691
  _globals['_CHROMELATENCYINFO_INPUTTYPE']._serialized_end=1863
# @@protoc_insertion_point(module_scope)
