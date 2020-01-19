meta:
  id: tlg5
  title: TLG5 image format
  file-extension: tlg
  endian: le

seq:
  - id: magic
    contents: ['TLG5.0', 0x00, 'raw', 0x1A]
  - id: header
    type: tlg5_header

instances:
  blocks:
    type: tlg5_block
    pos: 13 + (4 * header.block_count)
    repeat: expr
    repeat-expr: |
      header.height % header.block_height == 0 ?
      header.height / header.block_height:
      header.height / header.block_height + 1
  

types:
  tlg5_header:
    seq:
      - id: colors
        type: u1
        doc: |
          Color component count
          Supported values: 3,4
      - id: width
        type: u4
        doc: |
          Image width
      - id: height 
        type: u4
        doc: |
          Image height
      - id: block_height 
        type: u4
        doc: |
          Block height
    instances:
      block_count:
        value: ((height - 1) / block_height) + 1
  tlg5_block:
    seq:
      - id: data_entry
        type: tlg5_data
        repeat: expr
        repeat-expr: _parent.header.colors
        doc: |
          Single block of tlg5 data
  tlg5_data:
    seq:
      - id: is_compressed
        type: u1
        doc: |
          If equals 0 compressed
          Else raw data
      - id: data_size
        type: u4
        doc: |
          Data size
      - id: data
        size: data_size
        doc: |
          Either raw data or LZSS compressed data
          This depends on is_compressed value
