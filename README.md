#  Applied AI Engineer Challenge: Multi-Agent Content Generation System
A modular, agentic content generation system that autonomously converts structured product data into machine-readable JSON pages using multi-agent orchestration, reusable content logic blocks, and template-based automation.

## Problem Statement
Modern content systems often rely on monolithic scripts or prompt-based pipelines that tightly couple data parsing, logic, and content generation. These approaches are difficult to scale, reuse, or audit, especially when generating structured, machine-readable outputs across multiple page types.

## Objective 
The objective of this project is to Design and implement a modular agentic automation system that takes a small product dataset and automatically generates structured, machine-readable content pages.  
- multi-agent workflows
- automation graphs
- reusable content logic
- template-based generation
- structured JSON output
- system abstraction & documentation 

---

## Solution Overview
This system implements a **multi-agent content automation pipeline** where:
- Each agent has a **single, well-defined responsibility**
- A central **orchestrator** controls execution order and data flow
- Reusable **content logic blocks** transform data deterministically
- Custom **templates** define page structure and formatting
- All outputs are emitted as **machine-readable JSON**

The system automatically generates:
- A **Product Page**
- An **FAQ Page** (with 15+ categorized questions)
- A **Comparison Page** (against a fictional product)
- An **orchestration graph** describing execution flow

All processing strictly uses the provided dataset and **does not add external facts**.

---

## Scope & Assumptions

Scope
- Processes a single structured product dataset
- Uses a modular, multi-agent architecture with orchestration
- Generates Product, FAQ, and Comparison pages
- Produces fully structured, machine-readable JSON outputs
- Implements reusable content logic blocks and custom templates

Assumptions
- Input data is well-structured and schema-consistent
- No external data sources or research are used
- All content is derived strictly from the given dataset
- Comparison uses a fictional competitor
- The system runs as a batch automation pipeline

---

## System Design (Core Architecture)

The system is designed as a **layered, agentic architecture** with explicit data flow and zero hidden global state.

---

### 1. High-Level System Architecture
This diagram shows the complete system structure from input to final outputs, highlighting agent boundaries and separation of concerns.

![System Architecture](System Design/System Architecture.png)

**Key Design Principles**
- Orchestrator manages execution and coordination
- Agents operate independently with clear I/O contracts
- Content logic blocks are reusable and stateless
- Templates define structure, not business logic
- Outputs are always structured JSON

---

### 2. Orchestration Graph (DAG)
This diagram represents the **automation graph** executed by the orchestrator.  
Each node represents an agent or processing step, and edges represent data dependencies.

![Orchestration Graph](<img width="1354" height="312" alt="Screenshot 2025-12-25 175139" src="https://github.com/user-attachments/assets/f00a33aa-e4a5-4d1f-8b0f-cf5a23bb37b4" />)

**Why this matters**
- Demonstrates non-monolithic execution
- Enables extensibility and agent reuse
- Makes execution order explicit and auditable

---

### 3. End-to-End Flow Chart
This flow chart explains the system behavior at a **conceptual level**, suitable for non-technical stakeholders.

![Flow Chart](<img width="1206" height="157" alt="Screenshot 2025-12-25 174522" src="https://github.com/user-attachments/assets/0e6e83ef-43f4-4f30-bfe7-319ccc2e0694" />)

**Flow Summary**
1. Product data is ingested
2. Data is parsed into an internal model
3. Content logic blocks are generated
4. FAQ questions are auto-generated and categorized
5. Pages are rendered using templates
6. JSON outputs are saved

---

### 4. Sequence Diagram (Runtime Interaction)
This sequence diagram illustrates runtime interactions between the orchestrator and agents.

![Sequence Diagram](Screenshot%202025-12-25%20170225.png)

**What this demonstrates**
- Orchestrator is the single controller
- Agents do not share global state
- All communication is explicit
- The pipeline is deterministic and traceable

---

## Agent Responsibilities (Conceptual View)

| Agent | Responsibility |
|------|---------------|
| Data Parser Agent | Converts raw product input into a structured internal model |
| Question Generator Agent | Generates 15+ categorized user questions |
| Content Block Agents | Produce benefits, usage, ingredients, safety, comparison data |
| Page Generator Agent | Assembles pages using templates |
| Orchestrator | Coordinates execution and data flow |

Each agent:
- Has a single responsibility
- Defines explicit inputs and outputs
- Can be replaced or extended independently

---

## Reusable Content Logic Blocks

Content logic is implemented as **pure, reusable blocks**, such as:
- Benefits extraction
- Usage instruction formatting
- Ingredient listing
- Safety disclaimer generation
- Product comparison logic

These blocks:
- Contain no orchestration logic
- Are template-agnostic
- Can be reused across multiple page types

---

## Template Engine Design

Templates are **structured definitions**, not free-text prompts.

Each template specifies:
- Required fields
- Dependencies on content blocks
- Output structure
- Formatting rules

Templates exist for:
- Product Page
- FAQ Page
- Comparison Page

This separation ensures **business logic and presentation remain decoupled**.

---

## Outputs

All final outputs are generated as **machine-readable JSON**:

- `product_page.json`
- `faq.json`
- `comparison_page.json`
- `graph.json` (orchestration metadata)

These outputs are suitable for:
- CMS ingestion
- API responses
- Static site generators
- Downstream automation pipelines

---

## Conclusion

This project demonstrates a **production-style agentic automation system** focused on **modularity, orchestration, and system design**, rather than content writing. It fully satisfies the assignment requirements and reflects real-world engineering practices for scalable AI systems.
