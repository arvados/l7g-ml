cwlVersion: v1.0
class: CommandLineTool
$namespaces:
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"

requirements:
  DockerRequirement:
    dockerPull: tileglm 
  ResourceRequirement:
    coresMin: 8 
    ramMin: 200000

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
  annotationfile:
    type: File 
    inputBinding:
      position: 4
    
outputs:
  Xoutput:
    type: File
    outputBinding:
      glob: X*.npy
  y:
    type: File
    outputBinding:
      glob: y*.npy
  pathdataoh:
    type: File
    outputBinding:
      glob: pathdataOH*.npy
  oldpath:
    type: File
    outputBinding:
      glob: oldpath*.npy
  varvals:
    type: File
    outputBinding:
      glob: varvals*.npy
  zygosity:
    type: File
    outputBinding:
      glob: zygosity*.npy
