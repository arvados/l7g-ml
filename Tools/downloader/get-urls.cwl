#/usr/bin/env cwl-runner

cwlVersion: v1.0
class: ExpressionTool
label: parses list of URLs and generates an array to scatter over

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
- class: InlineJavascriptRequirement

inputs:
  infile:
    type: File
    label: list of URLs to download from
    inputBinding:
      loadContents: true

outputs:
  urls:
    type: string[]

expression: "${var lines = inputs.infile.contents.split('\\n');
               var nblines = lines.length;
               var urls = [];
               for (var i = 0; i < nblines; i++) {
                  var line = lines[i];
                  if (line) {
                    urls.push(line);
                  }
                }
               return { 'urls': urls } ;
              }"
