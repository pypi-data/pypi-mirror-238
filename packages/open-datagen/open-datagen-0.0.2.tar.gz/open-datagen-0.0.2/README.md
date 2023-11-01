# ⬜️ Open-Datagen ⬜️

Elevate your model training with **Open-Datagen** - a steerable data generation system.

## 🌱 Features

- Generate data in any format
- Craft custom templates with Pydantic models
- Utilize predefined templates

## 📥 Installation

```bash
pip install --upgrade open-datagen
```

## 🛠 Usage

```python
from data_manager import Template, Variable, generate_data

# Example: Defining a custom template to generate medium-level Python exercises
user_template = Template(
    description="Custom template for Python exercises",
    prompt="Python exercise: '{python_exercise}'",
    completion="Answer using python:\n---\n{python_code}\n---",
    prompt_variation_number=1,
    prompt_variables={
        "python_exercise": Variable(
            name="Python exercice",
            temperature=1,
            max_tokens=126,
            generation_number=5,
            note="The python exercise statement must be medium level."
        
        )
    },
    completion_variables={
        "python_code": Variable(
            name="Python code",
            temperature=0,
            max_tokens=256,
            generation_number=1
        )
    }
)

# Generate your data
data = generate_data(template=user_template, output_path="output.csv")
```

This code will generate 5 medium-level Python exercises

### Predefined Templates:

```python
manager = TemplateManager()
template = manager.get_template(template_name=TemplateName.PRODUCT_REVIEW.value)
generate_data(template=template, output_path="output.csv")
```

## 🚀 Roadmap 

- Enhance completion quality with sources like SERPLY, local files, and vector databases
- Augment and replicate sourced data
- Ensure data anonymity & open-source model support
- Future releases to support multimodal data
  
## 📣 Note 

`open-datagen` uses OpenAI models. Be aware of potential biases. Use `start_with` and `note` to guide outputs.

## 📞 Connect 

Reach us on Twitter: [@thoddnn](https://twitter.com/thoddnn).