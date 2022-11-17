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
      location: src/getanno.py
  featurecoef: File
  annotationvcf: File
outputs:
  tsv:
    type: File
    outputBinding:
      glob: "*.tsv"
baseCommand: python3
arguments:
  - $(inputs.script)
  - $(inputs.featurecoef)
  - $(inputs.annotationvcf)
