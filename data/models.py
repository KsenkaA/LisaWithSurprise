from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Sprint(models.Model):
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            previous_sprint = Sprint.objects.all().order_by('-id')[0]
            previous_sprint_states = previous_sprint.states
            for state in previous_sprint_states.all():
                if state.per_from_all_tests > 80:
                    state.user.extrainfo.achieves += 1
                    state.user.save()
                    achieve = Achieve.objects.create(user=state.user, sprint=previous_sprint, type_of_ach='PAL')
                    achieve.save()
                if state.per_from_builds > 80:
                    state.user.extrainfo.achieves += 1
                    state.user.save()
                    achieve = Achieve.objects.create(user=state.user, sprint=previous_sprint, type_of_ach='PFB')
                    achieve.save()
                if state.num_commits > 80:
                    state.user.extrainfo.achieves += 1
                    state.user.save()
                    achieve = Achieve.objects.create(user=state.user, sprint=previous_sprint, type_of_ach='NC')
                    achieve.save()
                if state.per_from_builds > 80:
                    state.user.extrainfo.achieves += 1
                    state.user.save()
                    achieve = Achieve.objects.create(user=state.user, sprint=previous_sprint, type_of_ach='POT')
                    achieve.save()
                if state.per_over_tests > 80:
                    state.user.extrainfo.achieves += 1
                    state.user.save()
                    achieve = Achieve.objects.create(user=state.user, sprint=previous_sprint, type_of_ach='PFB')
                    achieve.save()
                if state.num_of_unclosed_tasks > 80:
                    state.user.extrainfo.achieves += 1
                    state.user.save()
                    achieve = Achieve.objects.create(user=state.user, sprint=previous_sprint, type_of_ach='NOUT')
                    achieve.save()
        super(Sprint, self).save(*args, **kwargs)


class Achieve(models.Model):
    user = models.ForeignKey(
        User,
        default=0,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='achieves'
    )
    sprint = models.ForeignKey(
        Sprint,
        default=0,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='achieves'
    )
    types = (
        ('PAL', 'per_from_all_tests'),
        ('PFB', 'per_from_builds'),
        ('NC', 'num_commits'),
        ('POT', 'per_over_tests'),
        ('NOUT', 'num_of_unclosed_tasks'),
    )
    type_of_ach = models.CharField(
        max_length=4,
        choices=types,
        default='PAL',
    )


class States(models.Model):
    sprint = models.ForeignKey(
        Sprint,
        default=0,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='states'
    )
    per_from_all_tests = models.IntegerField(
        default=0,
    )
    per_from_builds = models.IntegerField(
        default=0,
    )
    num_commits = models.IntegerField(
        default=0,
    )
    per_over_tests = models.IntegerField(
        default=0,
    )
    num_of_unclosed_tasks = models.IntegerField(
        default=0,
    )
    user = models.ForeignKey(
        User,
        default=0,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='states'
    )


class ExtraInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    achieves = models.IntegerField(
        default=0,
    )
    role = models.CharField(
        max_length=100,
        default=''
    )
    bought = models.CharField(
        max_length=1000,
        default=''
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ExtraInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.extrainfo.save()
