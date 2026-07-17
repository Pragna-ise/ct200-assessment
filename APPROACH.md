# CT200 QA System - Approach Document

# 1. Architecture

The system converts the CT200 manual into a structured hierarchical document tree and supports versioning, selections, LLM-generated QA test cases, staleness detection, and retrieval.

Workflow:

Markdown Document
↓
Parser
↓
Hierarchy Builder
↓
SQLite Storage
↓
Version Management
↓
Selection API
↓
Groq LLM Generation
↓
Generation Storage
↓
Staleness Detection
↓
Retrieval API

---

# 2. Data Model

The system uses SQLite for storing document structure and metadata.

Tables:

## documents

Stores document information.

- id
- name

## document_versions

Stores document versions.

- id
- document_id
- version_name
- created_at

## nodes

Stores document tree nodes.

- id
- logical_node_id
- version_id
- title
- content
- content_hash
- level
- parent_title

## selections

Stores user selections.

- id
- name

## selection_nodes

Maps selections to nodes.

- selection_id
- node_id

## generations

Stores generated QA outputs.

- id
- selection_id
- generated_text
- model_name
- source_hash

---

# 3. Markdown Parsing Strategy

The parser reads the markdown document line by line.

For every heading:

- Extract heading title
- Determine heading level
- Create node object
- Store content until next heading

Each node contains:

- Title
- Level
- Content
- Parent
- Content Hash

---

# 4. Handling Document Irregularities

## Duplicate Headings

Duplicate headings are stored as separate nodes.

They receive different database IDs and maintain independent parent relationships.

## Missing Content

Empty sections are still stored as valid nodes.

## Nested Headings

Parent-child relationships are assigned using heading levels.

A stack-based hierarchy builder is used to determine parents.

---

# 5. Version Matching Strategy

Logical node matching is performed using normalized section titles.

Example:

Battery Life
battery life

Both resolve to:

logical_node_id = battery life

Advantages:

- Simple
- Deterministic
- Fast

Limitations:

If a heading is renamed significantly between versions, the system may incorrectly treat it as a new node.

Example:

Battery Life
Battery Lifetime

would be treated as different logical nodes.

---

# 6. Browse API Design

The Browse API supports:

- Listing top-level sections
- Retrieving a node and its children
- Searching document content
- Viewing version changes

Change detection is based on content hash comparison between versions.

---

# 7. Selection Design

Selections allow users to group multiple nodes.

Selections are version-pinned because they store actual node IDs belonging to a specific document version.

This ensures that selections continue to reference the exact content they were created from even after newer document versions are ingested.

---

# 8. LLM Prompt Design

The system uses Groq with the Llama 3.3 70B Versatile model.

Prompt Structure:

- QA Engineer Role
- Selected Manual Content
- Request for 3–5 QA Test Cases
- Required Fields:
  - Test Case Name
  - Objective
  - Expected Result

The LLM only receives content from the selected nodes.

---

# 9. Structured Output Validation

LLM responses are validated before storage.

Validation Rules:

- Response must not be empty
- Response must exceed minimum length
- Invalid responses are rejected

If validation fails:

- Output is not stored
- Error response is returned

This prevents malformed or empty generations from entering the system.

---

# 10. Generation Storage Strategy

Generated outputs are stored in:

- SQLite database
- JSON files inside generated_outputs/

The stored generation includes:

- Selection ID
- Generated Text
- Source Hash
- Model Name

This ensures generated outputs remain traceable even when document versions change.

---

# 11. Staleness Detection Strategy

Every generation stores a SHA256 hash of the exact content used during generation.

When a generation is retrieved:

Current Selection Content
↓
New SHA256 Hash
↓
Compare With Stored Hash

If hashes differ:

stale = true

Otherwise:

stale = false

---

# 12. Staleness Limitations

Hash comparison identifies content changes but does not understand semantic importance.

Examples:

Minor punctuation change → stale = true

Major pressure threshold change → stale = true

Both changes are treated equally.

Therefore impact is reported as:

- none
- unknown

instead of claiming semantic understanding.

---

# 13. Retrieval Strategy

Generated outputs can be retrieved by:

## Generation ID

Returns a specific generation.

## Selection ID

Returns all generations associated with a selection.

## Node ID

Returns all generations associated with selections containing that node.

Every retrieval response includes:

- stale status
- impact status

---

# 14. Decision Log

## Decision 1: Title-Based Node Matching

Reason:

Simple and deterministic.

Limitation:

Heading renames may break matching.

---

## Decision 2: SHA256 Hashes

Reason:

Fast and reliable change detection.

Limitation:

Cannot determine semantic importance.

---

## Decision 3: Version-Pinned Selections

Reason:

Guarantees historical traceability.

---

## Decision 4: Groq LLM

Reason:

Fast inference and free-tier availability.

---

## Decision 5: Duplicate Generation Policy

Policy:

Allow duplicate generations.

Reason:

Different LLM executions may produce different outputs even for the same selection.

---

## Decision 6: JSON Output Storage

Reason:

Provides lightweight document-oriented storage for generated outputs.

---

# 15. Future Improvements

- SQLAlchemy ORM migration
- MongoDB integration
- Semantic node matching using embeddings
- Structured JSON output from LLM
- Automatic regeneration of stale outputs
- Improved diff summaries
- User authentication and access control

