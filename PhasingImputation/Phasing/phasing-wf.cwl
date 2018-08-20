cwlVersion: v1.0
class: Workflow
$namespaces:
  arv: "http://arvados.org/cwl#"
requirements:
  ScatterFeatureRequirement: {}
  arv:RunInSingleContainer: {}
hints:
  DockerRequirement:
    dockerPull: l7g-ml/phasing
  ResourceRequirement:
    ramMin: 10000
inputs:
  sample: string
  chrs:
    type: string[]
    default: ["chr1","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr2","chr20","chr21","chr22","chr3","chr4","chr5","chr6","chr7","chr8","chr9"]
  refsdir: Directory
  map: File
  target:
    type: File
    secondaryFiles: [.tbi]

outputs:
  phasedvcfgz:
    type: File
    outputSource: bcftools-concat/vcfgz

steps:
  match-ref-chr:
    run: match-ref-chr.cwl
    in:
      chrs: chrs
      refsdir: refsdir
    out: [refs]
  eagle:
    scatter: [chr, ref]
    scatterMethod: dotproduct
    run: eagle.cwl
    in:
      sample: sample
      chr: chrs
      ref: match-ref-chr/refs
      target: target
      map: map
    out: [phased]
  bcftools-concat:
    run: bcftools-concat.cwl
    in:
      sample: sample
      vcfgzs: eagle/phased
    out: [vcfgz]
