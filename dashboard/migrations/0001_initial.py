from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='NetflixTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_id', models.CharField(max_length=20, unique=True)),
                ('type', models.CharField(choices=[('Movie', 'Movie'), ('TV Show', 'TV Show')], max_length=10)),
                ('title', models.CharField(max_length=300)),
                ('director', models.CharField(blank=True, max_length=300, null=True)),
                ('cast', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('date_added', models.DateField(blank=True, null=True)),
                ('release_year', models.IntegerField(blank=True, null=True)),
                ('rating', models.CharField(blank=True, max_length=20, null=True)),
                ('duration', models.CharField(blank=True, max_length=20, null=True)),
                ('listed_in', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('year_added', models.IntegerField(blank=True, null=True)),
                ('rating_category', models.CharField(
                    choices=[('Adult', 'Adult'), ('Teen', 'Teen'), ('Kids', 'Kids'), ('Unknown', 'Unknown')],
                    default='Unknown', max_length=10,
                )),
                ('primary_genre', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'netflix_titles',
            },
        ),
        migrations.AddIndex(
            model_name='netflixtitle',
            index=models.Index(fields=['type'], name='netflix_tit_type_idx'),
        ),
        migrations.AddIndex(
            model_name='netflixtitle',
            index=models.Index(fields=['release_year'], name='netflix_tit_release_idx'),
        ),
        migrations.AddIndex(
            model_name='netflixtitle',
            index=models.Index(fields=['rating_category'], name='netflix_tit_rating_cat_idx'),
        ),
        migrations.AddIndex(
            model_name='netflixtitle',
            index=models.Index(fields=['country'], name='netflix_tit_country_idx'),
        ),
        migrations.AddIndex(
            model_name='netflixtitle',
            index=models.Index(fields=['year_added'], name='netflix_tit_year_added_idx'),
        ),
    ]
