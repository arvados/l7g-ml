cwlVersion: v1.0
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
inputs:
  sample: string
  originalbed: File
  rawimputedbed: File
outputs:
  mergedbed: stdout
baseCommand: [bedops, --merge]
arguments:
  - $(inputs.originalbed)
  - $(inputs.rawimputedbed)
stdout: $(inputs.sample)_merged.bed
