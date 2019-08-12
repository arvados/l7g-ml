$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"
requirements:
  InlineJavascriptRequirement: {}
hints:
  cwltool:LoadListingRequirement:
    loadListing: deep_listing
cwlVersion: v1.0
class: ExpressionTool
label: Get listing of ggzipped files and associated filenames
inputs:
  gzipdir:
    type: Directory
    label: Directory containing compressed VCF, md5sum, and index files for processing
outputs:
  gzips:
    type: File[]
    label: Array of compressed VCF files from input directory
  filenames:
    type: string[]
    label: Array of file names to maintain naming convention for integrity files
expression: |
  ${
    var gzips = [];
    var filenames = [];

    for (var i = 0; i < inputs.gzipdir.listing.length; i++) {
      var file = inputs.gzipdir.listing[i];
      if (file.nameext == '.gz') {
        var main = file;
        var baseName = file.nameroot.split(".")[0];
        gzips.push(main);
        filenames.push(baseName);
      }
    }
    return { "gzips": gzips, "filenames": filenames };
  }
