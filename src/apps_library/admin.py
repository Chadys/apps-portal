from django.contrib import admin

from apps_library.models import Application, DeployedEnvironment, Deployment, Tag


@admin.register(DeployedEnvironment)
class DeployedEnvironmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("tag",)


class DeploymentInline(admin.TabularInline):
    model = Deployment
    extra = 3


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "tags_list", "environments_list")
    list_filter = ("deployments", "tags")
    search_fields = ("name",)
    inlines = [
        DeploymentInline,
    ]
    autocomplete_fields = ("tags",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags", "deployments")

    @admin.display(description="Tags")
    def tags_list(self, obj: Application):
        return ", ".join(str(tag) for tag in obj.tags.all())

    @admin.display(description="Deployments")
    def environments_list(self, obj: Application):
        return ", ".join(str(env) for env in obj.deployments.all())
