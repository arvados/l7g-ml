$namespaces:
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"
requirements:
  DockerRequirement:
    dockerPull: glmextra
  ResourceRequirement:
    coresMin: 2
    ramMin: 100000
hints:
  cwltool:LoadListingRequirement: 
    loadListing: deep_listing
cwlVersion: v1.0
class: CommandLineTool
inputs: 
  glmnet_file:
    type: File
    inputBinding:
      position: 0
  X:
    type: File
    inputBinding:
      position: 1
  Xr:
    type: File
    inputBinding:
      position: 2
  Xc:
    type: File
    inputBinding:
      position: 3
  y:
    type: File
    inputBinding:
      position: 4
  pathdataoh:
    type: File
    inputBinding:
      position: 5
  oldpath:
    type: File
    inputBinding:
      position: 6
  varvals:
    type: File
    inputBinding:
      position: 7
  zygosity:
    type: File
    inputBinding:
      position: 8
  colorblood:
    type: string
    inputBinding:
      position: 9
  type_measure:
    type: string
    inputBinding:
      position: 10 
outputs: 
  text_file:
    type: File[]
    outputBinding:
      glob: "*.txt"

  graph:
    type: File[]
    outputBinding:
      glob: "*.png"

baseCommand: Rscript
