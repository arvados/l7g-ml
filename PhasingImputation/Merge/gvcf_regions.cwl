cwlVersion: v1.0
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
inputs:
  sample: string
  rawimputedvcfgz: File
outputs:
  rawimputedbed: stdout
baseCommand: /gvcf_regions/gvcf_regions.py
arguments:
  - $(inputs.rawimputedvcfgz)
stdout: $(inputs.sample)_rawimputed.bed
