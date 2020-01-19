meta:
  id: tlg0
  title: TLG0 image format
  file-extension: tlg
  endian: le

seq:
  - id: magic
    contents: ['TLG0.0', 0x00, 'sds', 0x1A]
  - id: raw_length
    type: u4
  - id: tlg_raw_data
    size: raw_length
    doc: |
      Raw tlg data
      Can be TLG5.0 or TLG6.0

types:
  tlg0_chunk:
    seq:
      - id: name
        size: 4
      - id: chunk_size
        type: u4
      - id: data
        # if: name == "tags"
        size: chunk_size
    
instances:
  raw_data_magic:
    pos: 15
    size: 11
  info_data_point:
    value: raw_length + 11 + 4
  chunks:
    pos: info_data_point
    type: tlg0_chunk
    repeat: eos
