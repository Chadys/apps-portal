from django.db import models


class Tag(models.Model):
    tag = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ("tag",)


class DeployedEnvironment(models.Model):
    name = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Application(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.ImageField()
    tags = models.ManyToManyField(Tag, related_name="applications", blank=True)
    deployments = models.ManyToManyField(
        DeployedEnvironment, through="Deployment", related_name="applications"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Deployment(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="applications"
    )
    environment = models.ForeignKey(
        DeployedEnvironment, on_delete=models.CASCADE, related_name="environments"
    )
    url = models.URLField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["application", "environment"],
                name="%(app_label)s_%(class)s_unique_application_by_environment",
            ),
        ]

    def __str__(self):
        return self.url
