class: ExpressionTool
cwlVersion: v1.2
inputs:
  files: File[]
  dirname:
    type: string
outputs:
  dir: Directory
requirements:
  InlineJavascriptRequirement: {}
expression: |
  ${
    var dir = {"class": "Directory",
               "basename": inputs.dirname,
               "listing": []};
    for (var i = 0; i < inputs.files.length; i++) {
      var file = inputs.files[i];
      file.basename = file.nameroot + "_" + i + file.nameext;
      dir.listing.push(file);
    }
    return {"dir": dir};
  }
