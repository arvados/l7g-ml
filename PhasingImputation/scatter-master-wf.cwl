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
  refdir: Directory
  
outputs:
  master:
    type: File[]
    outputSource: master-wf/master
  statsfile:
    type: File
    outputSource: catstats/statsfile
  imputedvcfgz:
    type: File[]
    outputSource: master-wf/imputedvcfgz
  phasedvcfgz:
    type: File[]
    outputSource: master-wf/phasedvcfgz

steps:
  getfiles:
    run: getfiles.cwl
    in: 
      vcfsdir: vcfsdir
    out: [samples,targets,bedfiles]
  master-wf:
    scatter: [sample, target, bedfile]
    scatterMethod: dotproduct
    in: 
      sample: getfiles/samples
      target: getfiles/targets
      bedfile: getfiles/bedfiles
      phasingrefsdir: phasingrefsdir
      phasingmap: phasingmap
      imputationrefsdir: imputationrefsdir
      imputationmapsdir: imputationmapsdir
      refdir: refdir
    run: master-wf.cwl
    out: [master,statstsv,imputedvcfgz,phasedvcfgz]
  catstats:
    run: catstats.cwl
    in: 
      statstxt: master-wf/statstsv
    out: [statsfile]
