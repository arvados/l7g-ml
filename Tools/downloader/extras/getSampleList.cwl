#/usr/bin/env cwl-runner

cwlVersion: v1.0
class: ExpressionTool

$namespaces:
  arv: "http://arvados.org/cwl#"
  cwltool: "http://commonwl.org/cwltool#"

requirements:
- class: InlineJavascriptRequirement

inputs:
  inputCollection:
    type: Directory
    inputBinding:
      loadContents: true

outputs:
  directories:
    type: Directory[]

expression: |
  ${
     var directories = [];
     for (var i = 0; i < inputs.inputCollection.listing.length; i++) {
       var file = inputs.inputCollection.listing[i];
       if (file.class == 'Directory') {
         var pushit = 1;
         // Handle this in md5sum.sh so we can 'copy' the inputs there
         // Downside: some compute node usage.
         //for (var j = 0; j < file.listing.length; j++) {
         //  var f2 = file.listing[j];
         //  if (f2.basename == file.basename+".bam.md5sum") {
         //    pushit = 0;
         //  }
         //}
         if (pushit == 1) {
           directories.push(file);
         }
       }
     }
     return { 'directories': directories } ;
   }
