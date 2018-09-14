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
  vcfgz:
    type: File
    secondaryFiles: [.tbi]
  bed: File
  recordstatsscript:
    type: File
    default:
      class: File
      location: Getstats/recordstats.sh
  sdf: Directory

outputs:
  phasedvcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: phasing-wf/phasedvcfgz
  imputedvcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: merge-phased-imputed-wf/imputedvcfgz
  mergedvcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: merge-phased-imputed-wf/mergedvcfgz
  mergedbed:
    type: File
    outputSource: merge-phased-imputed-wf/mergedbed
  statstsv:
    type: File
    outputSource: getstats-wf/statstsv

steps:
  phasing-wf:
    run: Phasing/phasing-wf.cwl
    in:
      sample: sample
      refsdir: phasingrefsdir
      map: phasingmap
      target: vcfgz
    out: [phasedvcfgz]
  imputation-wf:
    run: Imputation/imputation-wf.cwl
    in:
      sample: sample
      refsdir: imputationrefsdir
      mapsdir: imputationmapsdir
      target: phasing-wf/phasedvcfgz
    out: [rawimputedvcfgz]
  merge-phased-imputed-wf:
    run: Merge/merge-phased-imputed-wf.cwl
    in:
      sample: sample
      originalvcfgz: vcfgz
      originalbed: bed
      phasedvcfgz: phasing-wf/phasedvcfgz
      rawimputedvcfgz: imputation-wf/rawimputedvcfgz
    out: [mergedvcfgz, mergedbed, imputedvcfgz, imputedoutsidevcfgz]
  getstats-wf:
    run: Getstats/getstats-wf.cwl
    in:
      sample: sample
      originalvcfgz: vcfgz
      phasedvcfgz: phasing-wf/phasedvcfgz
      imputedvcfgz: merge-phased-imputed-wf/imputedvcfgz
      imputedoutsidevcfgz: merge-phased-imputed-wf/imputedoutsidevcfgz
      sdf: sdf
      recordstatsscript: recordstatsscript
    out: [statstsv]
