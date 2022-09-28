cwlVersion: v1.2
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: glm
inputs:
  script:
    type: File
    default:
      class: File
      location: src/generateSeeds.py
  seedsnumber:
    type: int
  seedslimit:
    type: int
outputs:
  seedsstr:
    type: string
    outputBinding:
      glob: seeds.txt
      loadContents: true
      outputEval: $(self[0].contents)
baseCommand: python3
arguments:
  - $(inputs.script)
  - $(inputs.seedsnumber)
  - $(inputs.seedslimit)
stdout: seeds.txt
