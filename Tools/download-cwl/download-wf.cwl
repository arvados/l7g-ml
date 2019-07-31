#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
label: Downloads files from URL(s)

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
  - class: DockerRequirement
    dockerPull: curii/arvados-download
  - class: ScatterFeatureRequirement

hints:
  arv:RuntimeConstraints:
    outputDirType: keep_output_dir
  arv:ReuseRequirement:
    enableReuse: false
  arv:IntermediateOutput:
    outputTTL: 86400

inputs:
  bashScript:
    type: File
    label: script handling curl and md5
  
  urlFile:
    type: File
    label: list of URLs to download from

outputs:
  out1:
    type: File[]
    label: container with downloaded files
    outputBinding:
      glob: "*"
    outputSource: download-urls/out1

steps:
  get-urls:
    run: get-urls.cwl
    in:
      infile: urlFile
    out: [urls]

  downloadUrl:
    run: download-urls.cwl
    scatter: [url]
    scatterMethod: dotproduct
    in:
      bashScript: bashScript
      url: get-urls/urls
    out: [out1]
