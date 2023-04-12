---
hide:
  - navigation
---

# Overview

An Architectural Decision (AD) is a justified design choice that addresses a functional or non-functional requirement that is architecturally significant. An Architecturally Significant Requirement (ASR) is a requirement that has a measurable effect on a system’s architecture and quality.

The purpose of this application is to capture an Architectural Decision and its rationale; display the collection of ADRs created and maintained as a decision log.

![App Icon](./images/icon-adr.png){: style="width: 50%;"}

## Documentation

The documentation contains a

- [User Guide](user/app_overview/) Overview,  Using the App, and Getting Started.
- [Administrator Guide](admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](dev/contributing/) - Extending the App, Code Reference, Contribution Guide.

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://github.com/psmware-ltd/arch-decision-rec-app/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!
