import os
import django
import sys
from django.conf import settings
from django.apps import apps

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def generate_mermaid_diagram():
    print("Graph TD;")
    
    # Iterate over our specific apps
    target_apps = ['academic', 'recommendations', 'scraping', 'users']
    
    models_to_graph = []
    
    for app_label in target_apps:
        try:
            app_config = apps.get_app_config(app_label)
            for model in app_config.get_models():
                models_to_graph.append(model)
        except LookupError:
            continue

    # Define Classes
    for model in models_to_graph:
        model_name = model.__name__
        fields = []
        for field in model._meta.fields:
            field_type = field.get_internal_type()
            fields.append(f"{field.name}: {field_type}")
        
        fields_str = "<br>".join(fields)
        print(f"    {model_name}[\"{model_name}<br>--<br>{fields_str}\"]")

    # Define Relationships
    for model in models_to_graph:
        model_name = model.__name__
        for field in model._meta.fields:
            if field.is_relation and field.related_model in models_to_graph:
                related_model_name = field.related_model.__name__
                # Determine cardinality (simplified)
                if field.many_to_one:
                    print(f"    {model_name} -->|FK| {related_model_name}")
                elif field.one_to_one:
                    print(f"    {model_name} --|1:1| {related_model_name}")
                elif field.many_to_many:
                    print(f"    {model_name} <..>|M:M| {related_model_name}")

if __name__ == "__main__":
    generate_mermaid_diagram()
