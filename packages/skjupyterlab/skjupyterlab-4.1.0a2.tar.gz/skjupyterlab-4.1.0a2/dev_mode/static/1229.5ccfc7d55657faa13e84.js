"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1229],{

/***/ 61229:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "EditorSyntaxStatus": () => (/* reexport */ EditorSyntaxStatus),
  "EditorTableOfContentsFactory": () => (/* reexport */ EditorTableOfContentsFactory),
  "FileEditor": () => (/* reexport */ FileEditor),
  "FileEditorAdapter": () => (/* reexport */ FileEditorAdapter),
  "FileEditorFactory": () => (/* reexport */ FileEditorFactory),
  "FileEditorSearchProvider": () => (/* reexport */ FileEditorSearchProvider),
  "IEditorTracker": () => (/* reexport */ IEditorTracker),
  "LaTeXTableOfContentsFactory": () => (/* reexport */ LaTeXTableOfContentsFactory),
  "LaTeXTableOfContentsModel": () => (/* reexport */ LaTeXTableOfContentsModel),
  "MarkdownTableOfContentsFactory": () => (/* reexport */ MarkdownTableOfContentsFactory),
  "MarkdownTableOfContentsModel": () => (/* reexport */ MarkdownTableOfContentsModel),
  "PythonTableOfContentsFactory": () => (/* reexport */ PythonTableOfContentsFactory),
  "PythonTableOfContentsModel": () => (/* reexport */ PythonTableOfContentsModel),
  "TabSpaceStatus": () => (/* reexport */ TabSpaceStatus)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var index_js_ = __webpack_require__(40200);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/lsp@~4.1.0-alpha.2 (singleton) (fallback: ../packages/lsp/lib/index.js)
var lib_index_js_ = __webpack_require__(84144);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/fileeditor/lib/fileeditorlspadapter.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



class FileEditorAdapter extends lib_index_js_.WidgetLSPAdapter {
    constructor(editorWidget, options) {
        const { docRegistry, ...others } = options;
        super(editorWidget, others);
        this._readyDelegate = new dist_index_js_.PromiseDelegate();
        this.editor = editorWidget.content;
        this._docRegistry = docRegistry;
        // Ensure editor uniqueness
        this._virtualEditor = Object.freeze({
            getEditor: () => this.editor.editor,
            ready: () => Promise.resolve(this.editor.editor),
            reveal: () => Promise.resolve(this.editor.editor)
        });
        Promise.all([this.editor.context.ready, this.connectionManager.ready])
            .then(async () => {
            await this.initOnceReady();
            this._readyDelegate.resolve();
        })
            .catch(console.error);
    }
    /**
     * Promise that resolves once the adapter is initialized
     */
    get ready() {
        return this._readyDelegate.promise;
    }
    /**
     * Get current path of the document.
     */
    get documentPath() {
        return this.widget.context.path;
    }
    /**
     * Get the mime type of the document.
     */
    get mimeType() {
        var _a;
        const mimeTypeFromModel = this.editor.model.mimeType;
        const codeMirrorMimeType = Array.isArray(mimeTypeFromModel)
            ? (_a = mimeTypeFromModel[0]) !== null && _a !== void 0 ? _a : index_js_.IEditorMimeTypeService.defaultMimeType
            : mimeTypeFromModel;
        const contentsModel = this.editor.context.contentsModel;
        // when MIME type is not known it defaults to 'text/plain',
        // so if it is different we can accept it as it is
        if (codeMirrorMimeType != index_js_.IEditorMimeTypeService.defaultMimeType) {
            return codeMirrorMimeType;
        }
        else if (contentsModel) {
            // a script that does not have a MIME type known by the editor
            // (no syntax highlight mode), can still be known by the document
            // registry (and this is arguably easier to extend).
            let fileType = this._docRegistry.getFileTypeForModel(contentsModel);
            return fileType.mimeTypes[0];
        }
        else {
            // "text/plain" this is
            return codeMirrorMimeType;
        }
    }
    /**
     * Get the file extension of the document.
     */
    get languageFileExtension() {
        let parts = this.documentPath.split('.');
        return parts[parts.length - 1];
    }
    /**
     * Get the CM editor
     */
    get ceEditor() {
        return this.editor.editor;
    }
    /**
     * Get the activated CM editor.
     */
    get activeEditor() {
        return this._virtualEditor;
    }
    /**
     * Get the inner HTMLElement of the document widget.
     */
    get wrapperElement() {
        return this.widget.node;
    }
    /**
     * Get current path of the document.
     */
    get path() {
        return this.widget.context.path;
    }
    /**
     *  Get the list of CM editors in the document, there is only one editor
     * in the case of file editor.
     */
    get editors() {
        var _a, _b;
        return [
            {
                ceEditor: this._virtualEditor,
                type: 'code',
                value: (_b = (_a = this.editor) === null || _a === void 0 ? void 0 : _a.model.sharedModel.getSource()) !== null && _b !== void 0 ? _b : ''
            }
        ];
    }
    /**
     * Dispose the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.editor.model.mimeTypeChanged.disconnect(this.reloadConnection);
        super.dispose();
    }
    /**
     * Generate the virtual document associated with the document.
     */
    createVirtualDocument() {
        return new lib_index_js_.VirtualDocument({
            language: this.language,
            foreignCodeExtractors: this.options.foreignCodeExtractorsManager,
            path: this.documentPath,
            fileExtension: this.languageFileExtension,
            // notebooks are continuous, each cell is dependent on the previous one
            standalone: true,
            // notebooks are not supported by LSP servers
            hasLspSupportedFile: true
        });
    }
    /**
     * Get the index of editor from the cursor position in the virtual
     * document. Since there is only one editor, this method always return
     * 0
     * @deprecated This is error-prone and will be removed in JupyterLab 5.0, use `getEditorIndex()` with `virtualDocument.getEditorAtVirtualLine(position)` instead.
     *
     * @param position - the position of cursor in the virtual document.
     * @return  {number} - index of the virtual editor
     */
    getEditorIndexAt(position) {
        return 0;
    }
    /**
     * Get the index of input editor
     *
     * @param ceEditor - instance of the code editor
     */
    getEditorIndex(ceEditor) {
        return 0;
    }
    /**
     * Get the wrapper of input editor.
     *
     * @param ceEditor
     * @return  {HTMLElement}
     */
    getEditorWrapper(ceEditor) {
        return this.wrapperElement;
    }
    /**
     * Initialization function called once the editor and the LSP connection
     * manager is ready. This function will create the virtual document and
     * connect various signals.
     */
    async initOnceReady() {
        this.initVirtual();
        // connect the document, but do not open it as the adapter will handle this
        // after registering all features
        await this.connectDocument(this.virtualDocument, false);
        this.editor.model.mimeTypeChanged.connect(this.reloadConnection, this);
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var apputils_lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codemirror@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codemirror/lib/index.js)
var codemirror_lib_index_js_ = __webpack_require__(29239);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/fileeditor/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The data attribute added to a widget that can run code.
 */
const CODE_RUNNER = 'jpCodeRunner';
/**
 * The data attribute added to a widget that can undo.
 */
const UNDOER = 'jpUndoer';
/**
 * A widget for editors.
 */
class FileEditor extends index_es6_js_.Widget {
    /**
     * Construct a new editor widget.
     */
    constructor(options) {
        super();
        this._ready = new dist_index_js_.PromiseDelegate();
        this.addClass('jp-FileEditor');
        const context = (this._context = options.context);
        this._mimeTypeService = options.mimeTypeService;
        const editorWidget = (this._editorWidget = new index_js_.CodeEditorWrapper({
            factory: options.factory,
            model: context.model,
            editorOptions: {
                config: FileEditor.defaultEditorConfig
            }
        }));
        this._editorWidget.addClass('jp-FileEditorCodeWrapper');
        this._editorWidget.node.dataset[CODE_RUNNER] = 'true';
        this._editorWidget.node.dataset[UNDOER] = 'true';
        this.editor = editorWidget.editor;
        this.model = editorWidget.model;
        void context.ready.then(() => {
            this._onContextReady();
        });
        // Listen for changes to the path.
        this._onPathChanged();
        context.pathChanged.connect(this._onPathChanged, this);
        const layout = (this.layout = new index_es6_js_.StackedLayout());
        layout.addWidget(editorWidget);
    }
    /**
     * Get the context for the editor widget.
     */
    get context() {
        return this._context;
    }
    /**
     * A promise that resolves when the file editor is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the widget's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        if (!this.model) {
            return;
        }
        switch (event.type) {
            case 'mousedown':
                this._ensureFocus();
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        const node = this.node;
        node.addEventListener('mousedown', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('mousedown', this);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this._ensureFocus();
    }
    /**
     * Ensure that the widget has focus.
     */
    _ensureFocus() {
        if (!this.editor.hasFocus()) {
            this.editor.focus();
        }
    }
    /**
     * Handle actions that should be taken when the context is ready.
     */
    _onContextReady() {
        if (this.isDisposed) {
            return;
        }
        // Prevent the initial loading from disk from being in the editor history.
        this.editor.clearHistory();
        // Resolve the ready promise.
        this._ready.resolve(undefined);
    }
    /**
     * Handle a change to the path.
     */
    _onPathChanged() {
        const editor = this.editor;
        const localPath = this._context.localPath;
        editor.model.mimeType =
            this._mimeTypeService.getMimeTypeByFilePath(localPath);
    }
}
/**
 * The namespace for editor widget statics.
 */
(function (FileEditor) {
    /**
     * File editor default configuration.
     */
    FileEditor.defaultEditorConfig = {
        lineNumbers: true,
        scrollPastEnd: true
    };
})(FileEditor || (FileEditor = {}));
/**
 * A widget factory for editors.
 */
class FileEditorFactory extends docregistry_lib_index_js_.ABCWidgetFactory {
    /**
     * Construct a new editor widget factory.
     */
    constructor(options) {
        super(options.factoryOptions);
        this._services = options.editorServices;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const func = this._services.factoryService.newDocumentEditor;
        const factory = options => {
            // Use same id as document factory
            return func(options);
        };
        const content = new FileEditor({
            factory,
            context,
            mimeTypeService: this._services.mimeTypeService
        });
        content.title.icon = ui_components_lib_index_js_.textEditorIcon;
        const widget = new docregistry_lib_index_js_.DocumentWidget({ content, context });
        return widget;
    }
}

;// CONCATENATED MODULE: ../packages/fileeditor/lib/searchprovider.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * File editor search provider
 */
class FileEditorSearchProvider extends codemirror_lib_index_js_.EditorSearchProvider {
    /**
     * Constructor
     * @param widget File editor panel
     */
    constructor(widget) {
        super();
        this.widget = widget;
    }
    get isReadOnly() {
        return this.editor.getOption('readOnly');
    }
    /**
     * Support for options adjusting replacement behavior.
     */
    get replaceOptionsSupport() {
        return {
            preserveCase: true
        };
    }
    /**
     * Text editor
     */
    get editor() {
        return this.widget.content.editor;
    }
    /**
     * Editor content model
     */
    get model() {
        return this.widget.content.model;
    }
    async startQuery(query, filters) {
        await super.startQuery(query, filters);
        await this.highlightNext(true, {
            from: 'selection-start',
            scroll: false,
            select: false
        });
    }
    /**
     * Instantiate a search provider for the widget.
     *
     * #### Notes
     * The widget provided is always checked using `isApplicable` before calling
     * this factory.
     *
     * @param widget The widget to search on
     * @param translator [optional] The translator object
     *
     * @returns The search provider on the widget
     */
    static createNew(widget, translator) {
        return new FileEditorSearchProvider(widget);
    }
    /**
     * Report whether or not this provider has the ability to search on the given object
     */
    static isApplicable(domain) {
        return (domain instanceof apputils_lib_index_js_.MainAreaWidget &&
            domain.content instanceof FileEditor &&
            domain.content.editor instanceof codemirror_lib_index_js_.CodeMirrorEditor);
    }
    /**
     * Get an initial query value if applicable so that it can be entered
     * into the search box as an initial query
     *
     * @returns Initial value used to populate the search box.
     */
    getInitialQuery() {
        const cm = this.editor;
        const selection = cm.state.sliceDoc(cm.state.selection.main.from, cm.state.selection.main.to);
        return selection;
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/fileeditor/lib/syntaxstatus.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */






/**
 * A pure function that returns a tsx component for an editor syntax item.
 *
 * @param props: the props for the component.
 *
 * @returns an editor syntax component.
 */
function EditorSyntaxComponent(props) {
    return react_index_js_default().createElement(statusbar_lib_index_js_.TextItem, { source: props.language, onClick: props.handleClick });
}
/**
 * StatusBar item to change the language syntax highlighting of the file editor.
 */
class EditorSyntaxStatus extends ui_components_lib_index_js_.VDomRenderer {
    /**
     * Construct a new VDomRenderer for the status item.
     */
    constructor(options) {
        var _a;
        super(new EditorSyntaxStatus.Model(options.languages));
        /**
         * Create a menu for selecting the language of the editor.
         */
        this._handleClick = () => {
            const languageMenu = new index_es6_js_.Menu({ commands: this._commands });
            const command = 'fileeditor:change-language';
            if (this._popup) {
                this._popup.dispose();
            }
            this.model.languages
                .getLanguages()
                .sort((a, b) => {
                var _a, _b;
                const aName = (_a = a.displayName) !== null && _a !== void 0 ? _a : a.name;
                const bName = (_b = b.displayName) !== null && _b !== void 0 ? _b : b.name;
                return aName.localeCompare(bName);
            })
                .forEach(spec => {
                var _a;
                if (spec.name.toLowerCase().indexOf('brainf') === 0) {
                    return;
                }
                const args = {
                    name: spec.name,
                    displayName: (_a = spec.displayName) !== null && _a !== void 0 ? _a : spec.name
                };
                languageMenu.addItem({
                    command,
                    args
                });
            });
            this._popup = (0,statusbar_lib_index_js_.showPopup)({
                body: languageMenu,
                anchor: this,
                align: 'left'
            });
        };
        this._popup = null;
        this._commands = options.commands;
        this.translator = (_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        this.addClass('jp-mod-highlighted');
        this.title.caption = trans.__('Change text editor syntax highlighting');
    }
    /**
     * Render the status item.
     */
    render() {
        if (!this.model) {
            return null;
        }
        return (react_index_js_default().createElement(EditorSyntaxComponent, { language: this.model.language, handleClick: this._handleClick }));
    }
}
/**
 * A namespace for EditorSyntax statics.
 */
(function (EditorSyntaxStatus) {
    /**
     * A VDomModel for the current editor/mode combination.
     */
    class Model extends ui_components_lib_index_js_.VDomModel {
        constructor(languages) {
            super();
            this.languages = languages;
            /**
             * If the editor mode changes, update the model.
             */
            this._onMIMETypeChange = (mode, change) => {
                var _a;
                const oldLanguage = this._language;
                const spec = this.languages.findByMIME(change.newValue);
                this._language = (_a = spec === null || spec === void 0 ? void 0 : spec.name) !== null && _a !== void 0 ? _a : index_js_.IEditorMimeTypeService.defaultMimeType;
                this._triggerChange(oldLanguage, this._language);
            };
            this._language = '';
            this._editor = null;
        }
        /**
         * The current editor language. If no editor is present,
         * returns the empty string.
         */
        get language() {
            return this._language;
        }
        /**
         * The current editor for the application editor tracker.
         */
        get editor() {
            return this._editor;
        }
        set editor(editor) {
            var _a;
            const oldEditor = this._editor;
            if (oldEditor !== null) {
                oldEditor.model.mimeTypeChanged.disconnect(this._onMIMETypeChange);
            }
            const oldLanguage = this._language;
            this._editor = editor;
            if (this._editor === null) {
                this._language = '';
            }
            else {
                const spec = this.languages.findByMIME(this._editor.model.mimeType);
                this._language = (_a = spec === null || spec === void 0 ? void 0 : spec.name) !== null && _a !== void 0 ? _a : index_js_.IEditorMimeTypeService.defaultMimeType;
                this._editor.model.mimeTypeChanged.connect(this._onMIMETypeChange);
            }
            this._triggerChange(oldLanguage, this._language);
        }
        /**
         * Trigger a rerender of the model.
         */
        _triggerChange(oldState, newState) {
            if (oldState !== newState) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    EditorSyntaxStatus.Model = Model;
})(EditorSyntaxStatus || (EditorSyntaxStatus = {}));

;// CONCATENATED MODULE: ../packages/fileeditor/lib/tabspacestatus.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A pure functional component for rendering the TabSpace status.
 */
function TabSpaceComponent(props) {
    const translator = props.translator || translation_lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    const description = typeof props.tabSpace === 'number'
        ? trans.__('Spaces')
        : trans.__('Tab Indent');
    return (react_index_js_default().createElement(statusbar_lib_index_js_.TextItem, { onClick: props.handleClick, source: typeof props.tabSpace === 'number'
            ? `${description}: ${props.tabSpace}`
            : description, title: trans.__('Change the indentation…') }));
}
/**
 * A VDomRenderer for a tabs vs. spaces status item.
 */
class TabSpaceStatus extends ui_components_lib_index_js_.VDomRenderer {
    /**
     * Create a new tab/space status item.
     */
    constructor(options) {
        super(new TabSpaceStatus.Model());
        this._popup = null;
        this._menu = options.menu;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this.addClass('jp-mod-highlighted');
    }
    /**
     * Render the TabSpace status item.
     */
    render() {
        var _a;
        if (!((_a = this.model) === null || _a === void 0 ? void 0 : _a.indentUnit)) {
            return null;
        }
        else {
            const tabSpace = this.model.indentUnit === 'Tab'
                ? null
                : parseInt(this.model.indentUnit, 10);
            return (react_index_js_default().createElement(TabSpaceComponent, { tabSpace: tabSpace, handleClick: () => this._handleClick(), translator: this.translator }));
        }
    }
    /**
     * Handle a click on the status item.
     */
    _handleClick() {
        const menu = this._menu;
        if (this._popup) {
            this._popup.dispose();
        }
        menu.aboutToClose.connect(this._menuClosed, this);
        this._popup = (0,statusbar_lib_index_js_.showPopup)({
            body: menu,
            anchor: this,
            align: 'right'
        });
        // Update the menu items
        menu.update();
    }
    _menuClosed() {
        this.removeClass('jp-mod-clicked');
    }
}
/**
 * A namespace for TabSpace statics.
 */
(function (TabSpaceStatus) {
    /**
     * A VDomModel for the TabSpace status item.
     */
    class Model extends ui_components_lib_index_js_.VDomModel {
        /**
         * Code editor indentation unit
         */
        get indentUnit() {
            return this._indentUnit;
        }
        set indentUnit(v) {
            if (v !== this._indentUnit) {
                this._indentUnit = v;
                this.stateChanged.emit();
            }
        }
    }
    TabSpaceStatus.Model = Model;
})(TabSpaceStatus || (TabSpaceStatus = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/toc@~6.1.0-alpha.2 (singleton) (fallback: ../packages/toc/lib/index.js)
var toc_lib_index_js_ = __webpack_require__(95691);
;// CONCATENATED MODULE: ../packages/fileeditor/lib/toc/factory.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Base table of contents model factory for file editor
 */
class EditorTableOfContentsFactory extends toc_lib_index_js_.TableOfContentsFactory {
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    createNew(widget, configuration) {
        const model = super.createNew(widget, configuration);
        const onActiveHeadingChanged = (model, heading) => {
            if (heading) {
                widget.content.editor.setCursorPosition({
                    line: heading.line,
                    column: 0
                });
            }
        };
        model.activeHeadingChanged.connect(onActiveHeadingChanged);
        widget.disposed.connect(() => {
            model.activeHeadingChanged.disconnect(onActiveHeadingChanged);
        });
        return model;
    }
}

;// CONCATENATED MODULE: ../packages/fileeditor/lib/toc/latex.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Maps LaTeX section headings to HTML header levels.
 *
 * ## Notes
 *
 * -   As `part` and `chapter` section headings appear to be less common, assign them to heading level 1.
 *
 * @private
 */
const LATEX_LEVELS = {
    part: 1,
    chapter: 1,
    section: 1,
    subsection: 2,
    subsubsection: 3,
    paragraph: 4,
    subparagraph: 5
};
/**
 * Regular expression to create the outline
 */
const SECTIONS = /^\s*\\(section|subsection|subsubsection){(.+)}/;
/**
 * Table of content model for LaTeX files.
 */
class LaTeXTableOfContentsModel extends toc_lib_index_js_.TableOfContentsModel {
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType() {
        return 'latex';
    }
    /**
     * List of configuration options supported by the model.
     */
    get supportedOptions() {
        return ['maximalDepth', 'numberHeaders'];
    }
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    getHeadings() {
        if (!this.isActive) {
            return Promise.resolve(null);
        }
        // Split the text into lines:
        const lines = this.widget.content.model.sharedModel
            .getSource()
            .split('\n');
        const levels = new Array();
        let previousLevel = levels.length;
        const headings = new Array();
        for (let i = 0; i < lines.length; i++) {
            const match = lines[i].match(SECTIONS);
            if (match) {
                const level = LATEX_LEVELS[match[1]];
                if (level <= this.configuration.maximalDepth) {
                    const prefix = toc_lib_index_js_.TableOfContentsUtils.getPrefix(level, previousLevel, levels, {
                        ...this.configuration,
                        // Force base numbering and numbering first level
                        baseNumbering: 1,
                        numberingH1: true
                    });
                    previousLevel = level;
                    headings.push({
                        text: match[2],
                        prefix: prefix,
                        level,
                        line: i
                    });
                }
            }
        }
        return Promise.resolve(headings);
    }
}
/**
 * Table of content model factory for LaTeX files.
 */
class LaTeXTableOfContentsFactory extends EditorTableOfContentsFactory {
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget) {
        var _a, _b;
        const isApplicable = super.isApplicable(widget);
        if (isApplicable) {
            let mime = (_b = (_a = widget.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.mimeType;
            return mime && (mime === 'text/x-latex' || mime === 'text/x-stex');
        }
        return false;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    _createNew(widget, configuration) {
        return new LaTeXTableOfContentsModel(widget, configuration);
    }
}

;// CONCATENATED MODULE: ../packages/fileeditor/lib/toc/markdown.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Table of content model for Markdown files.
 */
class MarkdownTableOfContentsModel extends toc_lib_index_js_.TableOfContentsModel {
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType() {
        return 'markdown';
    }
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    getHeadings() {
        if (!this.isActive) {
            return Promise.resolve(null);
        }
        const content = this.widget.content.model.sharedModel.getSource();
        const headings = toc_lib_index_js_.TableOfContentsUtils.filterHeadings(toc_lib_index_js_.TableOfContentsUtils.Markdown.getHeadings(content), {
            ...this.configuration,
            // Force removing numbering as they cannot be displayed
            // in the document
            numberHeaders: false
        });
        return Promise.resolve(headings);
    }
}
/**
 * Table of content model factory for Markdown files.
 */
class MarkdownTableOfContentsFactory extends EditorTableOfContentsFactory {
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget) {
        var _a, _b;
        const isApplicable = super.isApplicable(widget);
        if (isApplicable) {
            let mime = (_b = (_a = widget.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.mimeType;
            return mime && toc_lib_index_js_.TableOfContentsUtils.Markdown.isMarkdown(mime);
        }
        return false;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    _createNew(widget, configuration) {
        return new MarkdownTableOfContentsModel(widget, configuration);
    }
}

;// CONCATENATED MODULE: ../packages/fileeditor/lib/toc/python.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Regular expression to create the outline
 */
let KEYWORDS;
try {
    // https://github.com/tc39/proposal-regexp-match-indices was accepted
    // in May 2021 (https://github.com/tc39/proposals/blob/main/finished-proposals.md)
    // So we will fallback to the polyfill regexp-match-indices if not available
    KEYWORDS = new RegExp('^\\s*(class |def |from |import )', 'd');
}
catch (_a) {
    KEYWORDS = new RegExp('^\\s*(class |def |from |import )');
}
/**
 * Table of content model for Python files.
 */
class PythonTableOfContentsModel extends toc_lib_index_js_.TableOfContentsModel {
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType() {
        return 'python';
    }
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    async getHeadings() {
        if (!this.isActive) {
            return Promise.resolve(null);
        }
        // Split the text into lines:
        const lines = this.widget.content.model.sharedModel
            .getSource()
            .split('\n');
        // Iterate over the lines to get the heading level and text for each line:
        let headings = new Array();
        let processingImports = false;
        let indent = 1;
        let lineIdx = -1;
        for (const line of lines) {
            lineIdx++;
            let hasKeyword;
            if (KEYWORDS.flags.includes('d')) {
                hasKeyword = KEYWORDS.exec(line);
            }
            else {
                const { default: execWithIndices } = await __webpack_require__.e(/* import() */ 2913).then(__webpack_require__.t.bind(__webpack_require__, 32913, 23));
                hasKeyword = execWithIndices(KEYWORDS, line);
            }
            if (hasKeyword) {
                // Index 0 contains the spaces, index 1 is the keyword group
                const [start] = hasKeyword.indices[1];
                if (indent === 1 && start > 0) {
                    indent = start;
                }
                const isImport = ['from ', 'import '].includes(hasKeyword[1]);
                if (isImport && processingImports) {
                    continue;
                }
                processingImports = isImport;
                const level = 1 + start / indent;
                if (level > this.configuration.maximalDepth) {
                    continue;
                }
                headings.push({
                    text: line.slice(start),
                    level,
                    line: lineIdx
                });
            }
        }
        return Promise.resolve(headings);
    }
}
/**
 * Table of content model factory for Python files.
 */
class PythonTableOfContentsFactory extends EditorTableOfContentsFactory {
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget) {
        var _a, _b;
        const isApplicable = super.isApplicable(widget);
        if (isApplicable) {
            let mime = (_b = (_a = widget.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.mimeType;
            return (mime &&
                (mime === 'application/x-python-code' || mime === 'text/x-python'));
        }
        return false;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    _createNew(widget, configuration) {
        return new PythonTableOfContentsModel(widget, configuration);
    }
}

;// CONCATENATED MODULE: ../packages/fileeditor/lib/toc/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





;// CONCATENATED MODULE: ../packages/fileeditor/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The editor tracker token.
 */
const IEditorTracker = new dist_index_js_.Token('@jupyterlab/fileeditor:IEditorTracker', `A widget tracker for file editors.
  Use this if you want to be able to iterate over and interact with file editors
  created by the application.`);

;// CONCATENATED MODULE: ../packages/fileeditor/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module fileeditor
 */









/***/ })

}]);
//# sourceMappingURL=1229.5ccfc7d55657faa13e84.js.map?v=5ccfc7d55657faa13e84