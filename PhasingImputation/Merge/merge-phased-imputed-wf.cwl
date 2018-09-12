cwlVersion: v1.0
class: Workflow
$namespaces:
  arv: "http://arvados.org/cwl#"
requirements:
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
  originalbed: File
  phasedvcfgz:
    type: File
    secondaryFiles: [.tbi]
  rawimputedvcfgz:
    type: File
    secondaryFiles: [.tbi]
outputs:
  mergedvcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: rtg-vcfmerge/mergedvcfgz
  mergedbed:
    type: File
    outputSource: bedops-merge/mergedbed
  imputedvcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: grep-home-ref/imputedvcfgz
  imputedoutsidevcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: rtg-vcffilter/imputedoutsidevcfgz
steps:
  grep-home-ref:
    run: grep-hom-ref.cwl
    in:
      sample: sample
      rawimputedvcfgz: rawimputedvcfgz
    out: [imputedvcfgz]
  gvcf_regions:
    run: gvcf_regions.cwl
    in:
      sample: sample
      rawimputedvcfgz: rawimputedvcfgz
    out: [rawimputedbed]
  bedops-merge:
    run: bedops-merge.cwl
    in:
      sample: sample
      originalbed: originalbed
      rawimputedbed: gvcf_regions/rawimputedbed
    out: [mergedbed]
  rtg-vcffilter:
    run: rtg-vcffilter.cwl
    in:
      sample: sample
      imputedvcfgz: grep-home-ref/imputedvcfgz
      originalbed: originalbed
    out: [imputedoutsidevcfgz]
  rtg-vcfmerge:
    run: rtg-vcfmerge.cwl
    in:
      sample: sample
      originalvcfgz: originalvcfgz
      phasedvcfgz: phasedvcfgz
      imputedoutsidevcfgz: rtg-vcffilter/imputedoutsidevcfgz
    out: [mergedvcfgz]
