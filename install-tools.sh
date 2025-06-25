#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' 

echo -e "${BLUE}🚀 Installing uv and task on macOS...${NC}\n"

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        return 1
    fi
}

# Install uv if not already installed
if command_exists uv; then
    echo -e "${YELLOW}⚠️  uv is already installed${NC}"
    uv --version
else
    echo -e "${BLUE}📦 Installing uv...${NC}"
    # Install uv using Homebrew (recommended for macOS)
    if command_exists brew; then
        brew install uv
        print_status $? "uv installation via Homebrew"
    else
        echo -e "${YELLOW}⚠️  Homebrew not found. Installing uv manually...${NC}"
        # Manual installation as fallback
        curl -LsSf https://astral.sh/uv/install.sh | sh
        print_status $? "uv installation via script"
    fi
    
    # Source the shell configuration to make uv available (only needed for manual install)
    if ! command_exists brew; then
        if [[ "$SHELL" == *"zsh"* ]]; then
            source ~/.zshrc 2>/dev/null || true
        elif [[ "$SHELL" == *"bash"* ]]; then
            source ~/.bashrc 2>/dev/null || true
        fi
    fi
fi

# Install task if not already installed
if command_exists task; then
    echo -e "${YELLOW}⚠️  task is already installed${NC}"
    task --version
else
    echo -e "${BLUE}📦 Installing task...${NC}"
    # Install task using Homebrew (recommended for macOS)
    if command_exists brew; then
        brew install go-task
        print_status $? "task installation via Homebrew"
    else
        echo -e "${YELLOW}⚠️  Homebrew not found. Installing task manually...${NC}"
        # Manual installation as fallback
        curl -sL https://taskfile.dev/install.sh | sh
        print_status $? "task installation via script"
    fi
fi

echo -e "\n${BLUE}🔍 Verifying installations...${NC}\n"

# Verify uv installation
if command_exists uv; then
    echo -e "${GREEN}✅ uv is installed and working:${NC}"
    uv --version
else
    echo -e "${RED}❌ uv installation failed${NC}"
    exit 1
fi

# Verify task installation
if command_exists task; then
    echo -e "${GREEN}✅ task is installed and working:${NC}"
    task --version
else
    echo -e "${RED}❌ task installation failed${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 Installation complete! Both uv and task are ready to use.${NC}"

# Show available tasks if Taskfile.yml exists
if [ -f "Taskfile.yml" ]; then
    echo -e "\n${BLUE}📋 Available tasks in this project:${NC}"
    task --list
fi

echo -e "\n${BLUE}💡 Next steps:${NC}"
echo -e "  • Run 'task --list' to see available tasks"
echo -e "  • Run 'task <task-name>' to execute a specific task/assignment" 