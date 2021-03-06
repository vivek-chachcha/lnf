from django.test import TestCase, RequestFactory, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.http import urlquote
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from . models import Post, Comment
from . views import importDataStart, parseData

class ParsingTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        
        self.data = [
            {
            "json_featuretype":"LostAnimals"
            ,"Date":"2015-01-02"
            ,"Breed":"Pomeranian"
            ,"Sex":"M"
            ,"State":"Lost"
            ,"DateCreated":"2015-01-02"
            ,"Name":"Tito"
            ,"Color":"Cream"
            }
            ,{
            "json_featuretype":"LostAnimals"
            ,"Date":"2015-01-02"
            ,"Breed":"Pomeranian"
            ,"Sex":"M"
            ,"State":"Lost"
            ,"DateCreated":"2015-01-02"
            ,"Name":"Chico"
            ,"Color":"Brown"
            }
            ,{
            "json_featuretype":"LostAnimals"
            ,"Date":"2015-01-02"
            ,"Breed":"Tabby"
            ,"Sex":"M/N"
            ,"State":"Lost"
            ,"DateCreated":"2015-01-02"
            ,"Name":"Rascal"
            ,"Color":"White"
            }
            ,{
            "json_featuretype":"LostAnimals"
            ,"Date":"2015-01-02"
            ,"Breed":"Husky X"
            ,"Sex":"M"
            ,"State":"Lost"
            ,"DateCreated":"2015-01-02"
            ,"Name":"Rae"
            ,"Color":"White"
            }]

    def test_import_data_start_json_load_success(self):
        request = self.factory.get('/admin/startimport')

        response = importDataStart(request)
        self.assertEqual(response.status_code, 302)
        
    def test_parse_data_no_duplicate_entries(self):
        data = self.data
        parseData(data)
        entry = Post.objects.get(pk=4)
        self.assertEqual(entry.name, "Rae")
        
        duplicateEntry = [{
            "json_featuretype":"LostAnimals"
            ,"Date":"2015-01-02"
            ,"Breed":"Husky X"
            ,"Sex":"M"
            ,"State":"Lost"
            ,"DateCreated":"2015-01-02"
            ,"Name":"Rae"
            ,"Color":"White"
            }]
        
        parseData(duplicateEntry)
        
        entry = Post.objects.get(date = "2015-01-02", colour = "White", breed = "Husky X", name = "Rae")
        self.assertEqual(entry.id, 4)
    
    def test_parse_data_new_entry_success(self):
        data = self.data
        parseData(data)
        
        # test for new female, and lost state
        newEntry = [{
            "json_featuretype":"LostAnimals"
            ,"Date":"2015-11-18"
            ,"Breed":"Catfish"
            ,"Sex":"F"
            ,"State":"Lost"
            ,"DateCreated":"2015-11-19"
            ,"Name":"Bob"
            ,"Color":"Yellow"
            }]
        parseData(newEntry)
        entry = Post.objects.get(date = "2015-11-18", colour = "Yellow", breed = "Catfish", name = "Bob")
        self.assertEqual(entry.sex, "F")
        self.assertEqual(entry.state, '0')
        self.assertEqual(entry.id, 5)
        
        # test for new male, and found state
        newEntry = [{
            "json_featuretype":"LostAnimals"
            ,"Date":"2015-11-18"
            ,"Breed":"Fish"
            ,"Sex":"M"
            ,"State":"Found"
            ,"DateCreated":"2015-11-19"
            ,"Name":"Ann"
            ,"Color":"Black"
            }]
        
        parseData(newEntry)
        
        entry = Post.objects.get(date = "2015-11-18", colour = "Black", breed = "Fish", name = "Ann")
        self.assertEqual(entry.sex, "M")
        self.assertEqual(entry.state, '1')
        self.assertEqual(entry.id, 6)
        
        # test for new unknown gender
        newEntry = [{
            "json_featuretype":"LostAnimals"
            ,"Date":"2015-11-18"
            ,"Breed":"Goldfish"
            ,"Sex":"X"
            ,"State":"Found"
            ,"DateCreated":"2015-11-19"
            ,"Name":"Tree"
            ,"Color":"Green"
            }]
        
        parseData(newEntry)
        
        entry = Post.objects.get(date = "2015-11-18", colour = "Green", breed = "Goldfish", name = "Tree")
        self.assertEqual(entry.sex, "X")
        self.assertEqual(entry.state, '1')
        self.assertEqual(entry.id, 7)

    def test_parse_data_no_old_entries(self):
        data = self.data
        parseData(data)
        
        # test that old entries (year = 2010) is not in db
        newEntry = [{
            "json_featuretype":"LostAnimals"
            ,"Date":"2010-11-18"
            ,"Breed":"Dog"
            ,"Sex":"F"
            ,"State":"Lost"
            ,"DateCreated":"2010-11-19"
            ,"Name":"Violet"
            ,"Color":"Purple"
            }]
        parseData(newEntry)
        try:
            entry = Post.objects.get(date = "2010-11-18", colour = "Purple", breed = "Dog", name = "Violet")
            exist = True
        except Post.DoesNotExist:
            exist = False
        
        self.assertEqual(exist, False)
        
        # test that old entries (year < 2010) is not in db
        newEntry = [{
            "json_featuretype":"LostAnimals"
            ,"Date":"2001-11-18"
            ,"Breed":"Dog"
            ,"Sex":"F"
            ,"State":"Lost"
            ,"DateCreated":"2001-11-19"
            ,"Name":"Violet"
            ,"Color":"Purple"
            }]
        parseData(newEntry)
        try:
            entry = Post.objects.get(date = "2001-11-18", colour = "Purple", breed = "Dog", name = "Violet")
            exist = True
        except Post.DoesNotExist:
            exist = False
        
        self.assertEqual(exist, False)
   
        # test that old entries (year < 2010) is not in db
        newEntry = [{
            "json_featuretype":"LostAnimals"
            ,"Date":"2010-11-18"
            ,"Breed":"Dog"
            ,"Sex":"F"
            ,"State":"Lost"
            ,"DateCreated":"2010-11-19"
            ,"Name":"Violet"
            ,"Color":"Purple"
            }]
        parseData(newEntry)
        try:
            entry = Post.objects.get(date = "2015-11-18", colour = "Purple", breed = "Dog", name = "Violet")
            exist = True
        except Post.DoesNotExist:
            exist = False
        
        self.assertEqual(exist, False)        
        
class NavigationBarTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        
        # create a new user and superuser
        User.objects.create_user(first_name = "FirstName", last_name = "LastName", username = "user1", email = "user@test.com", password = "user")
        User.objects.create_superuser('admin', 'admin@test.com', 'adminpw')
        
        super(NavigationBarTestCase, self).setUp()

    def tearDown(self):
        self.selenium.refresh()
        self.selenium.quit()
        super(NavigationBarTestCase, self).tearDown()

    def test_all_links_in_navigation_bar(self):
        # start at home page
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "")
        )
       
        self.assertIn("Home Page", self.selenium.title)
        
        # test about page
        self.selenium.find_element_by_link_text('About').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("About Page", self.selenium.title)
        
        # test lost posts page
        self.selenium.find_element_by_link_text('Lost Pets').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Lost Posts", self.selenium.title)
        
        # test found posts page
        self.selenium.find_element_by_link_text('Found Pets').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Found Posts", self.selenium.title)
        
        # test signup page
        self.selenium.find_element_by_link_text('Sign Up').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Sign Up", self.selenium.title)
        
        # test login page
        self.selenium.find_element_by_link_text('Login').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Login", self.selenium.title)
        
        # login
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("user1")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("user") 
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.selenium.implicitly_wait(1)
        
        # test profile page
        self.selenium.find_element_by_link_text('Profile').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Profile", self.selenium.title)
        
        # test create post page
        self.selenium.find_element_by_link_text('Create Post').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Create Post", self.selenium.title)
        
        # test logout page
        self.selenium.find_element_by_link_text('Logout').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Login", self.selenium.title)
        
class FoundPostsBasicTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        
        # create a new user and superuser
        User.objects.create_user(first_name = "FirstName", last_name = "LastName", username = "user1", email = "user@test.com", password = "user")
        User.objects.create_superuser('admin', 'admin@test.com', 'adminpw')
        
        # create found posts
        Post.objects.create(lat = "49.26162189999999", lon = "-123.138122", address = "1480 W 11th Avenue Vancouver, BC", author = "", name = "Boop", breed = "Fish", colour = "Yellow", description = "", date_created = timezone.now(), date = "2014-12-10", modified_date = timezone.now(), sex = "M", picture = "", state = "1")
        Post.objects.create(lat = None, lon = None, address = None, author = "", name = "Beep", breed = "Dog", colour = "Purple", description = "", date_created = timezone.now(), date = "2015-01-16", modified_date = timezone.now(), sex = "F", picture = "", state = "1")
       
        super(FoundPostsBasicTestCase, self).setUp()

    def tearDown(self):
        self.selenium.refresh()
        self.selenium.quit()
        super(FoundPostsBasicTestCase, self).tearDown()

    def test_switch_list_and_map(self):
        # go to found post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/list")
        )
       
        # list view
        self.assertIn("Found Posts", self.selenium.title)
        self.assertIn("LIST VIEW", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertIn("Fish", self.selenium.page_source)
        self.assertIn("Yellow", self.selenium.page_source)
        self.assertIn("Dec. 10, 2014", self.selenium.page_source)
        self.assertIn("Male", self.selenium.page_source)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Dog", self.selenium.page_source)
        self.assertIn("Purple", self.selenium.page_source)
        self.assertIn("Jan. 16, 2015", self.selenium.page_source)
        self.assertIn("Female", self.selenium.page_source)
        
        # switch to map view
        self.selenium.find_element_by_link_text('MAP VIEW').click()
        self.selenium.implicitly_wait(2)
        
        self.assertIn("Found Posts", self.selenium.title)
        self.assertIn("LIST VIEW", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertIn("Fish", self.selenium.page_source)
        self.assertIn("Yellow", self.selenium.page_source)
        self.assertIn("Dec. 10, 2014", self.selenium.page_source)
        self.assertIn("Male", self.selenium.page_source)
        
        # assert Beep is not present in map view
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Beep")]'))
        
class LostPostsBasicTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        
        # create a new user and superuser
        User.objects.create_user(first_name = "FirstName", last_name = "LastName", username = "user1", email = "user@test.com", password = "user")
        User.objects.create_superuser('admin', 'admin@test.com', 'adminpw')
        
        # create lost posts
        Post.objects.create(lat = "49.26162189999999", lon = "-123.138122", address = "1480 W 11th Avenue Vancouver, BC", author = "", name = "Boop", breed = "Fish", colour = "Yellow", description = "", date_created = timezone.now(), date = "2014-12-10", modified_date = timezone.now(), sex = "M", picture = "", state = "0")
        Post.objects.create(lat = None, lon = None, address = None, author = "", name = "Beep", breed = "Dog", colour = "Purple", description = "", date_created = timezone.now(), date = "2015-01-16", modified_date = timezone.now(), sex = "F", picture = "", state = "0")
       
        super(LostPostsBasicTestCase, self).setUp()

    def tearDown(self):
        self.selenium.refresh()
        self.selenium.quit()
        super(LostPostsBasicTestCase, self).tearDown()

    def test_switch_list_and_map(self):
        # go to lost post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/list")
        )
       
        # list view
        self.assertIn("Lost Posts", self.selenium.title)
        self.assertIn("LIST VIEW", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertIn("Fish", self.selenium.page_source)
        self.assertIn("Yellow", self.selenium.page_source)
        self.assertIn("Dec. 10, 2014", self.selenium.page_source)
        self.assertIn("Male", self.selenium.page_source)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Dog", self.selenium.page_source)
        self.assertIn("Purple", self.selenium.page_source)
        self.assertIn("Jan. 16, 2015", self.selenium.page_source)
        self.assertIn("Female", self.selenium.page_source)
        
        # switch to map view
        self.selenium.find_element_by_link_text('MAP VIEW').click()
        self.selenium.implicitly_wait(2)
        
        self.assertIn("Lost Posts", self.selenium.title)
        self.assertIn("LIST VIEW", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertIn("Fish", self.selenium.page_source)
        self.assertIn("Yellow", self.selenium.page_source)
        self.assertIn("Dec. 10, 2014", self.selenium.page_source)
        self.assertIn("Male", self.selenium.page_source)
        
        # assert Beep is not present in map view
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Beep")]'))          

class FoundPostsSortFilterTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        
        # create a new user and superuser
        User.objects.create_user(first_name = "FirstName", last_name = "LastName", username = "user1", email = "user@test.com", password = "user")
        User.objects.create_superuser('admin', 'admin@test.com', 'adminpw')
        
        # create found posts
        Post.objects.create(lat = "49.26162189999999", lon = "-123.138122", address = "1480 W 11th Avenue Vancouver, BC", author = "", name = "Boop", breed = "Fish", colour = "Yellow", description = "", date_created = timezone.now(), date = "2014-12-10", modified_date = timezone.now(), sex = "M", picture = "", state = "1")
        Post.objects.create(lat = None, lon = None, address = None, author = "", name = "Yip", breed = "Cat", colour = "Purple", description = "", date_created = timezone.now(), date = "2013-03-13", modified_date = timezone.now(), sex = "F", picture = "", state = "1")
        Post.objects.create(lat = "49.282903", lon = "-123.110590", address = "322 W Hastings Street Vancouver, BC", author = "", name = "Beep", breed = "Tiger", colour = "White", description = "", date_created = timezone.now(), date = "2014-01-16", modified_date = timezone.now(), sex = "X", picture = "", state = "1")
        Post.objects.create(lat = "49.238553", lon = "-123.065197", address = "5052 Victoria Drive Vancouver, BC", author = "", name = "Candy", breed = "Dog", colour = "Red", description = "", date_created = timezone.now(), date = "2015-06-25", modified_date = timezone.now(), sex = "M/N", picture = "", state = "1")
       
        super(FoundPostsSortFilterTestCase, self).setUp()

    def tearDown(self):
        self.selenium.refresh()
        self.selenium.quit()
        super(FoundPostsSortFilterTestCase, self).tearDown()
        
    def test_sort_list_view(self):
        # go to found post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/list")
        )
        self.assertIn("Found Posts", self.selenium.title)
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        row3 = rows + "[3]"
        row4 = rows + "[4]"
        
        # name sort ascending
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)
        
        # name sort descending
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Beep", order4.text)  

        # date sort ascending
        self.selenium.find_element_by_xpath('//input[@value="DATE"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Candy", order4.text)
        
        # date sort descending
        self.selenium.find_element_by_xpath('//input[@value="DATE"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)

        # color sort ascending
        self.selenium.find_element_by_xpath('//input[@value="COLOUR"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Boop", order4.text)
        
        # color sort descending
        self.selenium.find_element_by_xpath('//input[@value="COLOUR"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)

        # breed sort ascending
        self.selenium.find_element_by_xpath('//input[@value="BREED"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Beep", order4.text)
        
        # breed sort descending
        self.selenium.find_element_by_xpath('//input[@value="BREED"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)

        # sex sort ascending
        self.selenium.find_element_by_xpath('//input[@value="SEX"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Beep", order4.text)
        
        # sex sort descending
        self.selenium.find_element_by_xpath('//input[@value="SEX"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)
           
    def test_sort_map_view(self):
        # go to found post map view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/map")
        )
        self.assertIn("Found Posts", self.selenium.title)
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        row3 = rows + "[3]"
        
        # name sort ascending
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        
        # name sort descending
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)

        # date sort ascending
        self.selenium.find_element_by_xpath('//input[@value="DATE"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        
        # date sort descending
        self.selenium.find_element_by_xpath('//input[@value="DATE"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)

        # color sort ascending
        self.selenium.find_element_by_xpath('//input[@value="COLOUR"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        
        # color sort descending
        self.selenium.find_element_by_xpath('//input[@value="COLOUR"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)

        # breed sort ascending
        self.selenium.find_element_by_xpath('//input[@value="BREED"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)
        
        # breed sort descending
        self.selenium.find_element_by_xpath('//input[@value="BREED"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)

        # sex sort ascending
        self.selenium.find_element_by_xpath('//input[@value="SEX"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)
        
        # sex sort descending
        self.selenium.find_element_by_xpath('//input[@value="SEX"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        
    def test_filter_list_view(self):
        # go to found post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/list")
        )
        self.assertIn("Found Posts", self.selenium.title)
        
        # name filter
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # date filter 
        date = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date.send_keys("2013-03-13")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Yip", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Beep")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        date1 = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date1.send_keys("2014-01-01")
        date2 = self.selenium.find_element_by_xpath("//input[@name='date2']")
        date2.send_keys("2015-01-30")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # color filter
        color = self.selenium.find_element_by_xpath("//input[@name='colour']")
        color.send_keys("red")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Candy", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Beep")]'))         
       
        # breed filter
        breed = self.selenium.find_element_by_xpath("//input[@name='breed']")
        breed.send_keys("tiger")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))         
       
        # sex filter  
        self.selenium.find_element_by_xpath("//select[@name='sex']").click()
        self.selenium.find_element_by_xpath("//option[@value='X']").click()
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))         

    def test_filter_map_view(self):
        # go to found post map view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/map")
        )
        self.assertIn("Found Posts", self.selenium.title)
        
        # name filter
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # date filter 
        date = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date.send_keys("2014-01-16")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        date1 = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date1.send_keys("2014-01-01")
        date2 = self.selenium.find_element_by_xpath("//input[@name='date2']")
        date2.send_keys("2015-01-30")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # color filter
        color = self.selenium.find_element_by_xpath("//input[@name='colour']")
        color.send_keys("red")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Candy", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Beep")]'))         
       
        # breed filter
        breed = self.selenium.find_element_by_xpath("//input[@name='breed']")
        breed.send_keys("tiger")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))         
       
        # sex filter  
        self.selenium.find_element_by_xpath("//select[@name='sex']").click()
        self.selenium.find_element_by_xpath("//option[@value='X']").click()
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))         

    def test_sort_and_filter_list_view(self):
        # go to found post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/list")
        )
        self.assertIn("Found Posts", self.selenium.title)
        
        # filter first
        date1 = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date1.send_keys("2014-01-01")
        date2 = self.selenium.find_element_by_xpath("//input[@name='date2']")
        date2.send_keys("2015-01-30")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # make sure sort still works
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
    
    def test_sort_and_filter_map_view(self):
        # go to found post map view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/map")
        )
        self.assertIn("Found Posts", self.selenium.title)
        
        # filter first
        date1 = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date1.send_keys("2014-01-01")
        date2 = self.selenium.find_element_by_xpath("//input[@name='date2']")
        date2.send_keys("2015-01-30")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # make sure sort still works
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)    
        
    def test_sort_switch_view(self):
        # go to found post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/list")
        )
        self.assertIn("Found Posts", self.selenium.title)
         
        # sort
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        row3 = rows + "[3]"
        row4 = rows + "[4]"
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)
        
        # switch views
        self.selenium.find_element_by_link_text("MAP VIEW").click()
        self.selenium.implicitly_wait(2)
        
        # make sure order persists
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
              
    def test_filter_switch_view(self):
        # go to found post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/list")
        )
        self.assertIn("Found Posts", self.selenium.title)
         
        # filter
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # switch views
        self.selenium.find_element_by_link_text("MAP VIEW").click()
        self.selenium.implicitly_wait(2)
        
        # make sure filter persists
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
    def test_reset_filter(self):
     # go to found post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/foundposts/list")
        )
        self.assertIn("Found Posts", self.selenium.title)
         
        # filter in list view
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        self.selenium.find_element_by_xpath("//input[@name='reset']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertIn("Candy", self.selenium.page_source)
        self.assertIn("Yip", self.selenium.page_source)
        
        # switch views
        self.selenium.find_element_by_link_text("MAP VIEW").click()
        self.selenium.implicitly_wait(2)
        
        # filter in map view
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        self.selenium.find_element_by_xpath("//input[@name='reset']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertIn("Candy", self.selenium.page_source)
        
class LostPostsSortFilterTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        
        # create a new user and superuser
        User.objects.create_user(first_name = "FirstName", last_name = "LastName", username = "user1", email = "user@test.com", password = "user")
        User.objects.create_superuser('admin', 'admin@test.com', 'adminpw')
        
        # create lost posts
        Post.objects.create(lat = "49.26162189999999", lon = "-123.138122", address = "1480 W 11th Avenue Vancouver, BC", author = "", name = "Boop", breed = "Fish", colour = "Yellow", description = "", date_created = timezone.now(), date = "2014-12-10", modified_date = timezone.now(), sex = "M", picture = "", state = "0")
        Post.objects.create(lat = None, lon = None, address = None, author = "", name = "Yip", breed = "Cat", colour = "Purple", description = "", date_created = timezone.now(), date = "2013-03-13", modified_date = timezone.now(), sex = "F", picture = "", state = "0")
        Post.objects.create(lat = "49.282903", lon = "-123.110590", address = "322 W Hastings Street Vancouver, BC", author = "", name = "Beep", breed = "Tiger", colour = "White", description = "", date_created = timezone.now(), date = "2014-01-16", modified_date = timezone.now(), sex = "X", picture = "", state = "0")
        Post.objects.create(lat = "49.238553", lon = "-123.065197", address = "5052 Victoria Drive Vancouver, BC", author = "", name = "Candy", breed = "Dog", colour = "Red", description = "", date_created = timezone.now(), date = "2015-06-25", modified_date = timezone.now(), sex = "M/N", picture = "", state = "0")
       
        super(LostPostsSortFilterTestCase, self).setUp()

    def tearDown(self):
        self.selenium.refresh()
        self.selenium.quit()
        super(LostPostsSortFilterTestCase, self).tearDown()
        
    def test_sort_list_view(self):
        # go to lost post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/list")
        )
        self.assertIn("Lost Posts", self.selenium.title)
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        row3 = rows + "[3]"
        row4 = rows + "[4]"
        
        # name sort ascending
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)
        
        # name sort descending
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Beep", order4.text)  

        # date sort ascending
        self.selenium.find_element_by_xpath('//input[@value="DATE"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Candy", order4.text)
        
        # date sort descending
        self.selenium.find_element_by_xpath('//input[@value="DATE"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)

        # color sort ascending
        self.selenium.find_element_by_xpath('//input[@value="COLOUR"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Boop", order4.text)
        
        # color sort descending
        self.selenium.find_element_by_xpath('//input[@value="COLOUR"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)

        # breed sort ascending
        self.selenium.find_element_by_xpath('//input[@value="BREED"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Beep", order4.text)
        
        # breed sort descending
        self.selenium.find_element_by_xpath('//input[@value="BREED"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)

        # sex sort ascending
        self.selenium.find_element_by_xpath('//input[@value="SEX"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Yip", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Beep", order4.text)
        
        # sex sort descending
        self.selenium.find_element_by_xpath('//input[@value="SEX"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)
           
    def test_sort_map_view(self):
        # go to lost post map view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/map")
        )
        self.assertIn("Lost Posts", self.selenium.title)
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        row3 = rows + "[3]"
        
        # name sort ascending
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        
        # name sort descending
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)

        # date sort ascending
        self.selenium.find_element_by_xpath('//input[@value="DATE"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        
        # date sort descending
        self.selenium.find_element_by_xpath('//input[@value="DATE"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)

        # color sort ascending
        self.selenium.find_element_by_xpath('//input[@value="COLOUR"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        
        # color sort descending
        self.selenium.find_element_by_xpath('//input[@value="COLOUR"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)

        # breed sort ascending
        self.selenium.find_element_by_xpath('//input[@value="BREED"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Candy", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)
        
        # breed sort descending
        self.selenium.find_element_by_xpath('//input[@value="BREED"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)

        # sex sort ascending
        self.selenium.find_element_by_xpath('//input[@value="SEX"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Beep", order3.text)
        
        # sex sort descending
        self.selenium.find_element_by_xpath('//input[@value="SEX"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Candy", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Boop", order3.text)
        
    def test_filter_list_view(self):
        # go to lost post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/list")
        )
        self.assertIn("Lost Posts", self.selenium.title)
        
        # name filter
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # date filter 
        date = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date.send_keys("2013-03-13")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Yip", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Beep")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        date1 = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date1.send_keys("2014-01-01")
        date2 = self.selenium.find_element_by_xpath("//input[@name='date2']")
        date2.send_keys("2015-01-30")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # color filter
        color = self.selenium.find_element_by_xpath("//input[@name='colour']")
        color.send_keys("red")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Candy", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Beep")]'))         
       
        # breed filter
        breed = self.selenium.find_element_by_xpath("//input[@name='breed']")
        breed.send_keys("tiger")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))         
       
        # sex filter  
        self.selenium.find_element_by_xpath("//select[@name='sex']").click()
        self.selenium.find_element_by_xpath("//option[@value='X']").click()
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))         

    def test_filter_map_view(self):
        # go to lost post map view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/map")
        )
        self.assertIn("Lost Posts", self.selenium.title)
        
        # name filter
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # date filter 
        date = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date.send_keys("2014-01-16")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        date1 = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date1.send_keys("2014-01-01")
        date2 = self.selenium.find_element_by_xpath("//input[@name='date2']")
        date2.send_keys("2015-01-30")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # color filter
        color = self.selenium.find_element_by_xpath("//input[@name='colour']")
        color.send_keys("red")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Candy", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Beep")]'))         
       
        # breed filter
        breed = self.selenium.find_element_by_xpath("//input[@name='breed']")
        breed.send_keys("tiger")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))         
       
        # sex filter  
        self.selenium.find_element_by_xpath("//select[@name='sex']").click()
        self.selenium.find_element_by_xpath("//option[@value='X']").click()
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))         

    def test_sort_and_filter_list_view(self):
        # go to lost post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/list")
        )
        self.assertIn("Lost Posts", self.selenium.title)
        
        # filter first
        date1 = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date1.send_keys("2014-01-01")
        date2 = self.selenium.find_element_by_xpath("//input[@name='date2']")
        date2.send_keys("2015-01-30")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # make sure sort still works
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)
    
    def test_sort_and_filter_map_view(self):
        # go to lost post map view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/map")
        )
        self.assertIn("Lost Posts", self.selenium.title)
        
        # filter first
        date1 = self.selenium.find_element_by_xpath("//input[@name='date1']")
        date1.send_keys("2014-01-01")
        date2 = self.selenium.find_element_by_xpath("//input[@name='date2']")
        date2.send_keys("2015-01-30")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # make sure sort still works
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Boop", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Beep", order2.text)    
        
    def test_sort_switch_view(self):
        # go to lost post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/list")
        )
        self.assertIn("Lost Posts", self.selenium.title)
         
        # sort
        rows = "(//div[@class='row'])"
        row1 = rows + "[1]"
        row2 = rows + "[2]"
        row3 = rows + "[3]"
        row4 = rows + "[4]"
        self.selenium.find_element_by_xpath('//input[@value="NAME"]').click()
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
        order4 = self.selenium.find_element_by_xpath(row4)
        self.assertIn("Yip", order4.text)
        
        # switch views
        self.selenium.find_element_by_link_text("MAP VIEW").click()
        self.selenium.implicitly_wait(2)
        
        # make sure order persists
        order1 = self.selenium.find_element_by_xpath(row1)
        self.assertIn("Beep", order1.text)
        order2 = self.selenium.find_element_by_xpath(row2)
        self.assertIn("Boop", order2.text)
        order3 = self.selenium.find_element_by_xpath(row3)
        self.assertIn("Candy", order3.text)
              
    def test_filter_switch_view(self):
        # go to lost post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/list")
        )
        self.assertIn("Lost Posts", self.selenium.title)
         
        # filter
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
        # switch views
        self.selenium.find_element_by_link_text("MAP VIEW").click()
        self.selenium.implicitly_wait(2)
        
        # make sure filter persists
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        
    def test_reset_filter(self):
     # go to lost post list view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/lostposts/list")
        )
        self.assertIn("Lost Posts", self.selenium.title)
         
        # filter in list view
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Yip")]'))  
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        self.selenium.find_element_by_xpath("//input[@name='reset']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertIn("Candy", self.selenium.page_source)
        self.assertIn("Yip", self.selenium.page_source)
        
        # switch views
        self.selenium.find_element_by_link_text("MAP VIEW").click()
        self.selenium.implicitly_wait(2)
        
        # filter in map view
        name = self.selenium.find_element_by_xpath("//input[@name='name']")
        name.send_keys("beep")
        self.selenium.find_element_by_xpath("//input[@name='filter']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Boop")]')) 
        self.assertRaises(exceptions.NoSuchElementException, lambda: self.selenium.find_element_by_xpath('//div[contains(text(), "Candy")]'))     
        self.selenium.find_element_by_xpath("//input[@name='reset']").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Beep", self.selenium.page_source)
        self.assertIn("Boop", self.selenium.page_source)
        self.assertIn("Candy", self.selenium.page_source)
        
class AdminViewTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        
        # create a new user and superuser
        User.objects.create_user(first_name = "FirstName", last_name = "LastName", username = "user1", email = "user@test.com", password = "user")
        User.objects.create_superuser('admin', 'admin@test.com', 'adminpw')
        
        super(AdminViewTestCase, self).setUp()

    def tearDown(self):
        self.selenium.refresh()
        self.selenium.quit()
        super(AdminViewTestCase, self).tearDown()
        
    def test_import_buttons_present(self):
        # go to admin view
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/admin/")
        )
        
        username = self.selenium.find_element_by_xpath("//input[@id='id_username']")
        username.send_keys("admin")
        pw = self.selenium.find_element_by_xpath("//input[@id='id_password']")
        pw.send_keys("adminpw")
        self.selenium.find_element_by_xpath("//input[@type='submit']").click()
        self.selenium.implicitly_wait(1)
        
        self.assertIn("Import Data", self.selenium.page_source)
        
        self.selenium.find_element_by_link_text("Import Data").click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Start Import", self.selenium.page_source)

class CreatePostTestCase(StaticLiveServerTestCase):
    reset_sequences = True
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(CreatePostTestCase, self).setUp()
        
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Lost")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Found")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("Lost")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("lnf@mail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("lnf")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("lnf")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
  
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )      
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("Lost")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("lnf")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

    def tearDown(self):
        # Call tearDown to close the web browser
        self.selenium.refresh()
        self.selenium.quit()
        super(CreatePostTestCase, self).tearDown()

    def test_create_post(self):
        # missing name error
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Create Post", self.selenium.title)
        
       # missing breed
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Create Post", self.selenium.title)
        
        # missing colour
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Create Post", self.selenium.title)
        
        # missing date
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Create Post", self.selenium.title)
        
        # wrong date format
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("alsdja")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Create Post", self.selenium.title)
        
        # date after current
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/20")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Create Post", self.selenium.title)
        
        # invalid address
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/20")
        self.selenium.find_element_by_id("id_address").send_keys("as23jawuw")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Create Post", self.selenium.title)
        
        # address far away
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/20")
        self.selenium.find_element_by_id("id_address").send_keys("350 5th Ave, New York, NY 10118, United States")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Create Post", self.selenium.title)
        
        # valid (minimal) inputs
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)
        
        # valid (minimal) inputs + description
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_id("id_description").send_keys("He was a cute dog")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)

        # valid (minimal) inputs + description + state dropdown
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_id("id_description").send_keys("He was a cute dog")
        self.selenium.find_element_by_xpath("//select[@id='id_state']/option[@value='1']").click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)

        # valid (minimal) inputs + description + state dropdown + sex dropbown
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_id("id_description").send_keys("He was a cute dog")
        self.selenium.find_element_by_xpath("//select[@id='id_state']/option[@value='1']").click()
        self.selenium.find_element_by_xpath("//select[@id='id_sex']/option[@value='F']").click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)
        
        # valid (minimal) inputs + description + state dropdown + sex dropbown + address
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_id("id_description").send_keys("He was a cute dog")
        self.selenium.find_element_by_xpath("//select[@id='id_state']/option[@value='1']").click()
        self.selenium.find_element_by_xpath("//select[@id='id_sex']/option[@value='F']").click()
        self.selenium.find_element_by_id("id_address").send_keys("2329 West Mall, Vancouver, BC V6T 1Z4")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)
       
class BookmarkPostTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(BookmarkPostTestCase, self).setUp()
        
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Lost")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Found")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("Lost")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("lnf@mail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("lnf")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("lnf")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
  
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )      
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("Lost")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("lnf")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()        

    def tearDown(self):
        # Call tearDown to close the web browser        
        self.selenium.refresh()
        self.selenium.quit()
        super(BookmarkPostTestCase, self).tearDown()

    def test_bookmark_post(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_id("id_description").send_keys("He was a cute dog")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)
        url1 = self.selenium.current_url

        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Kat")
        self.selenium.find_element_by_id("id_breed").send_keys("Cat")
        self.selenium.find_element_by_id("id_colour").send_keys("Black")
        self.selenium.find_element_by_id("id_date").send_keys("11/11/14")
        self.selenium.find_element_by_id("id_description").send_keys("She was a cute cat")
        self.selenium.find_element_by_xpath("//select[@id='id_state']/option[@value='1']").click()
        self.selenium.find_element_by_xpath("//select[@id='id_sex']/option[@value='F']").click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)
        url2 = self.selenium.current_url

        # bookmark 1st post
        self.selenium.get(
            '%s' % (url1)
        )   
        bm = self.selenium.find_element_by_id("id_bookmark")
        bm.click()
        self.selenium.find_element_by_xpath('//input[@value="OK"]').click()
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/bmposts/")
        )   
        self.assertIn("Doug", self.selenium.page_source)
        
        # bookmark 1st post again (bookmark time change)
        self.selenium.get(
            '%s' % (url1)
        )   
        self.selenium.find_element_by_xpath('//input[@value="OK"]').click()
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/bmposts/")
        )   
        self.assertIn("Doug", self.selenium.page_source)
        
        # bookmark 2nd post
        self.selenium.get(
            '%s' % (url2)
        )   
        bm = self.selenium.find_element_by_id("id_bookmark")
        bm.click()
        self.selenium.find_element_by_xpath('//input[@value="OK"]').click()
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/bmposts/")
        )   
        self.assertIn("Doug", self.selenium.page_source)
        self.assertIn("Kat", self.selenium.page_source)
        
        # unbookmark 1st post
        self.selenium.get(
            '%s' % (url1)
        )
        bm = self.selenium.find_element_by_id("id_bookmark")
        bm.click()        
        self.selenium.find_element_by_xpath('//input[@value="OK"]').click()      
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/bmposts/")
        )   
        self.assertNotIn("Doug", self.selenium.page_source)
        self.assertIn("Kat", self.selenium.page_source)
        
        # unbookmark 1st post again (do nothing)
        self.selenium.get(
            '%s' % (url1)
        )   
        self.selenium.find_element_by_xpath('//input[@value="OK"]').click()      
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/bmposts/")
        )   
        self.assertNotIn("Doug", self.selenium.page_source)
        self.assertIn("Kat", self.selenium.page_source)
        
        # unbookmark 2nd post
        self.selenium.get(
            '%s' % (url2)
        )   
        bm = self.selenium.find_element_by_id("id_bookmark")
        bm.click()
        self.selenium.find_element_by_xpath('//input[@value="OK"]').click()      
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/bmposts/")
        )   
        self.assertNotIn("Doug", self.selenium.page_source)
        self.assertNotIn("Kat", self.selenium.page_source)
        
class SharePostTestCase(StaticLiveServerTestCase):
    reset_sequences = True
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(SharePostTestCase, self).setUp()
        
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Lost")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Found")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("Lost")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("lnf@mail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("lnf")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("lnf")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
  
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )      
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("Lost")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("lnf")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()        

    def tearDown(self):
        # Call tearDown to close the web browser
        self.selenium.refresh()
        self.selenium.quit()
        super(SharePostTestCase, self).tearDown()

    def test_share_post(self):
        # create & share 1st post
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Doug")
        self.selenium.find_element_by_id("id_breed").send_keys("Bulldog")
        self.selenium.find_element_by_id("id_colour").send_keys("Brown")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_id("id_description").send_keys("He was a cute dog")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)

        # share link unique to 1st post
        self.assertIn(urlquote(self.selenium.current_url), self.selenium.find_element_by_xpath("//div[@class='facebook-this']/a").get_attribute('href'))
        self.selenium.find_element_by_xpath("//*[@class='facebook-this']").click()
        self.selenium.switch_to_window(self.selenium.window_handles[1])
        self.selenium.implicitly_wait(1)
        # share link leads to Facebook
        self.assertIn("Facebook", self.selenium.page_source)
        self.selenium.switch_to_window(self.selenium.window_handles[0])
       
       # create & share 2nd post
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Kat")
        self.selenium.find_element_by_id("id_breed").send_keys("Cat")
        self.selenium.find_element_by_id("id_colour").send_keys("Black")
        self.selenium.find_element_by_id("id_date").send_keys("11/11/14")
        self.selenium.find_element_by_id("id_description").send_keys("She was a cute cat")
        self.selenium.find_element_by_xpath("//select[@id='id_state']/option[@value='1']").click()
        self.selenium.find_element_by_xpath("//select[@id='id_sex']/option[@value='F']").click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)

        # share link unique to 2nd post
        self.assertIn(urlquote(self.selenium.current_url), self.selenium.find_element_by_xpath("//div[@class='facebook-this']/a").get_attribute('href'))
        self.selenium.find_element_by_xpath("//*[@class='facebook-this']").click()
        self.selenium.switch_to_window(self.selenium.window_handles[2])
        self.selenium.implicitly_wait(1)
        # share link leads to Facebook
        self.assertIn("Facebook", self.selenium.page_source)
        self.selenium.switch_to_window(self.selenium.window_handles[0])
		
class SignUpTestCase(StaticLiveServerTestCase):
    def setUp(self):
	    # instantiate the webdriver
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        User.objects.create_user(first_name = "Oreo", last_name = "Cookies", username = "exist", email = "test1@gmail.com", password = "pass1")
        super(SignUpTestCase, self).setUp()

    def tearDown(self):
        # close the web browser
        self.selenium.quit()
        super(SignUpTestCase, self).tearDown()
	
    def test_signup(self):
        # test symbols in first name
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Or3o")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Cookies")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("test1@gmail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass1")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass1")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
		
        # test symbols in last name
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Oreo")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("C@@ki35")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test2")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("test2@gmail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass2")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass2")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # test symbols in last name
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Oreo")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("C@@ki35")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test2")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("test2@gmail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass2")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass2")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # test username already exists
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Hershey")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Chocolate")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("exist")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("test2@gmail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass2")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass2")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # test invalid email
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Wizard")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Oz")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("test1@")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass1")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass1")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
		
        # test passwords not matching
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Wizard")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Oz")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("test1@")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass1")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass2")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # test not checking user agreement
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Wizard")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Oz")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("test1@gmail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass1")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass1")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
		
        # test not filling all mandatory fields
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
		
        # test correct signup
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Oreo")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Cookies")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("user")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("user@gmail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass1")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass1")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.selenium.implicitly_wait(1)
        self.assertIn("Login", self.selenium.title)
		
class LoginTestCase(StaticLiveServerTestCase):
    def setUp(self):
	    # instantiate the webdriver
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        # create a new user
        User.objects.create_user(first_name = "Oreo", last_name = "Cookies", username = "test1", email = "test1@gmail.com", password = "pass1")
        super(LoginTestCase, self).setUp()

    def tearDown(self):
        # close the web browser
        self.selenium.quit()
        super(LoginTestCase, self).tearDown()
	
    def test_login(self):
        # test username does not exist
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("notexist")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("pass1")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
		
        # test wrong password
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("wrong")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
		
        # test correct login
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("pass1")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Home Page", self.selenium.title)
		
class LogoutTestCase(StaticLiveServerTestCase):
    def setUp(self):
	    # instantiate the webdriver
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        # create a new user
        User.objects.create_user(first_name = "Oreo", last_name = "Cookies", username = "test1", email = "test1@gmail.com", password = "pass1")
        super(LogoutTestCase, self).setUp()

    def tearDown(self):
        # close the web browser
        self.selenium.quit()
        super(LogoutTestCase, self).tearDown()
		
    def test_logout(self):
        
		# login
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("pass1") 
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

		#test logout
        self.selenium.find_element_by_link_text('Logout').click()
        self.assertIn("Login", self.selenium.title)

class MyPostTestCase(StaticLiveServerTestCase):
    def setUp(self):
	    # instantiate the webdriver
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        
		# create new users
        User.objects.create_user(first_name = "Oreo", last_name = "Cookies", username = "test1", email = "test1@gmail.com", password = "pass1")
        User.objects.create_user(first_name = "Hershey", last_name = "Chocolate", username = "test2", email = "test2@gmail.com", password = "pass2")      
        
        # create posts		
        Post.objects.create(lat = None, lon = None, address = None, author = "test1", name = "Toad", breed = "Fish", colour = "Yellow", description = "", date_created = timezone.now(), date = "2014-12-10", modified_date = timezone.now(), sex = "M", picture = "", state = "0")
        Post.objects.create(lat = None, lon = None, address = None, author = "test1", name = "Cappa", breed = "Dog", colour = "Purple", description = "", date_created = timezone.now(), date = "2015-01-16", modified_date = timezone.now(), sex = "F", picture = "", state = "1")
        Post.objects.create(lat = None, lon = None, address = None, author = "test2", name = "Planet", breed = "Dog", colour = "Purple", description = "", date_created = timezone.now(), date = "2015-01-16", modified_date = timezone.now(), sex = "F", picture = "", state = "0")		
        super(MyPostTestCase, self).setUp()
		
    def tearDown(self):
        # close the web browser
        self.selenium.quit()
        super(MyPostTestCase, self).tearDown()

    def test_mypost(self):
        
	    # test test1 my posts
		# login
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("pass1") 
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # go to profile and click my posts
        self.selenium.find_element_by_link_text('Profile').click()
        self.selenium.find_element_by_link_text('My Posts').click()
        self.assertIn("My Posts", self.selenium.title)
        
        # assert posts created by test1 are there
        self.assertIn("Toad", self.selenium.page_source)
        self.assertIn("Cappa", self.selenium.page_source)
        self.assertNotIn("Planet", self.selenium.page_source)
		
        # logout
        self.selenium.find_element_by_link_text('Logout').click()
		
	    # test test2 my posts
		# login
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test2")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("pass2") 
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

        # go to profile and click my posts
        self.selenium.find_element_by_link_text('Profile').click()
        self.selenium.find_element_by_link_text('My Posts').click()
        self.assertIn("My Posts", self.selenium.title)
        
        # assert posts created by test1 are there
        self.assertIn("Planet", self.selenium.page_source)
        self.assertNotIn("Toad", self.selenium.page_source)
        self.assertNotIn("Cappa", self.selenium.page_source)
	
class CommentTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(CommentTestCase, self).setUp()
        
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/signup/")
        )
        firstname = self.selenium.find_element_by_id("id_firstname")
        firstname.send_keys("Oreo")
        lastname = self.selenium.find_element_by_id("id_lastname")
        lastname.send_keys("Cookies")
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("test1@gmail.com")
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys("pass1")
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys("pass1")
        user_agreement = self.selenium.find_element_by_id("id_user_agreement")
        user_agreement.click()
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
  
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/login/")
        )      
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("test1")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("pass1")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()        

    def tearDown(self):
        # Call tearDown to close the web browser
        self.selenium.quit()
        super(CommentTestCase, self).tearDown()

    def test_comment(self):
        #  create a post
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/createpost/")
        )                
        self.selenium.find_element_by_id("id_name").send_keys("Planet")
        self.selenium.find_element_by_id("id_breed").send_keys("Fish")
        self.selenium.find_element_by_id("id_colour").send_keys("Gold")
        self.selenium.find_element_by_id("id_date").send_keys("10/10/14")
        self.selenium.find_element_by_id("id_description").send_keys("Planet needs water.")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn("Details Page", self.selenium.title)
        url1 = self.selenium.current_url

        self.assertNotIn("Leave Comments", self.selenium.page_source)
        # test not filling in all mandatory fields
        self.selenium.find_element_by_id("id_last_known_location").send_keys("2424 Main Mall")
        self.selenium.find_element_by_id("id_text").send_keys("")	
        self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        self.assertNotIn("Oreo Cookies", self.selenium.page_source)
	
        # test adding a valid comment
        self.selenium.find_element_by_id("id_last_known_location").send_keys("2424 Main Mall")
        self.selenium.find_element_by_id("id_text").send_keys("It has been sunny for days, I think Planet is dead now.")	
        self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        self.assertIn("Oreo Cookies", self.selenium.page_source)
        self.assertIn("2424 Main Mall", self.selenium.page_source)
        self.assertIn("It has been sunny for days, I think Planet is dead now.", self.selenium.page_source)	