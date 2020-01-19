meta:
  id: tlg6
  title: TLG6 image format
  file-extension: tlg
  endian: le

seq:
  - id: magic
    contents: ['TLG6.0', 0x00, 'raw', 0x1A]
  - id: header
    type: tlg6_header
  - id: filter_types
    type: tlg6_filter_types
  - id: lines
    type: tlg6_line 
    repeat: expr
    repeat-expr: |
      header.height % tlg6_h_block_size == 0 ?
      header.height / tlg6_h_block_size:
      header.height / tlg6_h_block_size + 1

types:
  tlg6_header:
    seq:
      - id: colors
        type: u1
        doc: |
          Color component count
          Supported values: 1,3,4
      - id: data_flag
        type: u1
        doc: |
          Data flag
          Must be 0
      - id: color_type
        type: u1
        doc: |
          Color type
          Must be 0
      - id: external_golomb_table
        type: u1
        doc:
          External golomb table
          Must be 0
      - id: width
        type: u4
        doc: |
          Image width
      - id: height 
        type: u4
        doc: |
          Image height
      - id: max_bit_length 
        type: u4
        doc: |
          Max bit length
    instances:
      x_block_count:
        value: ((width - 1) / _root.tlg6_w_block_size) + 1
      y_block_count:
        value: ((height - 1) / _root.tlg6_h_block_size) + 1
  tlg6_filter_types:
    seq:
      - id: size
        type: u4
        doc: |
          Filter types input buffer size
      - id: buffer
        size: size
        doc: |
          Filter types input buffer
  tlg6_line:
    seq:
      - id: bits
        type: tlg6_bits
        repeat: expr 
        repeat-expr: _parent.header.colors
        doc: |
          Lines
  tlg6_bits:
    seq:
      - id: length
        type: u4
        doc: |
          Bit pool length
      - id: bit_pool
        size: |
          length % _root.tlg6_h_block_size == 0 ?
          length / _root.tlg6_h_block_size :
          length / _root.tlg6_h_block_size + 1
        doc: |
          Bit pool
    instances:
      method:
        value: (length >> 30) & 3
        doc: |
          two most significant bits of bit_length are entropy coding method:
          00 means Golomb method,
          01 means Gamma method (not yet suppoted),
          10 means modified LZSS method (not yet supported),
          11 means raw (uncompressed) data (not yet supported).
      
instances:
  tlg6_w_block_size:
    value: 8
  tlg6_h_block_size:
    value: 8
  main_count:
    value: header.width / tlg6_w_block_size
  fraction:
    value: header.width - main_count * tlg6_w_block_size 
