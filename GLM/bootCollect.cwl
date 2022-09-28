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
      location: src/bootCollect.py
  txtdir:
    type: Directory
outputs:
  csv:
    type: File
    outputBinding:
      glob: "*csv"
baseCommand: python3
arguments:
  - $(inputs.script)
  - $(inputs.txtdir)
  - $(runtime.outdir)/CountAll.csv
