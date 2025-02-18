"""View representations of Accounts pages"""

from selenium.common.exceptions import NoSuchElementException
from widgetastic.widget import TextInput, GenericLocatorWidget, Text, View
from widgetastic_patternfly4 import PatternflyTable

from testsuite.ui.navigation import step
from testsuite.ui.views.admin.audience import BaseAudienceView
from testsuite.ui.widgets import ThreescaleDropdown, AudienceTable, ThreescaleCheckBox
from testsuite.ui.widgets.buttons import ThreescaleUpdateButton, ThreescaleDeleteButton, \
    ThreescaleEditButton, ThreescaleSubmitButton, ThreescaleSearchButton


class AccountsView(BaseAudienceView):
    """View representation of Accounts Listing page"""
    # TODO search will be separated into the AudienceTable Widget later.
    path_pattern = '/buyers/accounts'
    new_account = Text("//a[@href='/buyers/accounts/new']")
    table = AudienceTable("//*[@id='buyer_accounts']", column_widgets={
        'Group/Org.': Text('./a')
    })
    search_button = ThreescaleSearchButton()
    search_bar = TextInput(id="search_query")

    def search(self, value: str):
        """Search in account table by given value"""
        self.search_bar.fill(value)
        self.search_button.click()

    @step("AccountNewView")
    def new(self):
        """Create new Account"""
        self.new_account.click()

    @step("AccountsDetailView")
    def detail(self, account):
        """Opens detail Account by ID"""
        self.table.row(_row__attr=('id', f'account_{account.entity_id}')).grouporg.widget.click()

    def prerequisite(self):
        return BaseAudienceView

    @property
    def is_displayed(self):
        return BaseAudienceView.is_displayed.fget(self) and self.new_account.is_displayed and \
               self.table.is_displayed and self.path in self.browser.url


class AccountsDetailView(BaseAudienceView):
    """View representation of Account detail page"""
    path_pattern = '/buyers/accounts/{account_id}'
    edit_button = ThreescaleEditButton()
    plan_dropdown = ThreescaleDropdown("//*[@id='account_contract_plan_id']")
    change_plan_button = GenericLocatorWidget("//*[@value='Change']")
    applications_button = Text("//*[contains(@title,'applications')]")
    users_button = Text("//*[contains(@title,'users')]")
    invoices_button = Text("//*[contains(@title,'invoices')]")

    def __init__(self, parent, account):
        super().__init__(parent, account_id=account.entity_id)

    def change_plan(self, value):
        """Change account plan"""
        self.plan_dropdown.select_by_value(value)
        self.change_plan_button.click(handle_alert=True)

    @step("AccountEditView")
    def edit(self):
        """Edit account"""
        self.edit_button.click()

    @step("AccountApplicationsView")
    def applications(self):
        """Open account's applications"""
        self.applications_button.click()

    @step("AccountUserView")
    def users(self):
        """Open account's users"""
        self.users_button.click()

    @step("AccountInvoicesView")
    def invoices(self):
        """Open account's users"""
        self.invoices_button.click()

    def prerequisite(self):
        return AccountsView

    @property
    def is_displayed(self):
        return BaseAudienceView.is_displayed.fget(self) and self.path in self.browser.url and \
               self.edit_button.is_displayed and self.applications_button.is_displayed


class AccountNewView(BaseAudienceView):
    """View representation of New Account page"""
    path_pattern = '/buyers/accounts/new'
    username = TextInput(id='account_user_username')
    email = TextInput(id='account_user_email')
    password = TextInput(id='account_user_password')
    organization = TextInput(id='account_org_name')
    create_button = ThreescaleSubmitButton()

    def create(self, username: str, email: str, password: str, organization: str):
        """Crate new account"""
        self.username.fill(username)
        self.email.fill(email)
        self.password.fill(password)
        self.organization.fill(organization)
        self.create_button.click()

    def prerequisite(self):
        return AccountsView

    @property
    def is_displayed(self):
        return BaseAudienceView.is_displayed.fget(self) and self.path in self.browser.url \
               and self.username.is_displayed and self.email.is_displayed \
               and self.organization.is_displayed


class AccountEditView(BaseAudienceView):
    """View representation of Edit Account page"""
    path_pattern = "/buyers/accounts/{account_id}/edit"
    org_name = TextInput(id="account_org_name")
    update_button = ThreescaleUpdateButton()
    delete_button = ThreescaleDeleteButton()

    def __init__(self, parent, account):
        super().__init__(parent, account_id=account.entity_id)

    def update(self, org_name: str):
        """Update account"""
        self.org_name.fill(org_name)
        self.update_button.click()

    def delete(self):
        """Delete account"""
        self.delete_button.click()

    def prerequisite(self):
        return AccountsDetailView

    @property
    def is_displayed(self):
        return BaseAudienceView.is_displayed.fget(self) and self.org_name.is_displayed \
               and self.org_name.is_displayed and self.update_button.is_displayed


class AccountApplicationsView(BaseAudienceView):
    """View representation of Account's Applications page"""
    path_pattern = "/buyers/accounts/{account_id}/applications"
    create_button = Text("//*[contains(@href,'/applications/new')]")

    def __init__(self, parent, account):
        super().__init__(parent, account_id=account.entity_id)

    @step("ApplicationNewView")
    def new(self):
        """Crate new application"""
        self.create_button.click()

    def prerequisite(self):
        return AccountsDetailView

    @property
    def is_displayed(self):
        return BaseAudienceView.is_displayed.fget(self) and self.create_button.is_displayed and \
               self.path in self.browser.url


class AccountInvoicesView(BaseAudienceView):
    """View representation of Account's Applications page"""
    path_pattern = "/buyers/accounts/{account_id}/invoices"
    create_button = Text(".action.new")
    table = PatternflyTable(".data")

    def __init__(self, parent, account):
        super().__init__(parent, account_id=account.entity_id)

    @step("InvoiceDetailView")
    def new_invoice(self):
        """
        Creates new invoice
        Note: It creates new open invoice, without any form with random ID
        """
        self.create_button.click()
        next(self.table.rows()).id.click()

    def prerequisite(self):
        return AccountsDetailView

    @property
    def is_displayed(self):
        return BaseAudienceView.is_displayed.fget(self) and self.create_button.is_displayed and \
               self.path in self.browser.url


class LineItemForm(View):
    """Nested view for a Line add form"""
    ROOT = "//div[@id='colorbox']"
    name_input = TextInput("line_item[name]")
    quantity_input = TextInput("line_item[quantity]")
    description_input = TextInput("line_item[description]")
    cost_input = TextInput("line_item[cost]")
    submit = Text("//input[@type='submit']")

    def add_item(self, name, quantity, cost, description):
        """Adds item to an invoice"""
        self.name_input.fill(name)
        self.quantity_input.fill(quantity)
        self.description_input.fill(description)
        self.cost_input.fill(cost)
        self.submit.click()


class InvoiceDetailView(BaseAudienceView):
    """Invoice Detail page"""
    issue_button = Text("//form[contains(@action, 'issue.js')]/button")
    charge_button = Text("//form[contains(@action, 'charge.js')]/button")
    id_field = Text("#field-friendly_id")
    state_field = Text("#field-state")

    # Selector which we can use to check if the charge has finished
    paid_field = Text("//td[@id='field-state' and text()='Paid']")
    add_item_btn = GenericLocatorWidget("//a[contains(@class,'action add')]")
    line_item_form = View.nested(LineItemForm)

    def add_item(self, name, quantity, cost, description):
        """Adds item to an invoice"""
        self.add_item_btn.click()
        self.line_item_form.wait_displayed()
        self.line_item_form.add_item(name, quantity, cost, description)

    def issue(self):
        """Issues the invoices (OPEN -> PENDING)"""
        self.issue_button.click(handle_alert=True)
        self.browser.wait_for_element(self.charge_button, timeout=10)

    def charge(self, invoice=None):
        """Charges the invoices (PENDING -> PAID)"""
        # Charge button has two alerts which completely messed up with widgetastic.
        # https://issues.redhat.com/browse/THREESCALE-7276
        self.browser.click(self.charge_button, ignore_ajax=True)
        self.browser.handle_double_alert()

        # Wait until charge is done
        try:
            self.browser.wait_for_element(self.paid_field, timeout=5)
        except NoSuchElementException as err:
            if invoice is not None:
                latest_transaction = invoice.payment_transactions.list()[-1]
                raise RuntimeError(latest_transaction["message"]) from err
            raise err

    def prerequisite(self):
        return AccountInvoicesView


class UsageRulesView(BaseAudienceView):
    """View representation of Account's Usage Rules page"""
    path_pattern = "/site/usage_rules/edit"
    account_plans_checkbox = ThreescaleCheckBox(locator="//input[@id='settings_account_plans_ui_visible']")
    update_button = ThreescaleUpdateButton()

    def account_plans(self):
        """Allow account plans"""
        self.account_plans_checkbox.check()
        self.update_button.click()

    def prerequisite(self):
        return BaseAudienceView

    @property
    def is_displayed(self):
        return BaseAudienceView.is_displayed.fget(self) and self.account_plans_checkbox.is_displayed and \
               self.path in self.browser.url
