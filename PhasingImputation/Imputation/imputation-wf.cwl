cwlVersion: v1.0
class: Workflow
$namespaces:
  arv: "http://arvados.org/cwl#"
requirements:
  ScatterFeatureRequirement: {}
  arv:RunInSingleContainer: {}
hints:
  DockerRequirement:
    dockerPull: l7g-ml/imputation
  ResourceRequirement:
    ramMin: 10000
inputs:
  sample: string
  chrs:
    type: string[]
    default: ["chr1","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr2","chr20","chr21","chr22","chr3","chr4","chr5","chr6","chr7","chr8","chr9"]
  refsdir: Directory
  mapsdir: Directory
  target:
    type: File
    secondaryFiles: [.tbi]

outputs:
  rawimputedvcfgz:
    type: File
    secondaryFiles: [.tbi]
    outputSource: bcftools-concat/vcfgz

steps:
  match-ref-map-chr:
    run: match-ref-map-chr.cwl
    in:
      chrs: chrs
      refsdir: refsdir
      mapsdir: mapsdir
    out: [refs, maps]
  beagle:
    scatter: [chr, ref, map]
    scatterMethod: dotproduct
    run: beagle.cwl
    in:
      sample: sample
      chr: chrs
      ref: match-ref-map-chr/refs
      map: match-ref-map-chr/maps
      target: target
    out: [rawimputed]
  bcftools-concat:
    run: bcftools-concat.cwl
    in:
      sample: sample
      vcfgzs: beagle/rawimputed
    out: [vcfgz]
