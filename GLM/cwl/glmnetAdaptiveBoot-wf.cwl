$namespaces:
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"

requirements:
  ScatterFeatureRequirement: {}

cwlVersion: v1.0
class: Workflow

inputs:
  Nseeds:
    type: int
  glmnet_file:
    type: File
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
    type: string
  colorblood:
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
  generateRandArray:
    in:
      Nseeds: Nseeds 
    out: [randomseed]
    run: generateArray.cwl

  glmnetAdaptiveBoot:
    scatter: seed
    in:
      glmnet_file: glmnet_file
      X: X
      Xr: Xr
      Xc: Xc
      y: y
      pathdataoh: pathdataoh
      oldpath: oldpath
      varvals: varvals
      zygosity: zygosity
      gamma: gamma
      colorblood: colorblood
      type_measure: type_measure
      force_PCA: force_PCA
      weighted: weighted
      seed: generateRandArray/randomseed
    run: glmnetAdaptiveBoot.cwl
    out: [text_file,graph]
