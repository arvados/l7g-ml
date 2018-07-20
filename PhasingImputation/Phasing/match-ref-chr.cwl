cwlVersion: v1.0
class: ExpressionTool
requirements:
  InlineJavascriptRequirement: {}
inputs:
  chrs: string[]
  refsdir: Directory
outputs:
  refs:
    type: File[]
    secondaryFiles: [.tbi]
expression: |
  ${
    var refs = [];

    for (var i = 0; i < inputs.chrs.length; i++) {
      for (var j = 0; j < inputs.refsdir.listing.length; j++) {
        var file = inputs.refsdir.listing[j];
        if (file.nameext == ".gz" && file.basename.indexOf(inputs.chrs[i]+".") != -1) {
          var main = file;
        }
      }
      for (var j = 0; j < inputs.refsdir.listing.length; j++) {
        var file = inputs.refsdir.listing[j];
        if (file.basename == main.basename+".tbi") {
          main.secondaryFiles = [file]
        }
      }
      refs.push(main);
    }

    return {"refs": refs};
  }
