# COGENT Hook System

Shell scripts and Go utilities that integrate with Claude Code's hook system to detect file changes and trigger documentation generation.

## Architecture

- **Hook Scripts**: Shell scripts called by Claude Code
- **Go Utilities**: Compiled binaries for complex operations
- **Event Detection**: PostToolUse event monitoring
- **Async Processing**: Background documentation generation

## Key Components

### Hook Scripts
- `cogent-hook` - Main hook script entry point
- `post-tool-use.sh` - PostToolUse event handler
- `validate-config.sh` - Configuration validation

### Go Utilities  
- `file-detector/` - File change detection logic
- `doc-generator/` - Subagent documentation generation
- `config-validator/` - Configuration validation

## Hook Integration

### Claude Code Configuration
```json
{
  "hooks": {
    "postToolUse": {
      "command": "cogent-hook post-tool-use",
      "tools": ["Edit", "Write", "MultiEdit"],
      "timeout": 30000
    }
  }
}
```

### Hook Workflow

1. **Event Detection**: Claude Code calls hook after file modifications
2. **Synchronous Summary**: Generate brief file summary immediately
3. **Async Documentation**: Spawn subagent for detailed documentation
4. **Error Handling**: Graceful fallback if documentation fails

## Hook Behavior

### PostToolUse Event
- Triggered after Edit, Write, MultiEdit tools
- Receives file path and content changes
- Returns success/failure to Claude Code
- Spawns background documentation process

### File Change Detection
- Compares file hashes to detect actual changes
- Filters out non-documentation-worthy changes
- Respects include/exclude patterns from config

### Documentation Generation
- Uses Task tool to spawn Claude Code subagent
- Generates comprehensive documentation asynchronously
- Updates cross-references and related files
- Validates documentation quality

## Development

```bash
# Make scripts executable
chmod +x hooks/*.sh

# Build Go utilities
cd hooks/file-detector && go build
cd hooks/doc-generator && go build

# Test hook integration
./hooks/cogent-hook post-tool-use test-file.go
```

## Configuration

Hooks read from `.cogent/config.json`:
- File patterns for inclusion/exclusion
- Documentation templates
- Timeout settings
- Backend API configuration

## Error Handling

- Hooks never block code changes
- Failed documentation generates warnings
- Retry logic for transient failures
- Fallback placeholder documentation

## Track Assignments

This component is assigned to **Track 1: Hook System Development**.