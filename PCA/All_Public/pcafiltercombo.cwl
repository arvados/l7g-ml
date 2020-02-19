$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: DockerRequirement
    dockerPull: l7g-ml/pythonr 
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    ramMin: 320698 
    coresMin: 16 
hints:
  arv:RuntimeConstraints:
    keep_cache: 1500
baseCommand: python
inputs:
  pcafunc:
    type: File
    inputBinding:
      position: 1
  tilefile1:
    type: File 
    inputBinding:
      position: 2
  tileinfo1:
    type: File
    inputBinding:
      position: 3
  tilefile2:
    type: File
    inputBinding:
      position: 4
  tileinfo2:
    type: File
    inputBinding:
      position: 5

outputs:
  out1:
    type: File[]
    outputBinding:
      glob: "*npz"
