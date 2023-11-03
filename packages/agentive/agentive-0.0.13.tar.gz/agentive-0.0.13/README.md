# Agentive

## Introduction

Agentive is a Python package designed to provide a flexible framework for creating agents that can interact with Large Language Models (LLMs), Memory, and Tools. The package is built on four abstract base classes, making it both extensible and modular. 

## Features

- **Agent**: Manages the overall functionality and coordinates between other components.
- **LLM (Large Language Model)**: Serves as the core of the package, responsible for text-based processing tasks.
- **Memory**: Manages the storage and retrieval of information as messages.
- **Tools**: Provides utility methods and resources to extend capabilities. These may be either local or hosted services, but must have a consistent method of execution.

Each of these components is interoperable but can also function independently with the LLM at it's core.

## Installation

Install the package using pip:

```bash
pip install agentive
```

## Quickstart

The Quickstart section usually contains simple code examples showing basic usage of Agentive. You can demonstrate how to use Agent with LLM and Memory or how to use LLM with Tools.

## Extending Agentive

The abstract base classes allow you to extend the functionality by implementing your own versions. A code example here would usually show a simple subclass of one of the abstract base classes like LLM.

## Documentation

TODO: Add link to documentation.

## Contributing

TODO: Add link to contributing guidelines once open sources

## License

TODO: Add link to license once open sourced
```