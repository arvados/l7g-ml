cwlVersion: v1.0
class: CommandLineTool
requirements:
  ShellCommandRequirement: {}
hints:
  ResourceRequirement:
    coresMin: 2
    ramMin: 6000
inputs:
  sample: string
  chr: string
  ref:
    type: File
    secondaryFiles: [.tbi]
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
    valueFrom: "/Eagle_v2.4/tables/genetic_map_hg19_withX.txt.gz"
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
