# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/common/descriptor.proto
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
    'protos/perfetto/common/descriptor.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'protos/perfetto/common/descriptor.proto\x12\x0fperfetto.protos\"G\n\x11\x46ileDescriptorSet\x12\x32\n\x04\x66ile\x18\x01 \x03(\x0b\x32$.perfetto.protos.FileDescriptorProto\"\xbf\x02\n\x13\x46ileDescriptorProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07package\x18\x02 \x01(\t\x12\x12\n\ndependency\x18\x03 \x03(\t\x12\x19\n\x11public_dependency\x18\n \x03(\x05\x12\x17\n\x0fweak_dependency\x18\x0b \x03(\x05\x12\x36\n\x0cmessage_type\x18\x04 \x03(\x0b\x32 .perfetto.protos.DescriptorProto\x12\x37\n\tenum_type\x18\x05 \x03(\x0b\x32$.perfetto.protos.EnumDescriptorProto\x12\x38\n\textension\x18\x07 \x03(\x0b\x32%.perfetto.protos.FieldDescriptorProtoJ\x04\x08\x06\x10\x07J\x04\x08\x08\x10\tJ\x04\x08\t\x10\nJ\x04\x08\x0c\x10\r\"\xd2\x03\n\x0f\x44\x65scriptorProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x34\n\x05\x66ield\x18\x02 \x03(\x0b\x32%.perfetto.protos.FieldDescriptorProto\x12\x38\n\textension\x18\x06 \x03(\x0b\x32%.perfetto.protos.FieldDescriptorProto\x12\x35\n\x0bnested_type\x18\x03 \x03(\x0b\x32 .perfetto.protos.DescriptorProto\x12\x37\n\tenum_type\x18\x04 \x03(\x0b\x32$.perfetto.protos.EnumDescriptorProto\x12\x39\n\noneof_decl\x18\x08 \x03(\x0b\x32%.perfetto.protos.OneofDescriptorProto\x12\x46\n\x0ereserved_range\x18\t \x03(\x0b\x32..perfetto.protos.DescriptorProto.ReservedRange\x12\x15\n\rreserved_name\x18\n \x03(\t\x1a+\n\rReservedRange\x12\r\n\x05start\x18\x01 \x01(\x05\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x05J\x04\x08\x05\x10\x06J\x04\x08\x07\x10\x08\"\x9e\x02\n\x13UninterpretedOption\x12;\n\x04name\x18\x02 \x03(\x0b\x32-.perfetto.protos.UninterpretedOption.NamePart\x12\x18\n\x10identifier_value\x18\x03 \x01(\t\x12\x1a\n\x12positive_int_value\x18\x04 \x01(\x04\x12\x1a\n\x12negative_int_value\x18\x05 \x01(\x03\x12\x14\n\x0c\x64ouble_value\x18\x06 \x01(\x01\x12\x14\n\x0cstring_value\x18\x07 \x01(\x0c\x12\x17\n\x0f\x61ggregate_value\x18\x08 \x01(\t\x1a\x33\n\x08NamePart\x12\x11\n\tname_part\x18\x01 \x01(\t\x12\x14\n\x0cis_extension\x18\x02 \x01(\x08\"c\n\x0c\x46ieldOptions\x12\x0e\n\x06packed\x18\x02 \x01(\x08\x12\x43\n\x14uninterpreted_option\x18\xe7\x07 \x03(\x0b\x32$.perfetto.protos.UninterpretedOption\"\xaf\x05\n\x14\x46ieldDescriptorProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06number\x18\x03 \x01(\x05\x12:\n\x05label\x18\x04 \x01(\x0e\x32+.perfetto.protos.FieldDescriptorProto.Label\x12\x38\n\x04type\x18\x05 \x01(\x0e\x32*.perfetto.protos.FieldDescriptorProto.Type\x12\x11\n\ttype_name\x18\x06 \x01(\t\x12\x10\n\x08\x65xtendee\x18\x02 \x01(\t\x12\x15\n\rdefault_value\x18\x07 \x01(\t\x12.\n\x07options\x18\x08 \x01(\x0b\x32\x1d.perfetto.protos.FieldOptions\x12\x13\n\x0boneof_index\x18\t \x01(\x05\"\xb6\x02\n\x04Type\x12\x0f\n\x0bTYPE_DOUBLE\x10\x01\x12\x0e\n\nTYPE_FLOAT\x10\x02\x12\x0e\n\nTYPE_INT64\x10\x03\x12\x0f\n\x0bTYPE_UINT64\x10\x04\x12\x0e\n\nTYPE_INT32\x10\x05\x12\x10\n\x0cTYPE_FIXED64\x10\x06\x12\x10\n\x0cTYPE_FIXED32\x10\x07\x12\r\n\tTYPE_BOOL\x10\x08\x12\x0f\n\x0bTYPE_STRING\x10\t\x12\x0e\n\nTYPE_GROUP\x10\n\x12\x10\n\x0cTYPE_MESSAGE\x10\x0b\x12\x0e\n\nTYPE_BYTES\x10\x0c\x12\x0f\n\x0bTYPE_UINT32\x10\r\x12\r\n\tTYPE_ENUM\x10\x0e\x12\x11\n\rTYPE_SFIXED32\x10\x0f\x12\x11\n\rTYPE_SFIXED64\x10\x10\x12\x0f\n\x0bTYPE_SINT32\x10\x11\x12\x0f\n\x0bTYPE_SINT64\x10\x12\"C\n\x05Label\x12\x12\n\x0eLABEL_OPTIONAL\x10\x01\x12\x12\n\x0eLABEL_REQUIRED\x10\x02\x12\x12\n\x0eLABEL_REPEATED\x10\x03J\x04\x08\n\x10\x0b\"T\n\x14OneofDescriptorProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12.\n\x07options\x18\x02 \x01(\x0b\x32\x1d.perfetto.protos.OneofOptions\"\x80\x01\n\x13\x45numDescriptorProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x38\n\x05value\x18\x02 \x03(\x0b\x32).perfetto.protos.EnumValueDescriptorProto\x12\x15\n\rreserved_name\x18\x05 \x03(\tJ\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05\">\n\x18\x45numValueDescriptorProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06number\x18\x02 \x01(\x05J\x04\x08\x03\x10\x04\"!\n\x0cOneofOptions*\t\x08\xe8\x07\x10\x80\x80\x80\x80\x02J\x06\x08\xe7\x07\x10\xe8\x07')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.common.descriptor_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FILEDESCRIPTORSET']._serialized_start=60
  _globals['_FILEDESCRIPTORSET']._serialized_end=131
  _globals['_FILEDESCRIPTORPROTO']._serialized_start=134
  _globals['_FILEDESCRIPTORPROTO']._serialized_end=453
  _globals['_DESCRIPTORPROTO']._serialized_start=456
  _globals['_DESCRIPTORPROTO']._serialized_end=922
  _globals['_DESCRIPTORPROTO_RESERVEDRANGE']._serialized_start=867
  _globals['_DESCRIPTORPROTO_RESERVEDRANGE']._serialized_end=910
  _globals['_UNINTERPRETEDOPTION']._serialized_start=925
  _globals['_UNINTERPRETEDOPTION']._serialized_end=1211
  _globals['_UNINTERPRETEDOPTION_NAMEPART']._serialized_start=1160
  _globals['_UNINTERPRETEDOPTION_NAMEPART']._serialized_end=1211
  _globals['_FIELDOPTIONS']._serialized_start=1213
  _globals['_FIELDOPTIONS']._serialized_end=1312
  _globals['_FIELDDESCRIPTORPROTO']._serialized_start=1315
  _globals['_FIELDDESCRIPTORPROTO']._serialized_end=2002
  _globals['_FIELDDESCRIPTORPROTO_TYPE']._serialized_start=1617
  _globals['_FIELDDESCRIPTORPROTO_TYPE']._serialized_end=1927
  _globals['_FIELDDESCRIPTORPROTO_LABEL']._serialized_start=1929
  _globals['_FIELDDESCRIPTORPROTO_LABEL']._serialized_end=1996
  _globals['_ONEOFDESCRIPTORPROTO']._serialized_start=2004
  _globals['_ONEOFDESCRIPTORPROTO']._serialized_end=2088
  _globals['_ENUMDESCRIPTORPROTO']._serialized_start=2091
  _globals['_ENUMDESCRIPTORPROTO']._serialized_end=2219
  _globals['_ENUMVALUEDESCRIPTORPROTO']._serialized_start=2221
  _globals['_ENUMVALUEDESCRIPTORPROTO']._serialized_end=2283
  _globals['_ONEOFOPTIONS']._serialized_start=2285
  _globals['_ONEOFOPTIONS']._serialized_end=2318
# @@protoc_insertion_point(module_scope)
