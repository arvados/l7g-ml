$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: DockerRequirement
    dockerPull: kfang/dask
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    ramMin: 150000
    coresMin: 4 
stdout: $("1-hot_output.txt")
hints:
  arv:RuntimeConstraints:
    keep_cache: 1500
baseCommand: python
inputs:
  script:
    type: File
    inputBinding:
      position: 0
  all_tiles:
    type: File
    inputBinding:
      position: 1
  names:
    type: File
    inputBinding:
      position: 2
  all_info:
    type: File
    inputBinding:
      position: 3
  untap:
    type: File
    inputBinding:
      position: 4
outputs:
  enc_out:
    type: stdout
