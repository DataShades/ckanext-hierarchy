from ckan.controllers.organization import OrganizationController
from ckan.common import c, request, _
import ckan.model as model
import ckan.lib.base as base
import ckan.logic as logic
import ckan.lib.helpers as h

abort = base.abort
render = base.render

NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError

class OrganizationHierarchy(OrganizationController):

    def index(self):
        group_type = self._guess_group_type()

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'with_private': False}
        q = c.q = request.params.get('q', '')
        sort_by = c.sort_by_selected = request.params.get('sort')

        try:
            self._check_access('site_read', context)
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))

        page_limit = 21

        hierarchy_view = request.params.get('hierarchy', None)

        if hierarchy_view == 'true':
            page_limit = 1000

        if not sort_by:
            sort_by = 'name asc'

        page = h.get_page_number(request.params)

        top_orgs_list = []
        top_orgs = model.Group.get_top_level_groups(type='organization')
        for i in top_orgs:
            top_orgs_list.append(i.name)

        org_list = self._action('group_list')(
            context,
            {
                'q': q,
                'sort': sort_by,
                'rows': 1000,
                'all_fields': True,
            })

        c.page = h.Page(
            collection=org_list,
            page=page,
            url=h.pager_url,
            item_count=len(org_list),
            items_per_page=page_limit
        )
        return render('organization/index.html',
                      extra_vars={'selected_sort':sort_by, 'top_orgs_list': top_orgs_list, 'group_type': group_type})
