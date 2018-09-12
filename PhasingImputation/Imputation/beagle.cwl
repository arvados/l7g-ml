cwlVersion: v1.0
class: CommandLineTool
requirements:
  ShellCommandRequirement: {}
hints:
  DockerRequirement:
    dockerPull: l7g-ml/imputation
  ResourceRequirement:
    coresMin: 2
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
  rawimputed:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
    secondaryFiles: [.tbi]
baseCommand: java
arguments:
  - prefix: "-jar"
    valueFrom: "/beagle.03Jul18.40b.jar"
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
    valueFrom: $(inputs.sample)_rawimputed_$(inputs.chr)
  - prefix: "nthreads="
    separate: false
    valueFrom: $(runtime.cores)
  - shellQuote: false
    valueFrom: "&&"
  - "tabix"
  - prefix: "-p"
    valueFrom: "vcf"
  - "-f"
  - $(inputs.sample)_rawimputed_$(inputs.chr).vcf.gz
