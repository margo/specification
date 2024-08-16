FROM mcr.microsoft.com/vscode/devcontainers/python:3.10-bookworm

RUN pip install mkdocs \
    && pip install mkdocs-markdownextradata-plugin \
    && pip install mkdocs-material

EXPOSE 8000