#!/bin/sh
# Returns the GITHUB_PAT secret for git credential prompts.
# Git calls this script with a prompt string as $1:
#   "Username for ..." -> return the username
#   "Password for ..." -> return the token
case "$1" in
  Username*) echo "OKHP3" ;;
  Password*) echo "$GITHUB_PAT" ;;
esac
