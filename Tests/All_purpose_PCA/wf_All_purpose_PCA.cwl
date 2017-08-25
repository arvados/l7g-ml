cwlVersion: v1.0
class: Workflow
inputs:
    input_1hot_data: File

outputs:
   plotout:
       type: File
       outputSource: pca/plot_output
   textout:
       type: File
       outputSource: pca/text_output

steps:
    pca:
        run: All_purpose_PCA.cwl
        in:
            script_path:
                default: keep:4add3257391c278826bfd591f49d48d8+66/All_purpose_PCA.py
            data_1hot_file: input_1hot_data
        out:
            [plot_output, text_output]
