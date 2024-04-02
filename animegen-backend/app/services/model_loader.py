from PIL import Image



import torch
from diffusers import (
    StableDiffusionXLPipeline, 
    EulerAncestralDiscreteScheduler,
    AutoencoderKL
)


class AnimeGen:
    def __init__(self, vae_model_name="madebyollin/sdxl-vae-fp16-fix", pipeline_model_name="cagliostrolab/animagine-xl-3.0", device='cuda'):
        self.vae = AutoencoderKL.from_pretrained(vae_model_name, torch_dtype=torch.float16)
        self.pipe = StableDiffusionXLPipeline.from_pretrained(pipeline_model_name, vae=self.vae, torch_dtype=torch.float16, use_safetensors=True)
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.to(device)

    def generate(self, prompt, negative_prompt="worst quality", width=832, height=1216, guidance_scale=7, num_inference_steps=28):
        image = self.pipe(prompt, negative_prompt=negative_prompt, width=width, height=height, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps).images[0]
        return [image]



if __name__=="__main__":
    anime_gen = AnimeGen()
    prompt = "1girl, arima kana, oshi no ko, solo, upper body, v, smile, looking at viewer, outdoors, night"
    negative_prompt = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"

    image = anime_gen.generate(prompt, negative_prompt=negative_prompt)


    class Model:
        def predict(cls, prompt: str, negative_prompt, width, height, guidance_scale, num_inference_steps):
            print(prompt)
            img = Image.open(r"img.png")
            img2 = Image.open(r"deploy.png")
            return [img2, img]