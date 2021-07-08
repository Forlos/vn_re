meta:
  id: compressedbg
  title: compressedbg image file
  file-extension: ""
  endian: le

seq:
  - id: magic
    contents: "CompressedBG___\x00"
  - id: header
    type: header
  - id: some_alloc
    size: header.some_size
  - id: pixel_data
    size-eos: true

types:
  header:
    seq:
      - id: width
        type: u2
      - id: height
        type: u2
      - id: bpp
        type: u2
      - id: unk0
        type: u2
      - id: unk1
        type: u4
      - id: unk2
        type: u4
      - id: unk3
        type: u4
      - id: prng_seed
        type: u4
      - id: some_size
        type: u4
      - id: unk7
        type: u1
      - id: unk8
        type: u1
      - id: unk9
        type: u2
