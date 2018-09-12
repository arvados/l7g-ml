cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
  ResourceRequirement:
    ramMin: 5000
inputs:
  sample: string
  suffix: string
  baselinevcfgz:
    type: File
    secondaryFiles: [.tbi]
  callsvcfgz:
    type: File
    secondaryFiles: [.tbi]
  sdf: Directory
outputs:
  evaldir:
    type: Directory
    outputBinding:
      glob: "*eval"
baseCommand: [rtg, vcfeval]
arguments:
  - prefix: "-b"
    valueFrom: $(inputs.baselinevcfgz)
  - prefix: "-c"
    valueFrom: $(inputs.callsvcfgz)
  - prefix: "-t"
    valueFrom: $(inputs.sdf)
  - prefix: "-o"
    valueFrom: $(inputs.sample)_$(inputs.suffix)_eval
