import factory
from django.contrib.auth.models import User
from tasks.models import Workspace  # Apne Workspace model ko import karein

# 1. User ke liye Factory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    
    # Password set karne ke liye
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password(extracted or 'password123')

# 2. Workspace ke liye Factory
class WorkspaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Workspace
    
    name = factory.Faker('company')
    description = factory.Faker('text')
    owner = factory.SubFactory(UserFactory)  # Yahan UserFactory ko as owner link kiya