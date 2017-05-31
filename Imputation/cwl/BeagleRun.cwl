cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: DockerRequirement
    dockerPull: java8
  - class: ResourceRequirement
    coresMin: 4
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement 
    listing:
      - $(inputs.jar_file) 
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
outputs:
  out1:
    type: File
    outputBinding:
      glob: "*.log"
  out2:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
