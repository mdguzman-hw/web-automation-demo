from core.Constants import QUANTUM_API_BETA_DOMAIN, QUANTUM_API_BETA_BASE_URL
from suites.QuantumAPI import QuantumAPI


class QuantumAPIBeta(QuantumAPI):
    @property
    def domain(self):
        return QUANTUM_API_BETA_DOMAIN

    def __init__(self, driver, language):
        super().__init__(driver, language)
        self.base_url = QUANTUM_API_BETA_BASE_URL