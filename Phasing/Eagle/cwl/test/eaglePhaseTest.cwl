cwlVersion: v1.0
class: CommandLineTool
baseCommand: /Eagle_v2.3.4/eagle
hints:
    DockerRequirement:
        dockerPull: l7g-ml/eagle:v2.0

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
        secondaryFiles:
            - .tbi
    target:
        type: File
        inputBinding:
            position: 3
            prefix: --vcfTarget
        secondaryFiles:
            - .tbi
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
    phased_file:
        type: File
        outputBinding:
            glob: GS12877_phased_chr19.vcf.gz
