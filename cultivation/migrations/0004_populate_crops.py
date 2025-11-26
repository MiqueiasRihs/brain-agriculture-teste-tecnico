from django.db import migrations


CROP_DATA = [
    ("Algodão", "COTTON"),
    ("Arroz", "RICE"),
    ("Batata", "POTATO"),
    ("Cacau", "COCOA"),
    ("Café", "COFFEE"),
    ("Cana-de-açúcar", "SUGARCANE"),
    ("Feijão", "BEAN"),
    ("Girassol", "SUNFLOWER"),
    ("Laranja", "ORANGE"),
    ("Milho", "CORN"),
    ("Soja", "SOY"),
    ("Trigo", "WHEAT"),
]


def create_default_crops(apps, schema_editor):
    Crop = apps.get_model("cultivation", "Crop")

    for name, code in CROP_DATA:
        crop, created = Crop.objects.get_or_create(
            name=name,
            defaults={"code": code, "is_active": True},
        )

        if not created and crop.code != code:
            crop.code = code
            crop.save(update_fields=["code"])


def delete_default_crops(apps, schema_editor):
    Crop = apps.get_model("cultivation", "Crop")
    Crop.objects.filter(name__in=[name for name, _ in CROP_DATA]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cultivation", "0003_crop_code"),
    ]

    operations = [
        migrations.RunPython(create_default_crops, delete_default_crops),
    ]
