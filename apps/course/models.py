from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.choices import ModerationStatusChoices
from apps.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    icon = models.ImageField(
        verbose_name=_("Icon"),
        upload_to="category_icons",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Course(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        related_name="courses",
    )
    main_image = models.ImageField(verbose_name=_("Main image"), upload_to="courses")
    about = RichTextUploadingField(verbose_name=_("About"), null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name=_("Price"))
    moderation_status = models.CharField(
        verbose_name=_("Moderation status"),
        max_length=255,
        choices=ModerationStatusChoices.choices,
        default=ModerationStatusChoices.ACTIVE,
    )

    def __str__(self):
        return self.name


class UserCourse(BaseModel):
    profile = models.ForeignKey(
        verbose_name=_("User"),
        to="users.Profile",
        on_delete=models.CASCADE,
        related_name="user_courses",
    )
    course = models.ForeignKey(
        verbose_name=_("Course"),
        to="Course",
        on_delete=models.CASCADE,
        related_name="user_courses",
    )
    is_finished = models.BooleanField(verbose_name=_("Is finished"), default=False)

    class Meta:
        unique_together = ["profile", "course"]

    def __str__(self):
        return f"{self.profile} - {self.course}"


# LESSON
class Lesson(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    course = models.ForeignKey(
        verbose_name=_("Course"),
        to="Course",
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    order = models.PositiveIntegerField(verbose_name=_("Order"), default=0)
    moderation_status = models.CharField(
        verbose_name=_("Moderation status"),
        max_length=255,
        choices=ModerationStatusChoices.choices,
        default=ModerationStatusChoices.ACTIVE,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class VideoLesson(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    lesson = models.ForeignKey(
        verbose_name=_("Lesson"),
        to="Lesson",
        on_delete=models.CASCADE,
        related_name="video_lessons",
    )
    video = models.FileField(verbose_name=_("Video"), upload_to="videos")
    order = models.PositiveIntegerField(verbose_name=_("Order"), default=0)

    def __str__(self):
        return self.name


class VideoView(BaseModel):
    profile = models.ForeignKey(
        verbose_name=_("Profile"),
        to="users.Profile",
        on_delete=models.CASCADE,
        related_name="video_views",
    )
    video_lesson = models.ForeignKey(
        verbose_name=_("Video lesson"),
        to="VideoLesson",
        on_delete=models.CASCADE,
        related_name="video_views",
    )

    def __str__(self):
        return f"{self.profile.user.phone_number} - {self.video_lesson.name}"

    class Meta:
        unique_together = ["profile", "video_lesson"]


class CourseCertificate(BaseModel):
    user_course = models.OneToOneField(
        verbose_name=_("User course"),
        to="UserCourse",
        on_delete=models.CASCADE,
        related_name="certificate",
    )
    certificate = models.FileField(verbose_name=_("Certificate"), upload_to="certificates")

    def __str__(self):
        return f"{self.user_course.profile.user.phone_number} - {self.user_course.course.name}"

    def save(self, *args, **kwargs):
        if self.id is None:
            if not self.user_course.is_finished:
                raise ValueError(_("User course is not finished yet"))
        super().save(*args, **kwargs)


class CourseReview(BaseModel):
    course = models.ForeignKey(verbose_name=_("Course"), to="Course", on_delete=models.CASCADE, related_name="reviews")
    profile = models.ForeignKey(
        verbose_name=_("Profile"), to="users.Profile", on_delete=models.CASCADE, related_name="reviews"
    )
    comment = models.TextField(verbose_name=_("Comment"))
    rating = models.PositiveIntegerField(
        verbose_name=_("Rating"), default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ["course", "profile"]

    def __str__(self):
        return f"{self.profile} - {self.course}"
