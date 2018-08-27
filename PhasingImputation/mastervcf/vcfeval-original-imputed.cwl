cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
  ResourceRequirement:
    ramMin: 5000
baseCommand: [rtg, vcfeval]
arguments:
  - "-b"
  - $(inputs.original)
  - "-c"
  - $(inputs.imputed)
  - "-t"
  - $(inputs.refdir)
  - "-o"
  - originalimputedeval_$(inputs.sample)
inputs:
  original: 
    type: File
    secondaryFiles: [.tbi]
  imputed:
    type: File
    secondaryFiles: [.tbi]
  sample: string
  refdir: Directory
outputs:
  original_imputed_evaldir:
    type: Directory
    outputBinding:
      glob: "originalimputedeval_$(inputs.sample)"
