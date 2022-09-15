cwlVersion: v1.1
class: Workflow
requirements:
  ScatterFeatureRequirement: {}

inputs:
  seedsnumber:
    type: int
  seedslimit:
    type: int
  glmnet_file:
    type: File
  X:
    type: File
  coldata:
    type: File
  sampledata:
    type: File
  gamma:
    type: float
  weighted:
    type: string

outputs: 
  coefFiles:
    type:
      type: array
      items:
        type: array
        items: File
    outputSource: glmnetAdaptiveBoot/text_file

steps:
  generateSeeds:
    in:
      seedsnumber: seedsnumber
      seedslimit: seedslimit
    out: [seedsstr]
    run: generateSeeds.cwl

  string-to-array:
    in:
      str: generateSeeds/seedsstr
    out: [randomseeds]
    run: string-to-array.cwl

  glmnetAdaptiveBoot:
    scatter: seed
    in:
      glmnet_file: glmnet_file
      X: X
      coldata: coldata
      sampledata: sampledata
      gamma: gamma
      weighted: weighted
      seed: string-to-array/randomseeds
    run: glmnetBootNewFormat.cwl
    out: [text_file,graph]
