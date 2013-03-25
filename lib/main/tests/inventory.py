# (c) 2013, AnsibleWorks
#
# This file is part of Ansible Commander
#
# Ansible Commander is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible Commander is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible Commander.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import json

from django.contrib.auth.models import User as DjangoUser
import django.test
from django.test.client import Client
from lib.main.models import *
from lib.main.tests.base import BaseTest

class InventoryTest(BaseTest):

    def setUp(self):
        super(InventoryTest, self).setUp()
        self.setup_users()
        self.organizations = self.make_organizations(self.super_django_user, 3)
        self.organizations[0].admins.add(self.normal_django_user)
        self.organizations[0].users.add(self.other_django_user)
        self.organizations[0].users.add(self.normal_django_user)

        self.inventory_a = Inventory.objects.create(name='inventory-a', description='foo', organization=self.organizations[0])
        self.inventory_b = Inventory.objects.create(name='inventory-b', description='bar', organization=self.organizations[1])
 
        # the normal user is an org admin of org 0

        # create a permission here on the 'other' user so they have edit access on the org
        # we may add another permission type later.
        self.perm_read = Permission.objects.create(
             inventory       = self.inventory_b,
             user            = self.other_django_user,
             permission_type = 'read'
        )

        # and make one more user that won't be a part of any org, just for negative-access testing

        self.nobody_django_user = User.objects.create(username='nobody')
        self.nobody_django_user.set_password('nobody')
        self.nobody_django_user.save()

    def get_nobody_credentials(self):
        # here is a user without any permissions...
        return ('nobody', 'nobody')

    def test_main_line(self):
       
        # some basic URLs... 
        inventories   = '/api/v1/inventories/'
        inventories_1 = '/api/v1/inventories/1/'
        inventories_2 = '/api/v1/inventories/2/'
        hosts         = '/api/v1/hosts/'
        groups        = '/api/v1/groups/'
        variables     = '/api/v1/variables/'

        # a super user can list inventories
        data = self.get(inventories, expect=200, auth=self.get_super_credentials())
        self.assertEquals(data['count'], 2)

        # an org admin can list inventories but is filtered to what he adminsters
        data = self.get(inventories, expect=200, auth=self.get_normal_credentials())
        self.assertEquals(data['count'], 1)

        # a user who is on a team who has a read permissions on an inventory can see filtered inventories
        data = self.get(inventories, expect=200, auth=self.get_other_credentials())
        self.assertEquals(data['count'], 1)      

        # a regular user not part of anything cannot see any inventories
        data = self.get(inventories, expect=200, auth=self.get_nobody_credentials())
        self.assertEquals(data['count'], 0)

        # a super user can get inventory records
        data = self.get(inventories_1, expect=200, auth=self.get_super_credentials())
        self.assertEquals(data['name'], 'inventory-a')

        # an org admin can get inventory records
        data = self.get(inventories_1, expect=200, auth=self.get_normal_credentials())
        self.assertEquals(data['name'], 'inventory-a')

        # a user who is on a team who has read permissions on an inventory can see inventory records
        data = self.get(inventories_1, expect=403, auth=self.get_other_credentials())
        data = self.get(inventories_2, expect=200, auth=self.get_other_credentials())
        self.assertEquals(data['name'], 'inventory-b')

        # a regular user cannot read any inventory records
        data = self.get(inventories_1, expect=403, auth=self.get_nobody_credentials())
        data = self.get(inventories_2, expect=403, auth=self.get_nobody_credentials())

        # a super user can create inventory
        new_inv_1 = dict(name='inventory-c', description='baz', organization=1)
        data = self.post(inventories, data=new_inv_1, expect=201, auth=self.get_super_credentials())
        self.assertEquals(data['id'], 3)

        # an org admin of any org can create inventory, if it is one of his organizations
        # the organization parameter is required!
        new_inv_incomplete = dict(name='inventory-d', description='baz')
        data = self.post(inventories, data=new_inv_incomplete, expect=403,  auth=self.get_normal_credentials())
        new_inv_not_my_org = dict(name='inventory-d', description='baz', organization=3)

        data = self.post(inventories, data=new_inv_not_my_org, expect=403,  auth=self.get_normal_credentials())
        new_inv_my_org = dict(name='inventory-d', description='baz', organization=1)
        data = self.post(inventories, data=new_inv_my_org, expect=201, auth=self.get_normal_credentials())

        # a regular user cannot create inventory
        new_inv_denied = dict(name='inventory-e', description='glorp', organization=1)
        data = self.post(inventories, data=new_inv_denied, expect=403, auth=self.get_other_credentials())

        # a super user can add hosts
 
        # an org admin can add groups

        # a normal user cannot add hosts

        # a normal user with inventory edit permissions can create hosts

        # a super user can add groups

        # an org admin can create groups

        # a normal user cannot create groups

        # a normal user with inventory edit permissions can create groups

        # a super user can associate hosts with inventories

        # an org admin can associate hosts with inventories

        # a normal user cannot associate hosts with inventories

        # a normal user with edit permission on the inventory can associate hosts with inventories

        # a super user can associate groups with inventories

        # an org admin can associate groups with inventories

        # a normal user cannot associate hosts with inventories

        # a normal user with edit permissions on the inventory can associate hosts with inventories

        # a super user can create variable objects

        # an org admin can create variable objects

        # a normal user cannot create variable objects

        # a normal user with at least one inventory edit permission can create variable objects

        # a super user can associate variable objects with groups

        # an org admin can associate variable objects with groups
 
        # a normal user cannot associate variable objects with groups

        # a normal user with inventory edit permissions can associate variable objects with groups

        # a super user can associate variable objects with hosts

        # an org admin can associate variable objects with hosts
 
        # a normal user cannot associate variable objects with hosts

        # a normal user with inventory edit permissions can associate variable objects with hosts

        # a super user can set subgroups

        # an org admin can set subgroups
 
        # a normal user cannot set subgroups

        # a normal user with inventory edit permissions can associate subgroups

        # a super user can get a group record

        # an org admin can get a group record

        # a user who is on a team who has read permissions on an inventory can get a group record
         
        # a regular user cannot read any group records

        # a super user can get a host record

        # an org admin can get a host record

        # a user who is on a team who has read permissions on an inventory can get a host record

        # a regular user cannot get a host record

        # a super user can see the variables attached to a group

        # a org admin can see the variables attached to a group

        # a user who is on a team who has read permissions on an inventory can see the variables attached to a group

        # a regular user cannot get a host record

        # a super user can see the variables attached to a host

        # a org admin can see the variables attached to a host

        # a user who is on a team who has read permissions on an inventory can see the variables attached to a host

        # a regular user cannot see variables attached to a host

        # a super user can see the children attached to a group

        # a org admin can see the children attached to a group

        # a user who is on a team who has read permissions on an inventory can see the children attached to a group
      
        # a regular user cannot see children attached to a group

        # a super user can see a variable record

        # an org admin can see a variable record

        # a user who is on a team who has read permissions on an inventory can see the variable record
      
        # a regular user cannot see a variable record

        # a super user can disassociate...

        #    hosts from inventory

        #    groups from inventory

        #    subgroups from groups

        # the inventory task code returns valid inventory JSON.

        # an org admin user can disassociate...

        #    hosts from inventory

        #    groups from inventory

        #    subgroups from groups

        # a user with inventory edit permission disassociate...

        #    hosts from inventory

        #    groups from inventory

        #    subgroups from groups
      
        # a regular user cannot disassociate....

        #    hosts from inventory

        #    groups from inventory

        #    subgroups from inventory

        # the following objects can be tagged

        #    inventory

        #    host records

        #    group records

        #    variable records

        # the following objects can have their tags listed

        #    inventory

        #    host records

        #    group records

        #    variable records

        # the following tags can be removed

        #    inventory

        #    host records

        #    group records

        #    variable records

        #  on an inventory resource, I can see related resources for hosts and groups and permissions
        #  and these work 

        #  on a host resource, I can see related resources variables and inventories
        #  and these work

        #  on a group resource, I can see related resources for variables, inventories, and children
        #  and these work
                
    

       

