---
url: https://www.nvidia.com/en-us/ai-data-science/products/nemo/
tecnologia: NeMo
titulo: NeMo | Build, monitor, and optimize AI agents | NVIDIA
---

# NVIDIA NeMo

An agent-first, open suite of libraries with skills for accelerating AI agent specialization, optimization, and governance.

[Documentation](https://docs.nvidia.com/nemo/)  \|  [GitHub](https://github.com/NVIDIA-NeMo)

Overview

## What Is NVIDIA NeMo?

NVIDIA NeMo™ is an agent-first, open suite of libraries with skills for accelerating AI agent specialization, optimization, and governance.

NeMo integrates with existing AI tools and agent frameworks to optimize specialized agents across any cloud, on-premises, or hybrid environment.

### NVIDIA AI-Q Blueprint

A reference workflow for building custom enterprise research agents that securely connect to company data, tools, and workflows to deliver accurate, context-aware insights grounded in organizational knowledge.

### Features

## Tools and Skills for Accelerating Specialized AI Agent Optimization

The AI agent lifecycle is an end-to-end process for developing and continuously improving AI agents in production applications. NeMo integrates with existing AI tools and agent frameworks to optimize specialized agents across their lifecycles.

| Build |
| **Prepare AI-ready data**<br> Process existing multimodal datasets into high-quality, AI-ready formats for development pipelines, and generate synthetic data to close critical data gaps. | - [NeMo Curator](https://docs.nvidia.com/nemo/curator/latest/home/welcome)<br>  <br>  <br>Clean, filter, and prepare safe multimodal data for agentic use cases and model training. <br>- [NeMo Data Designer](https://nvidia-nemo.github.io/DataDesigner/latest/)<br>  <br>  <br>Create domain‑specific synthetic datasets from scratch for building and evaluating specialized agents. <br>- [NeMo Anonymizer](https://nvidia-nemo.github.io/Anonymizer/latest/)<br>  <br>  <br>Perform context-aware data anonymization to protect PII while preserving insights.<br>- [NeMo Safe Synthesizer](https://nvidia-nemo.github.io/Safe-Synthesizer/latest/)<br>  <br>  <br>Generate safe, synthetic versions of your sensitive datasets with no one-to-one mapping to original records. |
| **Select the right model**<br>Pick or build models suited to the use case: selecting from open Nemotron models, other open or proprietary options, or training from scratch. Validate with evaluation runs, and fine-tune as needed. | - [NVIDIA Nemotron](https://developer.nvidia.com/nemotron)<br>  <br>  <br>State-of-the-art open NVIDIA models for reasoning, RAG, speech, vision, and safety. <br>- [NeMo Evaluator](https://docs.nvidia.com/nemo/evaluator/latest/)<br>  <br>  <br>Benchmark and test models and agents using academic, LLM-as-a-judge, and custom evaluations. |
| Deploy |
| **Deploy your agent with maximum performance**<br>Optimize your agent for production with high-throughput, low-latency inference, ensuring it can scale to meet enterprise demands and deliver fast, reliable responses. | - [NVIDIA NIM](http://developer.nvidia.com/nim/)<br>  <br>  <br>Run AI models in optimized containers, exposed as OpenAI-compatible APIs. |
| **Stay grounded in data and apply guardrails**<br>Use retrieval-augmented generation (RAG) to anchor agent responses in trusted knowledge while applying safety, compliance, and content moderation guardrails. | - [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/index.html)<br>  <br>  <br>Enhance safety, compliance, and control across AI interactions. |
| **Validate agent and model safety before launch**<br>Identify and remediate safety and security vulnerabilities in models and agents before they reach production. | - [NeMo Auditor](https://docs.nvidia.com/nemo/microservices/latest/audit/index.html)<br>  <br>  <br>Identify safety and security vulnerabilities. |
| Optimize |
| **Profile and Optimize Your Agent**<br>Track the agent's real-world interactions with users and other systems. Systematically evaluate its performance and accuracy, finding opportunities to continuously improve. | - [NeMo Relay](https://docs.nvidia.com/nemo/relay/latest/)<br>  <br>  <br>Connect and observe black-box and general-purpose agent harnesses into the NeMo platform.<br>- [NeMo Customizer](https://docs.nvidia.com/nemo/microservices/latest/customizer/index.html)<br>  <br>  <br>Microservice to fine-tune and align models with domain data.<br>- [NeMo Framework](https://docs.nvidia.com/nemo-framework/user-guide/latest/overview.html)<br>  <br>  <br>Collection of all open-source NeMo libraries for training and aligning LLMs and multimodal models efficiently at scale. |
| **Continuously improve with data flywheels**<br>Use the feedback and data gathered from monitoring to create a data-driven flywheel, iteratively retraining the agent to continuously optimize and stay effective over time. | - [NeMo RL](https://docs.nvidia.com/nemo/rl/latest/index.html)<br>  <br>  <br>Post-train and align models at scale with advanced reinforcement learning (RL) techniques. <br>- [NeMo Gym](https://docs.nvidia.com/nemo/gym/main/about/)<br>  <br>  <br>Simulated RL training environments to generate high-quality agentic RL training data/rollouts. <br>- [NeMo Evaluator](https://docs.nvidia.com/nemo/evaluator/latest/)<br>  <br>  <br>Benchmark and test models and agents using academic, LLM-as-a-judge, and custom evaluations. <br>- [NeMo Customizer](https://docs.nvidia.com/nemo/microservices/latest/customizer/index.html)<br>  <br>  <br>Plug-in to fine-tune and align models with domain data. |

Use Cases

## How NeMo Is Being Used

See how NVIDIA NeMo supports industry use cases and jump-starts your AI development.

2. AI Agents

3. SDG for Agentic AI

4. AI Assistant

5. Enterprise Search

6. Content Generation

7. Humanoid Robot

### AI Agents

AI agents are transforming customer service across sectors, helping companies enhance customer conversations, achieve high resolution rates, and improve human representative productivity. AI agents can handle predictive tasks, reason and problem-solve, be trained to understand industry-specific terms, and pull relevant information from an organization’s knowledge bases, wherever that data resides.

[Learn More About AI Agents](https://blogs.nvidia.com/blog/ai-agents-customer-service/)

### Synthetic Data Generation for Agentic AI

Specialized agentic systems need massive, high-quality datasets that are slow and expensive to collect from real-world sources. Synthetic data created through simulations or generative AI models can eliminate this bottleneck by creating unlimited training scenarios without privacy restrictions or quality issues. This enables faster development of reasoning LLMs, multi-step decision-makers, and multimodal AI assistants.

[Learn More About SDG for Agentic AI](https://www.nvidia.com/en-us/use-cases/synthetic-data-generation-for-agentic-ai/)

### AI Assistant

Businesses are deploying AI assistants to efficiently address the queries of millions of customers and employees around the clock. Powered by customized NVIDIA NIM™ microservices for [LLMs](https://developer.nvidia.com/blog/building-nvidia-nemotron-3-agents-for-reasoning-multimodal-rag-voice-and-safety/), [RAG](https://developer.nvidia.com/blog/how-to-take-a-rag-application-from-pilot-to-production-in-four-steps/), and [speech](https://developer.nvidia.com/blog/an-easy-introduction-to-speech-ai/) and translation AI, these AI teammates deliver immediate and accurate spoken responses, even in the presence of background noise, poor sound quality, and diverse dialects and accents.

[Learn More About AI Assistants](https://www.nvidia.com/en-us/use-cases/ai-for-customer-support/)

### Enterprise Search

Enterprises generate trillions of documents annually—including PDFs, reports, presentations, —each containing text, images, charts, and tables—spread across disconnected systems. AI-powered enterprise search transforms this scattered data into a unified knowledge base, enabling employees to instantly surface insights using natural language and driving faster decisions at lower cost.

[Learn More About Enterprise Search](https://build.nvidia.com/nvidia/aiq)

### Content Generation

Generative AI makes it possible to generate highly relevant, bespoke, and accurate content grounded in the domain expertise and proprietary IP of your enterprise.

[Learn More About Content Generation](https://www.nvidia.com/en-us/use-cases/content-creation-using-generative-ai/)

### Humanoid Robot

Humanoid robots are built to adapt quickly to existing human-centric urban and industrial work spaces, tackling tedious, repetitive, or physically demanding tasks. Their versatility has them in such varied locations as factory floors to healthcare facilities, where these robots are assisting humans and helping alleviate labor shortages with automation.

[Learn More About Humanoid Robots](https://www.nvidia.com/en-us/use-cases/humanoid-robots/)

Apptronik

### Benefits

## Explore the Benefits of NVIDIA NeMo for Agentic AI

### Agent-First Development With Skills

Manage the full agent lifecycle from data curation and post-training to evaluation, guardrails, observability, and continuous optimization using an agent-friendly suite of agent skills.

### Accelerate at Scale

Deploy and scale data flywheels using enterprise data, with GPU-accelerated training, inference, multi-node scaling, and cost-efficient optimization for high-throughput agent workloads.

### Increased ROI

Build, customize, and deploy specialized agentic systems faster—shortening time to production and maximizing return on AI investments.

### Secure and Production-Ready

Safeguard sensitive data, enforce policy and prompt guardrails, validate models, and continuously detect vulnerabilities. Deploy securely with enterprise-grade support and stability across cloud, data center, and edge with [NVIDIA AI Enterprise](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/).

### Starting Options

## Ways to Get Started With NVIDIA NeMo

Manage the AI agent lifecycle with tools and technologies for building, monitoring, and optimizing AI agents in production.

### 1

Try NVIDIA-optimized foundation models like NVIDIA Nemotron.

### 2

Build, monitor, and optimize AI agents with NVIDIA NeMo.

### 3

Jump-start building your AI solutions with NVIDIA Blueprints.

### Customer Stories

## How Industry Leaders Are Driving Innovation With NeMo

### Adopters

## Leading Adopters Across All Industries

2. ### Customers

3. ### Partners

### Resources

## The Latest in NVIDIA NeMo Resources

2. Blogs

3. Sessions

4. Training

5. Videos

[June 23, 2026\\
\\
How Businesses Are Building Specialized AI They Can Trust\\
\\
Editor’s note: This post is part of the Nemotron Labs blog series, which explores how the latest open models, datasets and training techniques help businesses build specialized AI systems and applications on NVIDIA platforms. Each post highlights practical ways to use an open stack to deliver real value in production — from transparent research copilots \[…\]](https://blogs.nvidia.com/blog/nvidia-agent-toolkit-open-models-tools-skills-secure-runtime-ai-agents/)

[June 22, 2026\\
\\
From Materials Simulation to Experimental Astronomy, New NVIDIA AI Software Unlocks Scientific Discoveries\\
\\
At the ISC conference running in Hamburg this week, NVIDIA is introducing new software that speeds AI for science, from chemistry and materials discovery to the search for dark matter.  The NVIDIA DAQIRI library and new NVIDIA ALCHEMI NIM microservices — as well as the NVIDIA cuPhoton reference code, coming soon — turn work that \[…\]](https://blogs.nvidia.com/blog/ai-for-science-software-cuda/)

[June 22, 2026\\
\\
How Telcos Build Autonomous Networks with Agentic AI\\
\\
Telecom operators are adopting AI across network operations, customer care, and back-office workflows, but most are still early in the journey to autonomy.](https://developer.nvidia.com/blog/how-telcos-build-autonomous-networks-with-agentic-ai/)

Load More

### Get Started With LLM Customization

In this course, you’ll go beyond prompt-engineering LLMs and learn techniques to efficiently customize pretrained LLMs for your specific use cases. Using NVIDIA NIM microservices, NeMo Curator, and NeMo Framework, you’ll learn various parameter-efficient fine-tuning methods to customize LLM behavior for your organization.

### Elevate Your LLM Skills

Take advantage of our comprehensive LLM learning path, covering fundamental to advanced topics featuring hands-on training developed and delivered by NVIDIA experts. You can opt for the flexibility of self-paced courses or enroll in instructor-led workshops to earn a certificate of competency.

### Get Certified by NVIDIA

Showcase your Generative AI skills and advance your career by getting certified by NVIDIA. Our new professional certification program offers two developer exams focusing on proficiency in large language models (LLMs) and multimodal workflow skills.

### Train a Reasoning-Capable LLM in One Weekend

Explore a simple and computationally efficient recipe for training reasoning models with small amounts of training data curated from the Llama Nemotron post-training dataset and NVIDIA NeMo.

### Optimize AI Agents Using a Data Flywheel

Learn how to optimize AI agents in production using the NVIDIA Data Flywheel Blueprint—a continuous loop of distillation, fine-tuning, and evaluation powered by NeMo and NIM microservices.

### Build AI Agents With NeMo Agent Open-Source Toolkit

Learn how to build, integrate, and optimize custom AI agents using the NVIDIA NeMo Agent open-source Python toolkit.

[Watch Custom AI Agent Video](https://www.youtube.com/watch?v=NsogD7UhZ4Q)

### Next Steps

## Ready to Get Started?

Use the right tools and technologies to take your agentic AI applications from development to production.

### For Developers

Explore everything you need to start developing with NVIDIA NeMo, including the latest documentation, tutorials, technical blogs, and more.

### Get in Touch

Talk to an NVIDIA product specialist about moving from pilot to production with the assurance of security, API stability, and support that comes with [NVIDIA AI Enterprise](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/).

## Shell

**Shell Trains Custom AI Chatbot With NVIDIA NeMo to Uplevel Operations**

Shell, a global leader in the energy industry, has leveraged NVIDIA NeMo to empower its journey toward developing a custom AI chatbot for chemical domain expertise. This innovative solution has the potential to significantly enhance employee productivity by streamlining search processes, improving decision-making, and supporting research and development in production environments.

## AI Sweden

### **Accelerate Industry Applications With LLMs**

AI Sweden facilitated regional language model applications by providing easy access to a powerful 100 billion-parameter model. They digitized historical records to develop language models for commercial use.

## Amazon

### **How Amazon and NVIDIA Help Sellers Create Better Product Listings With AI**

Amazon doubles inference speeds for new AI capabilities using NVIDIA TensorRT-LLM and GPUs to help sellers optimize product listings faster.

## Amdocs

### **NVIDIA and Amdocs Bring Custom Generative AI to Global Telco Industry**

Amdocs plans to build custom LLMs for $1.7 trillion global telecommunications industry using NVIDIA AI foundry service on Microsoft Azure.

## AT&T

### **AT&T Drives Customer Care AI Agents’ Accuracy, Efficiency, and Performance With NVIDIA NeMo**

AT&T, one of the world’s largest telecommunications companies, is reimagining customer care through the power of AI. Facing challenges like model drift, rising computational demands, and the need for real-time data access, AT&T turned to NVIDIA NeMo™ microservices to build a feedback-driven AI platform that continuously improves performance while optimizing cost, speed, and compliance.

## AWS

### **NVIDIA Powers Training for Some of the Largest Amazon Titan Foundation Models**

Amazon leveraged the NVIDIA NeMo framework, GPUs, and AWS EFAs to train its next-generation LLM, giving some of the largest Amazon Titan foundation models customers a faster, more accessible solution for generative AI.

## Accenture

### **Accelerate Generative AI Adoption for Enterprises**

ServiceNow, NVIDIA, and Accenture announced the launch of AI Lighthouse, a first-of-its-kind program designed to fast-track the development and adoption of enterprise generative AI capabilities.

## Azure

### **Harnessing the Power of NVIDIA AI Enterprise on Azure Machine Learning**

Get access to a complete ecosystem of tools, libraries, frameworks, and support services tailored for enterprise environments on Microsoft Azure.

## Bria

### **Bria Builds Responsible Generative AI for Enterprises Using NVIDIA NeMo, Picasso**

Bria, a startup based in Tel Aviv, is helping businesses who are seeking responsible ways to integrate visual generative AI technology into their enterprise products with a generative AI service that emphasizes model transparency alongside fair attribution and copyright protections.

## Cohesity

### **Unlock Your Data Superpower: NVIDIA Microservices Unleash Enterprise-Grade Secure Generative AI for Cohesity**

With NVIDIA NIM and optimized models, Cohesity DataProtect customers can add generative AI intelligence to data backups and archives. This allows Cohesity and NVIDIA to bring the power of generative AI to all Cohesity DataProtect customers. Leveraging the power of NIM and NVIDIA optimized models, Cohesity DataProtect customers obtain the power of data-driven insights from their data backups and archives, unleashing new levels of efficiency, innovation, and growth.

## CrowdStrike

### **Shaping the Future of AI in the Cybersecurity Domain**

CrowdStrike and NVIDIA are leveraging accelerated computing and generative AI to provide customers with an innovative range of AI-powered solutions tailored to efficiently address security threats.

## Dell

### **Dell Validated Design for Generative AI With NVIDIA**

Dell Technologies and NVIDIA announced an initiative to make it easier for businesses to build and use generative AI models on premises quickly and securely.

## Deloitte

### **Unlock the Value of Generative AI Across Enterprise Software Platforms**

Deloitte will use NVIDIA AI technology and expertise to build high-performing generative AI solutions for enterprise software platforms to help unlock significant business value.

## Domino Data Lab

### **Domino Offers Production-Ready Generative AI Powered by NVIDIA**

With NVIDIA NeMo, data scientists can fine-tune LLMs in Domino’s platform for domain-specific use cases based on proprietary data and IP—without needing to start from scratch.

## Dropbox

### **Dropbox and NVIDIA to Bring Personalized Generative AI to Millions of Customers**

Dropbox plans to leverage NVIDIA’s AI foundry to build custom models and improve AI-powered knowledge work with Dropbox Dash universal search tool and Dropbox AI.

## Google Cloud

### **AI Titans Collaborate to Create Generative AI Magic**

At its Next conference, Google Cloud announced the availability of its A3 instances powered by NVIDIA H100 Tensor Core GPUs. Engineering teams from both companies have collaborated to bring NVIDIA NeMo to the A3 instances for faster training and inference.

## HuggingFace

### **Leading AI Community to Accelerate Data Curation Pipeline**

Hugging Face, the leading open platform for AI builders, is collaborating with NVIDIA to integrate NeMo Curator and accelerate DataTrove, their data filtering and deduplication library. “We are excited about the GPU acceleration capabilities of NeMo Curator and can’t wait to see them contributed to DataTrove!” says Jeff Boudier, Product Director at Hugging Face.

## KT

### **Creating New Customer Experiences With LLMs**

South Korea’s leading mobile operator builds billion-parameter LLMs trained with the NVIDIA DGX SuperPOD platform and NeMo framework to power smart speakers and customer call centers.

## Lenovo

### **New Reference Architecture for Generative AI Based on LLMs**

Solution to expedite innovation by empowering global partners and customers to develop, train, and deploy AI at scale across industry verticals with utmost safety and efficiency.

## Quantiphi

### **Enabling Enterprises to Fast-Track Their AI-Driven Journeys**

Quantiphi specializes in training and fine-tuning foundation models using the NVIDIA NeMo framework, as well as optimizing deployments at scale with the NVIDIA AI Enterprise software platform, while adhering to responsible AI principles.

## SAP

### **SAP and NVIDIA Accelerate Generative AI Adoption Across Enterprise Applications Powering Global Industries**

Customers can harness their business data in cloud solutions from SAP using customized LLMs deployed with NVIDIA AI foundry services and NVIDIA NIM Microservices.

## ServiceNow

### **Building Generative AI Across Enterprise IT**

ServiceNow develops custom LLMs on its ServiceNow platform to enable intelligent workflow automation and boost productivity across enterprise IT processes.

## Perplexity

### **Enhance Model Performance for AI-Powered Search Engines**

Using NVIDIA NeMo, Perplexity aims to quickly customize frontier models to improve the accuracy and quality of search results and optimize them for lower latency and high throughput for a better user experience.

## VMware

### **VMware and NVIDIA Unlock Generative AI for Enterprises**

VMware Private AI Foundation with NVIDIA will enable enterprises to customize models and run generative AI applications, including intelligent chatbots, assistants, search, and summarization.

## Weight & Biases

### **Debug, Optimize, and Monitor LLM Pipelines**

Weights & Biases helps teams working on generative AI use cases or with LLMs track and visualize all prompt-engineering experiments—helping users debug and optimize LLM pipelines—as well as provides monitoring and observability capabilities for LLMs.

## Writer

### **Startup Pens Generative AI Success Story With NVIDIA NeMo**

Using NVIDIA NeMo, Writer is building LLMs that are helping hundreds of companies create custom content for enterprise use cases across marketing, training, support, and more.

## Arize

### **Arize Powers Self-Improving AI Data Flywheels**

Arize’s LLM engineering and observability platform integrates NVIDIA NeMo microservices to power AI data flywheels, enabling continuous model refinement through real-world feedback. With NeMo Customizer, Evaluator, and Guardrails, Arize ensures agentic systems are performant, safe, and aligned with evolving enterprise needs. This collaboration supports the development of adaptive AI that learns and evolves over time.

## DataRobot

### **Enterprise-Ready, Trustworthy AI Agents With NeMo on DataRobot**

With NVIDIA NeMo embedded into the DataRobot Enterprise AI Suite, enterprises can ensure agentic systems are safe, compliant, and grounded in enterprise-specific data. This integration facilitates the development of AI agents that deliver accurate, context-aware responses while adhering to organizational standards.

## DataStax

### **DataStax and NVIDIA Build Data and AI Platform**

Over the past year, DataStax has partnered with NVIDIA to adopt NVIDIA NeMo microservices to enhance generative AI, retrieval-augmented generation, and hybrid search across its database and AI offerings. The results have been impressive: 19x better performance in throughput, a significant reduction in costs, and improved latency.

## Galileo

### **Galileo and NVIDIA NeMo: De-Risking Agentic AI in Production**

Galileo integrates NVIDIA NeMo microservices to build AI data flywheels that strengthen agent performance, reliability, and trust. NeMo adds complementary capabilities to the Galileo platform—enabling continuous domain-specific fine-tuning via NeMo Customizer, advanced evaluation with NeMo Evaluator, and safeguarding user interactions with NeMo Guardrails to empower AI teams to build, evaluate, and monitor agentic AI systems that learn and improve continuously in real-world environments.

Consent for Optional Cookies

[YouTube sets performance, advertising, and other optional cookies](https://policies.google.com/technologies/cookies) when you watch embedded videos. To watch this video, you need to turn on optional cookies for the site. By clicking “Accept and Play Video,” you will automatically turn on advertising and other optional cookies for the site and accept our [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) (which contains important waivers). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) and [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information.

Cancel

Accept and Play Video

Alternatively, you can [watch this video on YouTube](https://www.youtube.com/watch?v=1V5_wJzTCzc).

Consent for Optional Cookies

[YouTube sets performance, advertising, and other optional cookies](https://policies.google.com/technologies/cookies) when you watch embedded videos. To watch this video, you need to turn on optional cookies for the site. By clicking “Accept and Play Video,” you will automatically turn on advertising and other optional cookies for the site and accept our [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) (which contains important waivers). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) and [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information.

Cancel

Accept and Play Video

Alternatively, you can [watch this video on YouTube](https://www.youtube.com/watch?v=Hg2KibOvnLM).

### Building and Deploying Generative AI Models

Enterprises are turning to generative AI to revolutionize the way they innovate, optimize operations, and build a competitive advantage. NeMo is an end-to-end platform for curating data; training, customizing, and evaluating multimodal models; and running inference at scale. It supports text, image, video, and speech generation.

### Unlocking Synthetic Data Generation with Llama 3.1

Learn how to use the Meta Llama 3.1 405B model to generate tailored synthetic data for your specific domain and explore how to evaluate this data using the Nemotron-4 340B Reward model and ensure alignment with human preferences through NVIDIA NeMo.

### Build World-Class AI Virtual Assistants for Customer Service with RAG

Learn how companies can use the AI virtual assistant for customer service NVIDIA AI Blueprint to improve the operational efficiency of existing contact center solutions or build new customer service-centric systems.

Select Location

The Americas

- [Argentina](https://www.nvidia.com/es-la/ai-data-science/products/nemo/ "Argentina")
- [Brasil (Brazil)](https://www.nvidia.com/pt-br/ai-data-science/products/nemo/ "Brasil (Brazil)")
- [Canada](https://www.nvidia.com/en-us/ai-data-science/products/nemo/ "Canada")
- [Chile](https://www.nvidia.com/es-la/ai-data-science/products/nemo/ "Chile")
- [Colombia](https://www.nvidia.com/es-la/ai-data-science/products/nemo/ "Colombia")
- [México (Mexico)](https://www.nvidia.com/es-la/ai-data-science/products/nemo/ "México (Mexico)")
- [Peru](https://www.nvidia.com/es-la/ai-data-science/products/nemo/ "Peru")
- [United States](https://www.nvidia.com/en-us/ai-data-science/products/nemo/ "United States")

Europe

- [België (Belgium)](https://www.nvidia.com/nl-nl/ "België (Belgium)")
- [Belgique (Belgium)](https://www.nvidia.com/fr-be/ "Belgique (Belgium)")
- [Česká Republika (Czech Republic)](https://www.nvidia.com/cs-cz/ "Česká Republika (Czech Republic)")
- [Danmark (Denmark)](https://www.nvidia.com/da-dk/ "Danmark (Denmark)")
- [Deutschland (Germany)](https://www.nvidia.com/de-de/ai-data-science/products/nemo/ "Deutschland (Germany)")
- [España (Spain)](https://www.nvidia.com/es-es/ai-data-science/products/nemo/ "España (Spain)")
- [France](https://www.nvidia.com/fr-fr/ai-data-science/products/nemo/ "France")
- [Italia (Italy)](https://www.nvidia.com/it-it/ai-data-science/products/nemo/ "Italia (Italy)")
- [Nederland (Netherlands)](https://www.nvidia.com/nl-nl/ "Nederland (Netherlands)")
- [Norge (Norway)](https://www.nvidia.com/nb-no/ "Norge (Norway)")
- [Österreich (Austria)](https://www.nvidia.com/de-at/ "Österreich (Austria)")
- [Polska (Poland)](https://www.nvidia.com/pl-pl/ "Polska (Poland)")
- [România (Romania)](https://www.nvidia.com/ro-ro/ "România (Romania)")
- [Suomi (Finland)](https://www.nvidia.com/fi-fi/ "Suomi (Finland)")
- [Sverige (Sweden)](https://www.nvidia.com/sv-se/ "Sverige (Sweden)")
- [Türkiye (Turkey)](https://www.nvidia.com/tr-tr/ "Türkiye (Turkey)")
- [United Kingdom](https://www.nvidia.com/en-gb/ai-data-science/products/nemo/ "United Kingdom")
- [Rest of Europe](https://www.nvidia.com/en-eu/ai-data-science/products/nemo/ "Rest of Europe")

Asia

- [Australia](https://www.nvidia.com/en-au/ai-data-science/products/nemo/ "Australia")
- [中国大陆 (Mainland China)](https://www.nvidia.cn/ai-data-science/products/nemo/ "中国大陆 (Mainland China)")
- [India](https://www.nvidia.com/en-in/ai-data-science/products/nemo/ "India")
- [日本 (Japan)](https://www.nvidia.com/ja-jp/ai-data-science/products/nemo/ "日本 (Japan)")
- [대한민국 (South Korea)](https://www.nvidia.com/ko-kr/ai-data-science/products/nemo/ "대한민국 (South Korea)")
- [Singapore](https://www.nvidia.com/en-sg/ai-data-science/products/nemo/ "Singapore")
- [台灣 (Taiwan)](https://www.nvidia.com/zh-tw/ai-data-science/products/nemo/ "台灣 (Taiwan)")

Middle East

- [Middle East](https://www.nvidia.com/en-me/ "Middle East")

Enterprises need a scalable, efficient, and modular solution for building data flywheels to capture the latest data to periodically train and improve the models that power AI agents. NVIDIA NeMo offers a complete solution for building these flywheels. NeMo enables…

Trillions of PDF files are generated every year, each file likely consisting of multiple pages filled with various content types, including text, images, charts, and tables. Learn how generative AI and retrieval-augmented generation (RAG) is enabling enterprises to extract…

As AI systems grow more powerful and pervasive, interaction with users raises critical challenges beyond just technical implementation. Join NVIDIA experts as they discuss the complex and diverse set of regulatory compliance, safety protocols, and security…

The collaboration between UBS and NVIDIA focuses on real-time risk assessment and monitoring of production retrieval augmented generation (RAG). Unlike holistic evaluations of RAG applications, real-time solutions must introduce minimal latency and offer a high…

High-quality training data ensures that generative AI models learn accurately and generalize well, leading to more reliable outputs. In this webinar, we’ll explore how NVIDIA NeMo™ Curator enables developers to easily build scalable data processing pipelines to create high-…

Watch this insightful webinar replayy to learn how you can improve the accuracy and scalability of text retrieval for production-ready generative AI pipelines. With the newest available NVIDIA NeMo™ Retriever and NVIDIA NIM™ microservices, developers and…

Getting started with the right tools for creating and customizing Generative AI solutions for your enterprise can be overwhelming. And even beyond the tools and model choice, there are decisions to be made when selecting infrastructure to support your AI lifecycle. In this…

Advancements in Large Language Models (LLMs) have enabled developers to create a variety of applications such as code generation, translation, and text summarization. The effectiveness of all these models depends on the quality of the data used for training LLMs. Data from…

Training a large language model at scale while ensuring efficiency and reliability poses numerous challenges. During this presentation, we'll share our experience training LLMs at Amazon Search, utilizing NVIDIA's Nemo Framework in collaboration with AWS. We'll…

We'll focus on customizing foundation large language models (LLMs) for languages other than English. We'll go through techniques like prompt-engineering, prompt-tuning, parameter-efficient fine-tuning, and supervised instruction fine-tuning (SFT), enabling LLMs to adapt…

The demand for accelerated large language models (LLMs) has surged with the growing popularity of generative models. These models, often boasting billions of parameters, hold immense potential, but also pose challenges during large-scale deployments. Join us as we…

We all recognize the immense business opportunity from generative AI and large language models (LLMs) — particularly those trained or developed on proprietary company data. However, developing them is resource-intensive, time-consuming, and requires deep…

This session focuses on the integration of NeMo Framework and NeMo Retriever to generate a groundbreaking knowledge graph (KG) for financial documents data. By combining KGs with large language models and retrieval-augmented generation mechanisms, this…

We all recognize the immense business opportunity from generative AI and large language models (LLMs) — particularly those trained or developed on proprietary company data. However, developing them is resource-intensive, time-consuming, and requires deep…

Are you having trouble getting language models (LLMs) to work in your organization? You're not alone. We'll look at how to deploy an open-source language model on GKE. We'll show data scientists and machine learning engineers how to use NeMo and TRT LLM with GKE's…

Discover how health insurance calls can be improved through an AI-powered voice assistant leveraging NVIDIA Retriever, NIM inference microservices, and NeMo Guardrails. Learn how these technologies reduce human intervention and costs while improving caller…

Large language models (LLMs) provide new possibilities for engaging and intelligent conversational systems. However, productionizing and managing these models and ensuring they work to your advantage can be challenging. Two key strategies that can help are RAG-…

In this talk, we’ll explore the challenges and solutions related to building and deploying conversational AI workflows, including modalities like automatic speech recognition, large language models, and speech synthesis models focusing on regional languages. We’ll dive…

This session will cover the technical and architectural approach that CoRover took to create a grounded and secure generative AI-powered conversational platform. Architected with a large language model fine-tuned to deliver regional language capabilities and cost economics—…

Generative AI (GenAI) and large language models (LLMs) enable retailers to build novel and innovative solutions that empower internal employees, reduce costs, and revolutionize the customer experience. As the world’s most advanced platform for accelerated computing,…

Data storage and retrieval shifted to the cloud removing data siloing and enabling easier, more efficient sharing of large-scale data in Enterprises. Behind the rise of large language models (LLMs) has been an intense focus on leveraging custom data that can be used for business…

In this session, Kari Briski, VP Generative AI Software, will provide a deeper understanding of the new NVIDIA offerings announced at GTC and how they are helping organizations supercharge the development and tuning of custom generative AI applications. Kari will…

This session explores how generative AI can accelerate the development of software-defined vehicles by enhancing customer experience and streamlining the software engineering lifecycle. We'll focus on utilizing NVIDIA's NeMo framework to fine-tune large language…

LLM-based agents, a concept that emerged from the capabilities of LLMs, represent a paradigm shift from mere automation to genuine intelligence. Agents, in the context of artificial intelligence, are autonomous entities that interact with their environment to…

Join us for an exciting introduction to foundation models in generative AI! In this training lab, we'll explore the basics of foundation models, their significance, applications, and the latest developments in the field of AI. Whether you're an academic, industry professional, or…

Recent advancements in AI and machine learning have opened up a new world of possibilities, but many companies are drowning in petabytes of data and are struggling to deliver large language model (LLM) workflows and applications. Using a real-world use case, Dropbox…

Large language models (LLMs) such as GPT-4 can now generate realistic text in real time that's difficult to distinguish from human-written content. The reliability, validity, and fairness of text-based chat interview assessments can be impacted when job candidates use LLMs to…

Our panel of experts will talk about the best practices for building robust large language model (LLM)-based enterprise applications that deliver value and efficiency. Products such as ChatGPT have demonstrated the unprecedented power of LLMs in processing information…