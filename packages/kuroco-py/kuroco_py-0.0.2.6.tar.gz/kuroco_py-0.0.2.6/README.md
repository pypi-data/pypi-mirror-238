# kuroco-langchain-sdk

## Overview

kuroco-py is a SDK for Kuroco Headless CMS.

Current version support embedding API.

## Installation

```bash
pip install kuroco-py
```

## Usage

```python
from kuroco_embedding import KurocoEmbedding

k_emb = KurocoEmbedding(
        content=("test_endpoint",),
        kuroco_handler="kuroco.json",
    )

k_emb.similarity_search(
    query="What is Kuroco ?",
    limit=10,
    )
```
