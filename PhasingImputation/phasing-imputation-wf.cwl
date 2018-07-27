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
  target:
    type: File
    secondaryFiles: [.tbi]

outputs:
  imputedvcfgz:
    type: File
    outputSource: imputation-wf/imputedvcfgz
  phasedvcfgz:
    type: File
    outputSource: phasing-wf/phasedvcfgz

steps:
  phasing-wf:
    run: Phasing/phasing-wf.cwl
    in:
      sample: sample
      refsdir: phasingrefsdir
      map: phasingmap
      target: target
    out: [phasedvcfgz]
  imputation-wf:
    run: Imputation/imputation-wf.cwl
    in:
      sample: sample
      refsdir: imputationrefsdir
      mapsdir: imputationmapsdir
      target: phasing-wf/phasedvcfgz
    out: [imputedvcfgz]
      
