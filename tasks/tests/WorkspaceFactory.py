import factory
from django.contrib.auth.models import User
from tasks.models import Workspace

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password(extracted or 'password123')

class WorkspaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Workspace
    
    name = factory.Faker('company')
    description = factory.Faker('text')
    owner = factory.SubFactory(UserFactory)