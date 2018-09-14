cwlVersion: v1.0
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
baseCommand: [rtg, vcfstats]
inputs:
  sample: string
  suffix: string
  vcfgz: 
    type: File
    secondaryFiles: [.tbi]
outputs:
  statstxt: stdout
arguments:
  - $(inputs.vcfgz)
stdout: $(inputs.sample)_$(inputs.suffix)_stats.txt
