# 🤖 AI Software Engineering Team

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A production-ready multi-agent system that simulates a complete software engineering team using CrewAI**

[Features](#-features) • [Architecture](#-architecture) • [Agents](#-meet-the-team) • [Installation](#-installation) • [Usage](#-usage) • [Output](#-output-artifacts)

</div>

---

## 🎯 Overview

This project demonstrates an **autonomous AI-powered software development pipeline** that transforms high-level requirements into production-ready code, tests, and documentation. It showcases real-world enterprise patterns including requirements validation, code review, and iterative quality assurance.

### Key Innovation: Cost-Optimized Multi-LLM Architecture

**Problem:** LLM APIs are expensive at scale. Typical enterprise setups spend hundreds/month.

**Solution:** This project uses a **strategic multi-provider approach** that costs **$0 (free tier)** while maintaining enterprise-grade quality:
- Fast requirements analysis with Groq's ultra-fast Llama models
- Advanced code generation with Google Gemini
- Intelligent task-model matching for maximum efficiency

### Why This Project?

| Traditional Approach | This AI Team | Cost Difference |
|---------------------|--------------|-----------------|
| Manual requirement analysis | Automated contradiction & edge case detection | Hours of work → Minutes |
| Single-pass development | Multi-agent validation at each stage | Error-prone → Quality-assured |
| Code review bottlenecks | Instant security & quality analysis | Weeks → Minutes |
| Documentation as afterthought | Auto-generated docs from code | Manual → Automated |
| Enterprise LLM costs | Free-tier only architecture | $500+/month → $0 |

---

## ✨ Features

### 🔄 End-to-End SDLC Automation
- **Requirements → Design → Code → Review → Test → Documentation**
- Complete software lifecycle managed by specialized AI agents

### 💰 100% Free-Tier AI Infrastructure
- **Zero cost** to run the entire project
- Mix of Groq (fast, free inference) and Gemini (advanced reasoning)
- Optimized model selection per task for maximum efficiency
- Suitable for production-scale workflows

### 🧠 Intelligent Memory System
- **Short-term Memory**: Context sharing between agents within a run
- **Long-term Memory**: Pattern learning across multiple project generations
- **Entity Memory**: Tracking modules, classes, and requirements for consistency

### 🔍 Enterprise-Grade Quality Gates
- Requirements validation with IEEE 830 compliance
- Security-focused code review (OWASP-aware)
- Test prioritization based on code review findings

### 📊 Comprehensive Outputs
- Structured requirements specifications
- Technical design documents
- Production-ready Python modules
- Interactive Gradio demo UIs
- Code review reports with severity ratings
- Unit test suites
- Professional documentation (README, API docs, Quickstart)

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI SOFTWARE ENGINEERING TEAM                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │ Requirements │───▶│  Engineering │───▶│   Backend    │───▶│  Frontend  │ │
│  │   Analyst    │    │     Lead     │    │   Engineer   │    │  Engineer  │ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └────────────┘ │
│         │                   │                   │                   │        │
│         ▼                   ▼                   ▼                   ▼        │
│   requirements.md      design.md           module.py            app.py      │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │     Code     │───▶│     Test     │───▶│  Doc Writer  │                   │
│  │   Reviewer   │    │   Engineer   │    │              │                   │
│  └──────────────┘    └──────────────┘    └──────────────┘                   │
│         │                   │                   │                            │
│         ▼                   ▼                   ▼                            │
│   code_review.md      test_module.py     PROJECT_DOCS.md                    │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                          🧠 MEMORY LAYER                                     │
│            Short-term │ Long-term │ Entity Tracking                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 👥 Meet the Team

### 1. 🔍 Requirements Analyst
> *"Catching issues before they become bugs"*

| Aspect | Details |
|--------|---------|
| **Role** | Business Analyst & Requirements Engineer |
| **Responsibilities** | Validates requirements, detects contradictions, identifies edge cases |
| **Standards** | IEEE 830 Software Requirements Specifications |
| **Output** | `{module}_requirements.md` with acceptance criteria |

**Key Capabilities:**
- Contradiction & ambiguity detection
- Edge case identification
- Complexity risk assessment
- MoSCoW prioritization
- Testable acceptance criteria generation

---

### 2. 📐 Engineering Lead
> *"Translating requirements into actionable designs"*

| Aspect | Details |
|--------|---------|
| **Role** | Technical Architect |
| **Responsibilities** | Creates detailed technical designs from validated requirements |
| **Output** | `{module}_design.md` with class/method specifications |

**Key Capabilities:**
- Module architecture design
- Method signature specification
- Edge case handling strategies
- Self-contained module design

---

### 3. 💻 Backend Engineer
> *"Writing clean, efficient Python code"*

| Aspect | Details |
|--------|---------|
| **Role** | Python Developer |
| **Responsibilities** | Implements backend logic following the design |
| **Execution** | Safe code execution with Docker sandboxing |
| **Output** | `{module}.py` - Production-ready Python module |

**Key Capabilities:**
- Design-compliant implementation
- Error handling
- Clean code practices
- Self-contained modules

---

### 4. 🎨 Frontend Engineer
> *"Making backends accessible through intuitive UIs"*

| Aspect | Details |
|--------|---------|
| **Role** | Gradio UI Specialist |
| **Responsibilities** | Creates interactive demo interfaces |
| **Output** | `app.py` - Gradio-powered demo UI |

**Key Capabilities:**
- Rapid prototyping
- Backend integration
- User-friendly interfaces

---

### 5. 🛡️ Code Reviewer
> *"Quality is not an act, it's a habit"*

| Aspect | Details |
|--------|---------|
| **Role** | Senior Code Reviewer |
| **Responsibilities** | Security, quality, and performance analysis |
| **Standards** | OWASP Top 10, SOLID principles |
| **Output** | `{module}_code_review.md` with severity-rated findings |

**Review Categories:**
| Category | What's Checked |
|----------|----------------|
| 🔒 Security | Input validation, injection risks, data exposure |
| ⚠️ Error Handling | Unhandled exceptions, edge cases |
| ⚡ Performance | Algorithm efficiency, memory usage |
| 📏 Code Quality | Complexity, DRY, naming, SOLID |
| ✅ Requirements | Compliance verification |

**Severity Levels:** Critical → High → Medium → Low → Info

---

### 6. 🧪 Test Engineer
> *"If it's not tested, it's broken"*

| Aspect | Details |
|--------|---------|
| **Role** | QA Engineer |
| **Responsibilities** | Writes comprehensive unit tests informed by code review |
| **Framework** | pytest with Arrange-Act-Assert pattern |
| **Output** | `test_{module}.py` |

**Key Capabilities:**
- Prioritizes tests based on code review findings
- Edge case coverage from requirements analysis
- Security scenario testing
- Positive and negative test cases

---

### 7. 📝 Documentation Writer
> *"Good documentation is the difference between a project and a product"*

| Aspect | Details |
|--------|---------|
| **Role** | Technical Writer |
| **Responsibilities** | Generates comprehensive project documentation |
| **Framework** | Diátaxis documentation system |
| **Output** | `PROJECT_DOCS.md` (README, API Reference, Quickstart) |

**Documentation Includes:**
- Project overview with badges
- Feature list
- Installation instructions
- Quick start guide
- API reference with examples
- Testing instructions

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Core programming language |
| ![CrewAI](https://img.shields.io/badge/CrewAI-FF6B6B?style=flat) | Multi-agent orchestration framework |
| ![Groq](https://img.shields.io/badge/Groq-FF8C42?style=flat) | Fast inference LLM backend |
| ![Gemini](https://img.shields.io/badge/Gemini-4285F4?style=flat&logo=google&logoColor=white) | Google's multimodal LLM |
| ![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=flat) | Interactive UI generation |
| ![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white) | Testing framework |

---

## 🤖 Intelligent Model Selection Strategy

This project optimizes cost and performance by strategically selecting different LLMs for different tasks. All models are available in the **free tier**, making this enterprise-grade architecture accessible to everyone.

### Model Allocation

| Agent | Model | Rationale | Cost Tier |
|-------|-------|-----------|-----------|
| **Requirements Analyst** | `groq/llama-3.1-8b-instant` | Fast analysis for structured requirements | ✅ Free |
| **Engineering Lead** | `groq/llama-3.3-70b-versatile` | More capable for complex architecture design | ✅ Free |
| **Backend Engineer** | `gemini/gemini-2.5-flash-lite` | Excellent code generation with small token footprint | ✅ Free |
| **Frontend Engineer** | `gemini/gemini-2.5-flash-lite` | Optimized for UI generation | ✅ Free |
| **Code Reviewer** | `groq/llama-3.3-70b-versatile` | Comprehensive analysis of code quality & security | ✅ Free |
| **Test Engineer** | `gemini/gemini-2.5-flash-lite` | Strong at writing test cases | ✅ Free |
| **Doc Writer** | `gemini/gemini-2.5-flash` | Best for documentation quality | ✅ Free |

### Why This Strategy?

<table>
<tr>
<td width="50%">

#### 🚀 Cost Efficiency
- Mix of Groq (ultra-fast) & Gemini (excellent quality)
- Entirely free tier - no paid API required
- Average cost per run: **$0 (free tier limits)**

</td>
<td width="50%">

#### ⚡ Performance Optimization
- Groq: 200+ tokens/sec (fast reasoning)
- Gemini: Advanced reasoning (good for code)
- Different models for different workloads
- Best-in-class capability per dollar

</td>
</tr>
</table>

### Provider Strengths

#### Groq (llama-3.1-8b-instant & llama-3.3-70b-versatile)
| Strength | Usage |
|----------|-------|
| ⚡ **Ultra-fast inference** | Perfect for requirements analysis & quick reviews |
| 💰 **Free tier** | Unlimited requests within rate limits |
| 🎯 **Open-source models** | Transparent, reproducible results |

**Best for:** Analysis, structured output, code review logic

#### Google Gemini (gemini-2.5-flash-lite & gemini-2.5-flash)
| Strength | Usage |
|----------|-------|
| 📝 **Excellent at code generation** | Backend implementation, tests |
| 🧠 **Multimodal capabilities** | Understands complex architectures |
| ✅ **Reliable structured output** | API docs, documentation |
| 💰 **Competitive free tier** | 2M tokens/month free |

**Best for:** Code generation, documentation, creative problem-solving

### Free Tier Limits

| Provider | Free Limit | Your Usage |
|----------|-----------|------------|
| **Groq** | 30 requests/minute | ✅ Compatible |
| **Google Gemini** | 2M tokens/month | ✅ Well within limits |

---

## 📦 Installation

### Prerequisites
- Python 3.10 - 3.12
- [UV](https://docs.astral.sh/uv/) package manager (recommended)
- Google API key for Gemini

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/software_team_agents.git
cd software_team_agents
```

### Step 2: Install Dependencies

**Using UV (Recommended):**
```bash
pip install uv
crewai install
```

**Using pip:**
```bash
pip install -e .
```

### Step 3: Configure Environment
Create a `.env` file in the root directory with your free-tier API keys:

```env
# Google Gemini API Key (Free tier: 2M tokens/month)
# Get it from: https://ai.google.dev/
GOOGLE_API_KEY=your_gemini_api_key_here

# Groq API Key (Free tier: 30 requests/minute)
# Get it from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here
```

#### How to Get Free API Keys

**Google Gemini:**
1. Visit [https://ai.google.dev/](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new project or select existing
4. Copy the generated API key

**Groq:**
1. Visit [https://console.groq.com/](https://console.groq.com/)
2. Sign up for free account
3. Create an API key
4. Copy the key to `.env`

---

## 🚀 Usage

### Basic Run
```bash
crewai run
```

### Custom Requirements
Edit `src/engineering_team/main.py` to specify your requirements:

```python
requirements = """
Your custom requirements here...
"""
module_name = "your_module.py"
class_name = "YourClass"
```

### Example: Account Management System
```python
requirements = """
A simple account management system for a trading simulation platform.
- Create accounts, deposit/withdraw funds
- Record share buy/sell transactions
- Calculate portfolio value and profit/loss
- Report holdings and transaction history
- Prevent invalid transactions (negative balance, insufficient shares)
"""
```

---

## 📁 Output Artifacts

After a successful run, the `output/` directory contains:

```
output/
├── {module}_requirements.md    # Validated requirements spec
├── {module}_design.md          # Technical design document
├── {module}.py                 # Backend implementation
├── app.py                      # Gradio demo UI
├── {module}_code_review.md     # Code review report
├── test_{module}.py            # Unit test suite
└── PROJECT_DOCS.md             # README + API docs + Quickstart
```

## 🧠 Memory System

The crew uses CrewAI's memory system for intelligent context management:

| Memory Type | Function | Example |
|-------------|----------|---------|
| **Short-term** | Cross-agent context in single run | Code Reviewer sees Requirements Analyst's risk flags |
| **Long-term** | Learning across multiple runs | Remembers coding patterns from previous projects |
| **Entity** | Tracks key entities | Maintains consistency in class/module naming |

```python
# Enabled in crew.py
Crew(
    memory=True,
    respect_context_window=True,
)
```

---

## 📊 Project Structure

```
software_team_agents/
├── src/engineering_team/
│   ├── config/
│   │   ├── agents.yaml         # Agent definitions
│   │   └── tasks.yaml          # Task definitions
│   ├── tools/
│   │   ├── __init__.py
│   │   └── custom_tool.py      # Custom tools
│   ├── __init__.py
│   ├── crew.py                 # Crew orchestration
│   └── main.py                 # Entry point
├── knowledge/
│   └── user_preference.txt     # RAG knowledge base
├── output/                     # Generated artifacts
├── pyproject.toml
├── .env                        # API keys (not committed)
└── README.md
```

---

## 🔮 Future Enhancements

- [ ] **DevOps Agent**: Generate Dockerfile, CI/CD pipelines
- [ ] **CLI Interface**: `typer`-based command line tool
- [ ] **RAG Knowledge Base**: Coding standards, security guidelines
- [ ] **Streamlit Dashboard**: Visual workflow monitoring
- [ ] **Parallel Execution**: Hierarchical process for independent tasks

---

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) - Multi-agent orchestration framework
- [Google Gemini](https://ai.google.dev/) - LLM backbone
- [Gradio](https://gradio.app/) - UI framework

---

