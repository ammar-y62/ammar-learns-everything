# OCI AI Foundations

## Modalities & Tasks
- **Text**: classify (spam/sentiment), summarize, translate, extract entities, Q&A.
- **Speech/Audio**: ASR (speech→text), TTS, speaker ID; features: spectrograms/MFCCs.
- **Vision/Docs**: image classification, object detection, OCR/text detection, document extraction.
- **Language models**: classic ML → **LLMs** (generation, chat, few-shot).

## Learning Paradigms
- **Supervised**: labeled (x,y). Metrics: accuracy/F1 (cls), mAP (det), MAE/MSE (reg).
- **Unsupervised**: no labels—clustering, dimensionality reduction, anomaly detection.
- **Reinforcement**: agent learns by rewards for sequential decisions.
- **Deep learning**: CNNs (vision), Transformers/RNNs (text/audio).

## Practical Workflow
Define task & metric → collect/clean/split data → train baseline & iterate → evaluate & error analysis → deploy (batch/real‑time) → monitor drift/cost.

---

## Supervised Learning
- **Regression**: predict continuous value (e.g., house price).
  Loss compares **actual vs predicted**; model learns a **function** to minimize loss.
- **Classification**: predict category (**binary** or **multiclass**).
  Example: **Logistic Regression** uses sigmoid + **threshold** to map to class.

### Minimal ML pipeline (sklearn)
1. Import libs (`pandas`, `numpy`, `sklearn`).
2. Load CSV → split into **features** (X) & **labels** (y).
3. `train_test_split(random_state=…)`.
4. (Often) **Standardize** features (`StandardScaler`).
5. Create model (e.g., `LogisticRegression`).
6. Fit → Predict → Evaluate (accuracy/F1 for cls; MAE/MSE/R² for reg).

### Tools
- **Anaconda**: package & environment manager, multi‑project isolation, cross‑platform, GUI, ships with **Jupyter Notebook**.

## Unsupervised Learning
Use cases: **market segmentation**, **outlier detection**, **clustering**.
Steps: prepare data → choose **similarity metric** (e.g., Euclidean/cosine) → run clustering (K‑Means/DBSCAN) → interpret & adjust.

## Reinforcement Learning
Applications: autonomous vehicles, smart devices, industrial automation, games.
Key terms: **agent**, **environment**, **state**, **action**, **policy**, **reward/penalty**; goal is to maximize cumulative reward.

## Deep Learning (Basics)
- **What it is:** Computers learn from lots of examples using **many layers** of simple units called **neurons**.
- **Data it works with:** images, videos, text, and audio.
- **What it can do:** image classification, speech/text understanding, **LLMs** (chat, writing), audio/image generation.

### Core ideas (simple)
- **Layers & neurons:** each neuron passes a number to the next layer.
- **Weights & bias:** knobs the model turns to fit the data.
- **Activation function:** a squish/trigger (like ReLU or sigmoid) so the network can learn complex, non-linear patterns.
- **Input layer → hidden layers → output layer.**
- **Learning loop:**
  1) **Guess** → 2) **Compare** with the right answer (error/loss) → 3) **Adjust** by nudging weights (backprop) → 4) **Repeat**.

## Sequence Models (for ordered data)
- **Goal:** find patterns over **time or order** (sentences, sensor readings, stock prices).
- **RNN (Recurrent Neural Network):** has a small **memory (hidden state)** passed from step to step via a loop, so earlier info can affect later predictions.
- **Shapes:**
  - **One→One:** single input → single output (e.g., image → label)
  - **One→Many:** single input → sequence (e.g., image → caption)
  - **Many→One:** sequence → single label (e.g., review → sentiment)
  - **Many→Many:** sequence → sequence (e.g., translation)
- **LSTM (Long Short-Term Memory):** an RNN that **chooses what to remember/forget** using gates.
  Steps: take new input → mix with **previous memory** → **gates** decide keep/forget → **update memory** → **make output**.

## Convolutional Neural Networks (CNNs) — vision
- **Why:** images are grids; CNNs learn **visual features** (edges → textures → parts → objects).
- **Main layers (plain words + quick analogy):**
  - **Convolution:** tiny filters slide over the image to spot patterns (like a **blueprint detector**).
  - **Activation:** highlights useful patterns (the **pattern highlighter**).
  - **Pooling:** shrinks information to keep the important bits (a **room summarizer**) → fewer numbers, faster, less overfitting.
  - **Fully connected:** uses all learned features to decide the label (the **house expert**).
  - **Softmax:** turns scores into class probabilities (the **guess maker**).
  - **Dropout:** randomly drops units during training to reduce overfitting (the **quality checker**).
- **Typical pipeline:** input image → [Conv → Activation → Pool] × N → Fully Connected → Softmax.
- **Limits:** needs lots of data/computing, can **overfit**, harder to **explain**, can be sensitive to noise.
- **Common uses:** image classification, object detection, segmentation, face ID, medical imaging, autonomous driving, remote sensing.

## Model Zoo (when to use what)
- **FNN / MLP:** basic feed-forward nets for tabular/simple data.
- **CNN:** images/videos (grid-like data).
- **RNN / LSTM / GRU:** sequences, time series, language.
- **Autoencoders:** compress data, denoise, feature learning.
- **GANs:** generate new samples (images, audio).
- **Transformers:** state-of-the-art for language and more (LLMs, vision transformers).

## Practical Workflow (Deep Learning)
1. **Define task & metric.** (e.g., accuracy for classification, MAE/MSE for regression)
2. **Data:** collect → clean/label → train/val/test split → (for images) consider augmentation.
3. **Model:** start small/baseline → add layers/units carefully.
4. **Train:** pick batch size, learning rate; watch training **and** validation curves.
5. **Evaluate:** metrics + **error analysis** (what’s failing and why).
6. **Prevent overfitting:** more data, augmentation, **dropout**, **regularization**, early stopping.
7. **Deploy & monitor:** latency, drift, cost, and fairness.

## Quick Mental Map
- **Images/Videos → CNNs**
- **Text/Time Series → RNN/LSTM/Transformers**
- **Generation → GANs / Transformers**
- **Bigger/deeper isn’t always better:** increase **neurons/layers** only if validation results improve.

## Big Picture
- **AI → ML → Deep Learning → Generative AI (GenAI).**
- **GenAI** learns patterns from lots of examples and **creates new content**: text, code, images, audio, video.
- Two kinds of GenAI systems:
  - **Text-only** (LLMs).
  - **Multimodal** (mix of text + images/audio/video).

---

## LLM Basics
- **LLM = Large Language Model:** a math model that guesses the **next token** (small chunk of text).
- **Large** = many **parameters** (millions → billions). More parameters let it store more patterns.
- **Built with Transformers** (a deep‑learning design). Jobs: write, summarize, chat, answer, translate, code.

### Tokens & Embeddings
- **Tokens:** pieces of a word. Simple words may be 1 token; long/rare words may be several.
- **Embeddings:** number lists that represent the **meaning** of text. Similar meanings → vectors near each other.
  - Use in **semantic search** (find “meaning” matches) and **RAG** (retrieve helpful passages).

---

## Transformer — how it reads & writes
- **Why Transformers?** They look at all words **at once** using **attention** to see what relates to what.
- **Encoder:** turns input text into embeddings (good for understanding/search).
- **Decoder:** writes the answer **one token at a time** (good for generation).
- **Model types:**
  - **Encoder‑only:** BERT‑style → strong at search, classify, RAG re‑ranking.
  - **Decoder‑only:** GPT‑style → strong at **generating** text/code.
  - **Encoder‑Decoder:** T5‑style → strong at **translation** or “text‑to‑text” tasks.

> Quick example: “Jane threw the frisbee and her dog fetched it.”
> **Attention** helps map **“it”** to **“frisbee.”**

---

## Prompt Engineering (steer the model)
- **Goal:** say clearly what you want.
- Start simple → **iterate**.
- **Few‑shot (k‑shot):** show a few examples of the task.
- **Chain‑of‑Thought:** ask the model to **show steps**.
- **Formatting helps:** roles, bullet lists, constraints (tone, length).
- Note: models predict likely text, **not guaranteed truth** → can **hallucinate**.

---

## Alignment & Tuning
- **Instruction tuning:** fine‑tune on task instructions so it follows directions better.
- **RLHF (Reinforcement Learning from Human Feedback):** humans rank answers → training prefers better ones (safer, more helpful).
- **Domain fine‑tuning:** further train on **your** examples to learn your style, terms, or specialized tasks.
  - Upside: better accuracy for your use case; no extra runtime latency.
  - Cost: need labeled examples; risk of overfitting; must evaluate bias/safety.

---

## Retrieval‑Augmented Generation (RAG)
- **Idea:** at answer time, **search your knowledge** (docs, wiki, DB), pass the best passages to the model, and let it write the final answer.
- **Why:** keeps answers **grounded**, reduces **hallucination**, and stays **up‑to‑date** without retraining.
- **How:**
  1) Make **embeddings** for your docs and store in a **vector DB**.
  2) For a question, embed it and find **similar** passages.
  3) Put those passages in the prompt (**context**) → generate answer.
- **Tip:** add citations, chunk docs cleanly, filter by source/date, and evaluate relevance.

---

## Which method to use? (Prompting vs RAG vs Fine‑tuning)
| Method | Use when… | Pros | Cons |
|---|---|---|---|
| **Prompting** | Model already “knows” the topic | Fast to try, no training | Adds per‑request tokens; limited if model never saw your niche |
| **RAG** | Data changes often or must be factual/traceable | Latest info; grounded; no model retrain | Needs retrieval setup and clean data |
| **Fine‑tuning** | You need task/style accuracy beyond prompting+RAG | Higher accuracy for your domain; no extra inference latency | Needs labeled data; time/cost to train |
| **All of them** | You want best overall | Combine strengths | More system complexity |

**Simple path:** 1) Clear prompt → 2) Few‑shot → 3) Add RAG → 4) Fine‑tune → 5) Tune retrieval + prompts.

---

## Safety, Limits, and Quality
- **Hallucinations:** fix with RAG, better prompts, or verification steps.
- **Bias & safety:** check outputs on sensitive topics; add rules, filters, and audits.
- **Metrics:** track **accuracy**, **precision/recall** (Q&A), **faithfulness** (are claims in the sources?), latency, and cost.
- **Guardrails:** limit tools/data sources; add moderation and allow‑lists.

---

## Quick Glossary (one‑liners)
- **Parameters:** the model’s knobs.
- **Layers/Neurons/Weights/Bias/Activation:** building blocks of deep nets.
- **Attention:** focuses on important words.
- **Token:** small text piece; models read/write these.
- **Embedding:** vector that encodes meaning.
- **Vector DB:** database for embeddings + similarity search.
- **Instruction tuning / RLHF:** ways to align behavior.
- **RAG:** retrieval → add context → generate grounded answer.
- **Fine‑tuning:** keep training the model on your examples.

## Oracle AI Stack & Access
- **Access OCI AI services via:** OCI Console (UI), **REST APIs**, **Language SDKs**, and **OCI CLI**.
- **Core services (high level):**
  - **Language:** pretrained models (sentiment, key phrases), **custom models**, **translation**.
  - **Vision:** image analysis with **pretrained** or **custom** models.
  - **Speech:** speech-to-text, text-to-speech; speaker features.
  - **Document AI:** OCR + layout/entity extraction.
  - **Digital Assistant:** conversational bots powered by NLU.
  - **Data Science:** build/train/deploy ML with managed JupyterLab.

---

## OCI Data Science — What it is
- **Purpose:** end-to-end ML platform to **build, train, deploy, and monitor** models.
- **Interface:** **JupyterLab** notebook sessions with preinstalled libraries and the **Accelerated Data Science (ADS) SDK**.
- **Artifacts & Org:** **Projects**, **Notebook Sessions**, **Conda Environments**, **Model Catalog**, **Jobs**, **Model Deployments**.
- **Principles:** **Accelerated** (GPU/optimized libs), **Collaborative** (shared projects, jobs), **Enterprise-grade** (security, IAM, logging).

### Why use **OCI Data Science** instead of a local Jupyter Notebook?
- **Scale on demand:** spin up CPUs/GPUs (A100/H100/H200/B200/GB200) when needed; pause when idle.
- **Managed environments:** reproducible **Conda** envs; fewer “works on my machine” issues.
- **Data access:** private networking to OCI Object/File Storage, databases, data lakes.
- **Collaboration:** shared projects, versioned **Model Catalog**, **Jobs** for scheduled runs.
- **MLOps built-in:** easy **Model Deployments** (HTTPS endpoints), metrics/logging, IAM & VCN security.
- **Cost control:** right-size shapes; stop sessions; use jobs for off-hours training.
- **Compliance/security:** tenancy, compartments, policies, audit logs.
- **ADS SDK:** quick starters for data prep, training, evaluation, deployment.

---

## GPUs & Superclusters (plain-English)
- **GPU = many small cores** that do simple math **very fast in parallel** → perfect for deep learning.
- **NVIDIA lineup (simple view):**
  - **A100 (2020):** fast, 80GB.
  - **H100 (2022):** ~3× A100 speed, 80GB.
  - **H200 (2024):** like H100 **with more memory** (141GB).
  - **B200 (2025):** next-gen, ~2× H100, **192GB**.
  - **GB200 (2025):** **CPU+GPU together**, supercomputer-on-chip, for the **largest** models.
- **OCI Superclusters:** massive clusters that connect **tens of thousands of GPUs** with ultra‑fast networks + shared storage so training/fine‑tuning giant models is possible.

---

## Ethics & Reliability
- **Follow laws & policies.**
- Build **fair, robust, and transparent** systems; test for bias; protect privacy; keep audit trails.

---

## Typical OCI Data Science Workflow (from demo)
1. **Create a Project.**
2. Launch **Notebook Sessions** (select CPU/GPU, Conda env).
3. Use **ADS SDK** / notebooks for data prep & modeling.
4. Register models in **Model Catalog**.
5. Create **Jobs** for training/eval pipelines.
6. **Deploy** as managed endpoints; monitor logs/metrics.
7. Iterate and promote versions.

---

## Feature & Term Map (quick ref)
- **Project:** top-level workspace.
- **Notebook Session:** JupyterLab with chosen shape/env.
- **Conda Environment:** reproducible set of packages.
- **ADS SDK:** utilities for data → model → deployment.
- **Model Catalog:** registry of model artifacts & metadata.
- **Job:** scheduled/automated notebook or script run.
- **Model Deployment:** scalable HTTPS endpoint.

---

## What to remember
- Use **Console** for quick starts; **APIs/SDK/CLI** for automation.
- Pick service by modality: **Language / Vision / Speech / Document AI**.
- For team ML, prefer **OCI Data Science** over ad‑hoc notebooks: **scale, security, collaboration, and MLOps** built in.

# OCI AI Foundations — Oracle Generative AI

## What the service gives you
- **Customizable LLMs** you can call from apps.
- **Choice of model family:** Chat models (e.g., Cohere, Meta) and **Embedding models**.
- **Fine‑tuning options:** optimize a pretrained model on **your smaller, domain dataset** (e.g., Cohere’s few‑shot/fine‑tune).
- **Playground:** try prompts, tune settings, and test outputs in the browser.

---

## Model types (plain words)
- **Chat model:** you send a prompt, it writes an answer (use for chat, Q&A, summarization).
- **Embedding model:** turns text into **vectors** (number lists that capture meaning). Use for **semantic search**, **RAG**, deduping, clustering.

---

## Fine‑tuning (why/when)
- Start with a strong base model → teach it **your style/terms** using your examples.
- Helps when the base model **misses domain vocabulary** or **format**.
- Needs labeled examples and evaluation; keep a clean validation set.

---

## Dedicated AI Clusters (what and why)
**Problem:** Big AI jobs (fine‑tuning, heavy inference) need lots of **GPUs** and a **fast network**.
**Solution:** OCI gives you a **Dedicated AI Cluster**:
- A **private slice of GPUs** wired together with a **high‑speed RDMA network**.
- **Isolated** from other customers → **noisy‑neighbor free**, predictable speed, better security/compliance.
- Use it to **fine‑tune** big models and to run **inference** at scale.
- Think of it like getting your **own GPU farm** for your project, rather than sharing.

---

## Oracle Database 23ai (AI + data)
- **AI Vector Search:** store embeddings from your content; find **similar** passages fast → great for **RAG**.
- **Select AI:** “AI for your database” — ask questions in natural language; it plans queries and returns results (with your security in place).
- Designed to be **secure** (DB policies, roles) and **future‑ready** for AI apps.

---

## Typical build path on OCI GenAI
1. **Pick a model** (chat or embedding).
2. **Prototype in Playground** (prompts, temperature, system instructions).
3. (Optional) **Add RAG** using **23ai Vector Search** or another vector DB.
4. (Optional) **Fine‑tune** for your domain.
5. **Deploy** an endpoint; call via **Console, SDKs, REST, or CLI**.
6. **Monitor** quality, latency, and cost; iterate.

---

## When to use what
- **Just prompting**: quick tasks; model already knows the topic.
- **Prompting + RAG**: need **fresh, factual, cited** answers from your docs.
- **Fine‑tuning**: need **style/format/task accuracy** beyond prompting/RAG.
- **Dedicated cluster**: training or high‑throughput inference where you need **guaranteed GPU capacity**.

---

## Key terms
- **LLM, token, embedding, vector DB, RAG, fine‑tuning, RDMA, inference, playground.**

# OCI AI Foundations — Language, Speech, Vision, Document AI (Quick Notes)

## OCI Language
- Pretrained models in ~75 languages; industry-trained.
- Tasks: sentiment, key phrases, NER, language detection, PII/redaction, text classification, summarization, translation.
- No data science required; works via API/SDK/Console.

## OCI Speech
- Transcription (speech → text) with punctuation and casing.
- Text normalization and profanity filtering options.
- Supports diarization/timestamps; integrates with Language and RAG flows.

## OCI Vision
- Image classification (single/multi‑label) and object detection (bounding boxes).
- Use pretrained or custom models; dataset labeling, evaluation, deployment.

## Document AI
- Text recognition (OCR) and document classification.
- Language detection, table extraction, key‑value extraction for forms/invoices.
- Outputs structured data for downstream search, analytics, and automation.
