import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RoleChoice(models.TextChoices):
    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')


class FilmTypeChoice(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('tv_show')

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Filmwork(TimeStampedMixin, UUIDMixin):
    # MOVIE = "MV"
    # TV_SHOW = "TV"
    # type_choices = [
    #     (MOVIE, "movie"),
    #     (TV_SHOW, "tv_show")
    # ]
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateTimeField(auto_now=True)
    file_path = models.FileField(_('file_path'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(max_length=20, choices=FilmTypeChoice.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, to_field='id', db_column='film_work_id')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, to_field='id', db_column='genre_id')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'], name='film_work_genre_idx')
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'genre_id'],
                name='unique_film_work_genre',
            ),
        ]


class PersonFilmwork(UUIDMixin):
    # ACTOR = "ACT"
    # DIRECTOR = "DR"
    # WRITER = "WR"
    # role_choices = [
    #     (ACTOR, "actor"),
    #     (DIRECTOR, "director"),
    #     (WRITER, "writer")
    # ]
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, to_field='id', db_column='film_work_id')
    person = models.ForeignKey('Person', on_delete=models.CASCADE, to_field='id', db_column='person_id')
    role = models.CharField(_('role'), max_length=30, choices=RoleChoice.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'person_id', 'role'],
                name='unique_film_work_person',
            ),
        ]


class Person(TimeStampedMixin, UUIDMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    def __str__(self):
        return self. full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
