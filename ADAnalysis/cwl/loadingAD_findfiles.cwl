$namespaces:
  cwltool: "http://commonwl.org/cwltool#"
class: ExpressionTool
label: Create list of gVCFs from directory
cwlVersion: v1.1
requirements:
  InlineJavascriptRequirement: {}
hints:
  LoadListingRequirement:
    loadListing: shallow_listing
inputs:
  numpydir:
    type: Directory
    label: Directory of input tiled numpy files
  annotationdir:
    type: Directory
    label: Directory of input annotation files
outputs:
  numpyfiles:
    type: File[]
    label: Array of tiled numpy files
  annotationfiles:
    type: File[]
    label: Array of annotation files
expression: |
  ${
    var numpyfiles = [];
    var annotationfiles = [];

    for (var i = 0; i < inputs.numpydir.listing.length; i++) {
      var file = inputs.numpydir.listing[i];
      if (file.nameext == '.npy') {
        var main = file;
        for (var j = 0; j < inputs.annotationdir.listing.length; j++) {
          var file2 = inputs.annotationdir.listing[j];
          if (file2.basename == main.nameroot+'.annotations.csv') {
            var main2 = file2;
            annotationfiles.push(main2);
          }
        }
        numpyfiles.push(main);
       }
    }
    return {"numpyfiles": numpyfiles,"annotationfiles": annotationfiles};
  }
