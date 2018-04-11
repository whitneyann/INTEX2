from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Group, Permission, ContentType
import cuser

class UserModelTest(TestCase):

    fixtures = ['cData.json']

    def setUp(self):
        self.u1 = amod.User.objects.get(email='sage@roney.com')
        self.u1.set_password('password')
        self.assertTrue(self.u1.is_authenticated)
        self.u1.save()
        # self.u1 = amod.User()
        # self.u1.first_name = 'Marge'
        # self.u1.last_name = 'Simpson'
        # self.u1.email = 'marge@simpsons.com'
        # self.u1.set_password('password')
        # self.u1.address = '123 Street'
        # self.u1.city = 'Hometown'
        # self.u1.state = 'WY'
        # self.u1.birthdate = '1995-04-15'
        # self.u1.save()

    def test_user_create_save_load(self):
        '''Test round trip of user model data to/from database'''
        u2 = amod.User.objects.get(email='sage@roney.com') #instead of marge@simpsons.com you can put u1.email
        self.assertEquals(self.u1.first_name, u2.first_name)
        self.assertEquals(self.u1.last_name, u2.last_name)
        self.assertEquals(self.u1.email, u2.email)
        self.assertEquals(self.u1.password, u2.password)
        self.assertTrue(u2.check_password('password'))


    def test_add_group_check_group_permissions(self):
        '''Add permissions to a group and check permissions'''
        # for p in Permission.objects.all():
        #     print(p.codename)
        p1 = Permission()
        p1.name = 'Change product price'
        p1.codename = 'change_product_price'
        ct1 = ContentType.objects.get(id=1) #pulling an object here
        p1.content_type = ct1
        p1.save()
        g1 = Group()
        g1.name = 'Test Group'
        g1.save()
        g1.permissions.add(p1)
        g1.save()
        self.u1.groups.add(g1)
        self.u1.has_perm('account.change_product_price')

        #self.u1.user_permissions.add(Permission.objects.get('...'))

    def test_add_check_user_permissions(self):
        '''Check user permissions'''
        p1 = Permission()
        p1.name = 'Change product name'
        p1.codename = 'change_product_name'
        ct1 = ContentType.objects.get(id=1) #pulling an object here
        p1.content_type = ct1
        p1.save()
        self.u1.user_permissions.add(p1)
        self.u1.has_perm('change_product_name')


    def test_password(self):
        '''Test the Password'''
        self.u1.set_password('password')
        self.assertTrue(self.u1.check_password('password'))

    def test_regular_field_changes(self):
        '''Test regular field changes like firstname and lastname '''

        self.u1.first_name = 'Krista'
        self.u1.last_name = 'Tenney'
        self.u1.email = 'krista@tenney.com'
        self.u1.set_password('hello')
        self.u1.address = '4434 Ocean Way'
        self.u1.city = 'Temecula'
        self.u1.state = 'CA'
        self.u1.birthdate = '1994-08-15'

        self.assertFalse(self.u1.first_name == 'Marge')
        self.assertFalse(self.u1.last_name == 'Simpson')
        self.assertFalse(self.u1.email == 'marge@simpsons.com')
        self.assertFalse(self.u1.address == '123 Street')
        self.assertFalse(self.u1.city == 'Hometown')
        self.assertFalse(self.u1.state == 'WY')
        self.assertFalse(self.u1.birthdate == '1995-04-15')



