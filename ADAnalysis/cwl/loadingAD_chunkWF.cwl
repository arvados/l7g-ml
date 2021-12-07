cwlVersion: v1.0
class: Workflow
$namespaces:
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"

requirements:
  DockerRequirement:
    dockerPull: tileglm 
  ResourceRequirement:
    coresMin: 8 
    ramMin: 200000
  ScatterFeatureRequirement: {}

inputs:
  get_data_file:
    type: File
  dbfile:
    type: File
  numpydir:
    type: Directory
  namefile:
    type: File
  annotationdir:
    type: Directory 
    
outputs:
  Xoutput:
    type: File[]
    outputSource: filter/Xoutput
  y:
    type: File[]
    outputSource: filter/y
  pathdataoh:
    type: File[]
    outputSource: filter/pathdataoh
  oldpath:
    type: File[]
    outputSource: filter/oldpath
  varvals:
    type: File[]
    outputSource: filter/varvals
  zygosity:
    type: File[]
    outputSource: filter/zygosity

steps:
  findfiles:
    run: loadingAD_findfiles.cwl
    in:
      numpydir: numpydir
      annotationdir: annotationdir
    out: [numpyfiles,annotationfiles]

  filter:
    run: loadingAD_chunk.cwl
    scatter: [allfile,annotationfile]
    scatterMethod: dotproduct
    in:
      get_data_file: get_data_file
      dbfile: dbfile
      allfile: findfiles/numpyfiles
      namefile: namefile
      annotationfile: findfiles/annotationfiles
    out: [Xoutput,y,pathdataoh,oldpath,varvals,zygosity]

  array-to-dir-X:
    run: array-to-dir.cwl
    in:
      nestedarray: filter/Xoutput
      dirname:
        valueFrom: "Xdir"
    out: [Xdir]
    
  array-to-dir-y:
    run: array-to-dir.cwl
    in:
      nestedarray: filter/y
      dirname:
        valueFrom: "ydir"
    out: [ydir]
   
  array-to-dir-pathoh:
    run: array-to-dir.cwl
    in:
      nestedarray: filter/pathdataoh
      dirname:
        valueFrom: "pathdatadir"
    out: [pathdatadir]

  array-to-dir-oldpath:
    run: array-to-dir.cwl
    in:
      nestedarray: filter/oldpath
      dirname:
        valueFrom: "oldpathdir"
    out: [oldpathdir]

  array-to-dir-varvals:
    run: array-to-dir.cwl
    in:
      nestedarray: filter/varvals
      dirname:
        valueFrom: "varvaldir"
    out: [varvaldir]

  array-to-dir-zygosity:
    run: array-to-dir.cwl
    in:
      nestedarray: filter/zygosity
      dirname:
        valueFrom: "zygositydir"
    out: [zygositydir]

