# Hotstuff Python SDK

[![PyPI version](https://img.shields.io/pypi/v/hotstuff-python-sdk.svg)](https://pypi.org/project/hotstuff-python-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/hotstuff-python-sdk.svg)](https://pypi.org/project/hotstuff-python-sdk/)

> Python SDK for interacting with Hotstuff L1

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Clients](#api-clients)
  - [InfoClient](#infoclient)
  - [ExchangeClient](#exchangeclient)
  - [SubscriptionClient](#subscriptionclient)
- [Transports](#transports)
  - [HttpTransport](#httptransport)
  - [WebSocketTransport](#websockettransport)
- [Advanced Usage](#advanced-usage)
- [Signing](#signing)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Installation

### Using pip

```bash
pip install hotstuff-python-sdk
```

### Using Poetry

```bash
poetry add hotstuff-python-sdk
```

### Install from source

```bash
git clone https://github.com/hotstuff-labs/python-sdk.git
cd python-sdk

# Using Poetry (recommended)
poetry install

# Or using pip
pip install -e .
```
