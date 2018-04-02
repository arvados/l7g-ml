cwlVersion: v1.0
class: CommandLineTool
requirements:
  ShellCommandRequirement: {}
hints:
  ResourceRequirement:
    ramMin: 6000
inputs:
  sample: string
  chr: string
  ref: File
  map: File
  target:
    type: File
    secondaryFiles: [.tbi]
outputs:
  imputed:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
    secondaryFiles: [.tbi]
baseCommand: java
arguments:
  - prefix: "-jar"
    valueFrom: "/beagle.27Jan18.7e1.jar"
  - prefix: "ref="
    separate: false
    valueFrom: $(inputs.ref)
  - prefix: "map="
    separate: false
    valueFrom: $(inputs.map)
  - prefix: "gt="
    separate: false
    valueFrom: $(inputs.target)
  - prefix: "out="
    separate: false
    valueFrom: $(inputs.sample)_imputed_$(inputs.chr)
  - "nthreads=1"
  - shellQuote: false
    valueFrom: "&&"
  - "tabix"
  - prefix: "-p"
    valueFrom: "vcf"
  - "-f"
  - $(inputs.sample)_imputed_$(inputs.chr).vcf.gz
