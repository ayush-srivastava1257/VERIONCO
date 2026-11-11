# VERIONCO: A Risk-Adaptive, Evidence-Centric Adversarial Multi-Agent Decision-Support Framework for Precision Oncology

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cohort: TCGA-LUAD](https://img.shields.io/badge/Cohort-TCGA--LUAD%20(n=478)-green.svg)](https://portal.gdc.cancer.gov/projects/TCGA-LUAD)
[![Architecture: 14 Agents](https://img.shields.io/badge/Architecture-14%20Multi--Agent%20Dialectic-purple.svg)]()
[![Safety: Conformal Triage](https://img.shields.io/badge/Safety-Conformal%20Uncertainty%20Gating-red.svg)]()

> **Official repository for the study:**  
> *"VERIONCO: A Risk-Adaptive, Evidence-Centric Adversarial Multi-Agent Decision-Support Framework for Precision Oncology — A Comprehensive Multi-Agent Framework Mitigating Confirmation Bias and Miscalibration Across 478 Patients in Non-Small Cell Lung Cancer"*  
> **Authors:** Ayush Srivastava, Abhigyan Sinha, OmKumar Chandra Umakanthan, Suguna Marappan  
> **Affiliation:** School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, India  
> **Contact:** `ayush.srivastava2023a@vitstudent.ac.in`

---

## Executive Summary

Clinical application of Large Language Models (LLMs) in precision oncology is severely hindered by **confirmation bias** and **epistemic overconfidence**. Standard Retrieval-Augmented Generation (RAG) engines retrieve biomedical literature primarily to confirm initial therapeutic hypotheses, frequently missing critical negative factors such as acquired resistance alterations, drug contraindications, or multi-driver co-mutations.

**VERIONCO** introduces a closed-loop dialectical decision-support architecture that structures clinical reasoning across **14 specialized agents** and **4 distinct phases**:
1. **Multi-Omic Evidence Graph Synthesis:** Combines whole-exome somatic variant calls (MAF), copy-number profiles (GISTIC2.0), and gigapixel whole-slide image (WSI) patch embeddings (UNI ViT-Large/16) into a 295,854-node property graph.
2. **Polarity-Decoupled Dual-Stream Retrieval:** Simultaneously retrieves affirming support evidence and contraindicative counter-evidence.
3. **Adversarial Deliberation and Red-Teaming:** Incorporates a blinded independent second opinion, multidisciplinary orchestration, adversarial red-team critique (10 clinical failure modes), and required evidence-based plan revision.
4. **Conformal Uncertainty Gating:** Applies split-conformal prediction ($U(p) < 0.40$) to achieve selective classification, autonomously accepting confident cases and triaging complex, high-risk cases to human Multidisciplinary Tumor Boards (MDT).

---

## Key Empirical Findings (TCGA-LUAD, n = 478)

* **Overconfidence Miscalibration Mitigation:** Reduces proxy Expected Calibration Error (ECE) by **46.5%** (from $0.8225$ in standard RAG to $0.4397$) and Brier score from $0.6816$ to $0.4415$.
* **Breaking Confirmation Bias:** Counter-evidence retrieval uncovers resistance factors in **44.98%** of patients ($215/478$), driving a **14.85%** treatment recommendation pivot (McNemar $p < 0.0001$).
* **Adversarial Red-Team Catch Rate:** Catches **58.16%** of simulated high/critical clinical vulnerabilities ($278/478$), driving a **38.49%** plan revision rate ($184/478$, McNemar $p < 0.0001$).
* **Selective Guideline Concordance:** Achieves **81.36%** selective concordance ($179/220$) on the accepted autonomous cohort ($46.03\%$ coverage), reducing accepted silent failures to **1.82%** ($4/220$).
* **MDT Referral:** Systematically refers **53.97%** of complex, multi-alteration cases ($258/478$) to expert tumor boards with standardized 6-part clinical packets.

---

## Multi-Agent Architectural Taxonomy

| Agent ID | Agent Role | Subsystem / Phase | Engine / Model | Primary Function |
| :--- | :--- | :--- | :--- | :--- |
| **Agent 1** | Cohort Ingestion & Registry | Phase I: Multi-Omic Ingestion | GDC Data Client | Downloads and audits tripartite patient files with MD5 verification |
| **Agent 2** | WSI Pathology Engine | Phase I: Multi-Omic Ingestion | OpenSlide & UNI ViT-Large/16 | Segments tumor parenchyma and extracts 1024-d patch embeddings |
| **Agent 3** | Genomic Variant Curator | Phase I: Multi-Omic Ingestion | BioPython & CIViC Registry | Normalizes somatic MAF variants and calculates coding TMB |
| **Agent 4** | Clinical Staging Phenotyper | Phase I: Multi-Omic Ingestion | Pandas & XML/JSON Parser | Normalizes AJCC 7th/8th TNM stage and demographic variables |
| **Agent 5** | Heterogeneous Graph Builder | Phase I: Multi-Omic Ingestion | NetworkX MultiDiGraph | Builds unified 295,854-node multimodal evidence property graph |
| **Agent 6** | Topological Conflict Detector | Phase I: Multi-Omic Ingestion | Graph Cycle & Constraint Engine | Traverses graph and flags 1,176 genuine clinical contradictions |
| **Agent 7** | Support Retrieval Engine | Phase II: Dual-Stream Retrieval | ChromaDB Vector Index | Queries affirmative guideline and trial evidence (cosine sim $\ge 0.70$) |
| **Agent 8** | Counter-Evidence Retriever | Phase II: Dual-Stream Retrieval | ChromaDB Negated Query Engine | Retrieves drug resistance, toxicity, and clinical trial exclusions |
| **Agent 9** | Primary Treatment Planner | Phase III: Adversarial Deliberation | Gemini 1.5 Flash (temp=0.1) | Formulates initial guideline-concordant first-line therapy |
| **Agent 10** | Blind Second Opinion | Phase III: Adversarial Deliberation | Gemini 1.5 Flash (temp=0.3) | Independently reasons directly from raw molecular evidence |
| **Agent 11** | Multidisciplinary Orchestrator | Phase III: Adversarial Deliberation | Gemini 1.5 Flash (temp=0.1) | Synthesizes primary and second opinions; flags candidate discordances |
| **Agent 12** | Adversarial Red-Team Critic | Phase III: Adversarial Deliberation | Gemini 1.5 Flash (temp=0.4) | Aggressively probes 10 vulnerability classes to falsify recommendations |
| **Agent 13** | Deliberative Revision Planner | Phase III: Adversarial Deliberation | Gemini 1.5 Flash (temp=0.1) | Defends plan with Phase III evidence or pivots to safer alternative |
| **Agent 14** | Conformal Uncertainty Safety Gate | Phase IV: Conformal Triage | Conformal Prediction Logic | Evaluates composite uncertainty $U(p)$ and routes to ACCEPT vs MDT |

---

## Repository Structure

```
VERIONCO/
├── 00_cohort_and_download.ipynb               # Cohort audit, GDC download manifests, tripartite join
├── 01_pathology_pipeline.ipynb                # Gigapixel WSI tissue segmentation, patch QC, UNI embeddings
├── 02_genomic_pipeline.ipynb                  # Somatic variant curation, CIViC mapping, TMB calculation
├── 03_clinical_extraction.ipynb               # Clinical TNM extraction, patient staging tables
├── 04_evidence_graph_conflict.ipynb           # 295,854-node NetworkX graph construction & cycle detection
├── 05_retrieval_support_counter.ipynb         # ChromaDB dual-stream support & counter-evidence retrieval
├── 06_hypothesis_and_planners.ipynb           # Guideline grounding & primary treatment plan formulation
├── 07_orchestrator_redteam_secondopinion.ipynb# Blind second opinion, orchestration, and red-team attacks
├── 08_uncertainty_safety_gate.ipynb           # Conformal uncertainty calibration & 6-part MDT dossier generation
├── 09_ablation_experiments.ipynb              # Unified 6-rung ablation benchmark (Systems A through F)
├── 10_stats_failure_analysis.ipynb            # McNemar tests, bootstrap CIs, ECE curves, subgroup metrics
├── data/
│   ├── manifests/                             # 19 partitioned GDC WSI download manifests & batch summaries
│   ├── retrieval/                             # CIViC evidence summaries, PubMed corpus, ClinicalTrials JSON
│   └── tcga/                                  # TCGA-LUAD PanCancer Atlas 2018 tabular and clinical files
├── figures/                                   # High-resolution publication figures and dashboards
├── requirements.txt                           # Core Python dependencies
├── .gitignore                                 # Git rules (excludes API keys, large binaries, WSIs)
├── LICENSE                                    # MIT License
└── README.md                                  # Repository documentation
```

---

## Availability of Data and Materials

All datasets and models utilized in this study are publicly and freely accessible:

1. **TCGA-LUAD Multi-Omic and Clinical Data (n = 478):**
   * PanCancer Atlas publication portal: [https://gdc.cancer.gov/about-data/publications/pancanatlas](https://gdc.cancer.gov/about-data/publications/pancanatlas)
   * cBioPortal for Cancer Genomics (`luad_tcga_pan_can_atlas_2018`): [https://www.cbioportal.org/study/summary?id=luad_tcga_pan_can_atlas_2018](https://www.cbioportal.org/study/summary?id=luad_tcga_pan_can_atlas_2018)
2. **Diagnostic Whole-Slide Pathology Images (WSI):**
   * NCI GDC Data Portal: [https://portal.gdc.cancer.gov/repository](https://portal.gdc.cancer.gov/repository) (retrievable via `data/manifests/gdc_manifest_batch_1.txt` to `19.txt` and the public GDC API `https://api.gdc.cancer.gov/data/{file_id}`).
3. **Clinical Interpretation of Variants in Cancer (CIViC):**
   * CIViC Data Releases: [https://civicdb.org/releases](https://civicdb.org/releases) (`nightly-ClinicalEvidenceSummaries.tsv`).
4. **Biomedical Literature Corpus (PubMed / MEDLINE):**
   * National Library of Medicine PubMed: [https://pubmed.ncbi.nlm.nih.gov/](https://pubmed.ncbi.nlm.nih.gov/).
5. **ClinicalTrials.gov Registry:**
   * U.S. National Library of Medicine: [https://clinicaltrials.gov/](https://clinicaltrials.gov/) (API: [https://clinicaltrials.gov/api/v2/studies](https://clinicaltrials.gov/api/v2/studies)).
6. **Clinical Practice Guidelines:**
   * NCCN NSCLC Guidelines v3.2024: [https://www.nccn.org/](https://www.nccn.org/)
   * ESMO Early & Locally Advanced NSCLC Guidelines (2025): [https://www.esmo.org/](https://www.esmo.org/)
   * ASCO Stage IV NSCLC with Driver Alterations: [https://www.asco.org/](https://www.asco.org/)
   * NICE NG122: [https://www.nice.org.uk/guidance/ng122](https://www.nice.org.uk/guidance/ng122)
7. **Computational Pathology Foundation Model (UNI):**
   * Mahmood Lab Hugging Face repository: [https://huggingface.co/MahmoodLab/UNI](https://huggingface.co/MahmoodLab/UNI).

---

## Quickstart and Installation

### 1. Clone Repository and Setup Environment
```bash
git clone https://github.com/ayush-srivastava1257/VERIONCO.git
cd VERIONCO

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure API Keys
Configure your LLM provider keys in an environment variable or local config file (note: `.gitignore` automatically blocks secret commits):
```bash
export GEMINI_API_KEY="your-api-key"
```

---

## Citation

If you find this work, evidence graph schemas, or multi-agent architecture useful in your research, please cite:

```bibtex
@article{srivastava2024verionco,
  title={VERIONCO: A Risk-Adaptive, Evidence-Centric Adversarial Multi-Agent Decision-Support Framework for Precision Oncology},
  author={Srivastava, Ayush and Sinha, Abhigyan and Umakanthan, OmKumar Chandra and Marappan, Suguna},
  journal={arXiv preprint},
  year={2024},
  institution={Vellore Institute of Technology, Chennai}
}
```

---

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
