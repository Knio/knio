# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/perfetto/common/sys_stats_counters.proto
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
    'protos/perfetto/common/sys_stats_counters.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/protos/perfetto/common/sys_stats_counters.proto\x12\x0fperfetto.protos*\xa5\x07\n\x0fMeminfoCounters\x12\x17\n\x13MEMINFO_UNSPECIFIED\x10\x00\x12\x15\n\x11MEMINFO_MEM_TOTAL\x10\x01\x12\x14\n\x10MEMINFO_MEM_FREE\x10\x02\x12\x19\n\x15MEMINFO_MEM_AVAILABLE\x10\x03\x12\x13\n\x0fMEMINFO_BUFFERS\x10\x04\x12\x12\n\x0eMEMINFO_CACHED\x10\x05\x12\x17\n\x13MEMINFO_SWAP_CACHED\x10\x06\x12\x12\n\x0eMEMINFO_ACTIVE\x10\x07\x12\x14\n\x10MEMINFO_INACTIVE\x10\x08\x12\x17\n\x13MEMINFO_ACTIVE_ANON\x10\t\x12\x19\n\x15MEMINFO_INACTIVE_ANON\x10\n\x12\x17\n\x13MEMINFO_ACTIVE_FILE\x10\x0b\x12\x19\n\x15MEMINFO_INACTIVE_FILE\x10\x0c\x12\x17\n\x13MEMINFO_UNEVICTABLE\x10\r\x12\x13\n\x0fMEMINFO_MLOCKED\x10\x0e\x12\x16\n\x12MEMINFO_SWAP_TOTAL\x10\x0f\x12\x15\n\x11MEMINFO_SWAP_FREE\x10\x10\x12\x11\n\rMEMINFO_DIRTY\x10\x11\x12\x15\n\x11MEMINFO_WRITEBACK\x10\x12\x12\x16\n\x12MEMINFO_ANON_PAGES\x10\x13\x12\x12\n\x0eMEMINFO_MAPPED\x10\x14\x12\x11\n\rMEMINFO_SHMEM\x10\x15\x12\x10\n\x0cMEMINFO_SLAB\x10\x16\x12\x1c\n\x18MEMINFO_SLAB_RECLAIMABLE\x10\x17\x12\x1e\n\x1aMEMINFO_SLAB_UNRECLAIMABLE\x10\x18\x12\x18\n\x14MEMINFO_KERNEL_STACK\x10\x19\x12\x17\n\x13MEMINFO_PAGE_TABLES\x10\x1a\x12\x18\n\x14MEMINFO_COMMIT_LIMIT\x10\x1b\x12\x17\n\x13MEMINFO_COMMITED_AS\x10\x1c\x12\x19\n\x15MEMINFO_VMALLOC_TOTAL\x10\x1d\x12\x18\n\x14MEMINFO_VMALLOC_USED\x10\x1e\x12\x19\n\x15MEMINFO_VMALLOC_CHUNK\x10\x1f\x12\x15\n\x11MEMINFO_CMA_TOTAL\x10 \x12\x14\n\x10MEMINFO_CMA_FREE\x10!\x12\x0f\n\x0bMEMINFO_GPU\x10\"\x12\x10\n\x0cMEMINFO_ZRAM\x10#\x12\x10\n\x0cMEMINFO_MISC\x10$\x12\x14\n\x10MEMINFO_ION_HEAP\x10%\x12\x19\n\x15MEMINFO_ION_HEAP_POOL\x10&*\x81,\n\x0eVmstatCounters\x12\x16\n\x12VMSTAT_UNSPECIFIED\x10\x00\x12\x18\n\x14VMSTAT_NR_FREE_PAGES\x10\x01\x12\x19\n\x15VMSTAT_NR_ALLOC_BATCH\x10\x02\x12\x1b\n\x17VMSTAT_NR_INACTIVE_ANON\x10\x03\x12\x19\n\x15VMSTAT_NR_ACTIVE_ANON\x10\x04\x12\x1b\n\x17VMSTAT_NR_INACTIVE_FILE\x10\x05\x12\x19\n\x15VMSTAT_NR_ACTIVE_FILE\x10\x06\x12\x19\n\x15VMSTAT_NR_UNEVICTABLE\x10\x07\x12\x13\n\x0fVMSTAT_NR_MLOCK\x10\x08\x12\x18\n\x14VMSTAT_NR_ANON_PAGES\x10\t\x12\x14\n\x10VMSTAT_NR_MAPPED\x10\n\x12\x18\n\x14VMSTAT_NR_FILE_PAGES\x10\x0b\x12\x13\n\x0fVMSTAT_NR_DIRTY\x10\x0c\x12\x17\n\x13VMSTAT_NR_WRITEBACK\x10\r\x12\x1e\n\x1aVMSTAT_NR_SLAB_RECLAIMABLE\x10\x0e\x12 \n\x1cVMSTAT_NR_SLAB_UNRECLAIMABLE\x10\x0f\x12\x1e\n\x1aVMSTAT_NR_PAGE_TABLE_PAGES\x10\x10\x12\x1a\n\x16VMSTAT_NR_KERNEL_STACK\x10\x11\x12\x16\n\x12VMSTAT_NR_OVERHEAD\x10\x12\x12\x16\n\x12VMSTAT_NR_UNSTABLE\x10\x13\x12\x14\n\x10VMSTAT_NR_BOUNCE\x10\x14\x12\x1a\n\x16VMSTAT_NR_VMSCAN_WRITE\x10\x15\x12&\n\"VMSTAT_NR_VMSCAN_IMMEDIATE_RECLAIM\x10\x16\x12\x1c\n\x18VMSTAT_NR_WRITEBACK_TEMP\x10\x17\x12\x1b\n\x17VMSTAT_NR_ISOLATED_ANON\x10\x18\x12\x1b\n\x17VMSTAT_NR_ISOLATED_FILE\x10\x19\x12\x13\n\x0fVMSTAT_NR_SHMEM\x10\x1a\x12\x15\n\x11VMSTAT_NR_DIRTIED\x10\x1b\x12\x15\n\x11VMSTAT_NR_WRITTEN\x10\x1c\x12\x1b\n\x17VMSTAT_NR_PAGES_SCANNED\x10\x1d\x12\x1d\n\x19VMSTAT_WORKINGSET_REFAULT\x10\x1e\x12\x1e\n\x1aVMSTAT_WORKINGSET_ACTIVATE\x10\x1f\x12!\n\x1dVMSTAT_WORKINGSET_NODERECLAIM\x10 \x12(\n$VMSTAT_NR_ANON_TRANSPARENT_HUGEPAGES\x10!\x12\x16\n\x12VMSTAT_NR_FREE_CMA\x10\"\x12\x17\n\x13VMSTAT_NR_SWAPCACHE\x10#\x12\x1d\n\x19VMSTAT_NR_DIRTY_THRESHOLD\x10$\x12(\n$VMSTAT_NR_DIRTY_BACKGROUND_THRESHOLD\x10%\x12\x11\n\rVMSTAT_PGPGIN\x10&\x12\x12\n\x0eVMSTAT_PGPGOUT\x10\'\x12\x17\n\x13VMSTAT_PGPGOUTCLEAN\x10(\x12\x11\n\rVMSTAT_PSWPIN\x10)\x12\x12\n\x0eVMSTAT_PSWPOUT\x10*\x12\x16\n\x12VMSTAT_PGALLOC_DMA\x10+\x12\x19\n\x15VMSTAT_PGALLOC_NORMAL\x10,\x12\x1a\n\x16VMSTAT_PGALLOC_MOVABLE\x10-\x12\x11\n\rVMSTAT_PGFREE\x10.\x12\x15\n\x11VMSTAT_PGACTIVATE\x10/\x12\x17\n\x13VMSTAT_PGDEACTIVATE\x10\x30\x12\x12\n\x0eVMSTAT_PGFAULT\x10\x31\x12\x15\n\x11VMSTAT_PGMAJFAULT\x10\x32\x12\x17\n\x13VMSTAT_PGREFILL_DMA\x10\x33\x12\x1a\n\x16VMSTAT_PGREFILL_NORMAL\x10\x34\x12\x1b\n\x17VMSTAT_PGREFILL_MOVABLE\x10\x35\x12\x1d\n\x19VMSTAT_PGSTEAL_KSWAPD_DMA\x10\x36\x12 \n\x1cVMSTAT_PGSTEAL_KSWAPD_NORMAL\x10\x37\x12!\n\x1dVMSTAT_PGSTEAL_KSWAPD_MOVABLE\x10\x38\x12\x1d\n\x19VMSTAT_PGSTEAL_DIRECT_DMA\x10\x39\x12 \n\x1cVMSTAT_PGSTEAL_DIRECT_NORMAL\x10:\x12!\n\x1dVMSTAT_PGSTEAL_DIRECT_MOVABLE\x10;\x12\x1c\n\x18VMSTAT_PGSCAN_KSWAPD_DMA\x10<\x12\x1f\n\x1bVMSTAT_PGSCAN_KSWAPD_NORMAL\x10=\x12 \n\x1cVMSTAT_PGSCAN_KSWAPD_MOVABLE\x10>\x12\x1c\n\x18VMSTAT_PGSCAN_DIRECT_DMA\x10?\x12\x1f\n\x1bVMSTAT_PGSCAN_DIRECT_NORMAL\x10@\x12 \n\x1cVMSTAT_PGSCAN_DIRECT_MOVABLE\x10\x41\x12!\n\x1dVMSTAT_PGSCAN_DIRECT_THROTTLE\x10\x42\x12\x17\n\x13VMSTAT_PGINODESTEAL\x10\x43\x12\x18\n\x14VMSTAT_SLABS_SCANNED\x10\x44\x12\x1c\n\x18VMSTAT_KSWAPD_INODESTEAL\x10\x45\x12\'\n#VMSTAT_KSWAPD_LOW_WMARK_HIT_QUICKLY\x10\x46\x12(\n$VMSTAT_KSWAPD_HIGH_WMARK_HIT_QUICKLY\x10G\x12\x15\n\x11VMSTAT_PAGEOUTRUN\x10H\x12\x15\n\x11VMSTAT_ALLOCSTALL\x10I\x12\x14\n\x10VMSTAT_PGROTATED\x10J\x12\x19\n\x15VMSTAT_DROP_PAGECACHE\x10K\x12\x14\n\x10VMSTAT_DROP_SLAB\x10L\x12\x1c\n\x18VMSTAT_PGMIGRATE_SUCCESS\x10M\x12\x19\n\x15VMSTAT_PGMIGRATE_FAIL\x10N\x12\"\n\x1eVMSTAT_COMPACT_MIGRATE_SCANNED\x10O\x12\x1f\n\x1bVMSTAT_COMPACT_FREE_SCANNED\x10P\x12\x1b\n\x17VMSTAT_COMPACT_ISOLATED\x10Q\x12\x18\n\x14VMSTAT_COMPACT_STALL\x10R\x12\x17\n\x13VMSTAT_COMPACT_FAIL\x10S\x12\x1a\n\x16VMSTAT_COMPACT_SUCCESS\x10T\x12\x1e\n\x1aVMSTAT_COMPACT_DAEMON_WAKE\x10U\x12!\n\x1dVMSTAT_UNEVICTABLE_PGS_CULLED\x10V\x12\"\n\x1eVMSTAT_UNEVICTABLE_PGS_SCANNED\x10W\x12\"\n\x1eVMSTAT_UNEVICTABLE_PGS_RESCUED\x10X\x12\"\n\x1eVMSTAT_UNEVICTABLE_PGS_MLOCKED\x10Y\x12$\n VMSTAT_UNEVICTABLE_PGS_MUNLOCKED\x10Z\x12\"\n\x1eVMSTAT_UNEVICTABLE_PGS_CLEARED\x10[\x12#\n\x1fVMSTAT_UNEVICTABLE_PGS_STRANDED\x10\\\x12\x15\n\x11VMSTAT_NR_ZSPAGES\x10]\x12\x16\n\x12VMSTAT_NR_ION_HEAP\x10^\x12\x16\n\x12VMSTAT_NR_GPU_HEAP\x10_\x12\x19\n\x15VMSTAT_ALLOCSTALL_DMA\x10`\x12\x1d\n\x19VMSTAT_ALLOCSTALL_MOVABLE\x10\x61\x12\x1c\n\x18VMSTAT_ALLOCSTALL_NORMAL\x10\x62\x12&\n\"VMSTAT_COMPACT_DAEMON_FREE_SCANNED\x10\x63\x12)\n%VMSTAT_COMPACT_DAEMON_MIGRATE_SCANNED\x10\x64\x12\x15\n\x11VMSTAT_NR_FASTRPC\x10\x65\x12$\n VMSTAT_NR_INDIRECTLY_RECLAIMABLE\x10\x66\x12\x1b\n\x17VMSTAT_NR_ION_HEAP_POOL\x10g\x12%\n!VMSTAT_NR_KERNEL_MISC_RECLAIMABLE\x10h\x12%\n!VMSTAT_NR_SHADOW_CALL_STACK_BYTES\x10i\x12\x1d\n\x19VMSTAT_NR_SHMEM_HUGEPAGES\x10j\x12\x1d\n\x19VMSTAT_NR_SHMEM_PMDMAPPED\x10k\x12!\n\x1dVMSTAT_NR_UNRECLAIMABLE_PAGES\x10l\x12\x1e\n\x1aVMSTAT_NR_ZONE_ACTIVE_ANON\x10m\x12\x1e\n\x1aVMSTAT_NR_ZONE_ACTIVE_FILE\x10n\x12 \n\x1cVMSTAT_NR_ZONE_INACTIVE_ANON\x10o\x12 \n\x1cVMSTAT_NR_ZONE_INACTIVE_FILE\x10p\x12\x1e\n\x1aVMSTAT_NR_ZONE_UNEVICTABLE\x10q\x12 \n\x1cVMSTAT_NR_ZONE_WRITE_PENDING\x10r\x12\x13\n\x0fVMSTAT_OOM_KILL\x10s\x12\x15\n\x11VMSTAT_PGLAZYFREE\x10t\x12\x16\n\x12VMSTAT_PGLAZYFREED\x10u\x12\x13\n\x0fVMSTAT_PGREFILL\x10v\x12\x18\n\x14VMSTAT_PGSCAN_DIRECT\x10w\x12\x18\n\x14VMSTAT_PGSCAN_KSWAPD\x10x\x12\x15\n\x11VMSTAT_PGSKIP_DMA\x10y\x12\x19\n\x15VMSTAT_PGSKIP_MOVABLE\x10z\x12\x18\n\x14VMSTAT_PGSKIP_NORMAL\x10{\x12\x19\n\x15VMSTAT_PGSTEAL_DIRECT\x10|\x12\x19\n\x15VMSTAT_PGSTEAL_KSWAPD\x10}\x12\x12\n\x0eVMSTAT_SWAP_RA\x10~\x12\x16\n\x12VMSTAT_SWAP_RA_HIT\x10\x7f\x12\x1e\n\x19VMSTAT_WORKINGSET_RESTORE\x10\x80\x01\x12\x1d\n\x18VMSTAT_ALLOCSTALL_DEVICE\x10\x81\x01\x12\x1c\n\x17VMSTAT_ALLOCSTALL_DMA32\x10\x82\x01\x12\x1b\n\x16VMSTAT_BALLOON_DEFLATE\x10\x83\x01\x12\x1b\n\x16VMSTAT_BALLOON_INFLATE\x10\x84\x01\x12\x1b\n\x16VMSTAT_BALLOON_MIGRATE\x10\x85\x01\x12\x1a\n\x15VMSTAT_CMA_ALLOC_FAIL\x10\x86\x01\x12\x1d\n\x18VMSTAT_CMA_ALLOC_SUCCESS\x10\x87\x01\x12\x1d\n\x18VMSTAT_NR_FILE_HUGEPAGES\x10\x88\x01\x12\x1d\n\x18VMSTAT_NR_FILE_PMDMAPPED\x10\x89\x01\x12 \n\x1bVMSTAT_NR_FOLL_PIN_ACQUIRED\x10\x8a\x01\x12 \n\x1bVMSTAT_NR_FOLL_PIN_RELEASED\x10\x8b\x01\x12#\n\x1eVMSTAT_NR_SEC_PAGE_TABLE_PAGES\x10\x8c\x01\x12 \n\x1bVMSTAT_NR_SHADOW_CALL_STACK\x10\x8d\x01\x12\x19\n\x14VMSTAT_NR_SWAPCACHED\x10\x8e\x01\x12 \n\x1bVMSTAT_NR_THROTTLED_WRITTEN\x10\x8f\x01\x12\x1a\n\x15VMSTAT_PGALLOC_DEVICE\x10\x90\x01\x12\x19\n\x14VMSTAT_PGALLOC_DMA32\x10\x91\x01\x12\x1b\n\x16VMSTAT_PGDEMOTE_DIRECT\x10\x92\x01\x12\x1b\n\x16VMSTAT_PGDEMOTE_KSWAPD\x10\x93\x01\x12\x13\n\x0eVMSTAT_PGREUSE\x10\x94\x01\x12\x17\n\x12VMSTAT_PGSCAN_ANON\x10\x95\x01\x12\x17\n\x12VMSTAT_PGSCAN_FILE\x10\x96\x01\x12\x19\n\x14VMSTAT_PGSKIP_DEVICE\x10\x97\x01\x12\x18\n\x13VMSTAT_PGSKIP_DMA32\x10\x98\x01\x12\x18\n\x13VMSTAT_PGSTEAL_ANON\x10\x99\x01\x12\x18\n\x13VMSTAT_PGSTEAL_FILE\x10\x9a\x01\x12\x1e\n\x19VMSTAT_THP_COLLAPSE_ALLOC\x10\x9b\x01\x12%\n VMSTAT_THP_COLLAPSE_ALLOC_FAILED\x10\x9c\x01\x12#\n\x1eVMSTAT_THP_DEFERRED_SPLIT_PAGE\x10\x9d\x01\x12\x1b\n\x16VMSTAT_THP_FAULT_ALLOC\x10\x9e\x01\x12\x1e\n\x19VMSTAT_THP_FAULT_FALLBACK\x10\x9f\x01\x12%\n VMSTAT_THP_FAULT_FALLBACK_CHARGE\x10\xa0\x01\x12\x1a\n\x15VMSTAT_THP_FILE_ALLOC\x10\xa1\x01\x12\x1d\n\x18VMSTAT_THP_FILE_FALLBACK\x10\xa2\x01\x12$\n\x1fVMSTAT_THP_FILE_FALLBACK_CHARGE\x10\xa3\x01\x12\x1b\n\x16VMSTAT_THP_FILE_MAPPED\x10\xa4\x01\x12\x1e\n\x19VMSTAT_THP_MIGRATION_FAIL\x10\xa5\x01\x12\x1f\n\x1aVMSTAT_THP_MIGRATION_SPLIT\x10\xa6\x01\x12!\n\x1cVMSTAT_THP_MIGRATION_SUCCESS\x10\xa7\x01\x12$\n\x1fVMSTAT_THP_SCAN_EXCEED_NONE_PTE\x10\xa8\x01\x12%\n VMSTAT_THP_SCAN_EXCEED_SHARE_PTE\x10\xa9\x01\x12$\n\x1fVMSTAT_THP_SCAN_EXCEED_SWAP_PTE\x10\xaa\x01\x12\x1a\n\x15VMSTAT_THP_SPLIT_PAGE\x10\xab\x01\x12!\n\x1cVMSTAT_THP_SPLIT_PAGE_FAILED\x10\xac\x01\x12\x19\n\x14VMSTAT_THP_SPLIT_PMD\x10\xad\x01\x12\x16\n\x11VMSTAT_THP_SWPOUT\x10\xae\x01\x12\x1f\n\x1aVMSTAT_THP_SWPOUT_FALLBACK\x10\xaf\x01\x12\x1f\n\x1aVMSTAT_THP_ZERO_PAGE_ALLOC\x10\xb0\x01\x12&\n!VMSTAT_THP_ZERO_PAGE_ALLOC_FAILED\x10\xb1\x01\x12\x1a\n\x15VMSTAT_VMA_LOCK_ABORT\x10\xb2\x01\x12\x19\n\x14VMSTAT_VMA_LOCK_MISS\x10\xb3\x01\x12\x1a\n\x15VMSTAT_VMA_LOCK_RETRY\x10\xb4\x01\x12\x1c\n\x17VMSTAT_VMA_LOCK_SUCCESS\x10\xb5\x01\x12$\n\x1fVMSTAT_WORKINGSET_ACTIVATE_ANON\x10\xb6\x01\x12$\n\x1fVMSTAT_WORKINGSET_ACTIVATE_FILE\x10\xb7\x01\x12\x1c\n\x17VMSTAT_WORKINGSET_NODES\x10\xb8\x01\x12#\n\x1eVMSTAT_WORKINGSET_REFAULT_ANON\x10\xb9\x01\x12#\n\x1eVMSTAT_WORKINGSET_REFAULT_FILE\x10\xba\x01\x12#\n\x1eVMSTAT_WORKINGSET_RESTORE_ANON\x10\xbb\x01\x12#\n\x1eVMSTAT_WORKINGSET_RESTORE_FILE\x10\xbc\x01')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.perfetto.common.sys_stats_counters_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MEMINFOCOUNTERS']._serialized_start=69
  _globals['_MEMINFOCOUNTERS']._serialized_end=1002
  _globals['_VMSTATCOUNTERS']._serialized_start=1005
  _globals['_VMSTATCOUNTERS']._serialized_end=6638
# @@protoc_insertion_point(module_scope)
