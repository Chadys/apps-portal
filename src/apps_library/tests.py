from django.core.files.uploadedfile import SimpleUploadedFile

from apps_library.models import Application, DeployedEnvironment, Deployment, Tag
from apps_library.services import DeploymentService


class TestDeploymentService:
    def test_filter_by_tags_subset(self, db):
        infra_tag = Tag.objects.create(tag="infra")
        web_tag = Tag.objects.create(tag="web")
        ecom_tag = Tag.objects.create(tag="ecom")
        icon = SimpleUploadedFile(
            "best_file_eva.jpg", b"these are the contents of the txt file"
        )
        app1 = Application.objects.create(name="app1", icon=icon)
        app1.tags.set([web_tag, ecom_tag])
        app2 = Application.objects.create(name="app2", icon=icon)
        app2.tags.set([infra_tag])
        app3 = Application.objects.create(name="app3", icon=icon)
        app3.tags.set([web_tag, infra_tag])

        env = DeployedEnvironment.objects.create(name="production")
        dep1 = Deployment.objects.create(
            environment=env, application=app1, url="http://dummy.dummy"
        )
        dep2 = Deployment.objects.create(
            environment=env, application=app2, url="http://dummy.dummy"
        )
        dep3 = Deployment.objects.create(
            environment=env, application=app3, url="http://dummy.dummy"
        )
        service = DeploymentService()
        qs = Deployment.objects.all().order_by("application__name")

        assert list(service.filter_by_tags_subset(["web", "ecom", "infra"], qs)) == []
        assert list(service.filter_by_tags_subset(["web", "ecom"], qs)) == [dep1]
        assert list(service.filter_by_tags_subset(["web"], qs)) == [dep1, dep3]
        assert list(service.filter_by_tags_subset([], qs)) == [dep1, dep2, dep3]
