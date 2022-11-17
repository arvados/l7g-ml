cwlVersion: v1.2
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: glm
  ResourceRequirement:
    coresMin: 2
    ramMin: 10000
inputs: 
  script:
    type: File
    default:
      class: File
      location: src/validate.py
  onehotnpy: File
  onehotcolumnsnpy: File
  samplesphenotype: File
  count: File
  fractionthreshold: float
outputs:
  stats:
    type: stdout
  tsv:
    type: File
    outputBinding:
      glob: "*.tsv"
baseCommand: python3
arguments:
  - $(inputs.script)
  - $(inputs.onehotnpy)
  - $(inputs.onehotcolumnsnpy)
  - $(inputs.samplesphenotype)
  - $(inputs.count)
  - $(inputs.fractionthreshold)
stdout: stats.txt
