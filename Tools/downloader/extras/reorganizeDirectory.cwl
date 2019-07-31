#/usr/bin/env cwl-runner

cwlVersion: v1.0
class: ExpressionTool

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
- class: InlineJavascriptRequirement

inputs:
  input: Directory[]
outputs:
  out2: Directory[]

expression: |
  ${
    var samples = {};
    for (var j = 0; j < inputs.input.length; j++) {
      var dir = inputs.input[j];
      for (var i = 0; i < dir.listing.length; i++) {
        var file = dir.listing[i];
        var groups = file.basename.match(/^(.+)(_)(.+)$/);
        if (groups) {
          if (!samples[groups[1]]) {
            samples[groups[1]] = [];
          }
          samples[groups[1]].push(file);
        }
      }
    }
    var dirs = [];
    for (var key in samples) {
      dirs.push({"class": "Directory",
                 "basename": key,
                 "listing": samples[key]});
    }
    return {"out2": dirs};
  }
