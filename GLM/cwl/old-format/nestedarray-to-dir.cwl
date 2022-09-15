class: ExpressionTool
cwlVersion: v1.1
inputs:
  nestedarray:
    type:
      type: array
      items:
        type: array
        items: [File, Directory]
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
    for (var i = 0; i < inputs.nestedarray.length; i++) {
      for (var j = 0; j < inputs.nestedarray[i].length; j++) {
        dir.listing.push(inputs.nestedarray[i][j]);
      }
    }
    return {"dir": dir};
  }
