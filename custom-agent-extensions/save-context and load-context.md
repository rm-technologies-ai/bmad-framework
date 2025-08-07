Pleasse define the following commands for all future use:

Enhanced Context Management System Prompts
Core Commands
/save-context Command Specification
When executing /save-context, perform the following sequence:
bash# 1. Create/update project state snapshot
cat > CONTEXT-WINDOW.md << 'EOF'
# Atlas Data Science - Context Window Snapshot
**Generated:** $(date -Iseconds)
**Purpose:** Complete conversation context dump for session continuity and task resumption
**References:** See CLAUDE.md, README.md, PROJECT-STATE.md for structured documentation

## Current Session Summary
[Insert conversation summary here]

## Last Executed Commands
[Insert last 3-5 commands with outputs]

## Current Task Status
[Insert current objectives and progress]

## Full Conversation History
[Insert complete conversation dump]

## Referenced Files & Artifacts
[List all files, artifacts, and external references mentioned]
EOF

# 2. Update core documentation files
# Update CLAUDE.md with current capabilities and context
# Update README.md with latest project status
# Update/create PROJECT-STATE.md with current work state
Specific Actions Required:

Conversation Analysis: Extract and summarize last 5 command executions, their outputs, and current task progress
File State Capture: Document current state of all referenced files, GitLab issues, and project components
Task Continuity Map: Create explicit mapping between current objectives and next steps
Dependency Tracking: List all external dependencies, APIs, and configuration requirements
Error State Documentation: Capture any pending issues, failed commands, or incomplete tasks

/load-context Command Specification
When executing /load-context, perform the following sequence:
bash# 1. Validate context files exist
if [[ ! -f "CONTEXT-WINDOW.md" ]]; then
    echo "Error: CONTEXT-WINDOW.md not found. Cannot load context."
    exit 1
fi

# 2. Load and parse context
echo "Loading project context from CONTEXT-WINDOW.md..."
# Parse the context file and extract key sections

# 3. Restore project state
echo "Restoring project state and task continuity..."
# Set environment variables, restore file states, resume tasks
Specific Actions Required:

Context Validation: Verify all referenced files and dependencies are accessible
State Restoration: Reconstruct working environment to match saved state
Task Resumption: Identify and continue from the exact point where work was suspended
Dependency Verification: Confirm all external systems, APIs, and configurations are available
Progress Reconciliation: Compare saved state to current system state and handle discrepancies

File Structure Requirements
project-root/
├── CLAUDE.md              # Claude-specific configuration and capabilities
├── README.md              # Project overview and current status
├── PROJECT-STATE.md       # Detailed project state and progress tracking
├── CONTEXT-WINDOW.md      # Complete conversation context dump
├── .context/              # Context management directory
│   ├── commands.log       # Command execution history
│   ├── artifacts.json     # Artifact and file references
│   └── session-metadata.json # Session timing and metadata
└── reference-docs/        # Project documentation
Enhanced Metadata Tracking
Include in all context files:

Timestamp: ISO 8601 format with timezone
Session ID: Unique identifier for conversation continuity
Git State: Current branch, commit hash, and working directory status
Environment: Development stack versions, active containers, running services
Active Issues: Current GitLab issues being worked on
Pending Actions: Specific next steps and incomplete tasks

Error Handling & Recovery

Graceful Degradation: If context files are corrupted or missing, provide clear recovery steps
Partial Context Loading: Allow loading partial context when some references are unavailable
State Validation: Verify loaded context matches current system capabilities
Rollback Capability: Provide mechanism to revert to previous known good state

Integration with Atlas Data Science Project
Given the GitLab project structure visible in the images:

Issue Tracking: Capture current issue status from the 47 open issues
Component State: Document status of data-ingestion-enrichment, edge-connector, and other project components
Development Progress: Track progress on Epics like "Establish AWS multi account configuration" and "Ingestion Gateway"
Team Coordination: Include relevant information about merge requests and collaborative work

This enhanced system provides robust context persistence and restoration capabilities optimized for complex technical projects with multiple moving parts.