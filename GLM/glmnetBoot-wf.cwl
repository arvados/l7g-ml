cwlVersion: v1.2
class: Workflow
requirements:
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}

inputs:
  seedsnumber: int
  seedslimit: int
  onehotnpy: File
  onehotcolumnsnpy: File
  samplescsv: File
  phenotypedir: Directory
  gamma: float
  weighted: string
  thresholdratio: float

outputs:
  csv: 
    type: File 
    outputSource: bootCollect/csv
  stats:
    type: File
    outputSource: validate/stats
  graph:
    type: File
    outputSource: validate/graph

steps:
  generateSeeds:
    run: generateSeeds.cwl
    in:
      seedsnumber: seedsnumber
      seedslimit: seedslimit
    out: [seedsstr]

  string-to-array:
    run: string-to-array.cwl
    in:
      str: generateSeeds/seedsstr
    out: [randomseeds]

  makesamplesphenotype:
    run: makesamplesphenotype.cwl
    in:
      samplescsv: samplescsv
      phenotypedir: phenotypedir
    out: [samplesphenotype]

  glmnetBoot:
    run: glmnetBoot.cwl
    scatter: seed
    in:
      onehotnpy: onehotnpy
      onehotcolumnsnpy: onehotcolumnsnpy
      samplesphenotype: makesamplesphenotype/samplesphenotype
      gamma: gamma
      weighted: weighted
      seed: string-to-array/randomseeds
    out: [txt, graph]

  filearray-to-dir:
    run: filearray-to-dir.cwl
    in:
      files: glmnetBoot/txt
      dirname:
        valueFrom: "txtdir"
    out: [dir]

  bootCollect:
    run: bootCollect.cwl
    in:
      txtdir: filearray-to-dir/dir
    out: [csv]

  validate:
    run: validate.cwl
    in:
      onehotnpy: onehotnpy
      onehotcolumnsnpy: onehotcolumnsnpy
      samplesphenotype: makesamplesphenotype/samplesphenotype
      count: bootCollect/csv
      seedsnumber: seedsnumber
      thresholdratio: thresholdratio
    out: [stats, graph]
