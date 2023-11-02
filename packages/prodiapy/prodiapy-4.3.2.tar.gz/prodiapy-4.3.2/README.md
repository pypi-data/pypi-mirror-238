# Description
prodiapy is an unofficial lightweight Python package for Prodia Stable Diffusion API

# Installation 
```commandline
pip install -U prodiapy
```

# text2img example

```python
from prodiapy import StableDiffusionXL

pipe = StableDiffusionXL(
    api_key="YOUR_PRODIA_KEY"
)

job = pipe.generate(prompt="cat")
result = pipe.wait_for(job)

print(result['imageUrl'])
```
# Contact
Join our discord to get help with package - https://discord.gg/GyBCkGnbUN