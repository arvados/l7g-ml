cwlVersion: v1.0
class: Workflow
$namespaces:
  arv: "http://arvados.org/cwl#"
requirements:
  StepInputExpressionRequirement: {}
  arv:RunInSingleContainer: {}
hints:
  DockerRequirement:
    dockerPull: l7g-ml/vcfutil
  ResourceRequirement:
    ramMin: 5000
inputs:
  sample: string
  originalvcfgz:
    type: File
    secondaryFiles: [.tbi]
  phasedvcfgz:
    type: File
    secondaryFiles: [.tbi]
  imputedvcfgz:
    type: File
    secondaryFiles: [.tbi]
  imputedoutsidevcfgz:
    type: File
    secondaryFiles: [.tbi]
  sdf: Directory
  recordstatsscript: File
outputs:
  statstsv:
    type: File
    outputSource: recordstats/statstsv
steps:
  rtg-vcfstats_original:
    run: rtg-vcfstats.cwl
    in:
      sample: sample
      suffix:
        valueFrom: "original"
      vcfgz: originalvcfgz
    out: [statstxt]
  rtg-vcfstats_phased:
    run: rtg-vcfstats.cwl
    in:
      sample: sample
      suffix:
        valueFrom: "phased"
      vcfgz: phasedvcfgz
    out: [statstxt]
  rtg-vcfeval_original-imputed:
    run: rtg-vcfeval.cwl
    in:
      sample: sample
      suffix:
        valueFrom: "original-imputed"
      baselinevcfgz: originalvcfgz
      callsvcfgz: imputedvcfgz
      sdf: sdf
    out: [evaldir]
  rtg-vcfeval_original-imputedoutside:
    run: rtg-vcfeval.cwl
    in:
      sample: sample
      suffix:
        valueFrom: "original-imputedoutside"
      baselinevcfgz: originalvcfgz
      callsvcfgz: imputedoutsidevcfgz
      sdf: sdf
    out: [evaldir]
  recordstats:
    run: recordstats.cwl
    in:
      script: recordstatsscript
      sample: sample
      originalstats: rtg-vcfstats_original/statstxt
      phasedstats: rtg-vcfstats_phased/statstxt
      original_imputed_evaldir: rtg-vcfeval_original-imputed/evaldir
      original_imputedoutside_evaldir: rtg-vcfeval_original-imputedoutside/evaldir
    out: [statstsv]
