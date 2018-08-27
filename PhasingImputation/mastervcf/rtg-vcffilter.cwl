cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
  ResourceRequirement:
    ramMin: 5000
baseCommand: [rtg, vcffilter]
arguments:
  - "-i"
  - $(inputs.imputed)
  - "-o"
  - "$(inputs.sample)_imputed_excluded.vcf.gz"
  - "--exclude-bed"
  - $(inputs.bedfile)
inputs:
  imputed: 
    type: File
    secondaryFiles: [.tbi]
  sample: string
  bedfile: File
outputs:
  imputedexcluded:
    type: File
    secondaryFiles: [.tbi]
    outputBinding:
      glob: "$(inputs.sample)_imputed_excluded.vcf.gz"
