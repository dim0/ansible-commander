# Copyright (c) 2013 AnsibleWorks, INc.
#
# This file is part of Ansible Commander
#
# Ansible Commander is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.conf.urls import *
import lib.main.views as views

# organizations service
views_OrganizationsList            = views.OrganizationsList.as_view()
views_OrganizationsDetail          = views.OrganizationsDetail.as_view()
views_OrganizationsAuditTrailList  = views.OrganizationsAuditTrailList.as_view()
views_OrganizationsUsersList       = views.OrganizationsUsersList.as_view()
views_OrganizationsAdminsList      = views.OrganizationsAdminsList.as_view()
views_OrganizationsProjectsList    = views.OrganizationsProjectsList.as_view()
views_OrganizationsTagsList        = views.OrganizationsTagsList.as_view()
views_OrganizationsTeamsList       = views.OrganizationsTeamsList.as_view()

# users service
views_UsersList                    = views.UsersList.as_view()
views_UsersDetail                  = views.UsersDetail.as_view()
views_UsersMeList                  = views.UsersMeList.as_view()
views_UsersTeamsList               = views.UsersTeamsList.as_view()
views_UsersOrganizationsList       = views.UsersOrganizationsList.as_view()
views_UsersAdminOrganizationsList  = views.UsersAdminOrganizationsList.as_view()
views_UsersProjectsList            = views.UsersProjectsList.as_view()
views_UsersCredentialsList         = views.UsersCredentialsList.as_view()

# projects service
views_ProjectsList                 = views.ProjectsList.as_view()
views_ProjectsDetail               = views.ProjectsDetail.as_view()
views_ProjectsOrganizationsList    = views.ProjectsOrganizationsList.as_view()

# audit trail service

# team service
views_TeamsList                    = views.TeamsList.as_view()
views_TeamsDetail                  = views.TeamsDetail.as_view()
views_TeamsUsersList               = views.TeamsUsersList.as_view()
views_TeamsCredentialsList         = views.TeamsCredentialsList.as_view()
views_TeamsCredentialsList         = views.TeamsCredentialsList.as_view()

# inventory service
views_InventoryList                = views.InventoryList.as_view()
views_InventoryDetail              = views.InventoryDetail.as_view()
views_InventoryHostsList           = views.InventoryHostsList.as_view()
views_InventoryGroupsList          = views.InventoryGroupsList.as_view()

# group service
views_GroupsList                   = views.GroupsList.as_view()
views_GroupsDetail                 = views.GroupsDetail.as_view()
views_GroupsVariableDetail         = views.GroupsVariableDetail.as_view()
views_GroupsChildrenList           = views.GroupsChildrenList.as_view()

# host service
views_HostsList                    = views.HostsList.as_view()
views_HostsDetail                  = views.HostsDetail.as_view()
views_HostsVariableDetail          = views.HostsVariableDetail.as_view()

# seperate variable data
views_VariableDetail               = views.VariableDetail.as_view()

# log data services

# events services

# jobs services

# tags service
views_TagsDetail                   = views.TagsDetail.as_view()

# credentials service
views_CredentialsDetail            = views.CredentialsDetail.as_view()


urlpatterns = patterns('',

    # organizations vice
    url(r'^api/v1/organizations/$',                               views_OrganizationsList),
    url(r'^api/v1/organizations/(?P<pk>[0-9]+)/$',                views_OrganizationsDetail),
    url(r'^api/v1/organizations/(?P<pk>[0-9]+)/audit_trail/$',    views_OrganizationsAuditTrailList),
    url(r'^api/v1/organizations/(?P<pk>[0-9]+)/users/$',          views_OrganizationsUsersList),
    url(r'^api/v1/organizations/(?P<pk>[0-9]+)/admins/$',         views_OrganizationsAdminsList),
    url(r'^api/v1/organizations/(?P<pk>[0-9]+)/projects/$',       views_OrganizationsProjectsList),
    url(r'^api/v1/organizations/(?P<pk>[0-9]+)/tags/$',           views_OrganizationsTagsList),
    url(r'^api/v1/organizations/(?P<pk>[0-9]+)/teams/$',          views_OrganizationsTeamsList),

    # users service
    url(r'^api/v1/me/$',                                          views_UsersMeList),
    url(r'^api/v1/users/$',                                       views_UsersList),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/$',                        views_UsersDetail),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/teams/$',                  views_UsersTeamsList),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/organizations/$',          views_UsersOrganizationsList),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/admin_of_organizations/$', views_UsersAdminOrganizationsList),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/projects/$',               views_UsersProjectsList),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/credentials/$',            views_UsersCredentialsList),

    # projects service
    url(r'^api/v1/projects/$',                                    views_ProjectsList),
    url(r'^api/v1/projects/(?P<pk>[0-9]+)/$',                     views_ProjectsDetail),
    url(r'^api/v1/projects/(?P<pk>[0-9]+)/organizations/$',       views_ProjectsOrganizationsList),

    # audit trail service
    # api/v1/audit_trails/
    # api/v1/audit_trails/N/
    # and ./audit_trails/ on all resources

    # team service
    # api/v1/teams/
    url(r'^api/v1/teams/$',                                       views_TeamsList),
    url(r'^api/v1/teams/(?P<pk>[0-9]+)/$',                        views_TeamsDetail),
    url(r'^api/v1/teams/(?P<pk>[0-9]+)/users/$',                  views_TeamsUsersList),
    url(r'^api/v1/teams/(?P<pk>[0-9]+)/credentials/$',            views_TeamsCredentialsList),

    # api/v1/teams/N/
    # api/v1/teams/N/users/

    # inventory service
    url(r'^api/v1/inventories/$',                                 views_InventoryList),
    url(r'^api/v1/inventories/(?P<pk>[0-9]+)/$',                  views_InventoryDetail),
    url(r'^api/v1/inventories/(?P<pk>[0-9]+)/hosts/$',            views_InventoryHostsList),
    url(r'^api/v1/inventories/(?P<pk>[0-9]+)/groups/$',           views_InventoryGroupsList),

    # host service
    url(r'^api/v1/hosts/$',                                       views_HostsList),
    url(r'^api/v1/hosts/(?P<pk>[0-9]+)/$',                        views_HostsDetail),

    # group service
    url(r'^api/v1/groups/$',                                      views_GroupsList),
    url(r'^api/v1/groups/(?P<pk>[0-9]+)/$',                       views_GroupsDetail),
    url(r'^api/v1/groups/(?P<pk>[0-9]+)/children/$',              views_GroupsChildrenList),

    # variable data
    url(r'^api/v1/hosts/(?P<pk>[0-9]+)/variable_data/$',          views_HostsVariableDetail),
    url(r'^api/v1/groups/(?P<pk>[0-9]+)/variable_data/$',         views_GroupsVariableDetail),
    url(r'^api/v1/variable_data/(?P<pk>[0-9]+)/$',                views_VariableDetail),

    # log data (results) services

    # jobs & job status services
    # /jobs/
    # /jobs/N/
    # /job_statuses/
    # /job_statuses/N/

    # tags service
    url(r'^api/v1/tags/(?P<pk>[0-9]+)/$',                         views_TagsDetail),
    # ... and tag relations on all resources

    # credentials services
    url(r'^api/v1/credentials/(?P<pk>[0-9]+)/$',                  views_CredentialsDetail),

    # permissions services
    # ... users
    # ... teams

)

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )
