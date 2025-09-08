from app.application.api.users.sig_up.schemas import SigUpRequest
from app.domain.use_cases.users.sig_up.sig_up_input import SigUpInput


class SigUpInputMapper:

    @staticmethod
    def map(request: SigUpRequest) -> SigUpInput:
        return SigUpInput(
            username=request.username,
            email=request.email,
            password=request.password,
        )
