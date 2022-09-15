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
    ramMin: 250000

baseCommand: python

inputs:
  get_data_file:
    type: File
    inputBinding:
      position: 0
  allfiledir:
    type: Directory
    inputBinding:
      position: 1 
  namefile:
    type: File
    inputBinding:
      position: 2 
    
outputs:
  tiledPCA:
    type: File
    outputBinding:
      glob: tiledPCA.npy
  labels:
    type: File
    outputBinding:
      glob: labels.csv
