#/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool
label: Downloads files from URL(s)

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
  DockerRequirement:
    dockerPull: curii/arvados-download
  InitialWorkDirRequirement:
    listing:
      - entryname: secrets.conf
        entry: |
          [default]
          aws_access_key_id=$(inputs.accessKey)
          aws_secret_access_key=$(inputs.secretKey)

hints:
  arv:RuntimeConstraints:
    outputDirType: keep_output_dir
    keep_cache: 1048
  ResourceRequirement:
    ramMin: 2048
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
  accessKey: string
  secretKey: string

outputs:
  out1:
    type: File[]
    label: files generated from download and md5sum
    outputBinding:
      glob: ["*gz","*md5sum","*tbi"]
