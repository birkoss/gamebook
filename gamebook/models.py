from django.db import models

from core.models import TimeStampedModel, UUIDModel


class Story(TimeStampedModel, UUIDModel, models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        null=True
    )
    title = models.CharField(max_length=200, default="")
    is_active = models.BooleanField(default=False)
    #first_page


class Page(TimeStampedModel, UUIDModel, models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.PROTECT,
        null=False
    )

    title = models.CharField(max_length=200, default="")

    content = models.TextField(
        default=""
    )


class Action(TimeStampedModel, UUIDModel, models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.PROTECT,
        null=False
    )
    label = models.CharField(max_length=200, default="")
    order = models.IntegerField(default=0, null=True)

    extra = models.JSONField()

    class Meta:
        ordering = ('order',)

    def save(self, *args, **kwargs):
        if self.order == 0:
            action = Action.objects.filter(page=self.page).order_by("-order").first()
            if action is not None:
                self.order = action.order + 1
            else:
                self.order = 1
        super().save(args, kwargs)


class ActionCondition(TimeStampedModel, UUIDModel, models.Model):
    action = models.ForeignKey(
        Action,
        on_delete=models.PROTECT,
        null=False
    )

    extra = models.JSONField()
