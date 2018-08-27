cwlVersion: v1.0
class: Workflow
requirements:
  SubworkflowFeatureRequirement: {}
inputs:
  sample: string
  phasingrefsdir: Directory
  phasingmap: File
  imputationrefsdir: Directory
  imputationmapsdir: Directory
  target: #this is the original vcf
    type: File
    secondaryFiles: [.tbi]
  bedfile: File #this is the bedfile used for rtg vcffilter
  refdir: Directory #this is the reference for the rtgtools specific to target vcf

outputs:
  master:
    type: File
    secondaryFiles: [.tbi]
    outputSource: merge-phased-imputed/master
  statstsv:
    type: File
    outputSource: merge-phased-imputed/statstsv
  imputedvcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: phasing-imputation/imputedvcfgz
  phasedvcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: phasing-imputation/phasedvcfgz

steps:
  phasing-imputation:
    in: 
      sample: sample
      target: target
      phasingrefsdir: phasingrefsdir
      phasingmap: phasingmap
      imputationrefsdir: imputationrefsdir
      imputationmapsdir: imputationmapsdir
    run: phasing-imputation-wf.cwl
    out: [imputedvcfgz,phasedvcfgz]
  merge-phased-imputed:
    run: mastervcf/merge-phased-imputed-wf.cwl
    in:
      original: target
      sample: sample
      refdir: refdir
      bedfile: bedfile
      phased: phasing-imputation/phasedvcfgz
      imputed: phasing-imputation/imputedvcfgz
    out: [master, statstsv]
