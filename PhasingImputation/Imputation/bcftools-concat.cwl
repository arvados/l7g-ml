cwlVersion: v1.0
class: CommandLineTool
requirements:
  ShellCommandRequirement: {}
hints:
  DockerRequirement:
    dockerPull: l7g-ml/imputation
  ResourceRequirement:
    coresMin: 3
    ramMin: 1000
    tmpdirMin: 10000
inputs:
  sample: string
  vcfgzs:
    type: File[]
    secondaryFiles: [.tbi]
outputs:
  vcfgz:
    type: File
    outputBinding:
      glob: "*vcf.gz"
    secondaryFiles: [.tbi]
baseCommand: [bcftools, concat]
arguments:
  - $(inputs.vcfgzs)
  - shellQuote: false
    valueFrom: "|"
  - "bgzip"
  - "-f"
  - "-c"
  - shellQuote: false
    valueFrom: ">"
  - $(inputs.sample)_rawimputed.vcf.gz
  - shellQuote: false
    valueFrom: "&&"
  - "tabix"
  - prefix: "-p"
    valueFrom: "vcf"
  - "-f"
  - $(inputs.sample)_rawimputed.vcf.gz
