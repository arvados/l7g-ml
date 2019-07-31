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
  inputCollection: Directory

outputs:
  out1:
    type: Directory[]
    outputBinding:
      glob: "*"
    outputSource: calculateMd5sum/out1

steps:
  getSampleList:
    run: getSampleList.cwl
    in: 
      inputCollection: inputCollection
    out: [directories]

  calculateMd5sum:
    run: calculateMd5sum.cwl
    scatter: [dir]
    scatterMethod: dotproduct
    in:
      bashScript: bashScript
      keepDir: inputCollection
      dir: getSampleList/directories
    out: [out1]
