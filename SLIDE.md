---
marp: true
theme: 
paginate: true
---
<style>
section {
  background: #ECDCC3;
}
</style>

# Leveraging Python and LLMs for Innovative 3D Printing Projects

**PyCon APAC 2024**

---

## Introduction
**Ibrahim Hanif**
![width:200px](https://media.licdn.com/dms/image/v2/D5603AQFmdkKLcY1c6w/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1718691543845?e=1735171200&v=beta&t=0A4zgBSQHg5ymIHOmu3Iv1AL15gz4dcZ-FRs47b4ydc)
Email: ibrahim.hanif4529@gmail.com
Github: https://github.com/ibrahim4529
LinkedIn: https://www.linkedin.com/in/ibrahim-hanif4529
___

## About the Title
**"Leveraging Python and LLMs for Innovative 3D Printing Projects"**
- Sounds a bit strange?
- Clickbait?
___

## Actually... generated by an AI!
![height:550px](presentation/assets/Screenshot%202024-10-26%20at%2022.15.53.png)
___

## What do I actually want to share?
What I really want to share today is my journey of learning and experimenting with Python and Large Language Models for 3D printing projects, This journey culminated in creating a simple application to generate 3D models.

Project Repository: https://github.com/ibrahim4529/llm3dprint
___

## Why LLMs for 3D Printing?

- Addressing the "skill issue" in 3D modeling
- LLMs open up new possibilities in design, especially for those of us who aren't experts in 3D modeling.

---

## How To solve that?
1. Using Existing text-to-3D model llms
   - Example: OpenAI's Shape-E
2. Generating OpenSCAD Code
   - LLMs writing 3D modeling scripts
---

## What role does Python play in my project?
- Help me to interact with the llm model.
- Help me to generate the 3d model.
- Help me visualize the 3d model.


https://www.python.org/
https://pyvista.org/
https://openrouter.ai/
___

## Approach 1: Using Existing Models
- Focus of exploration: OpenAI's Shape-E
- Purpose: Text-to-3D model generation
- How it works: 
  - Input: Text description of the 3D model
  - Output: 3D model
- Limitations: 
  - Still in early stages.
  - Lack of control over the 3D model like size, shape, etc.

https://github.com/openai/shap-e
___

## Approach 2: Generating OpenSCAD Code
When we hear about LLMs, the first thing that often comes to mind for us as software engineers is their ability to help us generate code for our applications. This is where the idea struck me: what if we use LLMs to generate OpenSCAD code? For those unfamiliar, OpenSCAD is a programming language for creating 3D solid models. It's like coding, but for 3D objects.

```openscad
cylinder(h = 10, r1 = 5, r2 = 3);
translate([0, 0, 10])
sphere(r = 3);
```
https://openscad.org/
___

## Demo 

- Demo: Generating a 3D model using OpenAI's Shape-E
- Challenges: 
  - Model still in erly stages
  - Need to know how to use this model (utilize openrouter api)
  - Lack of control over the 3d model like size, shape, etc.
- Demo: Generating OpenSCAD code using LLMs
- Challenges:
  - Generate complex models

---
## Conclusion And Feasibility
- Still in early stages
- Requires a lot of experimentation and learning
- Can using RAG for better results (future work)
- Can try fine-tuning for better results (future work)

---

## Thank You!
Any questions?