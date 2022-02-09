# ROVAS - Risk Object Visual Analysis System for BIMProve project
Includes 
 - bimprove_rest - Visual detection as a REST service
 - clunk_integrator - Clunky integration with visualization to Pydio based image storage and Fuseki database

 ```mermaid
graph TB

  SubGraph1 --> SubGraph1Flow
  subgraph "SubGraph 1 Flow"
  SubGraph1Flow(SubNode 1)
  SubGraph1Flow -- Choice1 --> DoChoice1
  SubGraph1Flow -- Choice2 --> DoChoice2
  end

  subgraph "Main Graph"
  Node1[Node 1] --> Node2[Node 2]
  Node2 --> SubGraph1[Jump to SubGraph1]
  SubGraph1 --> FinalThing[Final Thing]
end
```
