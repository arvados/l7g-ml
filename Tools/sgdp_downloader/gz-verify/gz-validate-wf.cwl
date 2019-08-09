$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
cwlVersion: v1.0
class: Workflow
label: (workflow) Test file integrity of gzip compressed files
requirements:
  - class: DockerRequirement
    dockerPull: curii/arvados-download
  - class: ResourceRequirement
    coresMin: 1
    ramMin: 12000
  - class: ScatterFeatureRequirement
inputs:
  gzipdir:
    type: Directory
    label: Directory containing compressed VCF, md5sum, and index files for processing
outputs:
  validated:
    type: File[]
    label: Directory containing .vld (validate status) files
    outputSource: gz-validate/validated
steps:
  get-gzip:
    run: get-gzip.cwl
    in:
      gzipdir: gzipdir
    out: [gzips, filenames]
  gz-validate:
    run: gz-validate.cwl
    scatter: [zipped, filename]
    scatterMethod: dotproduct
    in:
      zipped: get-gzip/gzips
      filename: get-gzip/filenames
    out: [validated]
