cwlVersion: v1.0
class: CommandLineTool
inputs:
  script:
    type: File
    default:
      class: File
      location: recordstats.sh
  sample: string
  originalstats: File
  phasedstats: File
  original_imputed_evaldir: Directory
  original_imputedoutside_evaldir: Directory
outputs:
  statstsv: stdout
arguments:
  - $(inputs.script)
  - $(inputs.sample)
  - $(inputs.originalstats)
  - $(inputs.phasedstats)
  - $(inputs.original_imputed_evaldir.path)/summary.txt
  - $(inputs.original_imputedoutside_evaldir.path)/summary.txt
stdout: $(inputs.sample)_stats.tsv
