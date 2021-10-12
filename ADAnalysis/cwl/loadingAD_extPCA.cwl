cwlVersion: v1.1
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: tileglm 
  ResourceRequirement:
    coresMin: 16
    ramMin: 450000
inputs:
  get_data_file:
    type: File
    default:
      class: File
      location: ../loadingAD_zygosity_extPCA.py
      secondaryFiles:
        - class: Directory
          location: ../../tileml
        - class: Directory
          location: ../../adml
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
  PCAfile:
    type: File
    inputBinding:
      position: 5
  PCAnamesfile:
    type: File
    inputBinding:
      position: 6
  qualcutoff:
    type: float
    inputBinding:
      position: 7
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
baseCommand: python
