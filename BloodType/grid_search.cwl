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
    ramMin: 250000
    coresMin: 12
    outdirMin: 50000
    tmpdirMin: 50000
stdout: $("grid_search_output.txt")
hints:
  arv:RuntimeConstraints:
    keep_cache: 1500
baseCommand: python
inputs:
  script:
    type: File
    inputBinding:
      position: 0
  x_data:
    type: File
    inputBinding:
      position: 1
  y_data:
    type: File
    inputBinding:
      position: 2
outputs:
  enc_out:
    type: stdout
  pkl_out:
    type: File[]
    outputBinding:
      glob: "*pkl"
