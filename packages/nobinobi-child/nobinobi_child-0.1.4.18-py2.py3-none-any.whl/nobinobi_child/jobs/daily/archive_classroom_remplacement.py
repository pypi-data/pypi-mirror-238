from django.utils import timezone
from django.utils.translation import gettext as _
from django_extensions.management.jobs import DailyJob

from nobinobi_child.models import ReplacementClassroom


class Job(DailyJob):
    help = _("Archive classroom remplacement automatically child")

    def execute(self):
        # Obtention de la date actuelle
        today = timezone.localdate()

        # Parcours de tous les ReplacementClassroom non archivés
        for rc in ReplacementClassroom.objects.filter(archived=False):
            # Vérification si la date de fin est antérieure à aujourd'hui
            if rc.end_date < today:
                # Archivage du ReplacementClassroom en le marquant comme archivé
                rc.archived = True
                rc.save(update_fields=['archived'])
