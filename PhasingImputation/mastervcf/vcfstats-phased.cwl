cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
baseCommand: [rtg, vcfstats]
arguments:
  - $(inputs.phased)
inputs:
  sample: string
  phased: 
    type: File
    secondaryFiles: [.tbi]
outputs:
  phasedstats: stdout
stdout: $(inputs.sample)_phasedstats.txt
