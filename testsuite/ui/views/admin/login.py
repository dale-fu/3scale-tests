""" Representation of Login specific views"""
from widgetastic.widget import View, Text

from testsuite.ui.navigation import Navigable
from testsuite.ui.views.admin.wizard import WizardIntroView
from testsuite.ui.views.auth import Auth0View, RhssoView
from testsuite.ui.views.common.login import LoginForm


class LoginView(View, Navigable):
    """
    Basic login view page object that can be found on path
    """
    path = '/p/login'
    ROOT = "/html//div[@id='pf-login-page-container']"
    header = Text("//main/header/h2")
    error_message = Text("//p[@class='pf-c-form__helper-text pf-m-error']")
    login_widget = View.nested(LoginForm)
    password_reset_link = Text("//a[@href='/p/password/reset']")
    auth0_link = Text("//*[@class='login-provider-link' and contains(@href,'auth0')]")
    rhsso_link = Text("//*[@class='login-provider-link' and contains(@href,'keycloak')]")
    skip_wait_displayed = True

    def do_login(self, name, password):
        """
        Method handle login to 3scale admin portal
        :param name: User username for login
        :param password: User password for login
        :return DashboardView page object
        """
        self.login_widget.do_login(name, password)
        if '/p/admin/onboarding/wizard/intro' in self.browser.url:
            wizard = WizardIntroView(self.browser.root_browser)
            wizard.close_wizard()

    def do_auth0_login(self, email, password):
        """
        Method handle login to 3scale admin portal via Auth0
        :param email: User email for login
        :param password: User password for login
        :return DashboardView page object
        """
        if not self.auth0_link.is_displayed:
            raise Exception("Auth0 provider is not configured for admin portal")
        self.auth0_link.click()
        auth = Auth0View(self.browser.root_browser)
        auth.login(email, password)

    def do_rhsso_login(self, username, password, realm=None):
        """
        Method handle login to 3scale admin portal via RHSSO
        :param username: User email for login
        :param password: User password for login
        :param realm: RHSSO realm name (if more than one RHSSO integration is used)
        :return DashboardView page object
        """
        if not self.rhsso_link.is_displayed:
            raise Exception("RHSSO provider is not configured for admin portal")
        if realm:
            # RHOAM creates its own RHSSO integration, which we don't want to use
            self.browser.element(f"//a[contains(@href,'{realm}')]").click()
        else:
            self.rhsso_link.click()
        auth = RhssoView(self.browser.root_browser)
        auth.login(username, password)

    @property
    def is_displayed(self):
        return self.password_reset_link.is_displayed and self.path in self.browser.url and \
               self.browser.title == '3scale Login' and 'Log in to your account' in self.header.text and \
               self.login_widget.is_displayed
