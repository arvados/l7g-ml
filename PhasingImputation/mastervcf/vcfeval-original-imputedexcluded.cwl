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
  - $(inputs.imputedexcluded)
  - "-t"
  - $(inputs.refdir)
  - "-o"
  - $(inputs.sample)_imputed_excluded
inputs:
  original: 
    type: File
    secondaryFiles: [.tbi]
  imputedexcluded:
    type: File
    secondaryFiles: [.tbi]
  sample: string
  refdir: Directory
outputs:
  original_imputedexcluded_evaldir:
    type: Directory
    outputBinding:
      glob: "$(inputs.sample)_imputed_excluded"
