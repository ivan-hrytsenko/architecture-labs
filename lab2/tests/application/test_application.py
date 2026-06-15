import pytest
from src.domain.interfaces import UserRepository, ProductRepository
from src.domain.models import User, Product
from src.application.use_cases import RegisterUserUseCase, CreateProductUseCase
from src.domain.exceptions import InvariantViolationError, DomainError

class FakeUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.counter = 1

    def get_by_id(self, user_id: int):
        return self.users.get(user_id)

    def get_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def save(self, user: User):
        if not user.id:
            user.id = self.counter
            self.counter += 1
        self.users[user.id] = user
        return user

class FakeProductRepository(ProductRepository):
    def __init__(self):
        self.products = {}
        self.counter = 1

    def get_by_id(self, product_id: int):
        return self.products.get(product_id)

    def get_all(self):
        return list(self.products.values())

    def save(self, product: Product):
        if not product.id:
            product.id = self.counter
            self.counter += 1
        self.products[product.id] = product
        return product

def test_register_user_success():
    repo = FakeUserRepository()
    use_case = RegisterUserUseCase(repo)
    user = use_case.execute("customer1", "cust@example.com", "customer")
    assert user.id == 1
    assert repo.get_by_email("cust@example.com") is not None

def test_register_user_duplicate_email():
    repo = FakeUserRepository()
    use_case = RegisterUserUseCase(repo)
    use_case.execute("customer1", "cust@example.com", "customer")
    with pytest.raises(InvariantViolationError):
        use_case.execute("customer2", "cust@example.com", "customer")

def test_create_product_by_farmer():
    user_repo = FakeUserRepository()
    product_repo = FakeProductRepository()
    farmer = User(id=1, username="farmer1", email="f@ex.com", role="farmer")
    user_repo.save(farmer)
    
    use_case = CreateProductUseCase(product_repo, user_repo)
    product = use_case.execute("Apple", "Green", 5.0, 50, 1)
    assert product.id == 1
    assert product.farmer_id == 1

def test_create_product_by_non_farmer():
    user_repo = FakeUserRepository()
    product_repo = FakeProductRepository()
    customer = User(id=1, username="cust1", email="c@ex.com", role="customer")
    user_repo.save(customer)
    
    use_case = CreateProductUseCase(product_repo, user_repo)
    with pytest.raises(InvariantViolationError):
        use_case.execute("Apple", "Green", 5.0, 50, 1)