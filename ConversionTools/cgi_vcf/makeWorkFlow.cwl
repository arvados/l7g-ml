$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: Workflow
requirements:
  - class: DockerRequirement
    dockerPull: pythonsimple 
  - class: ResourceRequirement
    coresMin: 2 
    coresMax: 10000
  - class: ScatterFeatureRequirement
  - class: InlineJavascriptRequirement
  - class: SubworkflowFeatureRequirement

inputs:
  reference: File
  refdirectory: Directory

outputs:
  out1:
    type: File[]
    outputSource: step2/out1

steps:
  step1:
    run: getFiles.cwl
    in: 
      refdirectory: refdirectory
    out: [out1]

  step2:
    scatter: originalfile 
    scatterMethod: dotproduct
    in: 
         originalfile: step1/out1
         reference: reference
    run: makeVCF.cwl
    out: [out1]
