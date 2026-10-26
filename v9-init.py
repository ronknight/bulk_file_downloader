#!/usr/bin/env python3
"""
Comprehensive Auto-Documentation & AI Tools Configuration System Initializer

Sets up documentation, AI tool configurations, and repository memory for all AI assistants.
Automatically creates instructions, memory files, and compliance artifacts.

Usage: python init.py
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class ComprehensiveDocSystemInit:
    def __init__(self):
        self.repo_root = Path.cwd()
        self.dirs_to_create = [
            'docs/adr',
            '.agents/plugins',
            '.github',
            'openspec/diagram', 
            'openspec/changes',
            'archive',
            '.copilot',
            '.cursor',
            '.windsurf',
            '.cline',
            '.vscode',
            '.agent',
            '.agents',
            '.kilocode',
            '.roo',
            '.antigravity',
        ]
        
        # AI tools that should receive configuration
        self.ai_tools = {
            '.copilot': 'GitHub Copilot',
            '.cursor': 'Cursor',
            '.windsurf': 'Windsurf',
            '.cline': 'Claude with Cline',
            '.vscode': 'VS Code',
            '.agent': 'Agent',
            '.agents': 'Agents',
            '.kilocode': 'Kilocode',
            '.roo': 'Roo Cline',
            '.antigravity': 'Antigravity',
        }
        
        # Standard instruction files for each tool
        self.instruction_files = [
            'instructions.md',
            'copilot-instructions.md',
            '.copilot-instructions.md',
        ]
        
    def create_directories(self):
        """Create necessary directory structure."""
        for dir_path in self.dirs_to_create:
            (self.repo_root / dir_path).mkdir(parents=True, exist_ok=True)
        print("✓ Created directory structure")
    
    def detect_ai_tool_folders(self):
        """Detect all available AI tool folders at repository root."""
        detected = []
        for folder_name in self.ai_tools.keys():
            folder_path = self.repo_root / folder_name
            if folder_path.exists() and folder_path.is_dir():
                detected.append(folder_name)
        return detected
    
    def create_archive_script(self):
        """Create shell archiving script for Unix/Linux/Mac."""
        script_content = '''#!/bin/bash
# Shell script to archive project with timestamped folder
# Usage: ./archive-project.sh [project_path] [archive_path]
# Output: Creates timestamped folder in archive/ with complete project snapshot
# Note: Add "archive/" to .gitignore to keep archives local and avoid repo bloat

# Set default parameters
PROJECT_PATH="${1:-.}"
ARCHIVE_PATH="${2:-./archive}"

# Generate timestamp in format YYYY-MM-DD_HHmmss
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
ARCHIVE_FOLDER="$ARCHIVE_PATH/$TIMESTAMP"

# Create archive directory if it doesn't exist
if [ ! -d "$ARCHIVE_PATH" ]; then
    mkdir -p "$ARCHIVE_PATH"
fi

# Create timestamped archive directory
if [ ! -d "$ARCHIVE_FOLDER" ]; then
    mkdir -p "$ARCHIVE_FOLDER"
    echo "Created archive directory: $ARCHIVE_FOLDER"
else
    echo "Archive directory already exists: $ARCHIVE_FOLDER"
    exit 1
fi

# Define exclude patterns
EXCLUDE_PATTERNS=(".git" "archive" ".venv" "__pycache__" "*.pyc" ".DS_Store" "node_modules" "target" "build" "dist")

# Function to check if item should be excluded
should_exclude() {
    local item="$1"
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        case "$item" in
            $pattern) return 0 ;;
        esac
    done
    return 1
}

# Copy entire project to archive (excluding specified patterns)
cd "$PROJECT_PATH" || exit 1

total_items=0
for item in * .*; do
    # Skip . and .. directories
    if [ "$item" = "." ] || [ "$item" = ".." ]; then
        continue
    fi
    
    # Skip if item doesn't exist (handles case where no dotfiles exist)
    if [ ! -e "$item" ]; then
        continue
    fi
    
    # Check if item should be excluded
    if should_exclude "$item"; then
        continue
    fi
    
    # Copy item to archive folder
    if [ -d "$item" ]; then
        cp -r "$item" "$ARCHIVE_FOLDER/"
    else
        cp "$item" "$ARCHIVE_FOLDER/"
    fi
    ((total_items++))
done

echo "Archive created successfully at: $ARCHIVE_FOLDER"
echo "$total_items items archived"
'''
        
        (self.repo_root / 'archive-project.sh').write_text(script_content, encoding='utf-8')
        print("✓ Created: archive-project.sh")
        
        # Also create PowerShell version for Windows
        ps_content = '''# PowerShell script to archive project with timestamped folder
# Usage: .\\archive-project.ps1
# Output: Creates timestamped folder in archive/ with complete project snapshot

# Get current directory
$ProjectPath = Get-Location
$ArchivePath = Join-Path $ProjectPath "archive"

# Generate timestamp in format YYYY-MM-DD_HHmmss
$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$ArchiveFolder = Join-Path $ArchivePath $Timestamp

# Create archive directory if it doesn't exist
if (-not (Test-Path $ArchivePath)) {
    New-Item -ItemType Directory -Path $ArchivePath -Force | Out-Null
    Write-Host "Created archive directory: $ArchivePath"
}

# Check if timestamped archive already exists
if (Test-Path $ArchiveFolder) {
    Write-Host "Archive directory already exists: $ArchiveFolder"
    exit 1
}

# Create timestamped archive directory
New-Item -ItemType Directory -Path $ArchiveFolder -Force | Out-Null
Write-Host "Created archive directory: $ArchiveFolder"

# Define exclude patterns
$ExcludePatterns = @(".git", "archive", ".venv", "__pycache__", ".pyc", ".DS_Store", "node_modules", "target", "build", "dist", ".vscode", ".cursor", ".windsurf", ".cline", ".agent", ".agents")

# Get all items in project root
$items = Get-ChildItem -Force

$totalItems = 0
foreach ($item in $items) {
    $itemName = $item.Name
    
    # Check if item should be excluded
    $shouldExclude = $false
    foreach ($pattern in $ExcludePatterns) {
        if ($itemName -eq $pattern) {
            $shouldExclude = $true
            break
        }
    }
    
    if ($shouldExclude) {
        continue
    }
    
    # Copy item to archive folder
    $destination = Join-Path $ArchiveFolder $itemName
    if ($item.PSIsContainer) {
        Copy-Item -Path $item.FullName -Destination $destination -Recurse -Force
    } else {
        Copy-Item -Path $item.FullName -Destination $destination -Force
    }
    $totalItems++
}

Write-Host "Archive created successfully at: $ArchiveFolder"
Write-Host "$totalItems items archived"
'''
        
        (self.repo_root / 'archive-project.ps1').write_text(ps_content, encoding='utf-8')
        print("✓ Created: archive-project.ps1 (Windows)")
    
    def create_adr_template(self):
        """Create ADR template file."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        template_content = f'''# ADR: Lightweight Architecture Decision Records

## Date (ISO)
{today}

**Context**: For efficient decision documentation without heavy ceremony. We need a lightweight way to capture architectural decisions while maintaining clear ownership and traceability. Previous decisions were scattered across discussions, making them hard to reference later.

## Decision
We will adopt a lightweight ADR (Architecture Decision Record) system using markdown templates stored in version control. Each ADR is a single-page document including: ISO date, problem context, decision statement, consequences, decision owner, implementation lead, and an optional Git tag for release tracking. ADRs are stored chronologically in `docs/adr/` with a `YYYYMMDD-<title>.md` naming convention.

## Consequences

**Positive**:
- Decisions are explicitly documented and version-controlled
- Clear ownership ensures accountability  
- Easy to search and link from code comments and documentation
- Single-page format keeps decisions focused and concise
- No external tooling or approval gates required

**Tradeoffs**:
- Decision context relies on team familiarity with the domain
- No formal governance process; trust is placed in decision owners
- ADRs can become outdated as the codebase evolves

**Risks**:
- Decisions might be made without ADRs if not included in workflow → *Mitigation*: AI tools automatically create ADRs for architectural changes
- ADRs diverge from implementation over time → *Mitigation*: Treat ADRs as living documents; update them alongside code changes

## Decision Owner
Project Lead

## Implemented By
Auto-Documentation System

## Git Tag
adr/lightweight-adr-template
'''
        
        filename = f"{datetime.now().strftime('%Y%m%d')}-lightweight-adr-template.md"
        (self.repo_root / 'docs' / 'adr' / filename).write_text(template_content, encoding='utf-8')
        print(f"✓ Created: docs/adr/{filename}")
    
    def create_archiving_docs(self):
        """Create archiving documentation."""
        content = '''# Application Archiving Guide

## Purpose

This project uses timestamped directory snapshots for local version control and safe rollback capability. Before making significant changes to the codebase, create an archive to preserve the application state at that point in time.

## Archive Location

All project archives are stored in the `archive/` directory at the project root:
```
archive/
├── 2026-04-07_143022/     # Example: April 7, 2026 at 14:30:22 UTC
├── 2026-04-08_091545/     # Later archive  
└── 2026-04-10_162130/     # Another snapshot
```

**Archive Naming Convention**: `YYYY-MM-DD_HHmmss`
- `YYYY-MM-DD`: ISO date (e.g., 2026-04-07)
- `HHmmss`: Hour, minute, second in UTC (e.g., 143022 = 14:30:22)
- Example full path: `archive/2026-04-07_143022/`

## Creating an Archive

### Method 1: Automated Shell Script (Recommended)

The `archive-project.sh` script automates the archiving process:

```bash
./archive-project.sh
```

**What the script does**:
1. Creates a timestamped subfolder in `archive/` directory
2. Recursively copies all project files to the archive
3. Excludes: `.git/`, `.venv/`, `__pycache__/`, `*.pyc`, `.DS_Store`, `node_modules/`, `target/`, `build/`, `dist/`
4. Displays completion message with archive path

**Example output**:
```
Archive created successfully at: archive/2026-04-07_143022/
45 items archived
```

### Restoration

**Full Project Restoration**:
```powershell
# Copy entire archived project back to working directory
Copy-Item -Path "archive\\2026-04-07_143022\\*" -Destination "." -Recurse -Force
```

**Selective File Restoration**:
```powershell  
# Restore specific files
Copy-Item -Path "archive\\2026-04-07_143022\\src\\critical-file.py" -Destination "src\\critical-file.py"
```

## When to Archive

- Before major refactoring or architectural changes
- Before upgrading dependencies or frameworks
- Before experimental feature development
- Before production deployments
- AI tools automatically suggest archiving for significant changes

## Cleanup Strategy

Archives can accumulate over time. Consider:
- Keep last 10 archives for quick rollback  
- Archive older snapshots to external backup if needed
- Monitor disk space usage in `archive/` directory
- The `archive/` directory is automatically added to `.gitignore` to prevent repo bloat
- Archives remain local for fast rollback while keeping remote repository clean

## Bloat Management

**Repository Size**: Archives are excluded from git commits via `.gitignore`
**Local Storage**: Each archive = full project copy (~5-50MB depending on project size)  
**Cleanup Commands**:
```powershell
# Keep only last 5 archives
Get-ChildItem archive\\ | Sort-Object CreationTime | Select-Object -SkipLast 5 | Remove-Item -Recurse

# Remove archives older than 30 days  
Get-ChildItem archive\\ | Where-Object CreationTime -lt (Get-Date).AddDays(-30) | Remove-Item -Recurse
```'''
        
        (self.repo_root / 'docs' / 'ARCHIVING.md').write_text(content, encoding='utf-8')
        print("✓ Created: docs/ARCHIVING.md")
    
    def create_changelog(self):
        """Create initial CHANGELOG.md if it doesn't exist."""
        if (self.repo_root / 'CHANGELOG.md').exists():
            print("✓ CHANGELOG.md already exists")
            return
            
        content = f'''# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### {datetime.now().strftime('%Y-%m-%d')} - Auto-Documentation System
- Added timestamped archive directory system (`archive/<YYYY-MM-DD_HHmmss>/`) for local version control snapshots
- Created `archive-project.sh` shell script for automated project archiving
- Implemented lightweight ADR (Architecture Decision Record) system in `docs/adr/`
- Added mermaid diagram support in `openspec/diagram/` for GitHub-native rendering
- Configured AI chat tools for automatic documentation compliance
- Established file organization rules: documentation in `docs/`, specifications in `openspec/`, archives in `archive/`
'''
        
        (self.repo_root / 'CHANGELOG.md').write_text(content, encoding='utf-8')
        print("✓ Created: CHANGELOG.md")
    
    def create_openspec_config(self):
        """Create OpenSpec configuration."""
        config_content = '''schema: spec-driven

# Project context (optional)
# This is shown to AI when creating artifacts.
# Add your tech stack, conventions, style guides, domain knowledge, etc.
# Example:
#   context: |
#     Tech stack: Python, Flask, JavaScript
#     We use conventional commits
#     Domain: web application

# Per-artifact rules (optional)  
# Add custom rules for specific artifacts.
# Example:
#   rules:
#     proposal:
#       - Keep proposals under 500 words
#       - Always include a "Non-goals" section
#     tasks:
#       - Break tasks into chunks of max 2 hours
'''
        
        (self.repo_root / 'openspec' / 'config.yaml').write_text(config_content, encoding='utf-8')
        print("✓ Created: openspec/config.yaml")
    
    def create_sample_diagrams(self):
        """Create sample diagram files."""
        
        # Sample dataflow diagram
        dataflow_content = '''## System Data Flow Diagram

```mermaid
graph TD
    Start([User Input]) -->|Data| Process["Process Data<br/>Validation & Logic"]
    Process -->|Valid| Transform["Transform Data<br/>Business Logic"]
    Process -->|Invalid| Error["Return Error<br/>to User"]
    Transform -->|Processed| Storage[("Data Storage")]
    Storage -->|Retrieved| Output["Generate Output<br/>Response/File"]
    Output -->|Result| End([User Receives Result])
    Error -->|Feedback| Start
    
    style Start fill:#e1f5fe
    style Process fill:#ffe0b2  
    style Transform fill:#f3e5f5
    style Storage fill:#e8f5e8
    style Output fill:#e8f5e8
    style Error fill:#ffebee
    style End fill:#e8f5e8
```

## Legend

- **Blue (Cyan)**: User interaction points
- **Orange**: Processing/validation steps  
- **Purple**: Data transformation
- **Green**: Storage and output operations
- **Red**: Error handling

## Description

This diagram shows the basic data flow pattern through the system. Users provide input, which is processed and validated. Valid data flows through business logic transformation, gets stored if needed, and generates appropriate output. Invalid data triggers error handling with user feedback.

**Key Components:**
- Input validation with error feedback loop
- Business logic transformation layer
- Data persistence (if applicable)
- Output generation and delivery

Update this diagram when adding new data processing stages or changing the core system flow.
'''
        
        # Sample workflow diagram  
        workflow_content = '''## User Workflow Diagram

```mermaid
graph TD
    Start([User Starts]) -->|Access| Landing["Application<br/>Landing/Home"]
    Landing -->|Navigate| Action1["Primary Action<br/>Main Feature"]
    Landing -->|Navigate| Action2["Secondary Action<br/>Alternative Path"]
    
    Action1 -->|Input| Form1["Fill Form<br/>Required Fields"]
    Action2 -->|Configure| Setup["Configuration<br/>Settings/Preferences"]
    
    Form1 -->|Submit| Validate1{Validation<br/>Check}
    Setup -->|Save| Validate2{Validation<br/>Check}
    
    Validate1 -->|Pass| Process1["Process Request<br/>Execute Action"]
    Validate1 -->|Fail| Error1["Show Errors<br/>Return to Form"]
    Error1 --> Form1
    
    Validate2 -->|Pass| Process2["Save Settings<br/>Apply Configuration"]  
    Validate2 -->|Fail| Error2["Show Errors<br/>Return to Setup"]
    Error2 --> Setup
    
    Process1 -->|Complete| Success1["Success State<br/>Show Results"]
    Process2 -->|Complete| Success2["Settings Saved<br/>Confirmation"]
    
    Success1 -->|Continue| End([Workflow Complete])
    Success2 -->|Continue| End
    
    style Start fill:#e1f5fe
    style Landing fill:#e1f5fe
    style Action1 fill:#e1f5fe
    style Action2 fill:#e1f5fe
    style Form1 fill:#e1f5fe
    style Setup fill:#e1f5fe
    style Validate1 fill:#ffe0b2
    style Validate2 fill:#ffe0b2
    style Process1 fill:#f3e5f5
    style Process2 fill:#f3e5f5
    style Success1 fill:#e8f5e8
    style Success2 fill:#e8f5e8
    style Error1 fill:#ffebee
    style Error2 fill:#ffebee
    style End fill:#e8f5e8
```

## Workflow Description

This diagram represents the typical user journey through the application. Users start at a landing point and can choose between primary and secondary actions. Each path includes form filling or configuration, validation with error handling, processing, and success states.

**Key Features:**
- Multiple user entry paths
- Form validation with error feedback loops
- Clear success/error states
- Consistent user experience patterns

**Interaction Patterns:**
- All forms include validation with error recovery
- Success states provide clear feedback  
- Error states guide users back to correction points
- Workflow supports both primary and alternative user goals

Update this diagram when adding new user interaction paths or changing the core user experience flow.
'''
        
        (self.repo_root / 'openspec' / 'diagram' / 'dataflow.md').write_text(dataflow_content, encoding='utf-8')
        (self.repo_root / 'openspec' / 'diagram' / 'workflow.md').write_text(workflow_content, encoding='utf-8')
        print("✓ Created: openspec/diagram/dataflow.md")
        print("✓ Created: openspec/diagram/workflow.md")
    
    def build_repository_memory(self):
        """Build comprehensive repository memory shared by all AI tool artifacts."""
        return '''# Repository Memory: Auto-Documentation System

## STRUCTURED DEVELOPMENT WORKFLOWS

Apply these patterns based on task type - follow the sequence automatically:

### 🎯 New Feature Development
**Pattern**: Architecture → Design → Implementation → Testing → Deployment

1. **Propose architecture** - How does this fit into the existing system? Reference `openspec/` specs
2. **Design considerations** - API contracts, data models, dependencies. Create/update OpenSpec if needed
3. **Python best practices** - Type hints, error handling, async patterns where applicable
4. **Comprehensive testing** - Unit tests, integration tests, edge cases. Suggest pytest patterns
5. **Deployment readiness** - CI/CD considerations, environment variables, documentation updates
6. **Auto-create** - ADR in `docs/adr/` for major decisions, update `CHANGELOG.md`

### 🐛 Bug Fixing
**Pattern**: Diagnosis → Root Cause → Fix → Regression Testing → Review

1. **Systematic diagnosis** - Isolate the problem. Ask for error logs, reproduction steps, environment
2. **Root cause analysis** - Trace through code flow. Use Python debugging patterns (logging, breakpoints)
3. **Minimal fix** - Target the root cause, not symptoms. Keep changes focused
4. **Regression testing** - Add test cases that would catch this bug if reintroduced
5. **Code review lens** - Verify fix doesn't introduce other issues, check for edge cases

### 🔒 Security Audit
**Pattern**: Threat Review → Code Inspection → Guardian Checks → Approval

1. **Threat identification** - What are the attack vectors? (Authentication, injection, data exposure, etc.)
2. **Code inspection** - Review `services/auth.py`, `routes/api.py`, input validation, secrets handling
3. **Guardian checks** - Verify: no hardcoded secrets, proper input sanitization, secure dependencies
4. **Fix recommendations** - Suggest specific patches with examples
5. **Update docs** - Reference security decisions in ADR and code comments

### 📖 Code Documentation
**Pattern**: Reverse Engineer → Specification → Inline Docs → API Docs

1. **Analyze patterns** - Study existing code to understand intent and architecture
2. **Extract specification** - What does this module/function actually do? Document in comments
3. **Inline documentation** - Add docstrings with type hints, parameters, return values, examples
4. **API documentation** - Generate/update API specs in OpenAPI format if applicable
5. **Update specs** - Reflect in `openspec/specs/` if this is part of a feature spec

## AUTOMATIC COMPLIANCE RULES (SILENT APPLICATION)

### Critical: NO DISCUSSION OF DOCUMENTATION SYSTEM
- NEVER mention archiving, ADRs, changelog, or documentation processes in chat
- NEVER ask permission to create documentation
- NEVER announce documentation steps
- Apply patterns silently and automatically

### Critical: MemPalace-First Workflow
- Before asking the user for context, check MemPalace first
- Before responding about prior decisions, project history, people, or past events, use `mempalace_search` or `mempalace_kg_query`
- If MCP tools are unavailable, use the local CLI fallback: `mempalace search "<query>"`
- Treat MemPalace as the first source of project memory; ask the user only after memory lookup and repository inspection are insufficient
- Preserve session learnings with `mempalace_diary_write` when available

### Auto-Apply Before Major Changes
- If proposing significant code changes, include `./archive-project.sh` in first step (no explanation)
- For architectural changes, automatically create ADR in `docs/adr/YYYYMMDD-title.md`
- For any feature/change, automatically update `CHANGELOG.md` with proper format

### Silent Documentation Updates
- **ADR creation**: Use `docs/adr/` template format, name as `YYYYMMDD-kebab-case.md`
- **Changelog entries**: Always add `#### YYYY-MM-DD - Feature Name` with technical details
- **System diagrams**: Update `openspec/diagram/*.md` if flows change, use mermaid syntax
- **File placement**: All docs go to `docs/`, specs to `openspec/`, never create markdown at root

### Automatic Format Enforcement
- ADR: Date, Context, Decision, Consequences, Owner, Implementation, Git Tag fields
- Changelog: ISO dates, technical details, specific file paths affected
- Diagrams: Mermaid with colored nodes, explanatory text
- Organization: Respect root directory restrictions (only CHANGELOG.md, PRD.md, README.md)

### Implementation Style
- Include documentation steps naturally in implementation plan
- Treat as routine development tasks, not special documentation work  
- Never separate "documentation phase" - integrate seamlessly
- Apply repository organization rules without mentioning them

## Ready-to-Use Components

### Archiving System 
- **Script**: `./archive-project.sh` (automated timestamped backups)
- **Format**: `archive/YYYY-MM-DD_HHmmss/` 
- **Usage**: Run before major changes for rollback capability
- **Documentation**: `docs/ARCHIVING.md` (restoration procedures)

### ADR System
- **Template**: `docs/adr/` (lightweight template available)
- **Naming**: `docs/adr/YYYYMMDD-title.md` 
- **Format**: Date, Context, Decision, Consequences, Owner, Implementation, Git Tag

### Diagram System  
- **Location**: `openspec/diagram/`
- **Format**: Mermaid markdown (GitHub-native rendering)
- **Examples**: `workflow.md` (user flows), `dataflow.md` (system flows)
- **Colors**: Cyan (user input), Orange (validation), Purple (processing), Green (output)

### Changelog System
- **File**: `CHANGELOG.md` (project root)
- **Format**: `#### YYYY-MM-DD - Feature Name` with technical details
- **Standard**: ISO dates, specific paths, capabilities added/changed

### MemPalace System
- **Local source**: `mempalace/` nested project
- **Codex plugin**: `mempalace/.codex-plugin/plugin.json` exposes `mempalace-mcp`
- **Root plugin marketplace**: `.agents/plugins/marketplace.json` points Codex at the nested MemPalace plugin
- **Import fallback**: Application routes add `mempalace/` to `PYTHONPATH` before running `python -m mempalace`
- **Primary lookup**: `mempalace_search` for semantic memory, `mempalace_kg_query` for known facts
- **CLI fallback**: `mempalace search "<query>"`
- **Workflow rule**: Check MemPalace before asking the user for missing project context

### Multi-Repo Discovery
- **GitHub Copilot**: `.github/copilot-instructions.md` points to `.copilot/repository-memory.md`
- **Agent tools**: `AGENTS.md` points to `.copilot/repository-memory.md`
- **Nested clone support**: Open or attach this repository root when it is cloned inside another repository
- **Path policy**: Use repo-relative paths from this root; do not assume the parent repository is the project root

### File Organization Rules
- **Root**: Only `CHANGELOG.md`, `PRD.md`, `README.md` + app files
- **Documentation**: All in `docs/` (ADRs, guides, implementation notes) 
- **Specifications**: `openspec/` (diagrams, specs)
- **Archives**: `archive/` (timestamped snapshots)
'''
    
    def create_gitignore_entry(self):
        """Add archive directory to .gitignore to prevent repo bloat."""
        gitignore_path = self.repo_root / '.gitignore'
        archive_entry = '\n# Auto-documentation system archives (keep local to avoid repo bloat)\narchive/\n'
        
        if gitignore_path.exists():
            content = gitignore_path.read_text(encoding='utf-8')
            if 'archive/' not in content:
                gitignore_path.write_text(content + archive_entry, encoding='utf-8')
                print("✓ Added archive/ to .gitignore")
            else:
                print("✓ archive/ already in .gitignore")
        else:
            gitignore_path.write_text(archive_entry, encoding='utf-8')
            print("✓ Created .gitignore with archive/ exclusion")
    
    def create_copilot_instructions(self):
        """Create Copilot instructions file in .copilot folder."""
        instructions = self.build_copilot_instructions_content()
        
        (self.repo_root / '.copilot' / 'instructions.md').write_text(instructions, encoding='utf-8')
        print("✓ Created: .copilot/instructions.md")
    
    def create_ai_discovery_files(self):
        """Create standard AI instruction entrypoints for nested-repo discovery."""
        discovery_content = '''# Repository Instructions

This repository uses project-specific memory and workflow rules.

Before making or reviewing changes in this repository, read:

- `.copilot/repository-memory.md`

When this repository is cloned inside another repository, treat this directory as
the project root for repo-relative paths, MemPalace mining, OpenSpec changes,
archives, and changelog updates.

---

## Structured Development Workflows

Apply these workflow patterns based on the task type:

### 🎯 New Feature Development
**Pattern**: Architecture → Design → Implementation → Testing → Deployment

When implementing new features:
1. **Propose architecture** - How does this fit into the existing system? Reference `openspec/` specs.
2. **Design considerations** - API contracts, data models, dependencies. Create/update OpenSpec if needed.
3. **Python best practices** - Type hints, error handling, async patterns where applicable.
4. **Comprehensive testing** - Unit tests, integration tests, edge cases. Suggest pytest patterns.
5. **Deployment readiness** - CI/CD considerations, environment variables, documentation updates.
6. **Auto-create** - ADR in `docs/adr/` for major decisions, update `CHANGELOG.md`

### 🐛 Bug Fixing
**Pattern**: Diagnosis → Root Cause → Fix → Regression Testing → Review

When debugging issues:
1. **Systematic diagnosis** - Isolate the problem. Ask for error logs, reproduction steps, environment.
2. **Root cause analysis** - Trace through code flow. Use Python debugging patterns (logging, breakpoints).
3. **Minimal fix** - Target the root cause, not symptoms. Keep changes focused.
4. **Regression testing** - Add test cases that would catch this bug if reintroduced.
5. **Code review lens** - Verify fix doesn't introduce other issues, check for edge cases.

### 🔒 Security Audit
**Pattern**: Threat Review → Code Inspection → Guardian Checks → Approval

When reviewing for security:
1. **Threat identification** - What are the attack vectors? (Authentication, injection, data exposure, etc.)
2. **Code inspection** - Review `services/auth.py`, `routes/api.py`, input validation, secrets handling.
3. **Guardian checks** - Verify: no hardcoded secrets, proper input sanitization, secure dependencies.
4. **Fix recommendations** - Suggest specific patches with examples.
5. **Update docs** - Reference security decisions in ADR and code comments.

### 📖 Code Documentation
**Pattern**: Reverse Engineer → Specification → Inline Docs → API Docs

When documenting code:
1. **Analyze patterns** - Study existing code to understand intent and architecture.
2. **Extract specification** - What does this module/function actually do? Document in comments.
3. **Inline documentation** - Add docstrings with type hints, parameters, return values, examples.
4. **API documentation** - Generate/update API specs in OpenAPI format if applicable.
5. **Update specs** - Reflect in `openspec/specs/` if this is part of a feature spec.

---

## Python Project Conventions

- **Type hints**: Required for all function signatures
- **Testing**: pytest-based tests in `tests/` directory (or co-located with source)
- **Error handling**: Use custom exceptions, never silent failures
- **Async patterns**: Use async/await consistently, avoid mixing blocking calls
- **Import organization**: Standard lib → third-party → local (isort style)
'''

        (self.repo_root / '.github' / 'copilot-instructions.md').write_text(
            discovery_content,
            encoding='utf-8'
        )
        print("✓ Created: .github/copilot-instructions.md")

        (self.repo_root / 'AGENTS.md').write_text(discovery_content, encoding='utf-8')
        print("✓ Created: AGENTS.md")

    def create_mempalace_plugin_marketplace(self):
        """Expose the nested MemPalace plugin from this repository root."""
        marketplace = {
            "name": "auto-documentation-system",
            "interface": {
                "displayName": "Auto-Documentation System"
            },
            "plugins": [
                {
                    "name": "mempalace",
                    "source": {
                        "source": "local",
                        "path": "./mempalace/.codex-plugin"
                    },
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "NONE"
                    },
                    "category": "Coding"
                }
            ]
        }

        marketplace_path = self.repo_root / '.agents' / 'plugins' / 'marketplace.json'
        marketplace_path.write_text(json.dumps(marketplace, indent=2) + '\n', encoding='utf-8')
        print("✓ Created: .agents/plugins/marketplace.json")

    def distribute_ai_tool_configs(self):
        """Distribute configuration files to all detected AI tool folders."""
        detected_tools = self.detect_ai_tool_folders()
        
        if not detected_tools:
            print("ℹ No additional AI tool folders detected")
            return
        
        print()
        print(f"🔍 Detected AI tool folders: {', '.join(detected_tools)}")
        print(f"📦 Distributing configuration to all {len(detected_tools)} AI tools...")
        print()
        
        # Get the configuration content
        memory_content = self.build_repository_memory()
        instructions_content = self.build_copilot_instructions_content()
        
        # Distribute to each detected AI tool folder
        for tool_folder in detected_tools:
            tool_path = self.repo_root / tool_folder
            tool_path.mkdir(exist_ok=True)
            
            # Write repository-memory.md
            memory_file = tool_path / 'repository-memory.md'
            memory_file.write_text(memory_content, encoding='utf-8')
            
            # Write copilot-instructions.md
            instructions_file = tool_path / 'copilot-instructions.md'
            instructions_file.write_text(instructions_content, encoding='utf-8')
            
            print(f"✓ {tool_folder}/repository-memory.md")
            print(f"✓ {tool_folder}/copilot-instructions.md")
    
    def build_copilot_instructions_content(self):
        """Build copilot instructions content for AI tool folders."""
        return '''# AI Chat Tool Instructions

You are working with a repository that has an established auto-documentation system and structured development workflows.

## Structured Development Workflows

Apply these patterns automatically based on the user request - follow the sequence without asking:

### 🎯 New Feature Development
**Pattern**: Architecture → Design → Implementation → Testing → Deployment

When implementing new features:
1. **Propose architecture** - How does this fit into the existing system? Reference `openspec/` specs
2. **Design considerations** - API contracts, data models, dependencies. Create/update OpenSpec if needed
3. **Python best practices** - Type hints, error handling, async patterns where applicable
4. **Comprehensive testing** - Unit tests, integration tests, edge cases. Suggest pytest patterns
5. **Deployment readiness** - CI/CD considerations, environment variables, documentation updates
6. **Auto-create** - ADR in `docs/adr/` for major decisions, update `CHANGELOG.md`

### 🐛 Bug Fixing
**Pattern**: Diagnosis → Root Cause → Fix → Regression Testing → Review

When debugging issues:
1. **Systematic diagnosis** - Isolate the problem. Ask for error logs, reproduction steps, environment
2. **Root cause analysis** - Trace through code flow. Use Python debugging patterns (logging, breakpoints)
3. **Minimal fix** - Target the root cause, not symptoms. Keep changes focused
4. **Regression testing** - Add test cases that would catch this bug if reintroduced
5. **Code review lens** - Verify fix doesn't introduce other issues, check for edge cases

### 🔒 Security Audit
**Pattern**: Threat Review → Code Inspection → Guardian Checks → Approval

When reviewing for security:
1. **Threat identification** - What are the attack vectors? (Authentication, injection, data exposure, etc.)
2. **Code inspection** - Review `services/auth.py`, `routes/api.py`, input validation, secrets handling
3. **Guardian checks** - Verify: no hardcoded secrets, proper input sanitization, secure dependencies
4. **Fix recommendations** - Suggest specific patches with examples
5. **Update docs** - Reference security decisions in ADR and code comments

### 📖 Code Documentation
**Pattern**: Reverse Engineer → Specification → Inline Docs → API Docs

When documenting code:
1. **Analyze patterns** - Study existing code to understand intent and architecture
2. **Extract specification** - What does this module/function actually do? Document in comments
3. **Inline documentation** - Add docstrings with type hints, parameters, return values, examples
4. **API documentation** - Generate/update API specs in OpenAPI format if applicable
5. **Update specs** - Reflect in `openspec/specs/` if this is part of a feature spec

## CRITICAL: Silent Compliance Mode
- NEVER discuss documentation processes in chat
- NEVER ask permission for documentation tasks  
- NEVER announce archiving, ADR creation, or changelog updates
- Apply documentation patterns automatically and silently

## CRITICAL: MemPalace-First Context
- Check MemPalace before asking the user for missing context
- Use `mempalace_search` or `mempalace_kg_query` before answering about prior decisions, project history, people, or past events
- If MCP tools are unavailable, use `mempalace search "<query>"` as the local CLI fallback
- Ask the user only after MemPalace lookup and repository inspection do not answer the question

## Python Project Conventions

- **Type hints**: Required for all function signatures
- **Testing**: pytest-based tests in `tests/` directory (or co-located with source)
- **Error handling**: Use custom exceptions, never silent failures
- **Async patterns**: Use async/await consistently, avoid mixing blocking calls
- **Import organization**: Standard lib → third-party → local (isort style)
'''

    def setup_application_files(self):
        """Set up application dependency and environment files."""
        requirements_path = self.repo_root / 'requirements.txt'
        if not requirements_path.exists():
            requirements_content = '''# Core dependencies for auto-documentation-system
flask>=2.3.0
werkzeug>=2.3.0
jinja2>=3.1.0

# Documentation and file processing
pyyaml>=6.0
markdown>=3.4.0
python-dateutil>=2.8.0

# Optional: Development dependencies
# pytest>=7.0.0
# black>=22.0.0
# flake8>=4.0.0
'''
            requirements_path.write_text(requirements_content, encoding='utf-8')
            print("✓ Created: requirements.txt")
        
        env_path = self.repo_root / '.env.example'
        if not env_path.exists():
            env_content = '''# ============================================
# FLASK CONFIGURATION
# ============================================
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=true
FLASK_PORT=5000

# ============================================
# DOCUMENTATION SYSTEM
# ============================================
# Archive directory for project snapshots
ARCHIVE_PATH=./archive

# Documentation directory
DOCS_PATH=./docs

# Enable automatic archiving before changes
AUTO_ARCHIVE=true

# ============================================
# API CONFIGURATION
# ============================================
# API base URL for external integrations
API_BASE_URL=http://localhost:5000/api

# Enable API authentication (optional)
API_AUTH_ENABLED=false
API_SECRET_KEY=your-secret-key-here
'''
            env_path.write_text(env_content, encoding='utf-8')
            print("✓ Created: .env.example")
    
    def run(self):
        """Execute the complete initialization."""
        print("🚀 Initializing Auto-Documentation System...")
        print()
        
        self.create_directories()
        self.create_archive_script()
        self.create_gitignore_entry()
        self.create_adr_template()
        self.create_archiving_docs()
        self.create_changelog()
        self.create_openspec_config()
        self.create_sample_diagrams()
        copilot_dir = self.repo_root / '.copilot'
        copilot_dir.mkdir(exist_ok=True)
        memory_content = self.build_repository_memory()
        (copilot_dir / 'repository-memory.md').write_text(memory_content, encoding='utf-8')
        print("✓ Created: .copilot/repository-memory.md")
        self.create_copilot_instructions()
        self.create_ai_discovery_files()
        self.create_mempalace_plugin_marketplace()
        self.distribute_ai_tool_configs()
        self.setup_application_files()
        
        print()
        print("✅ Auto-Documentation System Initialized Successfully!")
        print()
        print("📁 Created Structure:")
        print("   docs/adr/          - Architecture Decision Records")
        print("   openspec/diagram/  - Mermaid diagrams")  
        print("   archive/           - Timestamped backups")
        print("   .copilot/          - AI tool configuration")
        print()
        print("🔧 Created Tools:")
        print("   archive-project.sh        - Automated archiving script")
        print("   requirements.txt          - Python dependencies")
        print("   CHANGELOG.md             - Change tracking")
        print("   docs/ARCHIVING.md        - Archiving documentation")
        print()
        print("🎯 Structured Development Workflows:")
        print("   • New Feature Development  - Architecture → Design → Implementation → Testing → Deployment")
        print("   • Bug Fixing              - Diagnosis → Root Cause → Fix → Regression Testing → Review")
        print("   • Security Audit          - Threat Review → Code Inspection → Guardian Checks → Approval")
        print("   • Code Documentation     - Reverse Engineer → Specification → Inline Docs → API Docs")
        print()
        print("🤖 AI Integration:")
        detected_tools = self.detect_ai_tool_folders()
        ai_tools_str = ", ".join(detected_tools) if detected_tools else "None detected"
        print(f"   Detected AI tool folders: {ai_tools_str}")
        print("   .copilot/instructions.md  - Structured workflow patterns + silent compliance")
        print("   .github/copilot-instructions.md - GitHub Copilot entrypoint")
        print("   AGENTS.md                 - Agent tool entrypoint")
        print("   .agents/plugins/marketplace.json - MemPalace plugin marketplace")
        print("   Repository memory         - Context-aware documentation")
        if detected_tools:
            print(f"   ✓ Configuration distributed to: {ai_tools_str}")
        print()
        print("📋 Next Steps:")
        print("   1. pip install -r requirements.txt     - Install dependencies")
        print("   2. ./archive-project.sh                - Create initial archive")
        print("   3. Start documenting in docs/adr/      - Create ADRs")
        print("   - Repository memory configured for silent compliance")
        print("   - Copilot instructions set for automatic documentation")
        print("   - Structured workflows configured for all AI tools")
        print("   - File organization rules enforced")
        print() 
        print("🎯 Initialization Complete:")
        print("   ✓ Copilot will automatically apply structured workflows")
        print("     • New features: Architecture → Design → Tests → Deploy")
        print("     • Bug fixes: Diagnosis → Root Cause → Fix → Regression Tests")
        print("     • Security: Threat Review → Inspection → Checks → Approval")
        print("     • Documentation: Reverse Engineer → Spec → Docs → API Docs")
        print("   ✓ AI tools will follow documentation patterns silently")
        print("   ✓ Run `./archive-project.sh` before major changes")
        print("   ✓ Archives are kept local (in .gitignore) to prevent repo bloat")

if __name__ == "__main__":
    init = ComprehensiveDocSystemInit()
    init.run()
