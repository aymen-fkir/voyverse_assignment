
# Example
#### input
```txt
 Enter your query (or type 'exit' to quit): /c MATCH path = (source:data_sources)-[*1..2]-(t:technique) RETURN DISTINCT startNode(relationships(path)[0]) AS a, relationships(path)[0] AS r, endNode(relationships(path)[0]) AS b
Executing manual query: MATCH path = (source:data_sources)-[*1..2]-(t:technique) RETURN DISTINCT startNode(relationships(path)[0]) AS a, relationships(path)[0] AS r, endNode(relationships(path)[0]) AS b
2026-06-19 00:26:40 | INFO     | ChatPipeline | Executed query against Neo4j | total_records=14
```
--- [Seeded Graph Context] ---
#### output
```txt
### Graph Path 1:
  * Node A: (attack-pattern--88a794e9-fa8c-5185-a677-bf476cd8890b:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': "Research labs at academic institutions and company R&D divisions often have blogs that highlight their use of artificial intelligence and its application to the organization's unique problems.\nIndividual researchers also frequently document their work in blogposts.\nAn adversary may search for posts made by the target victim organization or its employees.\nIn comparison to [Journals and Conference Proceedings](/techniques/AML.T0000.000) and [Pre-Print Repositories](/techniques/AML.T0000.001) this material will often contain more practical aspects of the AI system.\nThis could include underlying technologies and frameworks used, and possibly some information about the API access and use case.\nThis will help the adversary better understand how that organization is using AI internally and the details of their approach that could aid in tailoring an attack.", 'id': 'attack-pattern--88a794e9-fa8c-5185-a677-bf476cd8890b'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 2:
  * Node A: (attack-pattern--8eb979a1-1e5a-5955-8a7d-df82ecb14088:Node) -> Attributes: {'created': '2026-04-22T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries may acquire publicly accessible AI agent configuration files to understand agent capabilities, gain unauthorized access to tools and data sources, or identify credentials for further attacks. Configuration files define what tools an agent can use, credentials for external services, system prompts, and behavioral settings, making valuable resources for adversaries targeting AI agent deployments.\n\nOnce configuration files are acquired, adversaries may perform [Discover AI Agent Configuration](/techniques/AML.T0084) to gain additional insights they can use in their operation or [Credentials from AI Agent Configuration](/techniques/AML.T0083) to harvest secrets.\n\nAI agent configuration files come in multiple forms depending on the platform and agent framework. Agent configuration files adversaries may target include:\n- System prompts: Files containing agent instructions, behavioral guidelines, and internal logic.\n- Tool configuration: Files defining tools the agent can utilize, including Model Context Protocol (MCP) configs (e.g., `mcp.json`, `claude_desktop_config.json`), IDE-specific configs (e.g., `.claude/settings.json`, `.vscode/tasks.json`), and framework-specific settings that define external tool and data source integrations.\n- Skills and workflows: Files defining agent capabilities, behaviors, or workflows. Often a combination of instructions, scripts, and resources.\n- Environment and deployment configs: Files that control agent deployment and runtime behavior, often environment variables or framework-specific configs.', 'id': 'attack-pattern--8eb979a1-1e5a-5955-8a7d-df82ecb14088'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 3:
  * Node A: (attack-pattern--298dc6c6-5683-5475-b724-2a2a3db3a7dc:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': "Adversaries may replicate a private model.\nBy repeatedly querying the victim's [AI Model Inference API Access](/techniques/AML.T0040), the adversary can collect the target model's inferences into a dataset.\nThe inferences are used as labels for training a separate model offline that will mimic the behavior and performance of the target model.\n\nA replicated model that closely mimic's the target model is a valuable resource in staging the attack.\nThe adversary can use the replicated model to [Craft Adversarial Data](/techniques/AML.T0043) for various purposes (e.g. [Evade AI Model](/techniques/AML.T0015), [Spamming AI System with Chaff Data](/techniques/AML.T0046)).", 'id': 'attack-pattern--298dc6c6-5683-5475-b724-2a2a3db3a7dc'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 4:
  * Node A: (attack-pattern--0855cdf6-5b4f-5586-a658-942b7222ede7:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries may search private sources to identify AI learning artifacts that exist on the system and gather information about them.\nThese artifacts can include the software stack used to train and deploy models, training and testing data management systems, container registries, software repositories, and model zoos.\n\nThis information can be used to identify targets for further collection, exfiltration, or disruption, and to tailor and improve attacks.', 'id': 'attack-pattern--0855cdf6-5b4f-5586-a658-942b7222ede7'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}                                                                                                                                              * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}
### Graph Path 5:
  * Node A: (attack-pattern--2bc7b6ec-2304-5913-8b0c-bb92ba135724:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries may acquire consumer hardware to conduct their attacks.\nOwning the hardware provides the adversary with complete control of the environment. These devices can be hard to trace.', 'id': 'attack-pattern--2bc7b6ec-2304-5913-8b0c-bb92ba135724'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}                                                                                                                                              * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 6:                                                                                                                                                                                * Node A: (attack-pattern--647ac4ac-b2bc-53f7-ab83-81f421a1f0b5:Node) -> Attributes: {'created': '2026-03-30T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries may utilize commercial proxy services that resell access to AI services such as frontier model APIs.\n\nThis infrastructure can be used to conduct large-scale campaigns to perform [Exfiltration via AI Inference API](/techniques/AML.T0024) via distillation. Adversaries may also use this infrastructure to [Generate Malicious Commands](/techniques/AML.T0102) for offensive cyber operations, or to generate content for [Spearphishing via Social Engineering LLM](/techniques/AML.T0052.000).\n\nCommercial AI service proxies distribute traffic from different accounts and various cloud platforms. The mix of traffic can make malicious activity difficult to detect and block [[anthropic]].\n\nMalicious actors conduct [LLM Jacking](https://atlas.mitre.org/studies/AML.CS0030) attacks to gain access to victim accounts which they resell access to in their proxy services [[sysdig]].', 'id': 'attack-pattern--647ac4ac-b2bc-53f7-ab83-81f421a1f0b5'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 7:
  * Node A: (attack-pattern--2ea180c5-5df4-5815-8c78-a1cec1da6e18:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries may gain initial access to a system by compromising the unique portions of the AI supply chain.\nThis could include [Hardware](/techniques/AML.T0010.000), [Data](/techniques/AML.T0010.002) and its annotations, parts of the AI [AI Software](/techniques/AML.T0010.001) stack, or the [Model](/techniques/AML.T0010.003) itself.\nIn some instances the attacker will need secondary access to fully carry out an attack using compromised components of the supply chain.', 'id': 'attack-pattern--2ea180c5-5df4-5815-8c78-a1cec1da6e18'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 8:
  * Node A: (attack-pattern--1a1c3b28-eeab-52d0-87cf-4ba0a7ff687a:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'AI-enabled systems often rely on open sourced models in various ways.\nMost commonly, the victim organization may be using these models for fine tuning.\nThese models will be downloaded from an external source and then used as the base for the model as it is tuned on a smaller, private dataset.\nLoading models often requires executing some saved code in the form of a saved model file.\nThese can be compromised with traditional malware, or through some adversarial AI techniques.', 'id': 'attack-pattern--1a1c3b28-eeab-52d0-87cf-4ba0a7ff687a'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}                                                                                                                                              * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 9:
  * Node A: (attack-pattern--757f3580-72e6-514d-9770-af3ee98a1a0b:Node) -> Attributes: {'created': '2024-04-11T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': "An adversary may compromise a victim's container registry by pushing a manipulated container image and overwriting an existing container name and/or tag. Users of the container registry as well as automated CI/CD pipelines may pull the adversary's container image, compromising their AI Supply Chain. This can affect development and deployment environments.\n\nContainer images may include AI models, so the compromised image could have an AI model which was manipulated by the adversary (See [Manipulate AI Model](/techniques/AML.T0018)).", 'id': 'attack-pattern--757f3580-72e6-514d-9770-af3ee98a1a0b'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 10:
  * Node A: (attack-pattern--a5cc5062-f672-510a-8a4f-a8d1aa7f5024:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries may develop unsafe AI artifacts that when executed have a deleterious effect.\nThe adversary can use this technique to establish persistent access to systems.\nThese models may be introduced via a [AI Supply Chain Compromise](/techniques/AML.T0010).\n\nSerialization of models is a popular technique for model storage, transfer, and loading.\nHowever, this format without proper checking presents an opportunity for code execution.', 'id': 'attack-pattern--a5cc5062-f672-510a-8a4f-a8d1aa7f5024'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 11:
  * Node A: (attack-pattern--ed66b442-059b-54cb-a806-620e6f8109a6:Node) -> Attributes: {'created': '2022-01-24T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access.\nCredentials may take the form of usernames and passwords of individual user accounts or API keys that provide access to various AI resources and services.\n\nCompromised credentials may provide access to additional AI artifacts and allow the adversary to perform [Discover AI Artifacts](/techniques/AML.T0007).\nCompromised credentials may also grant an adversary increased privileges such as write access to AI artifacts used during development or production.', 'id': 'attack-pattern--ed66b442-059b-54cb-a806-620e6f8109a6'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

                                                                                                             ### Graph Path 12:
  * Node A: (attack-pattern--d74153d6-ac3c-52fb-9847-e0a6f675cd93:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries can [Craft Adversarial Data](/techniques/AML.T0043) that prevents an AI model from correctly identifying the contents of the data or [Generate Deepfakes](/techniques/AML.T0088) that fools an AI model expecting authentic data.\n\nThis technique can be used to evade a downstream task where AI is utilized. The adversary may evade AI-based virus/malware detection or network scanning towards the goal of a traditional cyber attack. AI model evasion through deepfake generation may also provide initial access to systems that use AI-based biometric authentication.', 'id': 'attack-pattern--d74153d6-ac3c-52fb-9847-e0a6f675cd93'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 13:
  * Node A: (attack-pattern--6635775c-5539-5512-95f1-a0e085770699:Node) -> Attributes: {'created': '2025-03-12T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': 'Adversaries may search for and obtain generative AI models or tools, such as large language models (LLMs), to assist them in various steps of their operation. Generative AI can be used in a variety of malicious ways, such as to generating malware, to [Generate Deepfakes](/techniques/AML.T0088), to [Generate Malicious Commands](/techniques/AML.T0102), for [Retrieval Content Crafting](/techniques/AML.T0066), or to generate [Phishing](/techniques/AML.T0052) content.\n\nAdversaries may obtain open source models and serve them locally using frameworks such as [Ollama](https://ollama.com/) or [vLLM]( https://docs.vllm.ai/en/latest/). They may host them using cloud infrastructure. Or, they may leverage AI service providers such as HuggingFace.\n\nThey may need to jailbreak the model (see [LLM Jailbreak](/techniques/AML.T0054)) to bypass any restrictions put in place to limit the types of responses it can generate. They may also need to break the terms of service of the model\'s developer.\n\nGenerative AI models may also be "uncensored" meaning they are designed to generate content without any restrictions such as guardrails or content filters. Uncensored GenAI is ripe for abuse by cybercriminals [[blog]] [[gbhackers]]. Models may be fine-tuned to remove alignment and guardrails [[erichartford]] or be subjected to targeted manipulations to bypass refusal [[arxiv]] resulting in uncensored variants of the model. Uncensored models may be built for offensive and defensive cybersecurity [[taico]], which can be abused by an adversary. There are also models that are expressly designed and advertised for malicious use [[gbhackers-1]].', 'id': 'attack-pattern--6635775c-5539-5512-95f1-a0e085770699'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

### Graph Path 14:
  * Node A: (attack-pattern--04641d66-7ecd-5b83-a3da-938e11a81254:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'modified': '2026-05-27T00:00:00.000Z', 'description': "Adversaries may directly modify an AI model's architecture to re-define it's behavior. This can include adding or removing layers as well as adding pre or post-processing operations.\n\nThe effects could include removing the ability to predict certain classes, adding erroneous operations to increase computation costs, or degrading performance. Additionally, a separate adversary-defined network could be injected into the computation graph, which can change the behavior based on the inputs, effectively creating a backdoor.", 'id': 'attack-pattern--04641d66-7ecd-5b83-a3da-938e11a81254'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}
```
------------------------------
Success: Context stored. Please enter your follow-up question now.
#### input
```txt
Enter your query (or type 'exit' to quit): How do hackers use our public data to plan an attack on our AI?
Processing question using your custom seeded graph context...
```
### output
```txt
Response from the model: Okay, here's a concise summary of the relationships and insights from the provided text, focusing on the key takeaways:

**Core Concept:** The text details how adversaries are increasingly targeting AI models – specifically large language models – by directly manipulating their architecture, potentially introducing backdoors, and bypassing security measures.

**Key Points:**

*   **Architectural Manipulation:** Adversaries are attempting to directly alter the AI model's structure (layers, operations) to compromise its behavior.
*   **Deepfake Generation & Generative AI:** A significant focus is on using generative AI models (like LLMs) to create deepfakes, malicious commands, and phishing content.
*   **Bypass Mechanisms:**  The text highlights techniques like jailbreaking, modifying the network graph, and injecting separate networks to evade detection.
*   **Tools & Techniques:** The text mentions specific tools like Ollama and vLLM, and the concept of "uncensored" GenAI models.
*   **Backdoor & Data Manipulation:** There's a clear emphasis on creating backdoors and manipulating data to gain access to AI systems.

**Overall Impression:** The text paints a concerning picture of an evolving threat landscape where attackers are actively probing and exploiting vulnerabilities within AI models, potentially with significant consequences.

Do you want me to elaborate on any specific aspect or provide a more detailed analysis?
```
# Example
#### input
```txt 
Enter your query (or type 'exit' to quit): /c MATCH (t:technique)-[r:Target]->(layer) WHERE layer.type IN ['model', 'data_sources', 'infrastructure', 'application'] RETURN t AS a, r, layer AS b
Executing manual query: MATCH (t:technique)-[r:Target]->(layer) WHERE layer.type IN ['model', 'data_sources', 'infrastructure', 'application'] RETURN t AS a, r, layer AS b
```
#### output
```txt
Received notification from DBMS server: <GqlStatusObject gql_status='01N52', status_description='warn: property key does not exist. The property `type` does not exist in database `neo4j`. Verify that the spelling is correct.', position=<SummaryInputPosition line=1, column=53, offset=52>, raw_classification='UNRECOGNIZED', classification=<NotificationClassification.UNRECOGNIZED: 'UNRECOGNIZED'>, raw_severity='WARNING', severity=<NotificationSeverity.WARNING: 'WARNING'>, diagnostic_record={'_classification': 'UNRECOGNIZED', '_severity': 'WARNING', '_position': {'offset': 52, 'line': 1, 'column': 53}, 'OPERATION': '', 'OPERATION_CODE': '0', 'CURRENT_SCHEMA': '/'}> for query: "MATCH (t:technique)-[r:Target]->(layer) WHERE layer.type IN ['model', 'data_sources', 'infrastructure', 'application'] RETURN t AS a, r, layer AS b"
2026-06-19 00:27:40 | INFO     | ChatPipeline | Executed query against Neo4j | total_records=0
--- [Seeded Graph Context] ---
No relevant information found in the graph database.
------------------------------
Success: Context stored. Please enter your follow-up question now.
```
#### input
```txt
Enter your query (or type 'exit' to quit): pass
Processing question using your custom seeded graph context...
```
#### output
```txt
Response from the model: The user is requesting a definition of “pass”. There is no graph data to interpret.
```
# Example
#### input 
```txt
Enter your query (or type 'exit' to quit): /c MATCH (arxiv:technique)-[r:Target]->(layer) WHERE arxiv.description CONTAINS "arXiv" OR arxiv.description CONTAINS "Pre-Print" RETURN arxiv AS a, r, layer AS b
Executing manual query: MATCH (arxiv:technique)-[r:Target]->(layer) WHERE arxiv.description CONTAINS "arXiv" OR arxiv.description CONTAINS "Pre-Print" RETURN arxiv AS a, r, layer AS b
```
#### output
```txt
2026-06-19 00:28:33 | INFO     | ChatPipeline | Executed query against Neo4j | total_records=3
--- [Seeded Graph Context] ---
### Graph Path 1:
  * Node A: (attack-pattern--c02f812d-59cc-5366-b1aa-7eb05154b772:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'description': 'Adversaries may search for publicly available research and technical documentation to learn how and where AI is used within a victim organization.\nThe adversary can use this information to identify targets for attack, or to tailor an existing attack to make it more effective.\nOrganizations often use open source model architectures trained on additional proprietary data in production.\nKnowledge of this underlying architecture allows the adversary to craft more realistic proxy models ([Create Proxy AI Model](/techniques/AML.T0005)).\nAn adversary can search these resources for publications for authors employed at the victim organization.\n\nResearch and technical materials may exist as academic papers published in [Journals and Conference Proceedings](/techniques/AML.T0000.000), or stored in [Pre-Print Repositories](/techniques/AML.T0000.001), as well as [Technical Blogs](/techniques/AML.T0000.002).', 'modified': '2026-05-27T00:00:00.000Z', 'id': 'attack-pattern--c02f812d-59cc-5366-b1aa-7eb05154b772'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-application-c842d4e2-5b8b-4cd8-afdb-15c6478648a8:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093761', 'modified': '2026-06-18 23:24:40.093761', 'description': 'Application Layer', 'id': 'node-application-c842d4e2-5b8b-4cd8-afdb-15c6478648a8'}

### Graph Path 2:
  * Node A: (attack-pattern--02ea7626-0eec-5a4b-98ff-b3f21733b783:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'description': "Pre-Print repositories, such as arXiv, contain the latest academic research papers that haven't been peer reviewed.\nThey may contain research notes, or technical reports that aren't typically published in journals or conference proceedings.\nPre-print repositories also serve as a central location to share papers that have been accepted to journals.\nSearching pre-print repositories  provide adversaries with a relatively up-to-date view of what researchers in the victim organization are working on.", 'modified': '2026-05-27T00:00:00.000Z', 'id': 'attack-pattern--02ea7626-0eec-5a4b-98ff-b3f21733b783'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-infrastructure-9abf90fa-2f04-4d5a-8d18-ffa8c28c1841:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093798', 'modified': '2026-06-18 23:24:40.093798', 'description': 'Infrastructure Layer', 'id': 'node-infrastructure-9abf90fa-2f04-4d5a-8d18-ffa8c28c1841'}

### Graph Path 3:
  * Node A: (attack-pattern--88a794e9-fa8c-5185-a677-bf476cd8890b:Node) -> Attributes: {'created': '2021-05-13T00:00:00.000Z', 'description': "Research labs at academic institutions and company R&D divisions often have blogs that highlight their use of artificial intelligence and its application to the organization's unique problems.\nIndividual researchers also frequently document their work in blogposts.\nAn adversary may search for posts made by the target victim organization or its employees.\nIn comparison to [Journals and Conference Proceedings](/techniques/AML.T0000.000) and [Pre-Print Repositories](/techniques/AML.T0000.001) this material will often contain more practical aspects of the AI system.\nThis could include underlying technologies and frameworks used, and possibly some information about the API access and use case.\nThis will help the adversary better understand how that organization is using AI internally and the details of their approach that could aid in tailoring an attack.", 'modified': '2026-05-27T00:00:00.000Z', 'id': 'attack-pattern--88a794e9-fa8c-5185-a677-bf476cd8890b'}
  * Relationship: -[:CONNECTED_TO]-> Attributes: {}
  * Node B: (node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe:Node) -> Attributes: {'created': '2026-06-18 23:24:40.093811', 'modified': '2026-06-18 23:24:40.093811', 'description': 'Data Sources Layer', 'id': 'node-data_sources-fae3f580-7cc7-4d80-8e9d-ed00a8013abe'}

------------------------------
Success: Context stored. Please enter your follow-up question now.
```
#### input
```txt
Enter your query (or type 'exit' to quit): Is it dangerous to upload our model data to arXiv before a security review?
Processing question using your custom seeded graph context...
```
### output
```txt
Response from the model: Okay, here’s a summary of the graph data, focusing on the potential dangers of uploading model data to arXiv:

**Overall Assessment:**

The data suggests a significant risk of adversaries exploiting arXiv for research and potentially gaining insights into your organization’s AI practices. The connections between nodes highlight a deliberate search for information – particularly regarding your organization’s AI architecture and techniques.

**Key Risks & Insights:**

*   **Information Leakage:** arXiv is a primary source for academic research.  Uploading model data exposes your work to potential scrutiny and, crucially, to researchers actively seeking to understand your AI systems.
*   **Target Identification:** The data reveals that researchers are searching for information about your organization’s AI, including details about its architecture, techniques, and internal processes. This could lead to targeted attacks.
*   **Attack Targeting:** The data suggests that adversaries are using arXiv to understand how your organization is using AI internally, which could inform the creation of more effective attacks.
*   **Technological Analysis:** The data indicates that researchers are examining your organization's AI systems through arXiv, potentially uncovering vulnerabilities or best practices that could be exploited.

**Specific Nodes & Relationships:**

*   **Attack Pattern (c02f812d-59cc-5366-b1aa-7eb05154b772):** This node represents a potential attack pattern, indicating adversaries are actively searching for information related to your AI.
*   **Node B (node-application-c842d4e2-5b8b-4cd8-afdb-15c6478648a8):** This node highlights the potential for researchers to use arXiv to understand the details of your AI system, potentially revealing vulnerabilities.
*   **Node A (attack-pattern-02ea7626-0eec-5a4b-98ff-b3f21733b783):** This node represents a potential attack, suggesting adversaries are actively searching for information about your AI.
*   **Node C (research-paper-02ea7626-0eec-5a4b-98ff-b3f21733b783):** This node indicates that researchers are using arXiv to understand your AI system, potentially revealing vulnerabilities.

**Recommendations:**

*   **Monitor arXiv Activity:**  Closely track arXiv activity related to your organization's AI models and techniques.
*   **Data Security:** Implement robust data security measures to protect model data stored on arXiv.
*   **Risk Assessment:** Conduct a thorough risk assessment to understand the potential impact of data leakage on your organization.

Do you want me to elaborate on any of these points or provide more specific analysis?
```
