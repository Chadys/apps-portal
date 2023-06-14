from django.db.models import OuterRef, QuerySet

from apps_library.models import Deployment, Tag
from common.expressions import SubqueryArray


class DeploymentService:
    def filter_by_tags_subset(
        self, selected_tags: list[str], qs: QuerySet[Deployment] | None = None
    ):
        if qs is None:
            qs = Deployment.objects.all()
        tags_qs = Tag.objects.filter(applications=OuterRef("application_id"))
        return qs.annotate(tags=SubqueryArray(tags_qs.values("tag"))).filter(
            tags__contains=selected_tags
        )
