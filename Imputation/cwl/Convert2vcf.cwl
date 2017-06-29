$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: DockerRequirement
    dockerPull: javatools
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    coresMin: 2
    coresMax: 2
hints:
  arv:RuntimeConstraints:
    keep_cache: 4096
baseCommand: bash 
inputs:
  bashscript:
    type: File
    inputBinding:
      position: 1
  filename:
    type: File
    inputBinding:  
      position: 2
  pastafile:
    type: File
    inputBinding:
      position: 3
  refstreamfile:
    type: File
    inputBinding:
      position: 4
  reffile:
    type: File
    inputBinding:
      position: 5 
outputs:
  out1:
    type: File
    outputBinding:
      glob: "*_FinalAll.vcf.gz"
