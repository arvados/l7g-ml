class: ExpressionTool
cwlVersion: v1.0
inputs:
  refdirectory: Directory
  mapdirectory: Directory
outputs:
  out1: File[]
  out2: File[]
  out3: string[]
requirements:
  InlineJavascriptRequirement: {}
expression: |
  ${
    var samples = [];
    var samples2 = [];
    var samples3 = [];
    for (var i = 0; i < inputs.refdirectory.listing.length; i++) {
      var file = inputs.refdirectory.listing[i];
      var filename = file.basename;
      var parts = filename.split("\.",1);
        for (var j = 0; j < inputs.mapdirectory.listing.length; j++) {
          var mapfile = inputs.mapdirectory.listing[j];
          var mapfilename = mapfile.basename;
          var teststr = parts + ".G"
          var result = mapfilename.indexOf(teststr) > -1;
          
          if (result) {
            samples.push(file)
            samples2.push(mapfile)
            samples3.push(parts + "imput")
          }
        }
    }
    return {"out1": samples, "out2": samples2, "out3": samples3};
  } 
