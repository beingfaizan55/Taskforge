import pytest
from rest_framework.test import APIClient
# Niche apni factory imports check kar lein, agar user aur workspace factory bani hui hain toh unhe import karein
from tasks.tests.factories import UserFactory, WorkspaceFactory 

@pytest.mark.django_db
def test_create_project_authenticated():
    # 1. User banayein aur workspace bhi banayein (kyunki project workspace ka hissa hota hai)
    user = UserFactory()
    workspace = WorkspaceFactory(owner=user) 
    
    client = APIClient()
    client.force_authenticate(user=user)
    
    # 2. POST request mein workspace_id bhi lazmi dein
    response = client.post('/api/projects/', {
        'name': 'Pytest Project',
        'description': 'Automated testing works!',
        'workspace': workspace.id # Workspace ka relation diya
    })
    
    # 3. Assertion check karein
    assert response.status_code == 201