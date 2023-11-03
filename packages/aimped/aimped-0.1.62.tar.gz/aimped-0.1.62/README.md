![aimped](https://dev.aimped.ai/static/media/AimpedBirdLogo.0b3c7cc26d31afe7bd73db496acb01d1.svg)
# **aimped**
[![PyPI version](https://badge.fury.io/py/aimped.svg)](https://badge.fury.io/py/aimped)
[![Downloads](https://pepy.tech/badge/aimped)](https://pepy.tech/project/aimped)


**Aimped is a unique python library that provides classes and functions for only exclusively business-tailored AI-based models.**   
In this version, we provide the following features:
Sound processing tools and functions, NLP tools and functions, and a pipeline class for NLP tasks. 

# Installation  
```python
pip install aimped
```

# Usage  
```python  
import aimped
print(aimped.__version__)
```

### Example 1

```python  
from aimped import nlp

result = nlp.sentence_tokenizer("Hi, welcome to aimped. Explore ai models.",language="english")
print(result)
# ['Hi, welcome to aimped.', 'Explore ai models.']
```

### Example 2

```python  
from aimped.utils import LimitChecker

checker = LimitChecker()
checker.check_video("video.mp4", input_limit=120)
# Output: True

```

### Example 3
```python  
from aimped.nlp.pipeline import Pipeline

pipe = Pipeline(model=model, tokenizer=tokenizer, device='cpu')
result = pipe.ner_result(
                        text=text,
                        sents_tokens_list=sents_tokens_list,
                        sentences=sentences)
print(result)
```

### Example 4
```python  
from aimped.nlp.pipeline import Pipeline
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from aimped.nlp import translation

checkpoint = "/path/to/model_checkpoint"
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
device = 0
aimped = Pipeline(model=model, tokenizer=tokenizer, device=device)
aimped.translation_result(["text1_de","text2_de",...],source_language="german", output_language="english")
```
