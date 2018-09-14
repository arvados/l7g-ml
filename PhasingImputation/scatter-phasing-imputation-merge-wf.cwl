cwlVersion: v1.0
class: Workflow
requirements:
  ScatterFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  phasingrefsdir: Directory
  phasingmap: File
  imputationrefsdir: Directory
  imputationmapsdir: Directory
  vcfsdir: Directory
  sdf: Directory

outputs:
  mergedvcfgz:
    type: File[]
    outputSource: phasing-imputation-merge-wf/mergedvcfgz
  mergedbed:
    type: File[]
    outputSource: phasing-imputation-merge-wf/mergedbed
  statstsv:
    type: File[]
    outputSource: phasing-imputation-merge-wf/statstsv

steps:
  get-samples:
    run: get-samples.cwl
    in: 
      vcfsdir: vcfsdir
    out: [samples, vcfgzs, beds]
  phasing-imputation-merge-wf:
    scatter: [sample, vcfgz, bed]
    scatterMethod: dotproduct
    run: phasing-imputation-merge-wf.cwl
    in:
      sample: get-samples/samples
      phasingrefsdir: phasingrefsdir
      phasingmap: phasingmap
      imputationrefsdir: imputationrefsdir
      imputationmapsdir: imputationmapsdir
      vcfgz: get-samples/vcfgzs
      bed: get-samples/beds
      sdf: sdf
    out: [phasedvcfgz, imputedvcfgz, mergedvcfgz, mergedbed, statstsv]
