cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
baseCommand: [rtg, vcfstats]
arguments:
  - $(inputs.original)
inputs:
  sample: string
  original: 
    type: File
    secondaryFiles: [.tbi]
outputs:
  originalstats: stdout
stdout: $(inputs.sample)_originalstats.txt
