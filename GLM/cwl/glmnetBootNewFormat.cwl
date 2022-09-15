$namespaces:
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"

requirements:
  DockerRequirement:
    dockerPull: glm_new
  ResourceRequirement:
    coresMin: 2
    ramMin: 100000

cwlVersion: v1.2

class: CommandLineTool

inputs: 

  glmnet_file:
    type: File
    inputBinding:
      position: 0
  X:
    type: File
    inputBinding:
      position: 1

  coldata:
    type: File
    inputBinding:
      position: 2

  sampledata:
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
  text_file:
    type: File[]
    outputBinding:
      glob: "*.txt"

  graph:
    type: File[]
    outputBinding:
      glob: "*.png"

baseCommand: Rscript
