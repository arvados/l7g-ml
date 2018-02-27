cwlVersion: v1.0
class: CommandLineTool
baseCommand: bash 
hints:
    DockerRequirement:
        dockerPull: l7g-ml/eagle:v3.0
inputs:
    eagle_script:
        type: File
        inputBinding:
            position: 1
    directory_of_reference_panel:
        type: Directory 
        inputBinding:
            position: 2
    target_vcf:
        type: File
        inputBinding:
            position: 3

outputs:
    all_text_output:
        type: stdout 
    phased_vcfs:
        type: File[]
        outputBinding:
            glob: GS12877_phased_chr*
