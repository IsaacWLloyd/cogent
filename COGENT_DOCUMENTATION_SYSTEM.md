# Cogent Documentation System - Setup & Usage Guide

## Overview
The Cogent Documentation System automatically generates comprehensive documentation for code files when they are edited through Claude Code. This system uses Claude Code's hook feature to trigger documentation creation, ensuring your codebase stays well-documented.

## How It Works
1. When you edit a code file using Claude Code (via Edit, Write, or MultiEdit tools)
2. The hook system triggers the documentation script
3. A documentation template is created at `.cogent/[path]/[filename].md`
4. Claude Code is instructed to fill in the template with actual content

## Setup Instructions

### Prerequisites
- Claude Code CLI installed and configured
- Bash shell available at `/bin/bash`
- Write permissions in your project directory

### Installation Steps

1. **The system is already installed!** The following components have been created:
   - `.claude/settings.json` - Hook configuration
   - `.cogent/create-documentation.sh` - Documentation generation script
   - Template embedded in the script

2. **Verify Installation**:
   ```bash
   # Check hook configuration
   cat .claude/settings.json
   
   # Verify script is executable
   ls -la .cogent/create-documentation.sh
   ```

3. **Test the System**:
   ```bash
   # Manual test (optional)
   echo '{"hook_event_name":"PostToolUse","tool_name":"Edit","tool_input":{"file_path":"/path/to/your/file.py"}}' | .cogent/create-documentation.sh
   ```

4. **Important**: Restart Claude Code for the hooks to take effect. Hooks are loaded at startup.

## Configuration

### Hook Configuration (`.claude/settings.json`)
The hook is configured to:
- Trigger on Edit, Write, and MultiEdit operations using a regex matcher
- The filtering for file types is handled in the bash script
- Skip documentation for:
  - Markdown files (`.md`)
  - Configuration files (`.json`, `.yml`, `.yaml`, `.toml`)
  - Lock files and environment files
  - Files in `.cogent/`, `.claude/`, `node_modules/`, `dist/`, etc.

### Customizing File Filters
To exclude additional file types or directories, edit the filtering logic in `.cogent/create-documentation.sh`:
```bash
# Check if file should be skipped
if [[ "$file_path" =~ \.(md|json|yml|yaml|toml|lock|gitignore|env)$ ]] || \
   [[ "$file_path" =~ /\.(cogent|claude|git)/ ]] || \
   [[ "$file_path" =~ /(node_modules|dist|__pycache__)/ ]]; then
    log "Skipping file based on exclusion rules: $file_path"
    exit 0
fi
```

## Example Walkthrough

### Scenario: Editing a Python Authentication Module

1. **You edit a file** `src/auth/login.py` using Claude Code:
   ```
   User: "Add input validation to the login function in src/auth/login.py"
   Claude: [Makes the edit using the Edit tool]
   ```

2. **Hook triggers automatically**:
   - The hook detects the Edit operation
   - Checks that `src/auth/login.py` is not in the exclusion list
   - Executes `.cogent/create-documentation.sh`

3. **Documentation template created** at `.cogent/src/auth/login.py.md`:
   ```markdown
   # Documentation: `login.py`
   
   ## File Overview
   [AI: Please describe the overall purpose and functionality of this file in 2-3 paragraphs]
   
   ## Intent
   [AI: Please explain the intent behind this file - why it was created and what problem it solves]
   
   [... rest of template ...]
   ```

4. **Claude Code receives instruction**:
   ```json
   {
     "message": "Documentation template created at .cogent/src/auth/login.py.md. Please read the source file at src/auth/login.py and the documentation template, then fill in all the placeholder sections with accurate, detailed information about the code."
   }
   ```

5. **Claude Code fills in the documentation**:
   - Reads the source file
   - Analyzes the code structure
   - Fills in each section with detailed information
   - Saves the completed documentation

### Result
You now have comprehensive documentation for `login.py` that includes:
- File overview and intent
- Project integration details
- Key components (classes, functions, variables)
- Dependencies (internal and external)
- Usage examples
- API documentation
- Testing, error handling, performance, and security considerations

## Documentation Structure

Documentation files are organized to mirror your source code structure:
```
project/
├── src/
│   ├── auth/
│   │   └── login.py
│   └── utils/
│       └── helpers.py
└── .cogent/
    └── src/
        ├── auth/
        │   └── login.py.md
        └── utils/
            └── helpers.py.md
```

## Updating Existing Documentation

When you edit a file that already has documentation:
1. The system detects existing documentation
2. Updates the "Last Updated" timestamp
3. Instructs Claude Code to update the documentation with recent changes
4. Preserves existing content while adding new information

## Best Practices

1. **Review Generated Documentation**: While Claude Code generates comprehensive documentation, review it for accuracy
2. **Keep Documentation Updated**: The system tracks changes, but ensure major refactors are reflected
3. **Add Project-Specific Sections**: Customize the template in the bash script for your needs
4. **Version Control**: Commit documentation files to track documentation evolution
5. **Team Collaboration**: Share documentation with team members for better code understanding

## Troubleshooting

### Hook Not Triggering
- Ensure Claude Code settings are loaded: Restart Claude Code
- Check file path filters in `.claude/settings.json`
- Verify script permissions: `chmod +x .cogent/create-documentation.sh`

### Documentation Not Created
- Check script output in Claude Code's response
- Verify directory permissions
- Run manual test to see error messages

### Incorrect Documentation Path
- Ensure absolute paths are used consistently
- Check the `get_relative_path` function in the script

## Advanced Customization

### Adding Custom Sections
Edit the template in `.cogent/create-documentation.sh`:
```bash
## Custom Section
<!-- PLACEHOLDER: Your custom content here -->
[AI: Please fill in custom section]
```

### Language-Specific Templates
Modify the script to use different templates based on file extension:
```bash
case "$extension" in
    py) use_python_template ;;
    js) use_javascript_template ;;
    *) use_default_template ;;
esac
```

## Conclusion

The Cogent Documentation System ensures your codebase remains well-documented with minimal effort. By leveraging Claude Code's capabilities, it provides intelligent, context-aware documentation that evolves with your code.

For issues or improvements, modify the components as needed or adjust the configuration to match your project's requirements.