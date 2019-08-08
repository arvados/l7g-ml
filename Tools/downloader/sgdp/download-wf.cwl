#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
label: Simons Diversity from URL(s)

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
  fn_list:
    type: string[]
  url_list:
    type: string[]

outputs:
  result:
    type: File[]
    label: container with downloaded files
    outputSource: download-urls/result
    outputBinding:
      glob: "*.vcf.gz"
    secondaryFiles:
      - .md5sum

steps:
  download-urls:
    run: download-urls.cwl
    scatter: [url, filename]
    scatterMethod: dotproduct
    in:
      url: url_list
      filename: fn_list
    out:
      [result]
