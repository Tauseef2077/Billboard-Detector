from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
from PIL import Image
import torch

MODEL = "Qwen/Qwen2-VL-2B-Instruct"


processor = AutoProcessor.from_pretrained(MODEL)

model = Qwen2VLForConditionalGeneration.from_pretrained(
    MODEL,
    torch_dtype="auto", 
    device_map="cpu"
)
def description(path):
    try:
        image = Image.open(path).convert("RGB")
    except FileNotFoundError:
        return "Error: Image file not found."

    prompt_text = """
    Task: detailed visual inspection of this billboard.
    
    Instructions:
    1. Look for rust, structural bending, cracks, loose panels, or vegetation.
    2. Write a SINGLE paragraph summarizing the condition.
    3. If the billboard is clean, simply state: "The structure appears to be in good condition with no visible defects."
    4. Do NOT use bullet points, lists, or asterisks (*). 
    5. Write in a professional, plain-text tone suitable for a safety report.
    6. Dont add "the text on billboard reads"
    """
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image,
                },
                {"type": "text", "text": prompt_text},
            ],
        }
    ]

    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = processor(
        text=[text],
        images=[image],
        padding=True,
        return_tensors="pt"
    )

    inputs = inputs.to("cpu")

    print("Analyzing image...")
    generated_ids = model.generate(
        **inputs,
        max_new_tokens=150,
        repetition_penalty=1.1
   
    )

    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    final_output = output_text[0].replace("*", "").replace("#", "").strip()
    return final_output
