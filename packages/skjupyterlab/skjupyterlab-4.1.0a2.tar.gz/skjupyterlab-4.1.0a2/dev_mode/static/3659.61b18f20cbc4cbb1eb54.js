"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[3659],{

/***/ 93659:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ lib)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/application@~4.1.0-alpha.2 (singleton) (fallback: ../packages/application/lib/index.js)
var index_js_ = __webpack_require__(65681);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/mainmenu@~4.1.0-alpha.2 (singleton) (fallback: ../packages/mainmenu/lib/index.js)
var mainmenu_lib_index_js_ = __webpack_require__(5184);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var services_lib_index_js_ = __webpack_require__(43411);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/virtualdom@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/virtualdom/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(49581);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/help-extension/lib/licenses.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







const FILTER_SECTION_TITLE_CLASS = 'jp-Licenses-Filters-title';
/**
 * A license viewer
 */
class Licenses extends widgets_dist_index_es6_js_.SplitPanel {
    constructor(options) {
        super();
        this.addClass('jp-Licenses');
        this.model = options.model;
        this.initLeftPanel();
        this.initFilters();
        this.initBundles();
        this.initGrid();
        this.initLicenseText();
        this.setRelativeSizes([1, 2, 3]);
        void this.model.initLicenses().then(() => this._updateBundles());
        this.model.trackerDataChanged.connect(() => {
            this.title.label = this.model.title;
        });
    }
    /**
     * Handle disposing of the widget
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._bundles.currentChanged.disconnect(this.onBundleSelected, this);
        this.model.dispose();
        super.dispose();
    }
    /**
     * Initialize the left area for filters and bundles
     */
    initLeftPanel() {
        this._leftPanel = new widgets_dist_index_es6_js_.Panel();
        this._leftPanel.addClass('jp-Licenses-FormArea');
        this.addWidget(this._leftPanel);
        widgets_dist_index_es6_js_.SplitPanel.setStretch(this._leftPanel, 1);
    }
    /**
     * Initialize the filters
     */
    initFilters() {
        this._filters = new Licenses.Filters(this.model);
        widgets_dist_index_es6_js_.SplitPanel.setStretch(this._filters, 1);
        this._leftPanel.addWidget(this._filters);
    }
    /**
     * Initialize the listing of available bundles
     */
    initBundles() {
        this._bundles = new widgets_dist_index_es6_js_.TabBar({
            orientation: 'vertical',
            renderer: new Licenses.BundleTabRenderer(this.model)
        });
        this._bundles.addClass('jp-Licenses-Bundles');
        widgets_dist_index_es6_js_.SplitPanel.setStretch(this._bundles, 1);
        this._leftPanel.addWidget(this._bundles);
        this._bundles.currentChanged.connect(this.onBundleSelected, this);
        this.model.stateChanged.connect(() => this._bundles.update());
    }
    /**
     * Initialize the listing of packages within the current bundle
     */
    initGrid() {
        this._grid = new Licenses.Grid(this.model);
        widgets_dist_index_es6_js_.SplitPanel.setStretch(this._grid, 1);
        this.addWidget(this._grid);
    }
    /**
     * Initialize the full text of the current package
     */
    initLicenseText() {
        this._licenseText = new Licenses.FullText(this.model);
        widgets_dist_index_es6_js_.SplitPanel.setStretch(this._grid, 1);
        this.addWidget(this._licenseText);
    }
    /**
     * Event handler for updating the model with the current bundle
     */
    onBundleSelected() {
        var _a;
        if ((_a = this._bundles.currentTitle) === null || _a === void 0 ? void 0 : _a.label) {
            this.model.currentBundleName = this._bundles.currentTitle.label;
        }
    }
    /**
     * Update the bundle tabs.
     */
    _updateBundles() {
        this._bundles.clearTabs();
        let i = 0;
        const { currentBundleName } = this.model;
        let currentIndex = 0;
        for (const bundle of this.model.bundleNames) {
            const tab = new widgets_dist_index_es6_js_.Widget();
            tab.title.label = bundle;
            if (bundle === currentBundleName) {
                currentIndex = i;
            }
            this._bundles.insertTab(++i, tab.title);
        }
        this._bundles.currentIndex = currentIndex;
    }
}
/** A namespace for license components */
(function (Licenses) {
    /**
     * License report formats understood by the server (once lower-cased)
     */
    Licenses.REPORT_FORMATS = {
        markdown: {
            id: 'markdown',
            title: 'Markdown',
            icon: ui_components_lib_index_js_.markdownIcon
        },
        csv: {
            id: 'csv',
            title: 'CSV',
            icon: ui_components_lib_index_js_.spreadsheetIcon
        },
        json: {
            id: 'csv',
            title: 'JSON',
            icon: ui_components_lib_index_js_.jsonIcon
        }
    };
    /**
     * The default format (most human-readable)
     */
    Licenses.DEFAULT_FORMAT = 'markdown';
    /**
     * A model for license data
     */
    class Model extends ui_components_lib_index_js_.VDomModel {
        constructor(options) {
            super();
            this._selectedPackageChanged = new index_es6_js_.Signal(this);
            this._trackerDataChanged = new index_es6_js_.Signal(this);
            this._currentPackageIndex = 0;
            this._licensesReady = new dist_index_js_.PromiseDelegate();
            this._packageFilter = {};
            this._trans = options.trans;
            this._licensesUrl = options.licensesUrl;
            this._serverSettings =
                options.serverSettings || services_lib_index_js_.ServerConnection.makeSettings();
            if (options.currentBundleName) {
                this._currentBundleName = options.currentBundleName;
            }
            if (options.packageFilter) {
                this._packageFilter = options.packageFilter;
            }
            if (options.currentPackageIndex) {
                this._currentPackageIndex = options.currentPackageIndex;
            }
        }
        /**
         * Handle the initial request for the licenses from the server.
         */
        async initLicenses() {
            try {
                const response = await services_lib_index_js_.ServerConnection.makeRequest(this._licensesUrl, {}, this._serverSettings);
                this._serverResponse = await response.json();
                this._licensesReady.resolve();
                this.stateChanged.emit(void 0);
            }
            catch (err) {
                this._licensesReady.reject(err);
            }
        }
        /**
         * Create a temporary download link, and emulate clicking it to trigger a named
         * file download.
         */
        async download(options) {
            const url = `${this._licensesUrl}?format=${options.format}&download=1`;
            const element = document.createElement('a');
            element.href = url;
            element.download = '';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            return void 0;
        }
        /**
         * A promise that resolves when the licenses from the server change
         */
        get selectedPackageChanged() {
            return this._selectedPackageChanged;
        }
        /**
         * A promise that resolves when the trackable data changes
         */
        get trackerDataChanged() {
            return this._trackerDataChanged;
        }
        /**
         * The names of the license bundles available
         */
        get bundleNames() {
            var _a;
            return Object.keys(((_a = this._serverResponse) === null || _a === void 0 ? void 0 : _a.bundles) || {});
        }
        /**
         * The current license bundle
         */
        get currentBundleName() {
            if (this._currentBundleName) {
                return this._currentBundleName;
            }
            if (this.bundleNames.length) {
                return this.bundleNames[0];
            }
            return null;
        }
        /**
         * Set the current license bundle, and reset the selected index
         */
        set currentBundleName(currentBundleName) {
            if (this._currentBundleName !== currentBundleName) {
                this._currentBundleName = currentBundleName;
                this.stateChanged.emit(void 0);
                this._trackerDataChanged.emit(void 0);
            }
        }
        /**
         * A promise that resolves when the licenses are available from the server
         */
        get licensesReady() {
            return this._licensesReady.promise;
        }
        /**
         * All the license bundles, keyed by the distributing packages
         */
        get bundles() {
            var _a;
            return ((_a = this._serverResponse) === null || _a === void 0 ? void 0 : _a.bundles) || {};
        }
        /**
         * The index of the currently-selected package within its license bundle
         */
        get currentPackageIndex() {
            return this._currentPackageIndex;
        }
        /**
         * Update the currently-selected package within its license bundle
         */
        set currentPackageIndex(currentPackageIndex) {
            if (this._currentPackageIndex === currentPackageIndex) {
                return;
            }
            this._currentPackageIndex = currentPackageIndex;
            this._selectedPackageChanged.emit(void 0);
            this.stateChanged.emit(void 0);
            this._trackerDataChanged.emit(void 0);
        }
        /**
         * The license data for the currently-selected package
         */
        get currentPackage() {
            var _a;
            if (this.currentBundleName &&
                this.bundles &&
                this._currentPackageIndex != null) {
                return this.getFilteredPackages(((_a = this.bundles[this.currentBundleName]) === null || _a === void 0 ? void 0 : _a.packages) || [])[this._currentPackageIndex];
            }
            return null;
        }
        /**
         * A translation bundle
         */
        get trans() {
            return this._trans;
        }
        get title() {
            return `${this._currentBundleName || ''} ${this._trans.__('Licenses')}`.trim();
        }
        /**
         * The current package filter
         */
        get packageFilter() {
            return this._packageFilter;
        }
        set packageFilter(packageFilter) {
            this._packageFilter = packageFilter;
            this.stateChanged.emit(void 0);
            this._trackerDataChanged.emit(void 0);
        }
        /**
         * Get filtered packages from current bundle where at least one token of each
         * key is present.
         */
        getFilteredPackages(allRows) {
            let rows = [];
            let filters = Object.entries(this._packageFilter)
                .filter(([k, v]) => v && `${v}`.trim().length)
                .map(([k, v]) => [k, `${v}`.toLowerCase().trim().split(' ')]);
            for (const row of allRows) {
                let keyHits = 0;
                for (const [key, bits] of filters) {
                    let bitHits = 0;
                    let rowKeyValue = `${row[key]}`.toLowerCase();
                    for (const bit of bits) {
                        if (rowKeyValue.includes(bit)) {
                            bitHits += 1;
                        }
                    }
                    if (bitHits) {
                        keyHits += 1;
                    }
                }
                if (keyHits === filters.length) {
                    rows.push(row);
                }
            }
            return Object.values(rows);
        }
    }
    Licenses.Model = Model;
    /**
     * A filter form for limiting the packages displayed
     */
    class Filters extends ui_components_lib_index_js_.VDomRenderer {
        constructor(model) {
            super(model);
            /**
             * Render a filter input
             */
            this.renderFilter = (key) => {
                const value = this.model.packageFilter[key] || '';
                return (react_index_js_.createElement("input", { type: "text", name: key, defaultValue: value, className: "jp-mod-styled", onInput: this.onFilterInput }));
            };
            /**
             * Handle a filter input changing
             */
            this.onFilterInput = (evt) => {
                const input = evt.currentTarget;
                const { name, value } = input;
                this.model.packageFilter = { ...this.model.packageFilter, [name]: value };
            };
            this.addClass('jp-Licenses-Filters');
            this.addClass('jp-RenderedHTMLCommon');
        }
        render() {
            const { trans } = this.model;
            return (react_index_js_.createElement("div", null,
                react_index_js_.createElement("label", null,
                    react_index_js_.createElement("strong", { className: FILTER_SECTION_TITLE_CLASS }, trans.__('Filter Licenses By'))),
                react_index_js_.createElement("ul", null,
                    react_index_js_.createElement("li", null,
                        react_index_js_.createElement("label", null, trans.__('Package')),
                        this.renderFilter('name')),
                    react_index_js_.createElement("li", null,
                        react_index_js_.createElement("label", null, trans.__('Version')),
                        this.renderFilter('versionInfo')),
                    react_index_js_.createElement("li", null,
                        react_index_js_.createElement("label", null, trans.__('License')),
                        this.renderFilter('licenseId'))),
                react_index_js_.createElement("label", null,
                    react_index_js_.createElement("strong", { className: FILTER_SECTION_TITLE_CLASS }, trans.__('Distributions')))));
        }
    }
    Licenses.Filters = Filters;
    /**
     * A fancy bundle renderer with the package count
     */
    class BundleTabRenderer extends widgets_dist_index_es6_js_.TabBar.Renderer {
        constructor(model) {
            super();
            this.closeIconSelector = '.lm-TabBar-tabCloseIcon';
            this.model = model;
        }
        /**
         * Render a full bundle
         */
        renderTab(data) {
            let title = data.title.caption;
            let key = this.createTabKey(data);
            let style = this.createTabStyle(data);
            let className = this.createTabClass(data);
            let dataset = this.createTabDataset(data);
            return dist_index_es6_js_.h.li({ key, className, title, style, dataset }, this.renderIcon(data), this.renderLabel(data), this.renderCountBadge(data));
        }
        /**
         * Render the package count
         */
        renderCountBadge(data) {
            const bundle = data.title.label;
            const { bundles } = this.model;
            const packages = this.model.getFilteredPackages((bundles && bundle ? bundles[bundle].packages : []) || []);
            return dist_index_es6_js_.h.label({}, `${packages.length}`);
        }
    }
    Licenses.BundleTabRenderer = BundleTabRenderer;
    /**
     * A grid of licenses
     */
    class Grid extends ui_components_lib_index_js_.VDomRenderer {
        constructor(model) {
            super(model);
            /**
             * Render a single package's license information
             */
            this.renderRow = (row, index) => {
                const selected = index === this.model.currentPackageIndex;
                const onCheck = () => (this.model.currentPackageIndex = index);
                return (react_index_js_.createElement("tr", { key: row.name, className: selected ? 'jp-mod-selected' : '', onClick: onCheck },
                    react_index_js_.createElement("td", null,
                        react_index_js_.createElement("input", { type: "radio", name: "show-package-license", value: index, onChange: onCheck, checked: selected })),
                    react_index_js_.createElement("th", null, row.name),
                    react_index_js_.createElement("td", null,
                        react_index_js_.createElement("code", null, row.versionInfo)),
                    react_index_js_.createElement("td", null,
                        react_index_js_.createElement("code", null, row.licenseId))));
            };
            this.addClass('jp-Licenses-Grid');
            this.addClass('jp-RenderedHTMLCommon');
        }
        /**
         * Render a grid of package license information
         */
        render() {
            var _a;
            const { bundles, currentBundleName, trans } = this.model;
            const filteredPackages = this.model.getFilteredPackages(bundles && currentBundleName
                ? ((_a = bundles[currentBundleName]) === null || _a === void 0 ? void 0 : _a.packages) || []
                : []);
            if (!filteredPackages.length) {
                return (react_index_js_.createElement("blockquote", null,
                    react_index_js_.createElement("em", null, trans.__('No Packages found'))));
            }
            return (react_index_js_.createElement("form", null,
                react_index_js_.createElement("table", null,
                    react_index_js_.createElement("thead", null,
                        react_index_js_.createElement("tr", null,
                            react_index_js_.createElement("td", null),
                            react_index_js_.createElement("th", null, trans.__('Package')),
                            react_index_js_.createElement("th", null, trans.__('Version')),
                            react_index_js_.createElement("th", null, trans.__('License')))),
                    react_index_js_.createElement("tbody", null, filteredPackages.map(this.renderRow)))));
        }
    }
    Licenses.Grid = Grid;
    /**
     * A package's full license text
     */
    class FullText extends ui_components_lib_index_js_.VDomRenderer {
        constructor(model) {
            super(model);
            this.addClass('jp-Licenses-Text');
            this.addClass('jp-RenderedHTMLCommon');
            this.addClass('jp-RenderedMarkdown');
        }
        /**
         * Render the license text, or a null state if no package is selected
         */
        render() {
            const { currentPackage, trans } = this.model;
            let head = '';
            let quote = trans.__('No Package selected');
            let code = '';
            if (currentPackage) {
                const { name, versionInfo, licenseId, extractedText } = currentPackage;
                head = `${name} v${versionInfo}`;
                quote = `${trans.__('License')}: ${licenseId || trans.__('No License ID found')}`;
                code = extractedText || trans.__('No License Text found');
            }
            return [
                react_index_js_.createElement("h1", { key: "h1" }, head),
                react_index_js_.createElement("blockquote", { key: "quote" },
                    react_index_js_.createElement("em", null, quote)),
                react_index_js_.createElement("code", { key: "code" }, code)
            ];
        }
    }
    Licenses.FullText = FullText;
})(Licenses || (Licenses = {}));

;// CONCATENATED MODULE: ../packages/help-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module help-extension
 */








/**
 * The command IDs used by the help plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'help:open';
    CommandIDs.about = 'help:about';
    CommandIDs.activate = 'help:activate';
    CommandIDs.close = 'help:close';
    CommandIDs.show = 'help:show';
    CommandIDs.hide = 'help:hide';
    CommandIDs.jupyterForum = 'help:jupyter-forum';
    CommandIDs.licenses = 'help:licenses';
    CommandIDs.licenseReport = 'help:license-report';
    CommandIDs.refreshLicenses = 'help:licenses-refresh';
})(CommandIDs || (CommandIDs = {}));
/**
 * A flag denoting whether the application is loaded over HTTPS.
 */
const LAB_IS_SECURE = window.location.protocol === 'https:';
/**
 * The class name added to the help widget.
 */
const HELP_CLASS = 'jp-Help';
/**
 * Add a command to show an About dialog.
 */
const about = {
    id: '@jupyterlab/help-extension:about',
    description: 'Adds a "About" dialog feature.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    optional: [lib_index_js_.ICommandPalette],
    activate: (app, translator, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        commands.addCommand(CommandIDs.about, {
            label: trans.__('About %1', app.name),
            execute: () => {
                // Create the header of the about dialog
                const versionNumber = trans.__('Version %1', app.version);
                const versionInfo = (react_index_js_.createElement("span", { className: "jp-About-version-info" },
                    react_index_js_.createElement("span", { className: "jp-About-version" }, versionNumber)));
                const title = (react_index_js_.createElement("span", { className: "jp-About-header" },
                    react_index_js_.createElement(ui_components_lib_index_js_.jupyterIcon.react, { margin: "7px 9.5px", height: "auto", width: "58px" }),
                    react_index_js_.createElement("div", { className: "jp-About-header-info" },
                        react_index_js_.createElement(ui_components_lib_index_js_.jupyterlabWordmarkIcon.react, { height: "auto", width: "196px" }),
                        versionInfo)));
                // Create the body of the about dialog
                const jupyterURL = 'https://jupyter.org/about.html';
                const contributorsURL = 'https://github.com/jupyterlab/jupyterlab/graphs/contributors';
                const externalLinks = (react_index_js_.createElement("span", { className: "jp-About-externalLinks" },
                    react_index_js_.createElement("a", { href: contributorsURL, target: "_blank", rel: "noopener noreferrer", className: "jp-Button-flat" }, trans.__('CONTRIBUTOR LIST')),
                    react_index_js_.createElement("a", { href: jupyterURL, target: "_blank", rel: "noopener noreferrer", className: "jp-Button-flat" }, trans.__('ABOUT PROJECT JUPYTER'))));
                const copyright = (react_index_js_.createElement("span", { className: "jp-About-copyright" }, trans.__('© 2015-2023 Project Jupyter Contributors')));
                const body = (react_index_js_.createElement("div", { className: "jp-About-body" },
                    externalLinks,
                    copyright));
                return (0,lib_index_js_.showDialog)({
                    title,
                    body,
                    buttons: [
                        lib_index_js_.Dialog.createButton({
                            label: trans.__('Dismiss'),
                            className: 'jp-About-button jp-mod-reject jp-mod-styled'
                        })
                    ]
                });
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.about, category });
        }
    }
};
/**
 * A plugin to add a command to open the Jupyter Forum.
 */
const jupyterForum = {
    id: '@jupyterlab/help-extension:jupyter-forum',
    description: 'Adds command to open the Jupyter Forum website.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    optional: [lib_index_js_.ICommandPalette],
    activate: (app, translator, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        commands.addCommand(CommandIDs.jupyterForum, {
            label: trans.__('Jupyter Forum'),
            execute: () => {
                window.open('https://discourse.jupyter.org/c/jupyterlab');
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.jupyterForum, category });
        }
    }
};
/**
 * A plugin to open resources in IFrames or new browser tabs.
 */
const lib_open = {
    id: '@jupyterlab/help-extension:open',
    description: 'Add command to open websites as panel or browser tab.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    optional: [index_js_.ILayoutRestorer],
    activate: (app, translator, restorer) => {
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const namespace = 'help-doc';
        const tracker = new lib_index_js_.WidgetTracker({ namespace });
        let counter = 0;
        /**
         * Create a new HelpWidget widget.
         */
        function newHelpWidget(url, text) {
            // Allow scripts and forms so that things like
            // readthedocs can use their search functionality.
            // We *don't* allow same origin requests, which
            // can prevent some content from being loaded onto the
            // help pages.
            const content = new ui_components_lib_index_js_.IFrame({
                sandbox: ['allow-scripts', 'allow-forms']
            });
            content.url = url;
            content.addClass(HELP_CLASS);
            content.title.label = text;
            content.id = `${namespace}-${++counter}`;
            const widget = new lib_index_js_.MainAreaWidget({ content });
            widget.addClass('jp-Help');
            return widget;
        }
        commands.addCommand(CommandIDs.open, {
            label: args => {
                var _a;
                return (_a = args['text']) !== null && _a !== void 0 ? _a : trans.__('Open the provided `url` in a tab.');
            },
            execute: args => {
                const url = args['url'];
                const text = args['text'];
                const newBrowserTab = args['newBrowserTab'] || false;
                // If help resource will generate a mixed content error, load externally.
                if (newBrowserTab ||
                    (LAB_IS_SECURE && coreutils_lib_index_js_.URLExt.parse(url).protocol !== 'https:')) {
                    window.open(url);
                    return;
                }
                const widget = newHelpWidget(url, text);
                void tracker.add(widget);
                shell.add(widget, 'main');
                return widget;
            }
        });
        // Handle state restoration.
        if (restorer) {
            void restorer.restore(tracker, {
                command: CommandIDs.open,
                args: widget => ({
                    url: widget.content.url,
                    text: widget.content.title.label
                }),
                name: widget => widget.content.url
            });
        }
    }
};
/**
 * A plugin to add a list of resources to the help menu.
 */
const resources = {
    id: '@jupyterlab/help-extension:resources',
    description: 'Adds menu entries to Jupyter reference documentation websites.',
    autoStart: true,
    requires: [mainmenu_lib_index_js_.IMainMenu, translation_lib_index_js_.ITranslator],
    optional: [index_js_.ILabShell, lib_index_js_.ICommandPalette],
    activate: (app, mainMenu, translator, labShell, palette) => {
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        const { commands, serviceManager } = app;
        const resources = [
            {
                text: trans.__('JupyterLab Reference'),
                url: 'https://jupyterlab.readthedocs.io/en/latest/'
            },
            {
                text: trans.__('JupyterLab FAQ'),
                url: 'https://jupyterlab.readthedocs.io/en/latest/getting_started/faq.html'
            },
            {
                text: trans.__('Jupyter Reference'),
                url: 'https://jupyter.org/documentation'
            },
            {
                text: trans.__('Markdown Reference'),
                url: 'https://commonmark.org/help/'
            }
        ];
        resources.sort((a, b) => {
            return a.text.localeCompare(b.text);
        });
        // Populate the Help menu.
        const helpMenu = mainMenu.helpMenu;
        const resourcesGroup = resources.map(args => ({
            args,
            command: CommandIDs.open
        }));
        helpMenu.addGroup(resourcesGroup, 10);
        // Generate a cache of the kernel help links.
        const kernelInfoCache = new Map();
        const onSessionRunningChanged = (m, sessions) => {
            var _a;
            // If a new session has been added, it is at the back
            // of the session list. If one has changed or stopped,
            // it does not hurt to check it.
            if (!sessions.length) {
                return;
            }
            const sessionModel = sessions[sessions.length - 1];
            if (!sessionModel.kernel ||
                kernelInfoCache.has(sessionModel.kernel.name)) {
                return;
            }
            const session = serviceManager.sessions.connectTo({
                model: sessionModel,
                kernelConnectionOptions: { handleComms: false }
            });
            void ((_a = session.kernel) === null || _a === void 0 ? void 0 : _a.info.then(kernelInfo => {
                var _a, _b;
                const name = session.kernel.name;
                // Check the cache second time so that, if two callbacks get scheduled,
                // they don't try to add the same commands.
                if (kernelInfoCache.has(name)) {
                    return;
                }
                const spec = (_b = (_a = serviceManager.kernelspecs) === null || _a === void 0 ? void 0 : _a.specs) === null || _b === void 0 ? void 0 : _b.kernelspecs[name];
                if (!spec) {
                    return;
                }
                // Set the Kernel Info cache.
                kernelInfoCache.set(name, kernelInfo);
                // Utility function to check if the current widget
                // has registered itself with the help menu.
                let usesKernel = false;
                const onCurrentChanged = async () => {
                    const kernel = await commands.execute('helpmenu:get-kernel');
                    usesKernel = (kernel === null || kernel === void 0 ? void 0 : kernel.name) === name;
                };
                // Set the status for the current widget
                onCurrentChanged().catch(error => {
                    console.error('Failed to get the kernel for the current widget.', error);
                });
                if (labShell) {
                    // Update status when current widget changes
                    labShell.currentChanged.connect(onCurrentChanged);
                }
                const isEnabled = () => usesKernel;
                // Add the kernel banner to the Help Menu.
                const bannerCommand = `help-menu-${name}:banner`;
                const kernelName = spec.display_name;
                const kernelIconUrl = spec.resources['logo-svg'] || spec.resources['logo-64x64'];
                commands.addCommand(bannerCommand, {
                    label: trans.__('About the %1 Kernel', kernelName),
                    isVisible: isEnabled,
                    isEnabled,
                    execute: () => {
                        // Create the header of the about dialog
                        const headerLogo = react_index_js_.createElement("img", { src: kernelIconUrl });
                        const title = (react_index_js_.createElement("span", { className: "jp-About-header" },
                            headerLogo,
                            react_index_js_.createElement("div", { className: "jp-About-header-info" }, kernelName)));
                        const banner = react_index_js_.createElement("pre", null, kernelInfo.banner);
                        const body = react_index_js_.createElement("div", { className: "jp-About-body" }, banner);
                        return (0,lib_index_js_.showDialog)({
                            title,
                            body,
                            buttons: [
                                lib_index_js_.Dialog.createButton({
                                    label: trans.__('Dismiss'),
                                    className: 'jp-About-button jp-mod-reject jp-mod-styled'
                                })
                            ]
                        });
                    }
                });
                helpMenu.addGroup([{ command: bannerCommand }], 20);
                // Add the kernel info help_links to the Help menu.
                const kernelGroup = [];
                (kernelInfo.help_links || []).forEach(link => {
                    const commandId = `help-menu-${name}:${link.text}`;
                    commands.addCommand(commandId, {
                        label: commands.label(CommandIDs.open, link),
                        isVisible: isEnabled,
                        isEnabled,
                        execute: () => {
                            return commands.execute(CommandIDs.open, link);
                        }
                    });
                    kernelGroup.push({ command: commandId });
                });
                helpMenu.addGroup(kernelGroup, 21);
            }).then(() => {
                // Dispose of the session object since we no longer need it.
                session.dispose();
            }));
        };
        // Create menu items for currently running sessions
        for (const model of serviceManager.sessions.running()) {
            onSessionRunningChanged(serviceManager.sessions, [model]);
        }
        serviceManager.sessions.runningChanged.connect(onSessionRunningChanged);
        if (palette) {
            resources.forEach(args => {
                palette.addItem({ args, command: CommandIDs.open, category });
            });
            palette.addItem({
                args: { reload: true },
                command: 'apputils:reset',
                category
            });
        }
    }
};
/**
 * A plugin to add a licenses reporting tools.
 */
const licenses = {
    id: '@jupyterlab/help-extension:licenses',
    description: 'Adds licenses used report tools.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    optional: [mainmenu_lib_index_js_.IMainMenu, lib_index_js_.ICommandPalette, index_js_.ILayoutRestorer],
    activate: (app, translator, menu, palette, restorer) => {
        // bail if no license API is available from the server
        if (!coreutils_lib_index_js_.PageConfig.getOption('licensesUrl')) {
            return;
        }
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        // translation strings
        const category = trans.__('Help');
        const downloadAsText = trans.__('Download All Licenses as');
        const licensesText = trans.__('Licenses');
        const refreshLicenses = trans.__('Refresh Licenses');
        // an incrementer for license widget ids
        let counter = 0;
        const licensesUrl = coreutils_lib_index_js_.URLExt.join(coreutils_lib_index_js_.PageConfig.getBaseUrl(), coreutils_lib_index_js_.PageConfig.getOption('licensesUrl')) + '/';
        const licensesNamespace = 'help-licenses';
        const licensesTracker = new lib_index_js_.WidgetTracker({
            namespace: licensesNamespace
        });
        /**
         * Return a full license report format based on a format name
         */
        function formatOrDefault(format) {
            return (Licenses.REPORT_FORMATS[format] ||
                Licenses.REPORT_FORMATS[Licenses.DEFAULT_FORMAT]);
        }
        /**
         * Create a MainAreaWidget for a license viewer
         */
        function createLicenseWidget(args) {
            const licensesModel = new Licenses.Model({
                ...args,
                licensesUrl,
                trans,
                serverSettings: app.serviceManager.serverSettings
            });
            const content = new Licenses({ model: licensesModel });
            content.id = `${licensesNamespace}-${++counter}`;
            content.title.label = licensesText;
            content.title.icon = ui_components_lib_index_js_.copyrightIcon;
            const main = new lib_index_js_.MainAreaWidget({
                content,
                reveal: licensesModel.licensesReady
            });
            main.toolbar.addItem('refresh-licenses', new ui_components_lib_index_js_.CommandToolbarButton({
                id: CommandIDs.refreshLicenses,
                args: { noLabel: 1 },
                commands
            }));
            main.toolbar.addItem('spacer', ui_components_lib_index_js_.Toolbar.createSpacerItem());
            for (const format of Object.keys(Licenses.REPORT_FORMATS)) {
                const button = new ui_components_lib_index_js_.CommandToolbarButton({
                    id: CommandIDs.licenseReport,
                    args: { format, noLabel: 1 },
                    commands
                });
                main.toolbar.addItem(`download-${format}`, button);
            }
            return main;
        }
        // register license-related commands
        commands.addCommand(CommandIDs.licenses, {
            label: licensesText,
            execute: (args) => {
                const licenseMain = createLicenseWidget(args);
                shell.add(licenseMain, 'main', { type: 'Licenses' });
                // add to tracker so it can be restored, and update when choices change
                void licensesTracker.add(licenseMain);
                licenseMain.content.model.trackerDataChanged.connect(() => {
                    void licensesTracker.save(licenseMain);
                });
                return licenseMain;
            }
        });
        commands.addCommand(CommandIDs.refreshLicenses, {
            label: args => (args.noLabel ? '' : refreshLicenses),
            caption: refreshLicenses,
            icon: ui_components_lib_index_js_.refreshIcon,
            execute: async () => {
                var _a;
                return (_a = licensesTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model.initLicenses();
            }
        });
        commands.addCommand(CommandIDs.licenseReport, {
            label: args => {
                if (args.noLabel) {
                    return '';
                }
                const format = formatOrDefault(`${args.format}`);
                return `${downloadAsText} ${format.title}`;
            },
            caption: args => {
                const format = formatOrDefault(`${args.format}`);
                return `${downloadAsText} ${format.title}`;
            },
            icon: args => {
                const format = formatOrDefault(`${args.format}`);
                return format.icon;
            },
            execute: async (args) => {
                var _a;
                const format = formatOrDefault(`${args.format}`);
                return await ((_a = licensesTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model.download({
                    format: format.id
                }));
            }
        });
        // handle optional integrations
        if (palette) {
            palette.addItem({ command: CommandIDs.licenses, category });
        }
        if (menu) {
            const helpMenu = menu.helpMenu;
            helpMenu.addGroup([{ command: CommandIDs.licenses }], 0);
        }
        if (restorer) {
            void restorer.restore(licensesTracker, {
                command: CommandIDs.licenses,
                name: widget => 'licenses',
                args: widget => {
                    const { currentBundleName, currentPackageIndex, packageFilter } = widget.content.model;
                    const args = {
                        currentBundleName,
                        currentPackageIndex,
                        packageFilter
                    };
                    return args;
                }
            });
        }
    }
};
const plugins = [
    about,
    jupyterForum,
    lib_open,
    resources,
    licenses
];
/* harmony default export */ const lib = (plugins);


/***/ })

}]);
//# sourceMappingURL=3659.61b18f20cbc4cbb1eb54.js.map?v=61b18f20cbc4cbb1eb54