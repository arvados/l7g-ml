cwlVersion: v1.0
class: CommandLineTool
baseCommand: python3
hints:
    DockerRequirement:
        dockerPull: python3_science
inputs:
    script_path:
        type: File
        inputBinding:
            position: 0
    data_dir_1hot:
        type: Directory
        inputBinding:
            position: 2
    data_dir_ethn:
        type: Directory
        inputBinding:
            position: 4

outputs:
    plot_output:
        type: File
        outputBinding:
            glob: PCA12-Pop_cwl.png
