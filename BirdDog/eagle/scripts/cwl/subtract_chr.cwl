cwlVersion: v1.0
class: CommandLineTool
baseCommand: awk
hints:
    DockerRequirement:
        dockerPull: l7g-ml/eagle:v2.0
inputs:
    awk_string:
        type: string 
        inputBinding:
            position: 0
    vcf_file:
        type: File
        inputBinding:
            position: 1

outputs:
    vcf_output:
        type: stdout 
