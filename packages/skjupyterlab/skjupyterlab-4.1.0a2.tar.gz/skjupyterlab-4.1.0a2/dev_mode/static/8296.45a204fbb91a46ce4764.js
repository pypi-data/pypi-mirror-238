"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[8296],{

/***/ 88296:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_csvviewer_lib_widget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(96324);
/* harmony import */ var _jupyterlab_csvviewer_lib_toolbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(58362);
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(80599);
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(5184);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module csvviewer-extension
 */








/**
 * The name of the factories that creates widgets.
 */
const FACTORY_CSV = 'CSVTable';
const FACTORY_TSV = 'TSVTable';
/**
 * The command IDs used by the csvviewer plugins.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.CSVGoToLine = 'csv:go-to-line';
    CommandIDs.TSVGoToLine = 'tsv:go-to-line';
})(CommandIDs || (CommandIDs = {}));
/**
 * The CSV file handler extension.
 */
const csv = {
    activate: activateCsv,
    id: '@jupyterlab/csvviewer-extension:csv',
    description: 'Adds viewer for CSV file types',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
        _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.ISearchProviderRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry
    ],
    autoStart: true
};
/**
 * The TSV file handler extension.
 */
const tsv = {
    activate: activateTsv,
    id: '@jupyterlab/csvviewer-extension:tsv',
    description: 'Adds viewer for TSV file types.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
        _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.ISearchProviderRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry
    ],
    autoStart: true
};
/**
 * Activate cssviewer extension for CSV files
 */
function activateCsv(app, translator, restorer, themeManager, mainMenu, searchRegistry, settingRegistry, toolbarRegistry) {
    const { commands, shell } = app;
    let toolbarFactory;
    if (toolbarRegistry) {
        toolbarRegistry.addFactory(FACTORY_CSV, 'delimiter', widget => new _jupyterlab_csvviewer_lib_toolbar__WEBPACK_IMPORTED_MODULE_6__/* .CSVDelimiter */ .p({
            widget: widget.content,
            translator
        }));
        if (settingRegistry) {
            toolbarFactory = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, FACTORY_CSV, csv.id, translator);
        }
    }
    const trans = translator.load('jupyterlab');
    const factory = new _jupyterlab_csvviewer_lib_widget__WEBPACK_IMPORTED_MODULE_7__/* .CSVViewerFactory */ .LT({
        name: FACTORY_CSV,
        label: trans.__('CSV Viewer'),
        fileTypes: ['csv'],
        defaultFor: ['csv'],
        readOnly: true,
        toolbarFactory,
        translator
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'csvviewer'
    });
    // The current styles for the data grids.
    let style = Private.LIGHT_STYLE;
    let rendererConfig = Private.LIGHT_TEXT_CONFIG;
    if (restorer) {
        // Handle state restoration.
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY_CSV }),
            name: widget => widget.context.path
        });
    }
    app.docRegistry.addWidgetFactory(factory);
    const ft = app.docRegistry.getFileType('csv');
    let searchProviderInitialized = false;
    factory.widgetCreated.connect(async (sender, widget) => {
        // Track the widget.
        void tracker.add(widget);
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        if (ft) {
            widget.title.icon = ft.icon;
            widget.title.iconClass = ft.iconClass;
            widget.title.iconLabel = ft.iconLabel;
        }
        // Delay await to execute `widget.title` setters (above) synchronously
        if (searchRegistry && !searchProviderInitialized) {
            const { CSVSearchProvider } = await __webpack_require__.e(/* import() */ 4525).then(__webpack_require__.bind(__webpack_require__, 24525));
            searchRegistry.add('csv', CSVSearchProvider);
            searchProviderInitialized = true;
        }
        // Set the theme for the new widget; requires `.content` to be loaded.
        await widget.content.ready;
        widget.content.style = style;
        widget.content.rendererConfig = rendererConfig;
    });
    // Keep the themes up-to-date.
    const updateThemes = () => {
        const isLight = themeManager && themeManager.theme
            ? themeManager.isLight(themeManager.theme)
            : true;
        style = isLight ? Private.LIGHT_STYLE : Private.DARK_STYLE;
        rendererConfig = isLight
            ? Private.LIGHT_TEXT_CONFIG
            : Private.DARK_TEXT_CONFIG;
        tracker.forEach(async (grid) => {
            await grid.content.ready;
            grid.content.style = style;
            grid.content.rendererConfig = rendererConfig;
        });
    };
    if (themeManager) {
        themeManager.themeChanged.connect(updateThemes);
    }
    // Add commands
    const isEnabled = () => tracker.currentWidget !== null &&
        tracker.currentWidget === shell.currentWidget;
    commands.addCommand(CommandIDs.CSVGoToLine, {
        label: trans.__('Go to Line'),
        execute: async () => {
            const widget = tracker.currentWidget;
            if (widget === null) {
                return;
            }
            const result = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getNumber({
                title: trans.__('Go to Line'),
                value: 0
            });
            if (result.button.accept && result.value !== null) {
                widget.content.goToLine(result.value);
            }
        },
        isEnabled
    });
    if (mainMenu) {
        // Add go to line capability to the edit menu.
        mainMenu.editMenu.goToLiners.add({
            id: CommandIDs.CSVGoToLine,
            isEnabled
        });
    }
}
/**
 * Activate cssviewer extension for TSV files
 */
function activateTsv(app, translator, restorer, themeManager, mainMenu, searchRegistry, settingRegistry, toolbarRegistry) {
    const { commands, shell } = app;
    let toolbarFactory;
    if (toolbarRegistry) {
        toolbarRegistry.addFactory(FACTORY_TSV, 'delimiter', widget => new _jupyterlab_csvviewer_lib_toolbar__WEBPACK_IMPORTED_MODULE_6__/* .CSVDelimiter */ .p({
            widget: widget.content,
            translator
        }));
        if (settingRegistry) {
            toolbarFactory = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, FACTORY_TSV, tsv.id, translator);
        }
    }
    const trans = translator.load('jupyterlab');
    const factory = new _jupyterlab_csvviewer_lib_widget__WEBPACK_IMPORTED_MODULE_7__/* .TSVViewerFactory */ ._d({
        name: FACTORY_TSV,
        label: trans.__('TSV Viewer'),
        fileTypes: ['tsv'],
        defaultFor: ['tsv'],
        readOnly: true,
        toolbarFactory,
        translator
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'tsvviewer'
    });
    // The current styles for the data grids.
    let style = Private.LIGHT_STYLE;
    let rendererConfig = Private.LIGHT_TEXT_CONFIG;
    if (restorer) {
        // Handle state restoration.
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY_TSV }),
            name: widget => widget.context.path
        });
    }
    app.docRegistry.addWidgetFactory(factory);
    const ft = app.docRegistry.getFileType('tsv');
    let searchProviderInitialized = false;
    factory.widgetCreated.connect(async (sender, widget) => {
        // Track the widget.
        void tracker.add(widget);
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        if (ft) {
            widget.title.icon = ft.icon;
            widget.title.iconClass = ft.iconClass;
            widget.title.iconLabel = ft.iconLabel;
        }
        // Delay await to execute `widget.title` setters (above) synchronously
        if (searchRegistry && !searchProviderInitialized) {
            const { CSVSearchProvider } = await __webpack_require__.e(/* import() */ 4525).then(__webpack_require__.bind(__webpack_require__, 24525));
            searchRegistry.add('tsv', CSVSearchProvider);
            searchProviderInitialized = true;
        }
        // Set the theme for the new widget; requires `.content` to be loaded.
        await widget.content.ready;
        widget.content.style = style;
        widget.content.rendererConfig = rendererConfig;
    });
    // Keep the themes up-to-date.
    const updateThemes = () => {
        const isLight = themeManager && themeManager.theme
            ? themeManager.isLight(themeManager.theme)
            : true;
        style = isLight ? Private.LIGHT_STYLE : Private.DARK_STYLE;
        rendererConfig = isLight
            ? Private.LIGHT_TEXT_CONFIG
            : Private.DARK_TEXT_CONFIG;
        tracker.forEach(async (grid) => {
            await grid.content.ready;
            grid.content.style = style;
            grid.content.rendererConfig = rendererConfig;
        });
    };
    if (themeManager) {
        themeManager.themeChanged.connect(updateThemes);
    }
    // Add commands
    const isEnabled = () => tracker.currentWidget !== null &&
        tracker.currentWidget === shell.currentWidget;
    commands.addCommand(CommandIDs.TSVGoToLine, {
        label: trans.__('Go to Line'),
        execute: async () => {
            const widget = tracker.currentWidget;
            if (widget === null) {
                return;
            }
            const result = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getNumber({
                title: trans.__('Go to Line'),
                value: 0
            });
            if (result.button.accept && result.value !== null) {
                widget.content.goToLine(result.value);
            }
        },
        isEnabled
    });
    if (mainMenu) {
        // Add go to line capability to the edit menu.
        mainMenu.editMenu.goToLiners.add({
            id: CommandIDs.TSVGoToLine,
            isEnabled
        });
    }
}
/**
 * Export the plugins as default.
 */
const plugins = [csv, tsv];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * The light theme for the data grid.
     */
    Private.LIGHT_STYLE = {
        voidColor: '#F3F3F3',
        backgroundColor: 'white',
        headerBackgroundColor: '#EEEEEE',
        gridLineColor: 'rgba(20, 20, 20, 0.15)',
        headerGridLineColor: 'rgba(20, 20, 20, 0.25)',
        rowBackgroundColor: i => (i % 2 === 0 ? '#F5F5F5' : 'white')
    };
    /**
     * The dark theme for the data grid.
     */
    Private.DARK_STYLE = {
        voidColor: 'black',
        backgroundColor: '#111111',
        headerBackgroundColor: '#424242',
        gridLineColor: 'rgba(235, 235, 235, 0.15)',
        headerGridLineColor: 'rgba(235, 235, 235, 0.25)',
        rowBackgroundColor: i => (i % 2 === 0 ? '#212121' : '#111111')
    };
    /**
     * The light config for the data grid renderer.
     */
    Private.LIGHT_TEXT_CONFIG = {
        textColor: '#111111',
        matchBackgroundColor: '#FFFFE0',
        currentMatchBackgroundColor: '#FFFF00',
        horizontalAlignment: 'right'
    };
    /**
     * The dark config for the data grid renderer.
     */
    Private.DARK_TEXT_CONFIG = {
        textColor: '#F5F5F5',
        matchBackgroundColor: '#838423',
        currentMatchBackgroundColor: '#A3807A',
        horizontalAlignment: 'right'
    };
})(Private || (Private = {}));


/***/ }),

/***/ 58362:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "p": () => (/* binding */ CSVDelimiter)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(72234);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to a csv toolbar widget.
 */
const CSV_DELIMITER_CLASS = 'jp-CSVDelimiter';
const CSV_DELIMITER_LABEL_CLASS = 'jp-CSVDelimiter-label';
/**
 * The class name added to a csv toolbar's dropdown element.
 */
const CSV_DELIMITER_DROPDOWN_CLASS = 'jp-CSVDelimiter-dropdown';
/**
 * A widget for selecting a delimiter.
 */
class CSVDelimiter extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    /**
     * Construct a new csv table widget.
     */
    constructor(options) {
        super({
            node: Private.createNode(options.widget.delimiter, options.translator)
        });
        this._widget = options.widget;
        this.addClass(CSV_DELIMITER_CLASS);
    }
    /**
     * The delimiter dropdown menu.
     */
    get selectNode() {
        return this.node.getElementsByTagName('select')[0];
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'change':
                this._widget.delimiter = this.selectNode.value;
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        this.selectNode.addEventListener('change', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        this.selectNode.removeEventListener('change', this);
    }
}
/**
 * A namespace for private toolbar methods.
 */
var Private;
(function (Private) {
    /**
     * Create the node for the delimiter switcher.
     */
    function createNode(selected, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
        // The supported parsing delimiters and labels.
        const delimiters = [
            [',', ','],
            [';', ';'],
            ['\t', trans.__('tab')],
            ['|', trans.__('pipe')],
            ['#', trans.__('hash')]
        ];
        const div = document.createElement('div');
        const label = document.createElement('span');
        const select = document.createElement('select');
        label.textContent = trans.__('Delimiter: ');
        label.className = CSV_DELIMITER_LABEL_CLASS;
        for (const [delimiter, label] of delimiters) {
            const option = document.createElement('option');
            option.value = delimiter;
            option.textContent = label;
            if (delimiter === selected) {
                option.selected = true;
            }
            select.appendChild(option);
        }
        div.appendChild(label);
        const node = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.Styling.wrapSelect(select);
        node.classList.add(CSV_DELIMITER_DROPDOWN_CLASS);
        div.appendChild(node);
        return div;
    }
    Private.createNode = createNode;
})(Private || (Private = {}));


/***/ }),

/***/ 96324:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "A9": () => (/* binding */ CSVViewer),
/* harmony export */   "B0": () => (/* binding */ TextRenderConfig),
/* harmony export */   "JZ": () => (/* binding */ GridSearchService),
/* harmony export */   "LT": () => (/* binding */ CSVViewerFactory),
/* harmony export */   "_d": () => (/* binding */ TSVViewerFactory),
/* harmony export */   "kw": () => (/* binding */ CSVDocumentWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(78254);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(16564);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(30205);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(72234);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(58362);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The class name added to a CSV viewer.
 */
const CSV_CLASS = 'jp-CSVViewer';
/**
 * The class name added to a CSV viewer datagrid.
 */
const CSV_GRID_CLASS = 'jp-CSVViewer-grid';
/**
 * The timeout to wait for change activity to have ceased before rendering.
 */
const RENDER_TIMEOUT = 1000;
/**
 * Configuration for cells textrenderer.
 */
class TextRenderConfig {
}
/**
 * Search service remembers the search state and the location of the last
 * match, for incremental searching.
 * Search service is also responsible of providing a cell renderer function
 * to set the background color of cells matching the search text.
 */
class GridSearchService {
    constructor(grid) {
        this._looping = true;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._grid = grid;
        this._query = null;
        this._row = 0;
        this._column = -1;
    }
    /**
     * A signal fired when the grid changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Returns a cellrenderer config function to render each cell background.
     * If cell match, background is matchBackgroundColor, if it's the current
     * match, background is currentMatchBackgroundColor.
     */
    cellBackgroundColorRendererFunc(config) {
        return ({ value, row, column }) => {
            if (this._query) {
                if (value.match(this._query)) {
                    if (this._row === row && this._column === column) {
                        return config.currentMatchBackgroundColor;
                    }
                    return config.matchBackgroundColor;
                }
            }
            return '';
        };
    }
    /**
     * Clear the search.
     */
    clear() {
        this._query = null;
        this._row = 0;
        this._column = -1;
        this._changed.emit(undefined);
    }
    /**
     * incrementally look for searchText.
     */
    find(query, reverse = false) {
        const model = this._grid.dataModel;
        const rowCount = model.rowCount('body');
        const columnCount = model.columnCount('body');
        if (this._query !== query) {
            // reset search
            this._row = 0;
            this._column = -1;
        }
        this._query = query;
        // check if the match is in current viewport
        const minRow = this._grid.scrollY / this._grid.defaultSizes.rowHeight;
        const maxRow = (this._grid.scrollY + this._grid.pageHeight) /
            this._grid.defaultSizes.rowHeight;
        const minColumn = this._grid.scrollX / this._grid.defaultSizes.columnHeaderHeight;
        const maxColumn = (this._grid.scrollX + this._grid.pageWidth) /
            this._grid.defaultSizes.columnHeaderHeight;
        const isInViewport = (row, column) => {
            return (row >= minRow &&
                row <= maxRow &&
                column >= minColumn &&
                column <= maxColumn);
        };
        const increment = reverse ? -1 : 1;
        this._column += increment;
        for (let row = this._row; reverse ? row >= 0 : row < rowCount; row += increment) {
            for (let col = this._column; reverse ? col >= 0 : col < columnCount; col += increment) {
                const cellData = model.data('body', row, col);
                if (cellData.match(query)) {
                    // to update the background of matching cells.
                    // TODO: we only really need to invalidate the previous and current
                    // cell rects, not the entire grid.
                    this._changed.emit(undefined);
                    if (!isInViewport(row, col)) {
                        this._grid.scrollToRow(row);
                    }
                    this._row = row;
                    this._column = col;
                    return true;
                }
            }
            this._column = reverse ? columnCount - 1 : 0;
        }
        // We've finished searching all the way to the limits of the grid. If this
        // is the first time through (looping is true), wrap the indices and search
        // again. Otherwise, give up.
        if (this._looping) {
            this._looping = false;
            this._row = reverse ? 0 : rowCount - 1;
            this._wrapRows(reverse);
            try {
                return this.find(query, reverse);
            }
            finally {
                this._looping = true;
            }
        }
        return false;
    }
    /**
     * Wrap indices if needed to just before the start or just after the end.
     */
    _wrapRows(reverse = false) {
        const model = this._grid.dataModel;
        const rowCount = model.rowCount('body');
        const columnCount = model.columnCount('body');
        if (reverse && this._row <= 0) {
            // if we are at the front, wrap to just past the end.
            this._row = rowCount - 1;
            this._column = columnCount;
        }
        else if (!reverse && this._row >= rowCount - 1) {
            // if we are at the end, wrap to just before the front.
            this._row = 0;
            this._column = -1;
        }
    }
    get query() {
        return this._query;
    }
}
/**
 * A viewer for CSV tables.
 */
class CSVViewer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new CSV viewer.
     */
    constructor(options) {
        super();
        this._monitor = null;
        this._delimiter = ',';
        this._revealed = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
        this._baseRenderer = null;
        this._context = options.context;
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.PanelLayout();
        this.addClass(CSV_CLASS);
        this._ready = this.initialize();
    }
    /**
     * Promise which resolves when the content is ready.
     */
    get ready() {
        return this._ready;
    }
    async initialize() {
        const layout = this.layout;
        if (this.isDisposed || !layout) {
            return;
        }
        const { BasicKeyHandler, BasicMouseHandler, DataGrid } = await Private.ensureDataGrid();
        this._defaultStyle = DataGrid.defaultStyle;
        this._grid = new DataGrid({
            defaultSizes: {
                rowHeight: 24,
                columnWidth: 144,
                rowHeaderWidth: 64,
                columnHeaderHeight: 36
            }
        });
        this._grid.addClass(CSV_GRID_CLASS);
        this._grid.headerVisibility = 'all';
        this._grid.keyHandler = new BasicKeyHandler();
        this._grid.mouseHandler = new BasicMouseHandler();
        this._grid.copyConfig = {
            separator: '\t',
            format: DataGrid.copyFormatGeneric,
            headers: 'all',
            warningThreshold: 1e6
        };
        layout.addWidget(this._grid);
        this._searchService = new GridSearchService(this._grid);
        this._searchService.changed.connect(this._updateRenderer, this);
        await this._context.ready;
        await this._updateGrid();
        this._revealed.resolve(undefined);
        // Throttle the rendering rate of the widget.
        this._monitor = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.ActivityMonitor({
            signal: this._context.model.contentChanged,
            timeout: RENDER_TIMEOUT
        });
        this._monitor.activityStopped.connect(this._updateGrid, this);
    }
    /**
     * The CSV widget's context.
     */
    get context() {
        return this._context;
    }
    /**
     * A promise that resolves when the csv viewer is ready to be revealed.
     */
    get revealed() {
        return this._revealed.promise;
    }
    /**
     * The delimiter for the file.
     */
    get delimiter() {
        return this._delimiter;
    }
    set delimiter(value) {
        if (value === this._delimiter) {
            return;
        }
        this._delimiter = value;
        void this._updateGrid();
    }
    /**
     * The style used by the data grid.
     */
    get style() {
        return this._grid.style;
    }
    set style(value) {
        this._grid.style = { ...this._defaultStyle, ...value };
    }
    /**
     * The config used to create text renderer.
     */
    set rendererConfig(rendererConfig) {
        this._baseRenderer = rendererConfig;
        void this._updateRenderer();
    }
    /**
     * The search service
     */
    get searchService() {
        return this._searchService;
    }
    /**
     * Dispose of the resources used by the widget.
     */
    dispose() {
        if (this._monitor) {
            this._monitor.dispose();
        }
        super.dispose();
    }
    /**
     * Go to line
     */
    goToLine(lineNumber) {
        this._grid.scrollToRow(lineNumber);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    }
    /**
     * Create the model for the grid.
     */
    async _updateGrid() {
        const { BasicSelectionModel } = await Private.ensureDataGrid();
        const { DSVModel } = await Private.ensureDSVModel();
        const data = this._context.model.toString();
        const delimiter = this._delimiter;
        const oldModel = this._grid.dataModel;
        const dataModel = (this._grid.dataModel = new DSVModel({
            data,
            delimiter
        }));
        this._grid.selectionModel = new BasicSelectionModel({ dataModel });
        if (oldModel) {
            oldModel.dispose();
        }
    }
    /**
     * Update the renderer for the grid.
     */
    async _updateRenderer() {
        if (this._baseRenderer === null) {
            return;
        }
        const { TextRenderer } = await Private.ensureDataGrid();
        const rendererConfig = this._baseRenderer;
        const renderer = new TextRenderer({
            textColor: rendererConfig.textColor,
            horizontalAlignment: rendererConfig.horizontalAlignment,
            backgroundColor: this._searchService.cellBackgroundColorRendererFunc(rendererConfig)
        });
        this._grid.cellRenderers.update({
            body: renderer,
            'column-header': renderer,
            'corner-header': renderer,
            'row-header': renderer
        });
    }
}
/**
 * A document widget for CSV content widgets.
 */
class CSVDocumentWidget extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget {
    constructor(options) {
        let { content, context, delimiter, reveal, ...other } = options;
        content = content || Private.createContent(context);
        reveal = Promise.all([reveal, content.revealed]);
        super({ content, context, reveal, ...other });
        if (delimiter) {
            content.delimiter = delimiter;
        }
    }
    /**
     * Set URI fragment identifier for rows
     */
    setFragment(fragment) {
        const parseFragments = fragment.split('=');
        // TODO: expand to allow columns and cells to be selected
        // reference: https://tools.ietf.org/html/rfc7111#section-3
        if (parseFragments[0] !== '#row') {
            return;
        }
        // multiple rows, separated by semi-colons can be provided, we will just
        // go to the top one
        let topRow = parseFragments[1].split(';')[0];
        // a range of rows can be provided, we will take the first value
        topRow = topRow.split('-')[0];
        // go to that row
        void this.context.ready.then(() => {
            this.content.goToLine(Number(topRow));
        });
    }
}
/**
 * A widget factory for CSV widgets.
 */
class CSVViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const translator = this.translator;
        return new CSVDocumentWidget({ context, translator });
    }
    /**
     * Default factory for toolbar items to be added after the widget is created.
     */
    defaultToolbarFactory(widget) {
        return [
            {
                name: 'delimiter',
                widget: new _toolbar__WEBPACK_IMPORTED_MODULE_5__/* .CSVDelimiter */ .p({
                    widget: widget.content,
                    translator: this.translator
                })
            }
        ];
    }
}
/**
 * A widget factory for TSV widgets.
 */
class TSVViewerFactory extends CSVViewerFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const delimiter = '\t';
        return new CSVDocumentWidget({
            context,
            delimiter,
            translator: this.translator
        });
    }
}
var Private;
(function (Private) {
    let gridLoaded = null;
    let modelLoaded = null;
    /**
     * Lazily load the datagrid module when the first grid is requested.
     */
    async function ensureDataGrid() {
        if (gridLoaded == null) {
            gridLoaded = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
            gridLoaded.resolve(await __webpack_require__.e(/* import() */ 2942).then(__webpack_require__.t.bind(__webpack_require__, 99331, 23)));
        }
        return gridLoaded.promise;
    }
    Private.ensureDataGrid = ensureDataGrid;
    async function ensureDSVModel() {
        if (modelLoaded == null) {
            modelLoaded = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
            modelLoaded.resolve(await Promise.all(/* import() */[__webpack_require__.e(2942), __webpack_require__.e(2019)]).then(__webpack_require__.bind(__webpack_require__, 62019)));
        }
        return modelLoaded.promise;
    }
    Private.ensureDSVModel = ensureDSVModel;
    function createContent(context) {
        return new CSVViewer({ context });
    }
    Private.createContent = createContent;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=8296.45a204fbb91a46ce4764.js.map?v=45a204fbb91a46ce4764