cwlVersion: v1.0
class: CommandLineTool
baseCommand: [cat]
arguments:
  - $(inputs.script)
  - $(inputs.statstxt)
inputs:
  statstxt: File[]
  script:
    type: File
    default: 
      class: File
      location: header.txt
outputs:
  statsfile: stdout
stdout: vcfstats.tsv
