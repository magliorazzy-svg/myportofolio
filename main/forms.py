from django.core.exceptions import ValidationError
from django.forms import ModelForm, NumberInput, TextInput, Textarea, URLInput
from django.utils.html import strip_tags
from main.models import Project, Achievement


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "tech_stack", "project_url", "project_image_url"]
        widgets = {
            "title": TextInput(attrs={"placeholder": "Portfolio Website", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Tell us about your project", "rows": 3}),
            "tech_stack": TextInput(attrs={"placeholder": "Django, Python, HTML, CSS"}),
            "project_url": URLInput(attrs={"placeholder": "https://github.com/..."}),
            "project_image_url": URLInput(attrs={"placeholder": "https://drive.google.com/thumbnail?id=..."}),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Project name can't contain only HTML tags.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = ["title", "event", "category", "description", "year",]
        widgets = {
            "title": TextInput(attrs={"placeholder": "Gold Medalist of Math Competition", "maxlength": 255}),
            "event": TextInput(attrs={"placeholder": "ONSB 2025", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Describe what you achieved", "rows": 3}),
            "year": NumberInput(attrs={"placeholder": "2025", "min": 1900, "max": 2100}),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Title can't contain only HTML tags.")
        return title

    def clean_event(self):
        return strip_tags(self.cleaned_data["event"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

