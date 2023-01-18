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
      location: src/makesamplesauxiliary.r
  samplescsv: File
  phenotypedir: Directory
outputs:
  samplesauxiliary:
    type: File
    outputBinding:
      glob: "*.tsv"
baseCommand: Rscript
arguments:
  - $(inputs.script)
  - $(inputs.samplescsv)
  - $(inputs.phenotypedir)
