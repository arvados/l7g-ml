#/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Downloads files from URL(s)

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
  - class: DockerRequirement
    dockerPull: cure/arvados-download

hints:
  arv:RuntimeConstraints:
    outputDirType: keep_output_dir
    keep_cache: 4096
  arv:APIRequirement: {}

baseCommand: bash
inputs:
  bashScript:
    type: File
    label: script handling curl and md5
    inputBinding:
      position: 1
  url:
    type: string
    label: url to download from
    inputBinding:
      position: 2

outputs:
  out1:
    type: File[]
    label: files generated from download and md5sum
    outputBinding:
      glob: "*"
