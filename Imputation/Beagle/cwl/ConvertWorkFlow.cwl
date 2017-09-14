$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: Workflow
requirements:
  - class: DockerRequirement
    dockerPull: javatools
  - class: ResourceRequirement
    coresMin: 2
    coresMax: 2
  - class: ScatterFeatureRequirement
  - class: InlineJavascriptRequirement
  - class: SubworkflowFeatureRequirement
hints:
  arv:RuntimeConstraints:
    keep_cache: 4096
inputs:
  refdirectory: Directory
  bashscript: File 
  pastafile: File
  refstreamfile: File
  reffile: File

outputs:
  out1:
    type: File[]
    outputSource: step2/out1

steps:
  step1:
    run: GetFilesGFF.cwl
    in: 
      refdirectory: refdirectory
    out: [out1]

  step2:
    scatter: filename
    scatterMethod: dotproduct
    in: 
         filename: step1/out1
         bashscript: bashscript
         pastafile: pastafile
         refstreamfile: refstreamfile
         reffile: reffile
    run: Convert2vcf.cwl
    out: [out1]
