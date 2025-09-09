from app.core.configurations import settings
from app.core.container import Container
from app.domain.repositories.brand_repository import BrandRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.product_view_repository import ProductViewRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.notification_service import NotificationService
from app.domain.use_cases.brands.create.brand_create_use_case import BrandCreateUseCase
from app.domain.use_cases.products.create.product_create_use_case import (
    ProductCreateUseCase,
)
from app.domain.use_cases.products.detail.product_detail_use_case import (
    ProductDetailUseCase,
)
from app.domain.use_cases.products.edit.product_update_use_case import (
    ProductUpdateUseCase,
)
from app.domain.use_cases.products.remove.product_remove_use_case import (
    ProductRemoveUseCase,
)
from app.domain.use_cases.products.view_report.product_view_report_use_case import (
    ProductViewReportUseCase,
)
from app.domain.use_cases.users.create.user_create_use_case import UserCreateUseCase
from app.domain.use_cases.users.edit.user_update_use_case import UserUpdateUseCase
from app.domain.use_cases.users.login.login_use_case import LoginUseCase
from app.domain.use_cases.users.remove.user_remove_use_case import UserRemoveUseCase
from app.domain.use_cases.users.sig_up.sig_up_use_case import SigUpUseCase
from app.infrastructure.db.database_repository import DatabaseRepository
from app.infrastructure.persistence.postgres_brand_repository import (
    PostgresBrandRepository,
)
from app.infrastructure.persistence.postgres_product_repository import (
    PostgresProductRepository,
)
from app.infrastructure.persistence.postgres_product_view_repository import (
    PostgresProductViewRepository,
)
from app.infrastructure.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.service.aws_ses_service import AwsSESNotificationService

container = Container()

# Repositories
container[UserRepository] = lambda _: PostgresUserRepository(
    database_repository=DatabaseRepository(),
)
container[ProductRepository] = lambda _: PostgresProductRepository(
    database_repository=DatabaseRepository(),
)
container[ProductViewRepository] = lambda _: PostgresProductViewRepository(
    database_repository=DatabaseRepository(),
)
container[BrandRepository] = lambda _: PostgresBrandRepository(
    database_repository=DatabaseRepository(),
)

# Use cases
container[SigUpUseCase] = lambda c: SigUpUseCase(
    user_repository=c[UserRepository],
)
container[UserCreateUseCase] = lambda c: UserCreateUseCase(
    user_repository=c[UserRepository],
)
container[LoginUseCase] = lambda c: LoginUseCase(
    user_repository=c[UserRepository],
)
container[UserUpdateUseCase] = lambda c: UserUpdateUseCase(
    user_repository=c[UserRepository],
)
container[UserRemoveUseCase] = lambda c: UserRemoveUseCase(
    user_repository=c[UserRepository],
)
container[ProductCreateUseCase] = lambda c: ProductCreateUseCase(
    product_repository=c[ProductRepository],
    brand_repository=c[BrandRepository],
)
container[ProductUpdateUseCase] = lambda c: ProductUpdateUseCase(
    product_repository=c[ProductRepository],
    brand_repository=c[BrandRepository],
    notification_service=c[NotificationService],
)
container[ProductRemoveUseCase] = lambda c: ProductRemoveUseCase(
    product_repository=c[ProductRepository],
    view_repository=c[ProductViewRepository],
)
container[ProductDetailUseCase] = lambda c: ProductDetailUseCase(
    product_repository=c[ProductRepository],
    view_repository=c[ProductViewRepository],
)
container[ProductViewReportUseCase] = lambda c: ProductViewReportUseCase(
    product_repository=c[ProductRepository],
)
container[BrandCreateUseCase] = lambda c: BrandCreateUseCase(
    brand_repository=c[BrandRepository],
)

# Services
container[NotificationService] = lambda _: AwsSESNotificationService(
    region_name=settings.SES_REGION_NAME,
)
