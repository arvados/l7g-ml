$namespaces:
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"
requirements:
  DockerRequirement:
    dockerPull: l7g-ml/pythonr
  ResourceRequirement:
    coresMin: 16
    ramMin: 200698
hints:
  cwltool:LoadListingRequirement: 
    loadListing: deep_listing
cwlVersion: v1.0
class: CommandLineTool
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
  infofile:
    type: File
    inputBinding:
      position: 3
  namefile:
    type: File
    inputBinding:
      position: 4
  colorblood:
    type: string
    inputBinding:
      position: 5
    
outputs:
  X:
    type: File
    outputBinding:
      glob: X.npz
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
