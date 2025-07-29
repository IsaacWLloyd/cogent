# Documentation: `install.sh`

## File Overview
<!-- PLACEHOLDER: Provide a comprehensive overview of what this Code file does, its main purpose, and its role in the system. Be specific about the functionality it provides. -->

This Bash script serves as the primary installer for the Cogent AutoDoc system, which provides automated documentation generation for Claude Code projects. The installer handles the complete setup process including dependency checking, project type detection, directory structure creation, and Claude Code hook configuration.

The script creates a `.cogent` directory structure, downloads the documentation generation hook script, configures Claude Code settings to trigger automatic documentation, and provides an interactive setup experience with colored output and comprehensive error handling. It supports multiple project types including React, TypeScript, Python, Rust, Go, and Java projects.

## Intent
<!-- PLACEHOLDER: Explain WHY this file exists, what problem it solves, and what requirements or user needs it addresses. Include the business logic or technical rationale. -->

This installer was created to solve the complex setup process required for integrating automated documentation generation into Claude Code workflows. It eliminates the manual steps of creating directory structures, configuring hooks, downloading scripts, and setting up project-specific configurations that would otherwise require users to understand the internal workings of the Cogent AutoDoc system.

The script addresses the user experience challenge of making advanced documentation automation accessible to developers regardless of their familiarity with bash scripting or Claude Code hook systems.

## Project Integration
<!-- PLACEHOLDER: Describe how this file connects to and interacts with the overall project architecture. Include:
- What other components depend on this file
- What this file depends on
- How it fits into the larger system design
- Data flow and communication patterns -->

This installer serves as the entry point for the entire Cogent AutoDoc ecosystem. It downloads and configures the core documentation generation script (`create-documentation.sh`) and integrates with Claude Code's hook system through the `.claude/settings.json` configuration file.

The script interacts with the project's existing structure by detecting project types through files like `package.json`, `requirements.txt`, `Cargo.toml`, etc. It creates the `.cogent` directory structure that mirrors the project's file hierarchy for storing generated documentation. The installer also modifies or creates `.gitignore` entries and can backup existing Claude Code configurations.

## Recent Changes
**Last Updated:** 2025-07-29 20:45:14 UTC
**Modified File:** `/home/isaac/Workspaces/cogent-autodoc/install.sh`

<!-- PLACEHOLDER: Document what was changed in the most recent edit and why -->

This file was newly created as a comprehensive installer script for the Cogent AutoDoc system. The implementation includes a full-featured installation workflow with dependency checking, project type detection, interactive configuration options, and robust error handling. The script includes colored output formatting, command-line argument processing (--help, --version, --uninstall), and provisions for future template customization features.

## Key Components

### Classes
<!-- PLACEHOLDER: List and describe all classes defined in this file -->

No classes are defined in this Bash script. The script follows a procedural programming approach with standalone functions.

### Functions
<!-- PLACEHOLDER: List and describe all standalone functions -->

**Utility Functions:**
- `log_info(message)` - Prints informational messages with blue icon
- `log_success(message)` - Prints success messages with green checkmark
- `log_warning(message)` - Prints warning messages with yellow warning icon
- `log_error(message)` - Prints error messages with red X icon
- `log_step(message)` - Prints step indicators with purple arrow
- `print_banner()` - Displays ASCII art banner and project title

**Core Functions:**
- `check_dependencies()` - Verifies required tools (curl/wget, grep, sed, mkdir, chmod)
- `detect_project_type()` - Returns project type string based on detected files
- `download_file(url, output)` - Downloads file using curl or wget
- `setup_cogent_directory()` - Creates .cogent structure and downloads scripts
- `setup_claude_settings()` - Configures Claude Code hooks in settings.json
- `create_gitignore_entries()` - Adds .cogent entries to .gitignore
- `show_usage_instructions()` - Displays post-installation usage information
- `interactive_setup(project_type)` - Runs interactive configuration wizard
- `main()` - Primary installation workflow orchestrator

### Important Variables/Constants
<!-- PLACEHOLDER: List and describe important variables, constants, or configuration values -->

**Color Constants:**
- `RED`, `GREEN`, `YELLOW`, `BLUE`, `PURPLE`, `CYAN` - ANSI color codes for output formatting
- `NC` - No Color reset code

**Configuration Variables:**
- `REPO_URL` - Base URL for GitHub repository raw files
- `SCRIPT_URL` - Direct URL to the documentation generation script
- `INSTALL_DIR` - Target directory name ('.cogent')
- `CLAUDE_SETTINGS_DIR` - Claude Code settings directory ('.claude')
- `CLAUDE_SETTINGS_FILE` - Path to Claude Code settings file

**Runtime Variables:**
- `project_type` - Detected project type (react, python, rust, etc.)
- `response` - User input for interactive prompts
- `doc_level` - User-selected documentation verbosity level
- `custom_exclusions` - User-defined file exclusion patterns

## Dependencies

### Internal Dependencies
<!-- PLACEHOLDER: List all internal project files/modules this file imports or depends on -->

This installer has no internal dependencies - it's designed to be a standalone script. However, it downloads and configures:

- `create-documentation.sh` - The core documentation generation hook script that gets installed into `.cogent/`
- `settings.json` template - Claude Code hook configuration that gets merged with existing settings

### External Dependencies
<!-- PLACEHOLDER: List all external libraries, packages, or frameworks used -->

**Required System Tools:**
- `bash` - Shell interpreter (version 4.0+ for associative arrays)
- `curl` OR `wget` - For downloading files from GitHub
- `grep` - Text pattern matching
- `sed` - Stream editor for text manipulation
- `mkdir` - Directory creation
- `chmod` - File permission modification
- `date` - Timestamp generation

**Runtime Environment:**
- POSIX-compliant Unix/Linux system
- Internet connection for downloading scripts
- Write permissions in the target project directory

## Usage Examples

### Basic Usage
```text
<!-- PLACEHOLDER: Provide a simple example of how to use the main functionality -->

# Basic installation
curl -fsSL https://raw.githubusercontent.com/yourusername/cogent-autodoc/main/install.sh | bash

# Or download and run
wget https://raw.githubusercontent.com/yourusername/cogent-autodoc/main/install.sh
chmod +x install.sh
./install.sh
```

### Advanced Usage
```text
<!-- PLACEHOLDER: Provide more complex usage examples showing different features -->

# Show help information
./install.sh --help

# Check version
./install.sh --version

# Run with interactive setup
./install.sh
# Choose 'y' when prompted for interactive setup
# Select documentation level (1-3)
# Add custom file exclusions
# Customize templates for project type

# Uninstall the system
./install.sh --uninstall

# Manual installation with verification
wget https://raw.githubusercontent.com/yourusername/cogent-autodoc/main/install.sh
# Review the script contents before running
less install.sh
# Run the installer
bash install.sh
```

## API Documentation
<!-- PLACEHOLDER: For files that expose public APIs, document all public methods/functions -->

**Command Line Interface:**

```bash
install.sh [OPTIONS]
```

**Options:**
- `--help, -h` - Display help message and exit
- `--version, -v` - Show version information and exit
- `--uninstall` - Remove Cogent AutoDoc from current project
- `(no args)` - Run full installation process

**Exit Codes:**
- `0` - Success or help/version display
- `1` - Error (missing dependencies, download failure, etc.)

**Interactive Prompts:**
- Documentation level selection (1-3)
- Custom exclusion patterns (comma-separated)
- Template customization (y/N)
- Settings backup confirmation (y/N)
- Continue in non-project directory (y/N)

## Testing
<!-- PLACEHOLDER: Describe how this file is tested, what test files cover it, and any special testing considerations -->

This installer script should be tested across multiple environments:

**Unit Testing:**
- Test individual functions with various inputs
- Mock external dependencies (curl, wget)
- Verify file creation and permission setting
- Test project type detection with different file combinations

**Integration Testing:**
- Test complete installation workflow on clean systems
- Verify hook integration with actual Claude Code
- Test backup and restore functionality
- Validate uninstall process

**Environment Testing:**
- Different Unix/Linux distributions
- Various project types (React, Python, Rust, etc.)
- Systems with/without curl or wget
- Existing vs. new Claude Code configurations

**Manual Testing:**
- Interactive setup workflow
- Error handling with invalid inputs
- Network failure scenarios

## Error Handling
<!-- PLACEHOLDER: Document how errors are handled, what exceptions might be thrown, and recovery strategies -->

The script implements comprehensive error handling:

**Bash Error Handling:**
- `set -euo pipefail` - Strict error mode (exit on errors, undefined variables, pipe failures)
- Function-level error checking with conditional logic
- Graceful degradation when optional features fail

**Dependency Validation:**
- Checks for required tools before proceeding
- Provides clear error messages for missing dependencies
- Offers alternative approaches (curl vs wget)

**User Input Validation:**
- Default values for interactive prompts
- Input sanitization and bounds checking
- Confirmation prompts for destructive operations

**Network Error Handling:**
- Download failure detection and reporting
- Fallback mechanisms for file retrieval
- Clear error messages for connectivity issues

**File System Errors:**
- Permission checking before file operations
- Backup creation before modifying existing files
- Directory creation with error checking

## Performance Considerations
<!-- PLACEHOLDER: Note any performance implications, optimizations, or concerns -->

The installer is optimized for quick execution:

**Network Optimization:**
- Minimal file downloads (only the hook script)
- Uses efficient download tools (curl -fsSL, wget -q)
- Single HTTP request for script download

**File System Efficiency:**
- Creates directory structures in single operations
- Avoids unnecessary file reads/writes
- Uses in-place sed operations for text modifications

**Process Optimization:**
- Minimal external process spawning
- Efficient text processing with built-in bash features
- Early exit on errors to avoid unnecessary work

**Memory Usage:**
- Streams large text outputs rather than storing in variables
- Uses local variables to limit scope
- Minimal variable retention between functions

**User Experience:**
- Immediate feedback with progress indicators
- Colored output for quick visual parsing
- Minimal required user interaction

## Security Considerations
<!-- PLACEHOLDER: Document any security implications, data validation, or authentication/authorization logic -->

Several security measures are implemented:

**Download Security:**
- Uses HTTPS URLs for all downloads
- Downloads from specific GitHub raw URLs (not redirects)
- Sets appropriate file permissions (755 for executable scripts)

**Input Validation:**
- Sanitizes user input from interactive prompts
- Uses quoted variables to prevent injection
- Validates file paths before operations

**File System Security:**
- Creates backups before modifying existing files
- Uses relative paths within project directory
- Avoids writing to system directories

**Execution Security:**
- Uses `set -euo pipefail` to prevent silent failures
- Avoids eval or dynamic code execution
- Explicit error handling for all external commands

**Privilege Management:**
- Runs with user privileges (no sudo required)
- Only modifies files within the project directory
- Clearly indicates what files will be modified

**Best Practices:**
- Users are encouraged to review the script before execution
- Provides uninstall option for easy removal
- Transparent about all operations performed

## Notes
<!-- PLACEHOLDER: Any additional important information, TODOs, known issues, or future improvements -->

**Important Notes:**
- This installer requires an active internet connection to download the hook script
- The script modifies `.claude/settings.json` and may backup existing configurations
- Generated documentation files are stored in `.cogent/` and should be committed to version control
- The installer is designed to be idempotent - running it multiple times is safe

**Warnings:**
- Always review the script contents before execution, especially when using `curl | bash`
- Existing Claude Code hook configurations may be modified
- The uninstall option removes the entire `.cogent` directory

**Future Enhancements:**
- Template customization system for different project types
- Configuration file validation and repair
- Integration with package managers (npm, pip, cargo)
- Automated testing and validation of installed hooks

**Troubleshooting:**
- If installation fails, check internet connectivity and file permissions
- For hook issues, verify `.claude/settings.json` syntax
- Documentation generation requires Claude Code to be properly configured
- Check the `.cogent/create-documentation.sh` script has execute permissions

---
*This documentation was automatically generated by the Cogent Documentation System*
