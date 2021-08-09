cwlVersion: v1.0
class: CommandLineTool
$namespaces:
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"

requirements:
  DockerRequirement:
    dockerPull: tileglm 
  ResourceRequirement:
    coresMin: 16
    ramMin: 450000

baseCommand: python

inputs:
  get_data_file:
    type: File
    inputBinding:
      position: 0
  dbfile:
    type: File
    inputBinding:
      position: 1
  allfile:
    type: File
    inputBinding:
      position: 2
  namefile:
    type: File
    inputBinding:
      position: 3
  phenotype:
    type: string
    inputBinding:
      position: 4
    
outputs:
  X:
    type: File
    outputBinding:
      glob: X.npy
  Xr:
    type: File
    outputBinding:
      glob: Xr.npy
  Xc:
    type: File
    outputBinding:
      glob: Xc.npy
  y:
    type: File
    outputBinding:
      glob: y.npy
  pathdataoh:
    type: File
    outputBinding:
      glob: pathdataOH.npy
  oldpath:
    type: File
    outputBinding:
      glob: oldpath.npy
  varvals:
    type: File
    outputBinding:
      glob: varvals.npy
  zygosity:
    type: File
    outputBinding:
      glob: zygosity.npy
