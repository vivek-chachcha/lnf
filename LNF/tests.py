from django.test import TestCase
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver

class CreatePostTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(CreatePostTestCase, self).setUp()

    def tearDown(self):
        # Call tearDown to close the web browser
        self.selenium.quit()
        super(CreatePostTestCase, self).tearDown()

    def test_create_post(self):
        """
        Django admin create user test
        This test will create a user in django admin and assert that
        page is redirected to the new user change form.
        """ 
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

