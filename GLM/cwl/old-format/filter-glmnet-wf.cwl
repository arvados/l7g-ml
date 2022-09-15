cwlVersion: v1.1
class: Workflow
requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}

inputs:
  dbfile:
    type: File
  allfile:
    type: File 
  namefile:
    type: File
  phenotype:
    type: string
  PCAfile:
    type: File
  PCAnamesfile:
    type: File
  qualcutoff:
    type: float
  gamma:
    type: float
  type_measure:
    type: string
  force_PCA:
    type: string
  weighted:
    type: string
  seedsnumber:
    type: int
  seedslimit:
    type: int

outputs:
  csv: 
    type: File 
    outputSource: bootCollect/csv

steps:
  filter:
    run: ../../ADAnalysis/cwl/loadingAD_extPCA.cwl
    in:
      dbfile: dbfile
      allfile: allfile
      namefile: namefile
      phenotype: phenotype
      PCAfile: PCAfile
      PCAnamesfile: PCAnamesfile
      qualcutoff: qualcutoff
    out: [X, Xr, Xc, y, pathdataoh, oldpath, varvals, zygosity]

  glmnetAdaptiveBoot-wf:
    run: glmnetAdaptiveBoot-wf.cwl
    in:
      X: filter/X
      Xr: filter/Xr
      Xc: filter/Xc
      y: filter/y
      pathdataoh: filter/pathdataoh
      oldpath: filter/oldpath
      varvals: filter/varvals
      zygosity: filter/zygosity
      gamma: gamma
      phenotype: phenotype
      type_measure: type_measure
      force_PCA: force_PCA
      weighted: weighted
      seedsnumber: seedsnumber
      seedslimit: seedslimit
    out: [coefFiles]

  nestedarray-to-dir:
    run: nestedarray-to-dir.cwl
    in:
      nestedarray: glmnetAdaptiveBoot-wf/coefFiles
      dirname:
        valueFrom: "txtdir"
    out: [dir]

  bootCollect:
    run: bootCollect.cwl
    in:
      txtdir: nestedarray-to-dir/dir
    out: [csv]
