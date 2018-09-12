cwlVersion: v1.0
class: CommandLineTool
requirements:
  ShellCommandRequirement: {}
hints:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
inputs:
  sample: string
  rawimputedvcfgz: File
outputs:
  imputedvcfgz:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
    secondaryFiles: [.tbi]
baseCommand: zcat
arguments:
  - $(inputs.rawimputedvcfgz)
  - shellQuote: false
    valueFrom: "|"
  - "grep"
  - prefix: "-v"
    valueFrom: "0|0"
  - shellQuote: false
    valueFrom: "|"
  - "bgzip"
  - "-c"
  - shellQuote: false
    valueFrom: ">"
  - $(inputs.sample)_imputed.vcf.gz
  - shellQuote: false
    valueFrom: "&&"
  - "tabix"
  - prefix: "-p"
    valueFrom: "vcf"
  - "-f"
  - $(inputs.sample)_imputed.vcf.gz
