cwlVersion: v1.0
class: CommandLineTool
requirements:
  ShellCommandRequirement: {}
hints:
  DockerRequirement:
    dockerPull: l7g-ml/phasing
  ResourceRequirement:
    coresMin: 2
    ramMin: 6000
inputs:
  sample: string
  chr: string
  ref:
    type: File
    secondaryFiles: [.tbi]
  map: File
  target:
    type: File
    secondaryFiles: [.tbi]
outputs:
  phased:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
    secondaryFiles: [.tbi]
baseCommand: eagle
arguments:
  - prefix: "--geneticMapFile"
    valueFrom: $(inputs.map)
  - prefix: "--vcfRef"
    valueFrom: $(inputs.ref)
  - prefix: "--vcfTarget"
    valueFrom: $(inputs.target)
  - prefix: "--vcfOutFormat"
    valueFrom: "z"
  - prefix: "--outPrefix"
    valueFrom: $(inputs.sample)_phased_$(inputs.chr)
  - prefix: "--numThreads"
    valueFrom: $(runtime.cores)
  - shellQuote: false
    valueFrom: "&&"
  - "tabix"
  - prefix: "-p"
    valueFrom: "vcf"
  - "-f"
  - $(inputs.sample)_phased_$(inputs.chr).vcf.gz
