from PIL import Image


class Model:
    def predict(cls, prompt: str, negative_prompt, width, height, guidance_scale, num_inference_steps):
        print(prompt)
        img = Image.open(r".\\img.png")
        img2 = Image.open(r".\\deploy.png")
        return [img2, img]