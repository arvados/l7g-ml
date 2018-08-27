class: ExpressionTool
cwlVersion: v1.0
inputs:
  vcfsdir: Directory
outputs:
  samples: string[]
  targets:
    type: File[]
    secondaryFiles: [.tbi]
  bedfiles: File[]
requirements:
  InlineJavascriptRequirement: {}
expression: |
  ${
    var samples = [];
    var targets = [];
    var bedfiles = [];
    for (var i = 0; i < inputs.vcfsdir.listing.length; i++) {
      var file = inputs.vcfsdir.listing[i];
      if (file.nameext == '.gz') {
        samples.push(file.nameroot.split('.').slice(0,-1).join('.'));
        targets.push(file);
        var j=0;
        //this adds all the bedfiles in the same order 
        do{ 
          var bed = inputs.vcfsdir.listing[j];
          var index = samples.length - 1;
          if(samples[index]+".bed" == bed.basename) { 
            bedfiles.push(bed);
            j = inputs.vcfsdir.listing.length;
          }
          j++;
        } while (j<inputs.vcfsdir.listing.length)
      }
    }
    
    //adds secondaryFiles parameter to the files in targets[]
    for(var i = 0; i < inputs.vcfsdir.listing.length; i++) {
      var secondaryF = inputs.vcfsdir.listing[i];
      if (secondaryF.nameext == '.tbi') {
        for (var j = 0; j < targets.length; j++) { 
          if(targets[j].basename+".tbi" == secondaryF.basename) {
            targets[j].secondaryFiles = [secondaryF];
          }
        }
      }
    }
    
    return {"samples": samples, "targets": targets, "bedfiles": bedfiles};
  }
