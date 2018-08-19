$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    coresMin: 2
    ramMin: 10000
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.originalfile)
  - class: DockerRequirement
    dockerPull: cgitools2
    
hints:
  arv:RuntimeConstraints:
    keep_cache: 4096

baseCommand: cgatools
arguments: ["mkvcf","--beta", "--output",  $(inputs.originalfile.nameroot).vcf, "--field-names", "GT,FT,HQ,EHQ,GQ", "--source-names","masterVar", "--include-no-calls"] 
inputs:
  originalfile:
    type: File
    inputBinding:
      prefix: --master-var
      position: 1
      valueFrom: $(self.basename) 
  reference:
    type: File 
    inputBinding:
      prefix: --reference
      position: 2
  

outputs:
  out1:
    type: File 
    outputBinding:
      glob: "*.vcf"

