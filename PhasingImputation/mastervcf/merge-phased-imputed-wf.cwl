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
  bedfile: File
  sample: string
  refdir: Directory
outputs:
  master:
    type: File
    secondaryFiles: [.tbi]
    outputSource: rtg-vcfmerge/master
  statstsv:
    type: File
    outputSource: stats-wf/statstsv
steps:
  rtg-vcffilter:
    run: rtg-vcffilter.cwl
    in:
      imputed: imputed
      bedfile: bedfile
      sample: sample
    out: [imputedexcluded]
  rtg-vcfmerge:
    run: rtg-vcfmerge.cwl
    in:
      original: original
      phased: phased
      imputedexcluded: rtg-vcffilter/imputedexcluded
      sample: sample
    out: [master]
  stats-wf:
    run: stats-wf.cwl
    in: 
      original: original
      phased: phased
      imputed: imputed
      imputedexcluded: rtg-vcffilter/imputedexcluded
      sample: sample
      refdir: refdir
    out: [statstsv]


    

  
      
