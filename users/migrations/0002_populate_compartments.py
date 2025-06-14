from django.db import migrations


COMPARTMENTS_DATA = [
    {'name': 'Miejsce dla osoby na wózku', 'koleo_id': 7},
    {'name': 'Wagon ciszy', 'koleo_id': 10},
    {'name': 'Miejsce dla podróżnego z rowerem', 'koleo_id': 11},
    {'name': 'Opiekun osoby z niepełnosprawnej', 'koleo_id': 17},
]

def populate_special_compartments(apps, schema_editor):
    """Wypełnia model SpecialCompartmentType danymi początkowymi."""
    SpecialCompartmentType = apps.get_model('users', 'SpecialCompartmentType')
    for comp_data in COMPARTMENTS_DATA:
        SpecialCompartmentType.objects.get_or_create(
            koleo_id=comp_data['koleo_id'],
            defaults={'name': comp_data['name']}
        )

def remove_special_compartments(apps, schema_editor):
    """Opcjonalnie: usuwa dane przy cofaniu migracji."""
    SpecialCompartmentType = apps.get_model('users', 'SpecialCompartmentType')
    koleo_ids_to_delete = [d['koleo_id'] for d in COMPARTMENTS_DATA]
    SpecialCompartmentType.objects.filter(koleo_id__in=koleo_ids_to_delete).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_special_compartments, remove_special_compartments),
    ]