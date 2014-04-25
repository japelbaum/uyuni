<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html"%>
<%@ taglib uri="http://struts.apache.org/tags-bean" prefix="bean"%>
<%@ taglib uri="http://rhn.redhat.com/rhn" prefix="rhn"%>
<%@ taglib uri="http://rhn.redhat.com/tags/list" prefix="rl"%>

<html>
<head>
    <script type="text/javascript" src="/rhn/dwr/interface/ProductsRenderer.js"></script>
    <script type="text/javascript" src="/rhn/dwr/interface/ProductSyncAction.js"></script>
    <script type="text/javascript" src="/rhn/dwr/engine.js"></script>
    <script type="text/javascript" src="/javascript/responsive-tab.js"></script>
    <script type="text/javascript" src="/javascript/susemanager-setup-wizard.js"></script>
    <script type="text/javascript" src="/javascript/susemanager-setup-wizard-suse-products.js"></script>
</head>
<body>
    <div class="responsive-wizard">
        <rhn:toolbar base="h1" icon="header-preferences" helpUrl="/rhn/help/user/en-US/s1-sm-sattools.jsp#s2-sattools-wizard">
            Setup Wizard
        </rhn:toolbar>
        <rhn:dialogmenu mindepth="0" maxdepth="1" definition="/WEB-INF/nav/setup_wizard.xml"
            renderer="com.redhat.rhn.frontend.nav.DialognavRenderer" />

        <div class="panel panel-default" id="products-content">
            <div class="panel-body">
                <div class="row" id="suse-products">
                    <div class="col-sm-9">
                        <div class="alert alert-danger" id="invalid-credentials-alert-popup" hidden>
                            <bean:message key="suse-products.jsp.invalid-credentials-alert-message" />
                        </div>
                        <div class="alert alert-danger" id="no-connection-alert-popup" hidden>
                            <bean:message key="suse-products.jsp.no-connection-alert-message" />
                        </div>
                        <table class="table table-rounded">
                            <thead>
                                <tr>
                                    <th><input type="checkbox" class="select-all" autocomplete="off" /></th>
                                    <th>Available Products Below</th>
                                    <th>Architecture</th>
                                    <th>Channels</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody class="table-content">
                                <tr id="loading-placeholder">
                                    <td colspan="5">
                                        <rhn:icon type="spinner"></rhn:icon>
                                        <span>Loading...</span>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td><input type="checkbox" class="select-all" autocomplete="off" /></td>
                                    <td colspan="5">
                                        <button class="btn btn-success" id="synchronize">
                                            <i class="fa fa-plus"></i> <bean:message key='suse-products.jsp.add-products' />
                                        </button>
                                    </td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                    <div class="col-sm-3 hidden-xs" id="wizard-faq">
                        <h4>Why aren't all SUSE products displayed in the list?</h4>
                        <p>The products displayed on this list are directly linked to
                           your Mirror Credentials as well as your SUSE subscriptions.</p>
                        <p>If you believe there are products missing, make sure you have
                           added the correct Mirror Credentials in the previous wizard step.</p>
                    </div>
                </div>
            </div>
            <jsp:include page="/WEB-INF/pages/common/fragments/setup/setup-tab-footer.jspf" />
        </div>
    </div>
</body>
</html>
