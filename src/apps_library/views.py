from django.http import Http404
from django.views.generic import TemplateView

from apps_library.models import DeployedEnvironment, Deployment, Tag
from apps_library.services import DeploymentService


class HomePageView(TemplateView):
    template_name = "library.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_environment_id"] = self.request.GET.get("environment")
        context["selected_tags"] = self.request.GET.getlist("tag")
        context["environments"] = list(DeployedEnvironment.objects.all())

        if context["selected_environment_id"]:
            try:
                context["selected_environment_id"] = int(
                    context["selected_environment_id"]
                )
            except ValueError:
                pass
            else:
                if context["selected_environment_id"] in {
                    env.id for env in context["environments"]
                }:
                    return context
        else:
            try:
                context["selected_environment_id"] = context["environments"][-1].id
            except IndexError:
                pass
            else:
                return context
        raise Http404("No DeployedEnvironment matches the given query.")


class DeploymentsListView(TemplateView):
    template_name = "deployments-list.html"

    def get_context_data(self, selected_environment, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_tags = self.request.GET.getlist("tag")

        context["selected_tags"] = selected_tags
        context["available_tags"] = Tag.objects.exclude(
            tag__in=selected_tags
        ).values_list("tag", flat=True)
        context["selected_environment_id"] = selected_environment
        context["deployments"] = (
            Deployment.objects.all()
            .select_related("application", "environment")
            .filter(environment_id=selected_environment)
        )
        if selected_tags:
            context["deployments"] = DeploymentService().filter_by_tags_subset(
                selected_tags, context["deployments"]
            )
        return context
