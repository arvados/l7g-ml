cwlVersion: v1.2
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: glm
  ResourceRequirement:
    coresMin: 2
    ramMin: 20000
inputs: 
  glmnet_file:
    type: File
    default:
      class: File
      location: src/glmnetBoot.r
    inputBinding:
      position: 0
  onehotnpy:
    type: File
    inputBinding:
      position: 1
  onehotcolumnsnpy:
    type: File
    inputBinding:
      position: 2
  samplesphenotype:
    type: File
    inputBinding:
      position: 3
  gamma:
    type: float
    inputBinding:
      position: 4
  weighted:
    type: string
    inputBinding:
      position: 5
  seed:
    type: string
    inputBinding:
      position: 6
outputs:
  txt:
    type: File
    outputBinding:
      glob: "*_min.txt"
  graph:
    type: File
    outputBinding:
      glob: "*.png"
baseCommand: Rscript
