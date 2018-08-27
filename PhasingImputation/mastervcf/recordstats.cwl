cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: InlineJavascriptRequirement
arguments:
  - $(inputs.script)
  - $(inputs.originalstats)
  - $(inputs.phasedstats)
  - "$(inputs.original_imputed_evaldir.path)/summary.txt"
  - "$(inputs.original_imputedexcluded_evaldir.path)/summary.txt"
  - $(inputs.sample)
  - $(inputs.sample)_stats.tsv
inputs:
  script:
    type: File
    default: 
      class: File
      location: bash_vcfstats.sh
  originalstats: File
  phasedstats: File
  original_imputed_evaldir: Directory
  original_imputedexcluded_evaldir: Directory
  sample: string
outputs:
  statstsv:
    type: File
    outputBinding: 
      glob: "*.tsv"
