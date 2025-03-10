from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def time_duration(value):
    if isinstance(value, timedelta):
        days = value.days
        hours, remainder = divmod(value.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # Affichage sous forme de "X jours Y heures Z minutes"
        time_str = ""
        if days > 0:
            time_str += f"{days} jour{'s' if days > 1 else ''} "
        if hours > 0:
            time_str += f"{hours} heure{'s' if hours > 1 else ''} "
        if minutes > 0:
            time_str += f"{minutes} minute{'s' if minutes > 1 else ''} "
        
        return time_str.strip()
    return value
