cwlVersion: v1.0
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
  ResourceRequirement:
    ramMin: 5000
inputs:
  sample: string
  originalvcfgz:
    type: File
    secondaryFiles: [.tbi]
  phasedvcfgz:
    type: File
    secondaryFiles: [.tbi]
  imputedoutsidevcfgz:
    type: File
    secondaryFiles: [.tbi]
outputs:
  mergedvcfgz:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
    secondaryFiles: [.tbi]
baseCommand: [rtg, vcfmerge]
arguments:
  - "--force-merge-all"
  - $(inputs.phasedvcfgz)
  - $(inputs.originalvcfgz)
  - $(inputs.imputedoutsidevcfgz)
  - prefix: "-o"
    valueFrom: $(inputs.sample)_phased_imputed_merged.vcf.gz
