from django.contrib import admin

from producers.models import Producer

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name', 'document_type', 'document', 'is_active', 'updated_at')
    list_filter = ('is_active', 'document_type')
    search_fields = ('id', 'name', 'document')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')