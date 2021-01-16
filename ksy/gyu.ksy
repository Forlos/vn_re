meta:
  id: gyu
  title: GYU image format
  file-extension: gyu
  endian: le

seq:
  - id: magic
    contents: "GYU\x1a"
  - id: version
    type: u4
  - id: mt_seed
    type: u4
  - id: bpp
    type: u4
  - id: width
    type: u4
  - id: height
    type: u4
  - id: data_size
    type: u4
  - id: alpha_channel_size
    type: u4
  - id: color_table_size
    type: u4
  - id: color_table
    size: color_table_size * 4
  - id: data
    size: data_size
  - id: alpha_channel
    size: alpha_channel_size
