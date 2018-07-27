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

outputs:
  imputedvcfgzs:
    type: File[]
    outputSource: phasing-imputation/imputedvcfgz
  phasedvcfgz:
    type: File[]
    outputSource: phasing-imputation/phasedvcfgz

steps:
  getfiles:
    run: getfiles.cwl
    in: 
      vcfsdir: vcfsdir
    out: [samples,targets]
  phasing-imputation:
    scatter: [sample, target]
    scatterMethod: dotproduct
    in: 
      sample: getfiles/samples
      target: getfiles/targets
      phasingrefsdir: phasingrefsdir
      phasingmap: phasingmap
      imputationrefsdir: imputationrefsdir
      imputationmapsdir: imputationmapsdir
    run: phasing-imputation-wf.cwl
    out: [imputedvcfgz,phasedvcfgz]
