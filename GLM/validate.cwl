cwlVersion: v1.2
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: glm
  ResourceRequirement:
    coresMin: 2
    ramMin: 100000
inputs: 
  script:
    type: File
    default:
      class: File
      location: src/validate.py
  onehotnpy: File
  onehotcolumnsnpy: File
  samplescsv: File
  count: File
  threshold: int
outputs: 
  stats:
    type: stdout
  graph:
    type: File
    outputBinding:
      glob: "*.png"
baseCommand: python3
arguments:
  - $(inputs.script)
  - $(inputs.onehotnpy)
  - $(inputs.onehotcolumnsnpy)
  - $(inputs.samplescsv)
  - $(inputs.count)
  - $(inputs.threshold)
stdout: stats.txt
