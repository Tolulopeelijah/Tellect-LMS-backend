from django.contrib import admin
from .models import SupportTicket, TicketReply


class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('subject', 'user__email')
    inlines = [TicketReplyInline]


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'is_staff_reply', 'created_at')
