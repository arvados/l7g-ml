cwlVersion: v1.0
class: CommandLineTool
baseCommand: /Eagle_v2.3.4/eagle
hints:
    DockerRequirement:
        dockerPull: l7g-ml/eagle:v1.0

inputs:
    genetic_map:
        type: File
        inputBinding:
            position: 1
            prefix:  --geneticMapFile
    reference_panel:
        type: File
        inputBinding:
            position: 2
            prefix: --vcfRef
    target:
        type: File
        inputBinding:
            position: 3
            prefix: --vcfTarget
    output_format:
        type: string
        inputBinding:
            position: 4
            prefix: --vcfOutFormat=
            separate: false
    output_prefix:
        type: string
        inputBinding:
            position: 5
            prefix: --outPrefix
    impute_missing:
        type: boolean
        inputBinding:
            position: 6
            prefix: --noImpMissing

outputs:
    text_output:
        type: stdout
