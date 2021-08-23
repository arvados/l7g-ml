$namespaces:
  cwltool: "http://commonwl.org/cwltool#"
class: ExpressionTool
label: Create list of gVCFs from directory
cwlVersion: v1.0

requirements:
  InlineJavascriptRequirement: {}

inputs:
  Nseeds:
    type: int
    label: Number of input seeds

outputs:
  randomseed:
    type: string[]
    label: Array of random seeds 

expression: |
  ${
    var randomseed = [];
    var t = []
    t = inputs.Nseeds

    for (var i=0, t; i<t; i++) {
        randomseed.push(Math.round(Math.random() * 1000).toString())
   }
 
    return {"randomseed": randomseed};
  }

