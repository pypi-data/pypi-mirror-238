# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
CORE-POS department views
"""

from corepos.db.office_op import model as corepos

from .master import CoreOfficeMasterView


class DepartmentView(CoreOfficeMasterView):
    """
    Base class for department views.
    """
    model_class = corepos.Department
    model_title = "CORE-POS Department"
    url_prefix = '/core-pos/departments'
    route_prefix = 'corepos.departments'

    labels = {
        'tax_rate_id': "Tax Rate ID",
        'see_id': "See ID",
        'modified_by_id': "Modified by ID",
    }

    grid_columns = [
        'number',
        'name',
        'tax_rate',
        'food_stampable',
        'limit',
        'minimum',
        'discount',
        'see_id',
        'modified',
        'modified_by_id',
        'margin',
        'sales_code',
        'member_only',
    ]

    def configure_grid(self, g):
        super().configure_grid(g)

        # number
        g.set_link('number')
        g.set_sort_defaults('number')
        g.filters['number'].default_active = True
        g.filters['number'].default_verb = 'equal'

        # name
        g.set_link('name')
        g.filters['name'].default_active = True
        g.filters['name'].default_verb = 'contains'

        # TODO: it should be easier to set only grid header label
        g.set_label('food_stampable', "FS")
        g.filters['food_stampable'].label = "Food Stampable"

        # currency fields
        g.set_type('limit', 'currency')
        g.set_type('minimum', 'currency')

        # modified
        g.set_type('modified', 'datetime_local')

        # margin
        g.set_renderer('margin', self.render_margin)

    def render_margin(self, dept, field):
        margin = getattr(dept, field)
        if margin is None:
            return
        app = self.get_rattail_app()
        return app.render_percent(100 * margin)

    def configure_form(self, f):
        super().configure_form(f)

        # tax_rate
        f.set_renderer('tax_rate', self.render_corepos_tax_rate)

        # currency fields
        f.set_type('limit', 'currency')
        f.set_type('minimum', 'currency')

        # margin
        f.set_renderer('margin', self.render_margin)

        # modified
        f.set_type('modified', 'datetime_local')

    def core_office_object_url(self, office_url, department):
        return '{}/item/departments/DepartmentEditor.php?did={}'.format(
            office_url, department.number)


def defaults(config, **kwargs):
    base = globals()

    DepartmentView = kwargs.get('DepartmentView', base['DepartmentView'])
    DepartmentView.defaults(config)


def includeme(config):
    defaults(config)
