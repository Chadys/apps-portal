from django.contrib.postgres.fields import ArrayField
from django.db import models


class SubqueryArray(models.Subquery):
    template = "ARRAY(%(subquery)s)"
    output_field = ArrayField(base_field=models.CharField())
