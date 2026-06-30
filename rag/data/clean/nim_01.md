---
url: https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/
tecnologia: NIM
titulo: NVIDIA NIM Microservices for Accelerated AI Inference | NVIDIA
---

# NVIDIA NIM Microservices

Designed for rapid, reliable deployment of accelerated generative AI inference anywhere.

[Video](https://www.youtube.com/watch?v=087spL8hMvM)   \|   [Solution Brief](https://nvdam.widen.net/s/r59kvpsqlp/llm-solution-overview-nim-3159981)   \|   [Documentation](https://docs.nvidia.com/nim/)   \|   [For Developers](https://developer.nvidia.com/nim)

## Overview

## What Is NVIDIA NIM?

NVIDIA NIM™ provides prebuilt, optimized inference microservices for rapidly deploying the latest AI models on any NVIDIA-accelerated infrastructure—cloud, data center, workstation, and edge.

### Sovereign AI Agents Think Local, Act Global With NVIDIA AI Factories

Validated design for AI factories pairs accelerated infrastructure with software, including new NVIDIA NIM™ capabilities and an expanded suite of NVIDIA blueprints.

### Free Development Access to NIM

Get access to unlimited prototyping with hosted APIs for NIM accelerated by DGX Cloud, or download and self-host NIM microservices for research and development as part of the NVIDIA Developer program.

## Accelerate AI Deployment With NVIDIA NIM

NVIDIA NIM combines the ease of use and operational simplicity of managed APIs with the flexibility and security of self-hosting models on your preferred infrastructure. NIM microservices come with everything AI teams need—the latest AI foundation models, optimized inference engines, industry-standard APIs, and runtime dependencies—prepackaged in enterprise-grade software containers ready to deploy and scale anywhere.

### Benefits

## Enterprise Generative AI That Does More for Less

Easy, production-ready microservices are built for high-performance AI and designed to work seamlessly and scale affordably. Get started building AI agents and other enterprise generative AI applications faster with the latest AI models for reasoning, simulation, speech, and more.

### Ease of Use

Accelerate innovation and time to market with prebuilt, optimized microservices for the latest AI models. With standard APIs, models can be deployed in five minutes and easily integrated into applications.

[Watch: Deploy NIM in 5 Minutes](https://www.youtube.com/watch?v=087spL8hMvM)

### Enterprise Grade

Deploy enterprise-grade microservices that are continuously managed by NVIDIA through rigorous validation processes and dedicated feature branches—all backed by NVIDIA enterprise support, which also offers direct access to NVIDIA AI experts.

### Performance and Scale

Improve TCO with low-latency, high-throughput AI inference that scales with the cloud, and achieve the best accuracy with support for fine-tuned models out of the box.

[Watch: NIM Performance and TCO Advantage](https://www.youtube.com/watch?v=WUBl6SMRy0g)

### Portability

Deploy anywhere with prebuilt, cloud-native microservices ready to run on any NVIDIA-accelerated infrastructure—cloud, data center, and workstation—and scale seamlessly on Kubernetes and cloud service provider environments.

### Demo

## Build AI Agents With NIM

Learn how to set up two AI agents—one for content generation and another for digital graphic design—and see how easy it is to get up and running with NIM microservices.

* * *

### Technology

## Building Blocks for Agentic AI

### Get the Latest AI Models

Access the latest AI models for reasoning, language, retrieval, speech, vision and more—ready to deploy in five minutes on any NVIDIA-accelerated infrastructure.

### Jump-Start Development With NVIDIA Blueprints

Build impactful agentic AI applications with comprehensive reference workflows featuring NVIDIA acceleration libraries, SDKs, and NIM microservices.

[Learn More](https://www.nvidia.com/en-us/ai-data-science/ai-workflows/) [Try Now](https://build.nvidia.com/blueprints)

### Simplify Development With NVIDIA NeMo Agent toolkit

Weave NIM microservices into agentic AI applications with the NVIDIA NeMo Agent toolkit library, a developer toolkit for building AI agents and integrating them into custom workflows.

[Learn More](https://developer.nvidia.com/agentiq) [Try Now](http://github.com/NVIDIA/AgentIQ)

### Benchmarks

## Boost Throughput With NIM

NVIDIA NIM provides optimized throughput and latency out of the box to maximize token generation, support concurrent users at peak times, and improve responsiveness. NIM microservices are continuously updated with the latest optimized inference engines, boosting performance on the same infrastructure over time.

0.0x0.5x1.0x1.5x2x2X1XNIM OnNIM Off

Configuration: Llama 3.1 8B instruct, 1x H100 SXM; concurrent requests: 200. NIM ON: FP8, throughput 1201 tokens/s, ITL 32ms. NIM OFF: FP8, throughput 613 tokens/sec, ITL 37ms.

### Models

## Unlock Enterprise-Ready Inference for Thousands of Open Models

Deploy large language models (LLMs) supported by NVIDIA® TensorRT™-LLM, vLLM, or SGLang for low-latency, high-throughput inferencing on NVIDIA-accelerated infrastructure.

Try NVIDIA NIM APIs

* * *

### Features

## The Easy Button for AI Development and Deployment

Designed to run anywhere, NIM microservices expose industry-standard APIs for easy integration with enterprise systems and applications and scale seamlessly on Kubernetes to deliver high-throughput, low-latency inference at cloud scale.

### Deploy NIM

Deploy NIM for your model with a single command. You can also easily run NIM with LLMs supported by NVIDIA TensorRT-LLM, vLLM, or SGLang, including fine-tuned models.

### Run Inference

Get NIM up and running with the optimal runtime engine based on your NVIDIA-accelerated infrastructure.

### Build

Integrate self-hosted NIM endpoints with just a few lines of code.

Deploy

Run

Build

docker run nvcr.io/nim/publisher\_name/model\_name

curl -X 'POST' \ 'http://0.0.0.0:8000/v1/completions' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "model" : "model\_name", "prompt" : "Once upon a time", "max\_tokens" : 64}'

import openaiclient = openai.OpenAI( base\_url = "YOUR\_LOCAL\_ENDPOINT\_URL", api\_key="YOUR\_LOCAL\_API\_KEY")chat\_completion = client.chat.completions.create( model="model\_name", messages=\[{"role" : "user" , "content" : "Write me a love song" }\], temperature=0.7)

### Use Cases

## How NIM Is Being Used

See how NVIDIA NIM supports industry use cases, and jump-start your AI development with curated examples.

2. AI Virtual Assistants

3. Document Intelligence

4. Hyperpersonalized Shopping

5. 3D Product Configurators

### AI Virtual Assistants

Enhance customer experiences and improve business processes with generative AI.

[Learn About AI for Customer Support](https://www.nvidia.com/en-us/use-cases/ai-for-customer-support/)

### Intelligent Document Processing

Use generative AI to accelerate and automate document processing.

[Learn About Intelligent Document Processing](https://www.nvidia.com/en-us/use-cases/intelligent-document-processing/)

### AI for Hyperpersonalized Shopping

Deliver tailored experiences that enhance customer satisfaction with the power of AI.

### 3D Product Configurators

Use OpenUSD and generative AI to develop and deploy 3D product configurator tools and experiences to nearly any device.

[Learn About 3D Product Configurators](https://www.nvidia.com/en-us/use-cases/3d-product-configurator/)

### Starting Options

## Ways to Get Started With NVIDIA NIM

### Start Prototyping for Free

Get started with easy-to-use API endpoints for NIM, powered by DGX Cloud.

- Access fully accelerated AI infrastructure.
- Ensure your data isn't used for model training.
- Access for development and testing as part of the [NVIDIA Developer Program](https://developer.nvidia.com/developer-program).

### Download and Deploy

Run NVIDIA NIM to scale optimized AI models in the cloud or data center of your choice.

- Ensure data never leaves your secure enclave.
- Seamlessly transition from cloud endpoints to self-hosted APIs without code changes.
- Start with free access for development and testing, and move to an NVIDIA AI Enterprise license for production.

### Get in Touch

Talk to an NVIDIA AI specialist about moving generative AI pilots to production with the security, API stability, and support that comes with NVIDIA AI Enterprise.

- Explore your generative AI use cases.
- Discuss your technical requirements.
- Align NVIDIA AI solutions to your goals and requirements.

### Resources

## The Latest NVIDIA NIM Resources

2. Blogs

3. Sessions

4. Courses

5. Videos

### NVIDIA NIM in the News

[See All Tech Blogs](https://developer.nvidia.com/blog/search-posts/?q=NIM) [See All Topic News](https://blogs.nvidia.com/blog/tag/nvidia-nim/)

[June 23, 2026\\
\\
Build an AI Scientist for Life Science Discovery with NVIDIA BioNeMo Agent Toolkit\\
\\
AI scientists are emerging as a new interface for scientific computing. These agents can read papers, write code, generate hypotheses, call APIs, inspect files…](https://developer.nvidia.com/blog/build-an-ai-scientist-for-life-science-discovery-with-nvidia-bionemo-agent-toolkit/)

[June 12, 2026\\
\\
Run DiffusionGemma on NVIDIA for Developer-Ready, High-Throughput Text Generation\\
\\
Developers building real-time AI—such as chat assistants, copilots, and agentic workflows—are often constrained by token-by-token generation speed.](https://developer.nvidia.com/blog/run-diffusiongemma-on-nvidia-for-developer-ready-high-throughput-text-generation/)

[May 21, 2026\\
\\
Building Token‑Metered AI Services on Telco AI Factories\\
\\
Telcos around the world are building sovereign AI factories based on the NVIDIA Cloud Partner (NCP) reference architecture, giving governments, enterprises…](https://developer.nvidia.com/blog/building-token-metered-ai-services-on-telco-ai-factories/)

Load More

### Introduction to NVIDIA NIM Microservices

Learn how NIM enables the building, deploying, and scaling of AI applications.

### Sizing LLM Inference Systems

Learn how to optimize and deploy large language models using NIM microservices for real-world applications.

### Developing an AI Background Generator With NIM

Review the process of creating an AI-enabled NVIDIA Omniverse™ Kit-based application. You’ll learn how to use Omniverse extensions, NIM microservices, and Python code to add an extension capable of generating backgrounds from text input.

### How to Build a Simple AI Agent in 5 Minutes With NVIDIA NIM

See how to set up two AI agents—one for content generation and another for digital graphic design.

### NVIDIA NIM Microservices for RTX AI PCs

Harness the latest generative AI models locally on your NVIDIA RTX™ AI PC with NVIDIA NIM and NVIDIA Blueprints.

### Generative AI Inference Powered by NVIDIA NIM

Visualize the impact of high-performance generative AI inferencing with NVIDIA NIM microservices.

### Next Steps

## Ready to Get Started?

Get unlimited access to NIM API endpoints for prototyping, accelerated by DGX Cloud. When ready for production, download and self-host NIM on your preferred infrastructure—workstation, datacenter, edge or cloud, or access NIM endpoints hosted by NVIDIA partners.

### Get in Touch

Talk to an NVIDIA product specialist about moving from pilot to production with the security, API stability, and support that comes with [NVIDIA AI Enterprise](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/).

### Stay Up to Date on NVIDIA NIM News

Get the latest news, technologies, breakthroughs, and more sent straight to your inbox.

Consent for Optional Cookies

[YouTube sets performance, advertising, and other optional cookies](https://policies.google.com/technologies/cookies) when you watch embedded videos. To watch this video, you need to turn on optional cookies for the site. By clicking “Accept and Play Video,” you will automatically turn on advertising and other optional cookies for the site and accept our [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) (which contains important waivers). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) and [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information.

Cancel

Accept and Play Video

Alternatively, you can [watch this video on YouTube](https://www.youtube.com/watch?v=mg0kwpmUhPU).

Select Location

The Americas

- [Argentina](https://www.nvidia.com/es-la/ai-data-science/products/nim-microservices/ "Argentina")
- [Brasil (Brazil)](https://www.nvidia.com/pt-br/ai-data-science/products/nim-microservices/ "Brasil (Brazil)")
- [Canada](https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/ "Canada")
- [Chile](https://www.nvidia.com/es-la/ai-data-science/products/nim-microservices/ "Chile")
- [Colombia](https://www.nvidia.com/es-la/ai-data-science/products/nim-microservices/ "Colombia")
- [México (Mexico)](https://www.nvidia.com/es-la/ai-data-science/products/nim-microservices/ "México (Mexico)")
- [Peru](https://www.nvidia.com/es-la/ai-data-science/products/nim-microservices/ "Peru")
- [United States](https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/ "United States")

Europe

- [België (Belgium)](https://www.nvidia.com/nl-nl/ "België (Belgium)")
- [Belgique (Belgium)](https://www.nvidia.com/fr-be/ "Belgique (Belgium)")
- [Česká Republika (Czech Republic)](https://www.nvidia.com/cs-cz/ "Česká Republika (Czech Republic)")
- [Danmark (Denmark)](https://www.nvidia.com/da-dk/ "Danmark (Denmark)")
- [Deutschland (Germany)](https://www.nvidia.com/de-de/ai-data-science/products/nim-microservices/ "Deutschland (Germany)")
- [España (Spain)](https://www.nvidia.com/es-es/ai-data-science/products/nim-microservices/ "España (Spain)")
- [France](https://www.nvidia.com/fr-fr/ai-data-science/products/nim-microservices/ "France")
- [Italia (Italy)](https://www.nvidia.com/it-it/ai-data-science/products/nim-microservices/ "Italia (Italy)")
- [Nederland (Netherlands)](https://www.nvidia.com/nl-nl/ "Nederland (Netherlands)")
- [Norge (Norway)](https://www.nvidia.com/nb-no/ "Norge (Norway)")
- [Österreich (Austria)](https://www.nvidia.com/de-at/ "Österreich (Austria)")
- [Polska (Poland)](https://www.nvidia.com/pl-pl/ "Polska (Poland)")
- [România (Romania)](https://www.nvidia.com/ro-ro/ "România (Romania)")
- [Suomi (Finland)](https://www.nvidia.com/fi-fi/ "Suomi (Finland)")
- [Sverige (Sweden)](https://www.nvidia.com/sv-se/ "Sverige (Sweden)")
- [Türkiye (Turkey)](https://www.nvidia.com/tr-tr/ "Türkiye (Turkey)")
- [United Kingdom](https://www.nvidia.com/en-gb/ai-data-science/products/nim-microservices/ "United Kingdom")
- [Rest of Europe](https://www.nvidia.com/en-eu/ai-data-science/products/nim-microservices/ "Rest of Europe")

Asia

- [Australia](https://www.nvidia.com/en-au/ai-data-science/products/nim-microservices/ "Australia")
- [中国大陆 (Mainland China)](https://www.nvidia.cn/ai-data-science/products/nim-microservices/ "中国大陆 (Mainland China)")
- [India](https://www.nvidia.com/en-in/ai-data-science/products/nim-microservices/ "India")
- [日本 (Japan)](https://www.nvidia.com/ja-jp/ai-data-science/products/nim-microservices/ "日本 (Japan)")
- [대한민국 (South Korea)](https://www.nvidia.com/ko-kr/ai-data-science/products/nim-microservices/ "대한민국 (South Korea)")
- [Singapore](https://www.nvidia.com/en-sg/ai-data-science/products/nim-microservices/ "Singapore")
- [台灣 (Taiwan)](https://www.nvidia.com/zh-tw/ai-data-science/products/nim-microservices/ "台灣 (Taiwan)")

Middle East

- [Middle East](https://www.nvidia.com/en-me/ "Middle East")

Computer vision applications are under transformational change with generative AI. New vision language models that understand both image/video and natural language enable the creation of visual AI agents that understand video footage and respond…

Enterprises, organizations, and sovereign nations are building and adapting applications to be powered by generative AI, but they have unique knowledge, language, and skill requirements. Learn how the NVIDIA AI Foundry, NVIDIA NIM,…

Discover how health insurance calls can be improved through an AI-powered voice assistant leveraging NVIDIA Retriever, NIM inference microservices, and NeMo Guardrails. Learn how these technologies reduce human intervention and costs…

This session explores how generative AI can accelerate the development of software-defined vehicles by enhancing customer experience and streamlining the software engineering lifecycle. We'll focus on utilizing NVIDIA's NeMo framework to fine-tune…

In this talk, we’ll explore the challenges and solutions related to building and deploying conversational AI workflows, including modalities like automatic speech recognition, large language models, and speech synthesis models focusing on…

In this session, we'll explore the work Tech Mahindra Ltd has done with the NVIDIA NeMo stack and NIM inference microservices for advancing the Bahasa language model for Indonesia. While AI has revolutionized enterprise solutions, developing…

In this advanced session, we explore Retrieval Augmented Generation (RAG) and how to use NVIDIA Inference Micro-Service (NIM) architectures for scalable, enterprise-grade RAG applications. As organizations seek to enhance AI…

The rapid advancement of generative AI has sparked innovation across diverse fields, but concerns about data security and privacy pose challenges in developing secure inference solutions. Businesses struggle with quick data analysis, relying on…

Unlocking the full potential of AI models demands an inference platform that combines optimized serving, scalable infrastructure and cutting-edge accelerators. In this session, discover how NVIDIA NIM on Google Cloud are empowering…

This talk presents a collective body of work that has arisen out of the NIH research collaboration with NVIDIA beginning in 2019, starting with various organ-specific segmentation models and recently producing the NVIDIA VISTA-3D NIM foundation…

In this session, we'll explore the diverse landscape of Generative AI (GenAI) tools and techniques, providing a roadmap for incorporating these technologies into daily workflows. We'll examine popular commercial GenAI tools like Claude and…

Learn how to build high-performance visual AI agents, from cloud to far edge, that help streamline operations across a range of industries. NVIDIA Metropolis reference workflows bring visual AI agents to life—powered by generative AI vision language…

Watch this insightful webinar replayy to learn how you can improve the accuracy and scalability of text retrieval for production-ready generative AI pipelines. With the newest available NVIDIA NeMo™ Retriever and NVIDIA NIM™ microservices,…

In the rapidly evolving landscape of capital markets, leveraging advanced data analytics has become a cornerstone for front office innovation. Traditional systems can't keep up with the deluge of information, leaving investment professionals…

This presentation explores Bria's innovative source-available platform for generative AI, highlighting its unique approach to copyright and respect of privacy. We examine the technical challenges in developing a generative AI system that balances…