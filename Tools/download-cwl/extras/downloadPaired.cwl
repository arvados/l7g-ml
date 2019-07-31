#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
  - class: DockerRequirement
    dockerPull: cure/arvados-download
  - class: ScatterFeatureRequirement

hints:
  arv:RuntimeConstraints:
    outputDirType: keep_output_dir
  arv:ReuseRequirement:
    enableReuse: false
  arv:IntermediateOutput:
    outputTTL: 86400

inputs:
  bashScript: File
  urlFile: File

outputs:
  out:
    type: Directory[]
    outputSource: collectOutput/out2
    outputBinding:
      glob: "*"

steps:
  readUrlList:
    run: readUrlList.cwl
    in: 
      infile: urlFile
    out: [urls]

  downloadUrl:
    run: downloadUrl.cwl
    scatter: [url]
    scatterMethod: dotproduct
    in:
      bashScript: bashScript
      url: readUrlList/urls
    out: [out1]

  collectOutput:
    run: reorganizeDirectory.cwl
    in:
      input: downloadUrl/out1
    out: [out2]
