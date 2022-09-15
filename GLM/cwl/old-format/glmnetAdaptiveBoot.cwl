cwlVersion: v1.1
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: glmextra
  ResourceRequirement:
    coresMin: 2
    ramMin: 100000
inputs: 
  glmnet_file:
    type: File
    default:
      class: File
      location: ../src/glmnetAdaptiveBoot.r
    inputBinding:
      position: 0
  X:
    type: File
    inputBinding:
      position: 1
  Xr:
    type: File
    inputBinding:
      position: 2
  Xc:
    type: File
    inputBinding:
      position: 3
  y:
    type: File
    inputBinding:
      position: 4
  pathdataoh:
    type: File
    inputBinding:
      position: 5
  oldpath:
    type: File
    inputBinding:
      position: 6
  varvals:
    type: File
    inputBinding:
      position: 7
  zygosity:
    type: File
    inputBinding:
      position: 8
  gamma:
    type: float
    inputBinding:
      position: 9
  phenotype:
    type: string
    inputBinding:
      position: 10
  type_measure:
    type: string
    inputBinding:
      position: 11 
  force_PCA:
    type: string 
    inputBinding:
      position: 12
  weighted:
    type: string
    inputBinding:
      position: 13
  seed:
    type: string
    inputBinding:
      position: 14
outputs:
  text_file:
    type: File[]
    outputBinding:
      glob: "*.txt"
  graph:
    type: File[]
    outputBinding:
      glob: "*.png"
baseCommand: Rscript
