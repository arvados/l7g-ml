cwlVersion: v1.0
class: Workflow
requirements:
  SubworkflowFeatureRequirement: {}
inputs:
  sample: string
  phasingrefsdir: Directory
  imputationrefsdir: Directory
  mapsdir: Directory
  target:
    type: File
    secondaryFiles: [.tbi]

outputs:
  imputedvcfgz:
    type: File
    outputSource: imputation-wf/imputedvcfgz

steps:
  phasing-wf:
    run: Phasing/phasing-wf.cwl
    in:
      sample: sample
      refsdir: phasingrefsdir
      target: target
    out: [phasedvcfgz]
  imputation-wf:
    run: Imputation/imputation-wf.cwl
    in:
      sample: sample
      refsdir: imputationrefsdir
      mapsdir: mapsdir
      target: phasing-wf/phasedvcfgz
    out: [imputedvcfgz]
      
