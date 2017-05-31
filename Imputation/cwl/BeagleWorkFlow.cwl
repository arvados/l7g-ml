cwlVersion: v1.0
class: Workflow
requirements:
  - class: DockerRequirement
    dockerPull: java8
  - class: ResourceRequirement
    coresMin: 4
  - class: ScatterFeatureRequirement
  - class: InlineJavascriptRequirement
  - class: SubworkflowFeatureRequirement
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.jar_file)

inputs:
  jar_file: 
    type: File
    inputBinding:
      valueFrom: $(self.basename)
  refdir: Directory
  mapdir: Directory
  target: File

outputs:
  out1:
    type: File[]
    outputSource: step2/out1
  out2:
    type: File[]
    outputSource: step2/out2

steps:
  step1:
    run: BeagleGetFilesFinal.cwl
    in: 
      refdirectory: refdir
      mapdirectory: mapdir
    out: [out1, out2, out3]

  step2:
    scatter: [reference, fileformap, outputprefix]
    scatterMethod: dotproduct
    in: 
         reference: step1/out1
         fileformap: step1/out2
         jar_file: jar_file
         target: target
         outputprefix: step1/out3 
    run: BeagleRun.cwl
    out: [out1,out2]
