from django.contrib import admin
from .models import ResearchPaper, Department  # এখানে Department যোগ করুন

# আপনার আগের কোডগুলো থাকবে...
admin.site.site_header = "RMS Admin Portal"
admin.site.site_title = "RMS Admin"
admin.site.index_title = "Research Management System"

@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# --- এই লাইনটা নতুন যোগ করুন ---
admin.site.register(Department)