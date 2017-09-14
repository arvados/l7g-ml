$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: DockerRequirement
    dockerPull: java8
  - class: ResourceRequirement
    coresMin: 1
    coresMax: 1
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement 
    listing:
      - $(inputs.jar_file) 
hints:
  arv:RuntimeConstraints:
    keep_cache: 4096 
baseCommand: java
inputs:
  jar_file:
    type: File
    inputBinding:
      position: 1
      prefix: "-jar"
  reference:
    type: File
    inputBinding:  
      position: 2
      prefix: "ref="
      separate: false
  target:
    type: File
    inputBinding:
      position: 3
      prefix: "gt="
      separate: false
  outputprefix:
    type: string
    inputBinding:
      position: 4
      prefix: "out="
      separate: false
  fileformap:
    type: File
    inputBinding:
      position: 5 
      prefix: "map="
      separate: false
  numthreads:
     type: string
     inputBinding:
       position: 6
       prefix: "nthreads="
       separate: false
  windowsize:
     type: string
     inputBinding:
       position: 7
       prefix: "window="
       separate: false
  windowoverlap:
     type: string
     inputBinding:
       position: 8
       prefix: "overlap="
       separate: false

outputs:
  out1:
    type: File
    outputBinding:
      glob: "*.log"
  out2:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
