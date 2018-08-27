cwlVersion: v1.0
class: Workflow
requirements:
  SubworkflowFeatureRequirement: {}
inputs:
  original: 
    type: File
    secondaryFiles: [.tbi]
  phased: 
    type: File
    secondaryFiles: [.tbi]
  imputed: 
    type: File
    secondaryFiles: [.tbi]
  imputedexcluded:
    type: File
    secondaryFiles: [.tbi]
  sample: string
  refdir: Directory
outputs:
  statstsv:
    type: File
    outputSource: recordstats/statstsv
steps:
  vcfstats-original:
    run: vcfstats-original.cwl
    in: 
      original: original
      sample: sample
    out: [originalstats]
  vcfstats-phased:
    run: vcfstats-phased.cwl
    in:
      phased: phased
      sample: sample
    out: [phasedstats]
  vcfeval-original-imputed:
    run: vcfeval-original-imputed.cwl
    in:
      original: original
      imputed: imputed
      sample: sample
      refdir: refdir
    out: [original_imputed_evaldir]
  vcfeval-original-imputedexcluded:
    run: vcfeval-original-imputedexcluded.cwl
    in:
      original: original
      imputedexcluded: imputedexcluded
      sample: sample
      refdir: refdir
    out: [original_imputedexcluded_evaldir]
  recordstats:
    run: recordstats.cwl
    in:
      originalstats: vcfstats-original/originalstats
      phasedstats: vcfstats-phased/phasedstats
      original_imputed_evaldir: vcfeval-original-imputed/original_imputed_evaldir
      original_imputedexcluded_evaldir: vcfeval-original-imputedexcluded/original_imputedexcluded_evaldir
      sample: sample
    out: [statstsv]
  
