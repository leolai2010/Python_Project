from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def valdiate_info(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
            errors["first_name"] = "First Name cannot be Empty!"
        elif len(postData['first_name']) < 3:
            errors["first_name"] = "First Name Too Short!"
        if len(postData['last_name']) == 0:
            errors["last_name"] = "Last Name cannot be Empty!"
        elif len(postData['last_name']) < 3:
            errors["last_name"] = "Last Name Too Short!"
        if len(postData['user_email']) == 0:
            errors["user_email"] = "Email cannot be Empty!"
        elif not EMAIL_REGEX.match(postData['user_email']):
            errors["user_email"] = "Email Format Incorrect"
        else:
            users_with_same_email = self.filter(email=postData['user_email'])
            if len(users_with_same_email)>0:
                errors['email'] = 'Email is already taken!'
        if len(postData['password']) == 0:
            errors["password"] = "Password cannot be Empty!"
        elif len(postData['password']) < 8:
            errors["password"] = "Password Too Short!"
        if len(postData['password_conf']) == 0:
            errors["password_conf"] = "Password Confirmation cannot be Empty!"
        elif postData['password'] != postData['password_conf']:
            errors['password'] = 'Password Fields Must Match!'
        if len(errors):
            result = {
                'errors':errors 
            }
            return result
        else:
            hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
            info = self.create(
                first_name = postData['first_name'], 
                last_name = postData['last_name'], 
                email = postData['user_email'], 
                password = hashed_pw.decode('utf-8'),
            )
            result = {
                'infos':info
            }
            return result

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Body_system(models.Model):
    system_name = models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ailment(models.Model):
    condition = models.CharField(max_length=255)
    system_ailment = models.ForeignKey(Body_system,related_name='body_systems', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Herb(models.Model):
    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)  
    desc = models.TextField()
    picture = models.CharField(max_length=255)
    delivery_method = models.CharField(max_length=255) 
    price = models.IntegerField() 
    ailment_herbs = models.ManyToManyField(Ailment,related_name='herb_ailments')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class JobManager(models.Manager):
    def validate_info(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = 'Title cannot be Empty!'
        elif len(postData['title']) < 3:
            errors['title'] = 'Title is too Short! Need to be Three Characters or More!'
        if len(postData['description_txt']) == 0:
            errors['description_txt'] = 'Description cannot be Empty!'
        elif len(postData['description_txt']) < 10:
            errors['description_txt'] = 'Description is too Short! Need to be Ten Characters or More!'
        if len(errors):
            result = {
                'errors':errors
            }
            return result
        else:
            job = self.create(
                title = postData['title'], 
                desc = postData['description_txt'],
                created_by_id= postData['userid']
            )
            result = {
                'jobs':job
            }
            return result
    def validate_edit(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = 'Please Update Your Title!'
        elif len(postData['title']) < 3:
            errors['title'] = 'Title is too Short! Need to be Three Characters or More!'
        if len(postData['description_txt']) == 0:
            errors['description_txt'] = 'Description cannot be Empty!'
        elif len(postData['description_txt']) < 10:
            errors['description_txt'] = 'Description is too Short! Need to be Ten Characters or More!'
        if len(errors):
            return {'errors':errors}
        else:
            job = Job.objects.get(id=postData['jobid'])
            job.title = postData['title']
            job.desc = postData['description_txt']
            job.created_by_id = postData['userid']
            job.save()
            result = {
                'jobs':job
            }
            return result

class Job(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,related_name='users_job',on_delete=models.CASCADE)
    objects = JobManager()

class SolutionManager(models.Manager):
    def validate_info(self, postData):
        errors = {}
        if len(postData['description_txt']) == 0:
            errors['description_txt'] = 'Description cannot be Empty!'
        elif len(postData['description_txt']) < 10:
            errors['description_txt'] = 'Description is too Short! Need to be Ten Characters or More!'
        if len(errors):
            result = {
                'errors':errors
            }
            return result
        else:
            solution = self.create(
                desc = postData['description_txt'],
                jobs_solution_id = postData['jobid'],
                comment_by_id= postData['userid']
            )
            result = {
                'soultions': solution
            }
            return result
    def validate_edit(self, postData):
        errors = {}
        if len(postData['description_txt']) == 0:
            errors['description_txt'] = 'Description cannot be Empty!'
        elif len(postData['description_txt']) < 10:
            errors['description_txt'] = 'Description is too Short! Need to be Ten Characters or More!'
        if len(errors):
            result = {
                'errors':errors
            }
            return result
        else:
            solution = Solution.objects.get(id=postData['solid'])
            solution.desc = postData['description_txt']
            solution.save()
            result = {
                'solutions':solution
            }
            return result

class Solution(models.Model):
    desc=models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    jobs_solution = models.ForeignKey(Job,related_name='jobs',on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User,related_name='users_solution',on_delete=models.CASCADE)
    objects = SolutionManager()

class CartManager(models.Manager):
    def add_product(self, postData):
        print(postData)
        product = self.create(
            item_added_id = postData['herbid'],
            purchase_by_id = postData['userid']
        )
        result = {
            'products':product
        }
        return result

class Cart(models.Model):
    item_added = models.ForeignKey(Herb,related_name='herb_in_cart',on_delete=models.CASCADE)
    purchase_by = models.ForeignKey(User,related_name='users_purchase',on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CartManager()