from django.test import TestCase, RequestFactory

from . models import Post
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