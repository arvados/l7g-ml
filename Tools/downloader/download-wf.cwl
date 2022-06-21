#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow
label: Downloads files from URL(s)

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
  - class: DockerRequirement
    dockerPull: cure/awscli-download
  - class: ScatterFeatureRequirement

hints:
  arv:RuntimeConstraints:
    outputDirType: keep_output_dir
  arv:ReuseRequirement:
    enableReuse: false
  arv:IntermediateOutput:
    outputTTL: 86400
  arv:WorkflowRunnerResources:
    ramMin: 4096
    coresMin: 2
    keep_cache: 2048
  cwltool:Secrets:
    secrets: [accessKey,secretKey]

inputs:
  bashScript:
    type: File
    label: script handling curl and md5

  urlFile:
    type: File
    label: list of URLs to download from

  accessKey: string
  secretKey: string

outputs:
  out1:
    type:
      type: array
      items:
        type: array
        items: File
    label: downloaded files
    outputSource: downloadUrls/out1

steps:
  get-urls:
    run: get-urls.cwl
    in:
      infile: urlFile
    out: [urls]

  downloadUrls:
    run: download-urls.cwl
    scatter: [url]
    scatterMethod: dotproduct
    in:
      bashScript: bashScript
      url: get-urls/urls
      accessKey: accessKey
      secretKey: secretKey
    out: [out1]
