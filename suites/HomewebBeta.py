from core.Constants import HOMEWEB_BETA_DOMAIN, HOMEWEB_BETA_BASE_URL
from suites.Homeweb import Homeweb


class HomewebBeta(Homeweb):
    @property
    def domain(self):
        return HOMEWEB_BETA_DOMAIN

    def __init__(self, driver, language):
        super().__init__(driver, language)
        self.base_url = HOMEWEB_BETA_BASE_URL
        self.landing_url = HOMEWEB_BETA_BASE_URL + "/" + language