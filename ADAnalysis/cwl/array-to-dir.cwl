class: ExpressionTool
cwlVersion: v1.1

inputs:
  filearray: File[]  
  dirname: string
outputs:
  dir: Directory
requirements:
  InlineJavascriptRequirement: {}

expression: |
  ${
    var dir = {"class": "Directory",
               "basename": inputs.dirname,
               "listing": []};
    for (var i = 0; i < inputs.filedarray.length; i++) {
        dir.listing.push(inputs.nestedarray[i][j]);
      }
    }
    return {"dir": dir};
  }
