#/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
  - class: DockerRequirement
    dockerPull: cure/arvados-download

hints:
  arv:RuntimeConstraints:
    keep_cache: 4096
  arv:APIRequirement: {}

baseCommand: bash
inputs:
  bashScript:
    type: File
    inputBinding:
      position: 1
  keepDir:
    type: Directory
    inputBinding:
      position: 2
  dir:
    type: Directory
    inputBinding:
      position: 3

outputs:
  out1:
    type: Directory
    outputBinding:
      glob: "*"
