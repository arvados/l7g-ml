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
    data_1hot_file:
        type: File 
        inputBinding:
            position: 1

outputs:
    plot_output:
        type: File
        outputBinding:
            glob: All_purpose_PCA_output_plot.png
    text_output:
        type: stdout
