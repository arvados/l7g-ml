class: ExpressionTool
cwlVersion: v1.0
inputs:
  vcfsdir: Directory
outputs:
  samples: string[]
  vcfgzs:
    type: File[]
    secondaryFiles: [.tbi]
  beds: File[]
requirements:
  InlineJavascriptRequirement: {}
expression: |
  ${
    var samples = [];
    var vcfgzs = [];
    var beds = [];

    for (var i = 0; i < inputs.vcfsdir.listing.length; i++) {
      var file = inputs.vcfsdir.listing[i];
      if (file.nameext == '.gz') {
        var sample = file.nameroot.split('.').slice(0,-1).join('.');
        var main = file;
        for (var j = 0; j < inputs.vcfsdir.listing.length; j++) {
          var file = inputs.vcfsdir.listing[j];
          if (file.basename == main.basename+".tbi") {
            main.secondaryFiles = [file];
          } else if (file.basename == sample+".bed") {
            var bed = file;
          }
        }
        samples.push(sample);
        vcfgzs.push(main);
        beds.push(bed);
      }
    }

    return {"samples": samples, "vcfgzs": vcfgzs, "beds": beds};
  }
