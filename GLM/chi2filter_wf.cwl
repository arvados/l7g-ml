$namespaces:
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"
requirements:
  DockerRequirement:
    dockerPull: l7g-ml/pythonr 
  ResourceRequirement:
    coresMin: 16
    ramMin: 32000
hints:
  cwltool:LoadListingRequirement: 
    loadListing: deep_listing
    
cwlVersion: v1.0
class: Workflow
inputs:
  get_data_file:
    type: File
    inputBinding:
      position: 1
  glmnet_file:
    type: File
    inputBinding:
      position: 2
  dbfile:
    type: File 
    inputBinding:
      position: 3

  allfile:
    type: File
    inputBinding:
      position: 4
  
  infofile:
    type: File
    inputBinding:
      position: 5

  namefile:
    type: File
    inputBinding:
      position: 6
  
  colorblood:
    type: string
    inputBinding:
      position: 7

  type_measure:
    type: string
    inputBinding:
      position: 8

outputs: 
  text_file: 
    type: File[]
    outputSource: glmnet/text_file
  graph:
    type: File
    outputSource: glmnet/graph
    
steps:
  gettingdata:
    in:
      get_data_file: get_data_file
      dbfile: dbfile
      allfile: allfile
      infofile: infofile
      namefile: namefile
      colorblood: colorblood
    out: [X, y, pathdataoh, oldpath, varvals]
    run: getting_data.cwl

  glmnet:
    in:
      glmnet_file: glmnet_file
      X: gettingdata/X
      y: gettingdata/y
      pathdataoh: gettingdata/pathdataoh
      oldpath: gettingdata/oldpath
      varvals: gettingdata/varvals
      colorblood: colorblood
      type_measure: type_measure

    out: [text_file,graph]
    run: glmnet.cwl