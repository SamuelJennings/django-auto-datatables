import json

from django.db.models import Count, Q
from rest_framework_datatables.filters import (
    DatatablesBaseFilterBackend,
    DatatablesFilterBackend,
)


class SearchPanesFilterBase(DatatablesBaseFilterBackend):
    """Filter that implements the searchPanes feature of DataTables"""

    def get_search_panes_fields(self, view):
        """
        Search fields are obtained from the view, but the request is always
        passed to this method. Sub-classes can override this method to
        dynamically change the search fields based on request content.
        """
        return getattr(view, "search_panes", [])

    def parse_datatables_query(self, request, view):
        """parse request.query_params into a list of fields and orderings and
        global search parameters (value and regex)"""
        ret = super().parse_datatables_query(request, view)
        ret["search_panes"] = self.get_search_panes(request, view)
        return ret

    def get_search_pane_values(self, q_params, field):
        """Parses query params and returns a list of values for a given field.
        E.g.
        ...
        searchPanes[is_active][0]: true
        searchPanes[is_active][1]: false
        ...
        returns [true, false]
        """
        vals = [v for k, v in q_params.items() if k.startswith(f"searchPanes[{field}]")]
        return json.loads("[" + ",".join(vals) + "]")

    def get_search_panes(self, request, view):
        """Parses query params and returns a dict of valid search pane fields and their values as a list.
        {
            "is_active": [false],
            "is_admin": [true],
            "user_type": ["student", "teacher"],
        }
        """
        ret = {}
        for field in self.get_search_panes_fields(view):
            ret[field] = self.get_search_pane_values(request.query_params, field)
        return ret


class SearchPanesFilter(DatatablesFilterBackend, SearchPanesFilterBase):
    def filter_queryset(self, request, queryset, view):
        if not self.check_renderer_format(request):
            return queryset

        total_count = view.get_queryset().count()
        self.set_count_before(view, total_count)

        filtered_count_before = (
            queryset.count()
            if len(getattr(view, "filter_backends", [])) > 1
            else total_count
        )
        datatables_query = self.parse_datatables_query(request, view)

        q = self.get_q(datatables_query)
        if q:
            queryset = queryset.filter(q).distinct()
            filtered_count = queryset.count()
        else:
            filtered_count = filtered_count_before
        self.set_count_after(view, filtered_count)

        search_panes = {"options": {}}
        for val in datatables_query["search_panes"]:
            search_panes["options"][val] = self.get_search_pane_qs(
                val, view.get_queryset(), queryset
            )

        view._search_panes = search_panes

        ordering = self.get_ordering(request, view, datatables_query["fields"])
        if ordering:
            queryset = queryset.order_by(*ordering)

        return queryset

    def choices_from_field(self, choices):
        """Converts a list of choices into a list of dicts with label and value keys."""
        return [{"label": label, "value": value} for value, label in choices]

    def choices_from_queryset(self, field, qs):
        """Converts a queryset into a list of dicts with label and value keys."""
        return [
            {"label": str(item), "value": item}
            for item in qs.values_list(field, flat=True).distinct()
        ]

    def get_field_choices(self, field, qs):
        # fetch the model field from the model
        model_field = qs.model._meta.get_field(field)
        if hasattr(model_field, "choices") and model_field.choices is not None:
            return self.choices_from_field(model_field.choices)
        else:
            return self.choices_from_queryset(field, qs)

    def get_search_pane_qs(self, val, qs, filtered_qs=None):
        # total = qs.values(val).annotate(total=Count(val))
        choices = {c["value"]: c for c in self.get_field_choices(val, qs)}
        for item in qs.values(val).annotate(total=Count(val)):
            choices[item[val]]["total"] = item["total"]
        if filtered_qs is not None:
            # count = filtered_qs.values(val).annotate(count=Count(val))
            for item in filtered_qs.values(val).annotate(count=Count(val)):
                choices[item[val]]["count"] = item["count"]

        # total = {item[val]: item for item in qs.values(val).annotate(total=Count(val))}
        # print(qs.values(val).annotate(total=Count(val)))
        # if filtered_qs is not None:
        #     # count = filtered_qs.values(val).annotate(count=Count(val))
        #     filtered_count = {item[val]: item for item in filtered_qs.values(val).annotate(count=Count(val))}

        # result = []
        # for k, v in total.items():
        #     ret = {"label": k, "value": k}
        #     if filtered_qs is not None:
        #         ret["total"] = filtered_count[k]["count"] if k in filtered_count else 0
        #         ret["count"] = filtered_count[k]["count"] if k in filtered_count else 0
        #     result.append(ret)
        return choices.values()

    def get_q(self, datatables_query):
        q = super().get_q(datatables_query)
        for k, v in datatables_query["search_panes"].items():
            if v:
                q &= Q(**{f"{k}__in": v})

        return q
