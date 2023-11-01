# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarms',
 'swarms.agents',
 'swarms.artifacts',
 'swarms.chunkers',
 'swarms.embeddings',
 'swarms.loaders',
 'swarms.memory',
 'swarms.models',
 'swarms.prompts',
 'swarms.schemas',
 'swarms.structs',
 'swarms.swarms',
 'swarms.tools',
 'swarms.utils',
 'swarms.workers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow',
 'agent-protocol',
 'asyncio',
 'attrs',
 'beautifulsoup4',
 'black',
 'chromadb',
 'dalle3',
 'datasets',
 'diffusers',
 'duckduckgo-search',
 'einops',
 'faiss-cpu',
 'ggl',
 'google-generativeai',
 'griptape',
 'httpx',
 'huggingface-hub',
 'langchain',
 'langchain-experimental',
 'nest_asyncio',
 'open-interpreter',
 'open_clip_torch',
 'openai',
 'pegasusx',
 'playwright',
 'pydantic',
 'redis',
 'rich',
 'sentencepiece',
 'soundfile',
 'tabulate',
 'tenacity',
 'termcolor',
 'torch',
 'torchvision',
 'transformers',
 'wget']

setup_kwargs = {
    'name': 'swarms',
    'version': '1.9.3',
    'description': 'Swarms - Pytorch',
    'long_description': '![Swarming banner icon](images/swarmslogobanner.png)\n\n<div align="center">\n\nSwarms is a modular framework that enables reliable and useful multi-agent collaboration at scale to automate real-world tasks.\n\n\n[![GitHub issues](https://img.shields.io/github/issues/kyegomez/swarms)](https://github.com/kyegomez/swarms/issues) [![GitHub forks](https://img.shields.io/github/forks/kyegomez/swarms)](https://github.com/kyegomez/swarms/network) [![GitHub stars](https://img.shields.io/github/stars/kyegomez/swarms)](https://github.com/kyegomez/swarms/stargazers) [![GitHub license](https://img.shields.io/github/license/kyegomez/swarms)](https://github.com/kyegomez/swarms/blob/main/LICENSE)[![GitHub star chart](https://img.shields.io/github/stars/kyegomez/swarms?style=social)](https://star-history.com/#kyegomez/swarms)[![Dependency Status](https://img.shields.io/librariesio/github/kyegomez/swarms)](https://libraries.io/github/kyegomez/swarms) [![Downloads](https://static.pepy.tech/badge/swarms/month)](https://pepy.tech/project/swarms)\n\n\n### Share on Social Media\n\n[![Join the Agora discord](https://img.shields.io/discord/1110910277110743103?label=Discord&logo=discord&logoColor=white&style=plastic&color=d7b023)![Share on Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Share%20%40kyegomez/swarms)](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20AI%20project:%20&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms) [![Share on Facebook](https://img.shields.io/badge/Share-%20facebook-blue)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms) [![Share on LinkedIn](https://img.shields.io/badge/Share-%20linkedin-blue)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&title=&summary=&source=)\n\n[![Share on Reddit](https://img.shields.io/badge/-Share%20on%20Reddit-orange)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&title=Swarms%20-%20the%20future%20of%20AI) [![Share on Hacker News](https://img.shields.io/badge/-Share%20on%20Hacker%20News-orange)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&t=Swarms%20-%20the%20future%20of%20AI) [![Share on Pinterest](https://img.shields.io/badge/-Share%20on%20Pinterest-red)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&media=https%3A%2F%2Fexample.com%2Fimage.jpg&description=Swarms%20-%20the%20future%20of%20AI) [![Share on WhatsApp](https://img.shields.io/badge/-Share%20on%20WhatsApp-green)](https://api.whatsapp.com/send?text=Check%20out%20Swarms%20-%20the%20future%20of%20AI%20%23swarms%20%23AI%0A%0Ahttps%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms)\n\n</div>\n\n[![Swarm Fest](images/swarmfest.png)](https://github.com/users/kyegomez/projects/1)\n\n## Vision\nAt Swarms, we\'re transforming the landscape of AI from siloed AI agents to a unified \'swarm\' of intelligence. Through relentless iteration and the power of collective insight from our 1500+ Agora researchers, we\'re developing a groundbreaking framework for AI collaboration. Our mission is to catalyze a paradigm shift, advancing Humanity with the power of unified autonomous AI agent swarms.\n\n-----\n\n## 🤝 Schedule a 1-on-1 Session\n\nBook a [1-on-1 Session with Kye](https://calendly.com/swarm-corp/30min), the Creator, to discuss any issues, provide feedback, or explore how we can improve Swarms for you.\n\n\n----------\n\n## Installation\n`pip3 install --upgrade swarms`\n\n---\n\n## Usage\nWe have a small gallery of examples to run here, [for more check out the docs to build your own agent and or swarms!](https://docs.apac.ai)\n\n### `Flow` Example\n- The `Flow` is a superior iteratioin of the `LLMChain` from Langchain, our intent with `Flow` is to create the most reliable loop structure that gives the agents their "autonomy" through 3 main methods of interaction, one through user specified loops, then dynamic where the agent parses a <DONE> token, and or an interactive human input verison, or a mix of all 3. \n```python\n\nfrom swarms.models import OpenAIChat\nfrom swarms.structs import Flow\n\napi_key = ""\n\n\n# Initialize the language model,\n# This model can be swapped out with Anthropic, ETC, Huggingface Models like Mistral, ETC\nllm = OpenAIChat(\n    openai_api_key=api_key,\n    temperature=0.5,\n)\n\n# Initialize the flow\nflow = Flow(\n    llm=llm,\n    max_loops=5,\n)\n\nout = flow.run("Generate a 10,000 word blog, say Stop when done")\nprint(out)\n\n\n```\n\n\n## `GodMode`\n- A powerful tool for concurrent execution of tasks using multiple Language Model (LLM) instances.\n\n```python\nfrom swarms.swarms import GodMode\nfrom swarms.models import OpenAIChat\n\napi_key = ""\n\nllm = OpenAIChat(\n    openai_api_key=api_key\n)\n\n\nllms = [\n    llm,\n    llm,\n    llm\n]\n\ngod_mode = GodMode(llms)\n\ntask = \'Generate a 10,000 word blog on health and wellness.\'\n\nout = god_mode.run(task)\ngod_mode.print_responses(task)\n```\n\n------\n\n### `OmniModalAgent`\n- OmniModal Agent is an LLM that access to 10+ multi-modal encoders and diffusers! It can generate images, videos, speech, music and so much more, get started with:\n\n```python\nfrom swarms.models import OpenAIChat\nfrom swarms.agents import OmniModalAgent\n\napi_key = "SK-"\n\nllm = OpenAIChat(model_name="gpt-4", openai_api_key=api_key)\n\nagent = OmniModalAgent(llm)\n\nagent.run("Create a video of a swarm of fish")\n\n```\n\n---\n\n## Documentation\n\n- For documentation, go here, [swarms.apac.ai](https://swarms.apac.ai)\n\n\n## Contribute\n\nWe\'re always looking for contributors to help us improve and expand this project. If you\'re interested, please check out our [Contributing Guidelines](CONTRIBUTING.md).\n\n# License\n\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
