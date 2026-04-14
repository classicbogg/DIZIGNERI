from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone
from openpyxl import Workbook

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "email", "phone")
    change_list_template = "admin/core/record/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "export-xlsx/",
                self.admin_site.admin_view(self.export_xlsx),
                name="core_record_export_xlsx",
            )
        ]
        return custom_urls + urls

    def export_xlsx(self, request):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Records"

        headers = ["ID", "Имя", "Email", "Телефон", "Комментарий", "Активен", "Создан", "Обновлен"]
        sheet.append(headers)

        queryset = Record.objects.all().order_by("id")
        for record in queryset.iterator():
            sheet.append(
                [
                    record.id,
                    record.name,
                    record.email,
                    record.phone,
                    record.comment,
                    "Да" if record.is_active else "Нет",
                    timezone.localtime(record.created_at).strftime("%Y-%m-%d %H:%M:%S"),
                    timezone.localtime(record.updated_at).strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        for column in sheet.columns:
            max_length = max(len(str(cell.value or "")) for cell in column)
            sheet.column_dimensions[column[0].column_letter].width = min(max_length + 2, 60)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="records_export.xlsx"'
        workbook.save(response)
        return response