meta:
  id: akb
  title: AKB image format
  file-extension: akb
  endian: le

seq:
  - id: magic
    contents: "AKB "
  - id: width
    type: u2
  - id: height
    type: u2
  - id: compression
    type: u4
  - id: fill
    type: u4
  - id: left
    type: u4
  - id: top
    type: u4
  - id: right
    type: u4
  - id: bottom
    type: u4
  - id: image_data
    size-eos: true
