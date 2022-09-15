cwlVersion: v1.1
class: Workflow
requirements:
  ScatterFeatureRequirement: {}

inputs:
  seedsnumber:
    type: int
  seedslimit:
    type: int
  X:
    type: File
  Xr:
    type: File
  Xc:
    type: File
  y:
    type: File
  pathdataoh:
    type: File
  oldpath:
    type: File
  varvals:
    type: File
  zygosity:
    type: File
  gamma:
    type: float
  phenotype:
    type: string
  type_measure:
    type: string
  force_PCA:
    type: string
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
      X: X
      Xr: Xr
      Xc: Xc
      y: y
      pathdataoh: pathdataoh
      oldpath: oldpath
      varvals: varvals
      zygosity: zygosity
      gamma: gamma
      phenotype: phenotype
      type_measure: type_measure
      force_PCA: force_PCA
      weighted: weighted
      seed: string-to-array/randomseeds
    run: glmnetAdaptiveBoot.cwl
    out: [text_file,graph]
