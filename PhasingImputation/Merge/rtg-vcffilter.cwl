cwlVersion: v1.0
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
  ResourceRequirement:
    ramMin: 5000
inputs:
  sample: string
  imputedvcfgz:
    type: File
    secondaryFiles: [.tbi]
  originalbed: File
outputs:
  imputedoutsidevcfgz:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
    secondaryFiles: [.tbi]
baseCommand: [rtg, vcffilter]
arguments:
  - prefix: "-i"
    valueFrom: $(inputs.imputedvcfgz)
  - prefix: "-o"
    valueFrom: $(inputs.sample)_imputedoutside.vcf.gz
  - prefix: "--exclude-bed"
    valueFrom: $(inputs.originalbed)
