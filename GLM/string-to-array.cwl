class: ExpressionTool
cwlVersion: v1.2
requirements:
  InlineJavascriptRequirement: {}
inputs:
  str:
    type: string
outputs:
  randomseeds:
    type: string[]
expression: |
  ${
    var randomseeds = inputs.str.trim().split('\n');
    return {"randomseeds": randomseeds};
  }

