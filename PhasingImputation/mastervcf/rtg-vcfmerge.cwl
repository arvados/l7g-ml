cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
baseCommand: [rtg, vcfmerge]
arguments:
  - "--force-merge-all"
  - $(inputs.phased)
  - $(inputs.original)
  - $(inputs.imputedexcluded)
  - "-o"
  - "$(inputs.sample)_phased_imputed_merged.vcf.gz"
inputs:
  original: 
    type: File
    secondaryFiles: [.tbi]
  phased:
    type: File
    secondaryFiles: [.tbi]
  imputedexcluded: 
    type: File
    secondaryFiles: [.tbi]
  sample: string
outputs:
  master:
    type: File
    secondaryFiles: [.tbi]
    outputBinding:
      glob: "$(inputs.sample)_phased_imputed_merged.vcf.gz"
