# Copyright © 2026 - Homewood Health Inc.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from core.BasePage import BasePage


class HeaderAnon:
    EN = {
        "elements": {
            "buttons": {
                "sign_in": "btn-login"
            }
        },
        "paths": {
            "buttons": {
                "sign_in": "/en/login"
            }
        }
    }

    FR = {
        "elements": {
            "buttons": {
                "sign_in": "btn-login"
            }
        },
        "paths": {
            "buttons": {
                "sign_in": "/fr/login"
            }
        }
    }


class HeaderAnonApi:
    EN = {
        "elements": {}
    }
    FR = {
        "elements": {}
    }


class HeaderHomeweb:
    EN = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "sign_out": "[aria-label=\"Sign out\"]",
                "dashboard": "[aria-label=\"Dashboard\"]",
                "resources": "[aria-label=\"Resources\"]",
                "wellness": "[aria-label=\"Wellness\"]"
            }
        },
        "paths": {
        }
    }

    FR = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "sign_out": "[aria-label=\"Se déconnecter\"]",
                "dashboard": "[aria-label=\"Tableau de bord\"]",
                "resources": "[aria-label=\"Ressources\"]",
                "wellness": "[aria-label=\"Bien-être\"]"
            }
        },
        "paths": {
        }
    }


class HeaderCustomerPortal:
    EN = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "menu_sign_out": "[aria-label=\"Sign out\"]",
                "menu_sign_out_group": ".dropdown-group.dropdown-group-sign-out",
                "menu_sign_out_single": "Sign out",
                "menu_sign_out_all": "Sign out everywhere",
                "menu_language": "[aria-label=\"Change language to  FR\"]",
                "toggle_language": "[aria-label=\"Toggle language to  FR\"]",
            },
            "dropdown": {
                "dropdown_insights": "ul.dropdown-menu.dropdown-insights.show",
                "dropdown_monthly": "Monthly Registrations Year-over-Year",
                "dropdown_eq": "Equitable Dashboard",
                "dropdown_ahs": "Insights: Alberta Health Services",
            }
        },
        "paths": {
        }
    }

    FR = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "menu_sign_out": "[aria-label=\"Se déconnecter\"]",
                "menu_sign_out_group": ".dropdown-group.dropdown-group-sign-out",
                "menu_sign_out_single": "Se déconnecter",
                "menu_sign_out_all": "Se déconnecter partou",
                "menu_language": "[aria-label=\"Changer la langue en  EN\"]",
                "toggle_language": "[aria-label=\"Basculer la langue en EN\"]",
            },
            "dropdown": {
                "dropdown_insights": "ul.dropdown-menu.dropdown-perspectives.show",
                "dropdown_monthly": "Monthly Registrations Year-over-Year",
                "dropdown_eq": "Rapport d'utilisation",
                "dropdown_ahs": "Perspectives: Alberta Health Services",
            }
        },
        "paths": {
        }
    }


class HeaderQuantumApi:
    EN = {
        "elements": {}
    }

    FR = {
        "elements": {}
    }


class HeaderSentioClient:
    EN = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "menu_sign_out": "[aria-label=\"Sign out\"]",
                "dashboard": "[aria-label=\"Dashboard\"]",
                "tasks": "[aria-label=\"Tasks\"]",
            }
        }
    }
    FR = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "menu_sign_out": "[aria-label=\"Se déconnecter\"]",
                "dashboard": "[aria-label=\"Tableau de bord\"]",
                "tasks": "[aria-label=\"Tâches\"]",
            }
        }
    }


class HeaderSentioProvider:
    EN = {
        "elements": {
            "classic": "[aria-label=\"Classic Dashboard\"]",
            "new": "[aria-label=\"New Dashboard\"]",
            "buttons": {
                "menu": "nav-account-toggle",
                "menu_sign_out": "[aria-label=\"Sign out\"]",
            }
        }
    }
    FR = {
        "elements": {
            "classic": "[aria-label=\"Tableau de bord classique\"]",
            "new": "[aria-label=\"Nouveau tableau de bord\"]",
            "buttons": {
                "menu": "nav-account-toggle",
                "menu_sign_out": "[aria-label=\"Se déconnecter\"]",
            }

        }
    }


class Header(BasePage):
    DOMAIN_MAP = {
        "homeweb": {"AUTH": HeaderHomeweb, "ANON": HeaderAnon},
        "customer_portal": {"AUTH": HeaderCustomerPortal, "ANON": HeaderAnon},
        "quantum_api": {"AUTH": HeaderQuantumApi, "ANON": HeaderAnonApi},
        "sentio_beta_client": {"AUTH": HeaderSentioClient, "ANON": HeaderAnon},
        "sentio_beta_provider": {"AUTH": HeaderSentioProvider, "ANON": HeaderAnon},
    }

    def __init__(self, driver, language, domain="homeweb", user="ANON"):
        super().__init__(driver, language)
        # self.type = HeaderHomeweb if user == "AUTH" else HeaderAnon
        self.domain = domain.lower()
        self.user = user.upper()

        domain_class = self.DOMAIN_MAP[self.domain][self.user]

        self.elements = domain_class.EN["elements"] if language == "en" else domain_class.FR["elements"]
        self.paths = domain_class.EN.get("paths", {}) if language == "en" else domain_class.FR.get("paths", {})

    def wait_for_account_menu(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.dropdown-menu.dropdown-account.show")
            )
        )

    def wait_for_insights_dropdown(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, self.elements["dropdown"]["dropdown_insights"])
            )
        )

    def wait_for_sign_out_group(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, self.elements["buttons"]["menu_sign_out_group"])
            )
        )
