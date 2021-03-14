from django import template
from django.db.models import Sum, Avg, Max, Min, Count
import datetime
register = template.Library()

@register.filter
def total_minutes(queryset):
	minutes = 0
	seconds = 0
	for lesson in queryset.all():
		m,s = str(lesson.duration).split('.')
		minutes += int(m)
		seconds += int(s)
	total_seconds = minutes*60 + seconds
	print(total_seconds)
	total_time = str(datetime.timedelta(seconds=total_seconds))
	if total_time.split(':')[0] == '0':
		total_time = ':'.join(total_time.split(':')[1:])
	return total_time