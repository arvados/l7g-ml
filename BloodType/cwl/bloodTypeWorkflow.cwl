cwlVersion: v1.0
class: CommandLineTool
baseCommand: python3
hints:
    ResourceRequirement:
        ramMin: 8192
        ramMax: 16384
    DockerRequirement:
        dockerPull: l7g-ml/py3_sci:v1.0
inputs:
    script_path:
        type: File
        inputBinding:
            position: 0
    data_dir_harvard_pgp_hiq_214:
        type: Directory
        inputBinding:
            position: 2
    data_dir_untap:
        type: Directory
        inputBinding:
            position: 4

outputs:
    plot_blood_type_totals:
        type: File
        outputBinding:
            glob: Blood_type_totals.png
    plot_confusion_A:
        type: File
        outputBinding:
            glob: A_Confusion.png
    plot_confusion_B:
        type: File
        outputBinding:
            glob: B_Confusion.png
    text_output:
        type: stdout
