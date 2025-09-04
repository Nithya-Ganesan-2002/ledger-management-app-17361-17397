#!/bin/bash
cd /home/kavia/workspace/code-generation/ledger-management-app-17361-17397/BackendServiceContainer
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

