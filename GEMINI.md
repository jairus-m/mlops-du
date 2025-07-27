# Python Development Workflow Instructions

## Standard Workflow:

### 1. Problem Analysis & Planning
- First think through the problem, read the codebase for relevant files, and write a plan.
- When in plan mode, always write the plan into `ai_docs/spec_v<version-num>.md`
- Each time you iterate on a new plan, create a new spec markdown file with the incremented number.
- For example: if we have a plan written in `spec_v1.md` and we update it with a new implementation, instead of modifying the existing file, create a new file `spec_v2.md` and write into that new document.

### 2. Plan Structure
- The plan should have a list of tasks that you can check off as you complete them
- Include specific file paths, function names, and implementation details
- Consider dependencies between tasks and their order of execution
- Include testing strategies and validation steps

### 3. Plan Verification
- Before you begin working, check in with me and I will verify the plan
- Once verified, write the implementation plan/tasks into the `ai_docs/spec_v<version-num>.md` spec file
- Confirm with me if it's okay to execute the implementation plan

### 4. Implementation Execution
- Once confirmed, begin working on the tasks, marking them as complete as you go
- Follow Python best practices:
  - Use type hints where appropriate
  - Follow PEP 8 style guidelines
  - Write docstrings for functions and classes
  - Implement proper error handling
  - Add logging where necessary
- For every change in Python files, ensure:
  - Update corresponding `pyproject.toml` if adding new dependencies
  - Add/update docstrings and comments
  - Update any relevant configuration files
  - Run `ruff format`
- Create proper documentation in appropriate `.md` files if necessary (or missing)
- Use existing documentation when appropriate rather than creating duplicates

### 5. Progress Communication
- Please every step of the way just give me a high level explanation of what changes you made
- Explain the reasoning behind design decisions
- Highlight any potential issues or considerations

### 6. Simplicity Principle
- Make every task and code change you do as simple as possible
- We want to avoid making any massive or complex changes
- Every change should impact as little code as possible
- Everything is about simplicity and maintainability
- Prefer composition over inheritance
- Use clear, descriptive variable and function names

### 7. Review & Documentation
- Finally, add a review section to the `spec_v<version-num>.md` file with:
  - Summary of the changes you made
  - Any relevant information about the implementation
  - Testing results and validation
  - Performance considerations if applicable
  - Future improvements or considerations

## Python-Specific Guidelines:

### Code Organization
- Follow the project structure established in the workspace
- Use appropriate Python packages and modules
- Maintain separation of concerns
- Keep functions and classes focused and single-purpose


### Dependency Management
- Use `uv` for dependency management (as established in this workspace)
- Add dependencies to `pyproject.toml` when needed
- Keep dependencies minimal and up-to-date
- Document why specific dependencies are needed

### Error Handling
- Implement proper exception handling
- Use custom exceptions when appropriate
- Provide meaningful error messages
- Log errors appropriately

### Performance Considerations
- Profile code when performance is critical
- Use appropriate data structures
- Consider memory usage for large datasets
- Optimize bottlenecks identified through profiling

## After Implementation:
Please explain the functionality and code you just built out in detail. Walk me through what you changed and how it works. Act like you're a senior engineer teaching me code.

---

## Project-Specific Notes:

### MLOps Focus
This workspace contains MLOps assignments with:
- Machine learning pipelines
- FastAPI applications
- Streamlit applications
- Docker containerization
- Model serving and deployment

### Key Technologies
- **uv**: Dependency management and workspace handling
- **task**: Task runner for executing assignments
- **Docker**: Containerization for deployment
- **FastAPI**: API development
- **Streamlit**: Web application development
- **Machine Learning**: Model training and serving

### Assignment Structure
Each assignment is in `assignments/<project-name>/` with its own:
- `pyproject.toml` for dependencies
- `src/` directory for source code
- `README.md` for project-specific documentation
- `Dockerfile` for containerization
