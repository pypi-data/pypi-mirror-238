"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[9701],{

/***/ 99701:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "Commands": () => (/* reexport */ Commands),
  "default": () => (/* binding */ lib),
  "tabSpaceStatus": () => (/* binding */ tabSpaceStatus)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/application@~4.1.0-alpha.2 (singleton) (fallback: ../packages/application/lib/index.js)
var index_js_ = __webpack_require__(65681);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var codeeditor_lib_index_js_ = __webpack_require__(40200);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codemirror@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codemirror/lib/index.js)
var codemirror_lib_index_js_ = __webpack_require__(29239);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/completer@~4.1.0-alpha.2 (singleton) (fallback: ../packages/completer/lib/index.js)
var completer_lib_index_js_ = __webpack_require__(4532);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/console@~4.1.0-alpha.2 (singleton) (fallback: ../packages/console/lib/index.js)
var console_lib_index_js_ = __webpack_require__(2116);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/documentsearch@~4.1.0-alpha.2 (singleton) (fallback: ../packages/documentsearch/lib/index.js)
var documentsearch_lib_index_js_ = __webpack_require__(80599);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/filebrowser@~4.1.0-alpha.2 (singleton) (fallback: ../packages/filebrowser/lib/index.js)
var filebrowser_lib_index_js_ = __webpack_require__(35855);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/fileeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/fileeditor/lib/index.js)
var fileeditor_lib_index_js_ = __webpack_require__(35012);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/launcher@~4.1.0-alpha.2 (singleton) (fallback: ../packages/launcher/lib/index.js)
var launcher_lib_index_js_ = __webpack_require__(45534);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/lsp@~4.1.0-alpha.2 (singleton) (fallback: ../packages/lsp/lib/index.js)
var lsp_lib_index_js_ = __webpack_require__(84144);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/mainmenu@~4.1.0-alpha.2 (singleton) (fallback: ../packages/mainmenu/lib/index.js)
var mainmenu_lib_index_js_ = __webpack_require__(5184);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var settingregistry_lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/toc@~6.1.0-alpha.2 (singleton) (fallback: ../packages/toc/lib/index.js)
var toc_lib_index_js_ = __webpack_require__(95691);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @codemirror/commands@^6.2.3 (strict) (fallback: ../node_modules/@codemirror/commands/dist/index.js)
var dist_index_js_ = __webpack_require__(83861);
// EXTERNAL MODULE: consume shared module (default) @codemirror/search@^6.3.0 (strict) (fallback: ../node_modules/@codemirror/search/dist/index.js)
var search_dist_index_js_ = __webpack_require__(35260);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
;// CONCATENATED MODULE: ../packages/fileeditor-extension/lib/commands.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








const autoClosingBracketsNotebook = 'notebook:toggle-autoclosing-brackets';
const autoClosingBracketsConsole = 'console:toggle-autoclosing-brackets';
/**
 * The command IDs used by the fileeditor plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'fileeditor:create-new';
    CommandIDs.createNewMarkdown = 'fileeditor:create-new-markdown-file';
    CommandIDs.changeFontSize = 'fileeditor:change-font-size';
    CommandIDs.lineNumbers = 'fileeditor:toggle-line-numbers';
    CommandIDs.currentLineNumbers = 'fileeditor:toggle-current-line-numbers';
    CommandIDs.lineWrap = 'fileeditor:toggle-line-wrap';
    CommandIDs.currentLineWrap = 'fileeditor:toggle-current-line-wrap';
    CommandIDs.changeTabs = 'fileeditor:change-tabs';
    CommandIDs.matchBrackets = 'fileeditor:toggle-match-brackets';
    CommandIDs.currentMatchBrackets = 'fileeditor:toggle-current-match-brackets';
    CommandIDs.autoClosingBrackets = 'fileeditor:toggle-autoclosing-brackets';
    CommandIDs.autoClosingBracketsUniversal = 'fileeditor:toggle-autoclosing-brackets-universal';
    CommandIDs.createConsole = 'fileeditor:create-console';
    CommandIDs.replaceSelection = 'fileeditor:replace-selection';
    CommandIDs.restartConsole = 'fileeditor:restart-console';
    CommandIDs.runCode = 'fileeditor:run-code';
    CommandIDs.runAllCode = 'fileeditor:run-all';
    CommandIDs.markdownPreview = 'fileeditor:markdown-preview';
    CommandIDs.undo = 'fileeditor:undo';
    CommandIDs.redo = 'fileeditor:redo';
    CommandIDs.cut = 'fileeditor:cut';
    CommandIDs.copy = 'fileeditor:copy';
    CommandIDs.paste = 'fileeditor:paste';
    CommandIDs.selectAll = 'fileeditor:select-all';
    CommandIDs.invokeCompleter = 'completer:invoke-file';
    CommandIDs.selectCompleter = 'completer:select-file';
    CommandIDs.openCodeViewer = 'code-viewer:open';
    CommandIDs.changeTheme = 'fileeditor:change-theme';
    CommandIDs.changeLanguage = 'fileeditor:change-language';
    CommandIDs.find = 'fileeditor:find';
    CommandIDs.goToLine = 'fileeditor:go-to-line';
})(CommandIDs || (CommandIDs = {}));
/**
 * The name of the factory that creates editor widgets.
 */
const FACTORY = 'Editor';
/**
 * A utility class for adding commands and menu items,
 * for use by the File Editor extension or other Editor extensions.
 */
var Commands;
(function (Commands) {
    let config = {};
    let scrollPastEnd = true;
    /**
     * Accessor function that returns the createConsole function for use by Create Console commands
     */
    function getCreateConsoleFunction(commands, languages) {
        return async function createConsole(widget, args) {
            var _a, _b, _c;
            const options = args || {};
            const console = await commands.execute('console:create', {
                activate: options['activate'],
                name: (_a = widget.context.contentsModel) === null || _a === void 0 ? void 0 : _a.name,
                path: widget.context.path,
                // Default value is an empty string -> using OR operator
                preferredLanguage: widget.context.model.defaultKernelLanguage ||
                    ((_c = (_b = languages.findByFileName(widget.context.path)) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : ''),
                ref: widget.id,
                insertMode: 'split-bottom'
            });
            widget.context.pathChanged.connect((sender, value) => {
                var _a;
                console.session.setPath(value);
                console.session.setName((_a = widget.context.contentsModel) === null || _a === void 0 ? void 0 : _a.name);
            });
        };
    }
    /**
     * Update the setting values.
     */
    function updateSettings(settings, commands) {
        var _a;
        config =
            (_a = settings.get('editorConfig').composite) !== null && _a !== void 0 ? _a : {};
        scrollPastEnd = settings.get('scrollPasteEnd').composite;
        // Trigger a refresh of the rendered commands
        commands.notifyCommandChanged(CommandIDs.lineNumbers);
        commands.notifyCommandChanged(CommandIDs.currentLineNumbers);
        commands.notifyCommandChanged(CommandIDs.lineWrap);
        commands.notifyCommandChanged(CommandIDs.currentLineWrap);
        commands.notifyCommandChanged(CommandIDs.changeTabs);
        commands.notifyCommandChanged(CommandIDs.matchBrackets);
        commands.notifyCommandChanged(CommandIDs.currentMatchBrackets);
        commands.notifyCommandChanged(CommandIDs.autoClosingBrackets);
        commands.notifyCommandChanged(CommandIDs.changeLanguage);
    }
    Commands.updateSettings = updateSettings;
    /**
     * Update the settings of the current tracker instances.
     */
    function updateTracker(tracker) {
        tracker.forEach(widget => {
            updateWidget(widget.content);
        });
    }
    Commands.updateTracker = updateTracker;
    /**
     * Update the settings of a widget.
     * Skip global settings for transient editor specific configs.
     */
    function updateWidget(widget) {
        const editor = widget.editor;
        editor.setOptions({ ...config, scrollPastEnd });
    }
    Commands.updateWidget = updateWidget;
    /**
     * Wrapper function for adding the default File Editor commands
     */
    function addCommands(commands, settingRegistry, trans, id, isEnabled, tracker, defaultBrowser, extensions, languages, consoleTracker, sessionDialogs) {
        /**
         * Add a command to change font size for File Editor
         */
        commands.addCommand(CommandIDs.changeFontSize, {
            execute: args => {
                var _a;
                const delta = Number(args['delta']);
                if (Number.isNaN(delta)) {
                    console.error(`${CommandIDs.changeFontSize}: delta arg must be a number`);
                    return;
                }
                const style = window.getComputedStyle(document.documentElement);
                const cssSize = parseInt(style.getPropertyValue('--jp-code-font-size'), 10);
                const currentSize = ((_a = config['customStyles']['fontSize']) !== null && _a !== void 0 ? _a : extensions.baseConfiguration['customStyles']['fontSize']) ||
                    cssSize;
                config.fontSize = currentSize + delta;
                return settingRegistry
                    .set(id, 'editorConfig', config)
                    .catch((reason) => {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                });
            },
            label: args => {
                const delta = Number(args['delta']);
                if (Number.isNaN(delta)) {
                    console.error(`${CommandIDs.changeFontSize}: delta arg must be a number`);
                }
                if (delta > 0) {
                    return args.isMenu
                        ? trans.__('Increase Text Editor Font Size')
                        : trans.__('Increase Font Size');
                }
                else {
                    return args.isMenu
                        ? trans.__('Decrease Text Editor Font Size')
                        : trans.__('Decrease Font Size');
                }
            }
        });
        /**
         * Add the Line Numbers command
         */
        commands.addCommand(CommandIDs.lineNumbers, {
            execute: async () => {
                var _a;
                config.lineNumbers = !((_a = config.lineNumbers) !== null && _a !== void 0 ? _a : extensions.baseConfiguration.lineNumbers);
                try {
                    return await settingRegistry.set(id, 'editorConfig', config);
                }
                catch (reason) {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                }
            },
            isEnabled,
            isToggled: () => { var _a; return (_a = config.lineNumbers) !== null && _a !== void 0 ? _a : extensions.baseConfiguration.lineNumbers; },
            label: trans.__('Show Line Numbers')
        });
        commands.addCommand(CommandIDs.currentLineNumbers, {
            label: trans.__('Show Line Numbers'),
            caption: trans.__('Show the line numbers for the current file.'),
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const lineNumbers = !widget.content.editor.getOption('lineNumbers');
                widget.content.editor.setOption('lineNumbers', lineNumbers);
            },
            isEnabled,
            isToggled: () => {
                var _a;
                const widget = tracker.currentWidget;
                return ((_a = widget === null || widget === void 0 ? void 0 : widget.content.editor.getOption('lineNumbers')) !== null && _a !== void 0 ? _a : false);
            }
        });
        /**
         * Add the Word Wrap command
         */
        commands.addCommand(CommandIDs.lineWrap, {
            execute: async (args) => {
                var _a;
                config.lineWrap = (_a = args['mode']) !== null && _a !== void 0 ? _a : false;
                try {
                    return await settingRegistry.set(id, 'editorConfig', config);
                }
                catch (reason) {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                }
            },
            isEnabled,
            isToggled: args => {
                var _a, _b;
                const lineWrap = (_a = args['mode']) !== null && _a !== void 0 ? _a : false;
                return (lineWrap ===
                    ((_b = config.lineWrap) !== null && _b !== void 0 ? _b : extensions.baseConfiguration.lineWrap));
            },
            label: trans.__('Word Wrap')
        });
        commands.addCommand(CommandIDs.currentLineWrap, {
            label: trans.__('Wrap Words'),
            caption: trans.__('Wrap words for the current file.'),
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const oldValue = widget.content.editor.getOption('lineWrap');
                widget.content.editor.setOption('lineWrap', !oldValue);
            },
            isEnabled,
            isToggled: () => {
                var _a;
                const widget = tracker.currentWidget;
                return ((_a = widget === null || widget === void 0 ? void 0 : widget.content.editor.getOption('lineWrap')) !== null && _a !== void 0 ? _a : false);
            }
        });
        /**
         * Add command for changing tabs size or type in File Editor
         */
        commands.addCommand(CommandIDs.changeTabs, {
            label: args => {
                var _a;
                if (args.size) {
                    // Use a context to differentiate with string set as plural in 3.x
                    return trans._p('v4', 'Spaces: %1', (_a = args.size) !== null && _a !== void 0 ? _a : '');
                }
                else {
                    return trans.__('Indent with Tab');
                }
            },
            execute: async (args) => {
                var _a;
                config.indentUnit =
                    args['size'] !== undefined
                        ? ((_a = args['size']) !== null && _a !== void 0 ? _a : '4').toString()
                        : 'Tab';
                try {
                    return await settingRegistry.set(id, 'editorConfig', config);
                }
                catch (reason) {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                }
            },
            isToggled: args => {
                var _a;
                const currentIndentUnit = (_a = config.indentUnit) !== null && _a !== void 0 ? _a : extensions.baseConfiguration.indentUnit;
                return args['size']
                    ? args['size'] === currentIndentUnit
                    : 'Tab' == currentIndentUnit;
            }
        });
        /**
         * Add the Match Brackets command
         */
        commands.addCommand(CommandIDs.matchBrackets, {
            execute: async () => {
                var _a;
                config.matchBrackets = !((_a = config.matchBrackets) !== null && _a !== void 0 ? _a : extensions.baseConfiguration.matchBrackets);
                try {
                    return await settingRegistry.set(id, 'editorConfig', config);
                }
                catch (reason) {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                }
            },
            label: trans.__('Match Brackets'),
            isEnabled,
            isToggled: () => { var _a; return (_a = config.matchBrackets) !== null && _a !== void 0 ? _a : extensions.baseConfiguration.matchBrackets; }
        });
        commands.addCommand(CommandIDs.currentMatchBrackets, {
            label: trans.__('Match Brackets'),
            caption: trans.__('Change match brackets for the current file.'),
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const matchBrackets = !widget.content.editor.getOption('matchBrackets');
                widget.content.editor.setOption('matchBrackets', matchBrackets);
            },
            isEnabled,
            isToggled: () => {
                var _a;
                const widget = tracker.currentWidget;
                return ((_a = widget === null || widget === void 0 ? void 0 : widget.content.editor.getOption('matchBrackets')) !== null && _a !== void 0 ? _a : false);
            }
        });
        /**
         * Add the Auto Close Brackets for Text Editor command
         */
        commands.addCommand(CommandIDs.autoClosingBrackets, {
            execute: async (args) => {
                var _a, _b;
                config.autoClosingBrackets = !!((_a = args['force']) !== null && _a !== void 0 ? _a : !((_b = config.autoClosingBrackets) !== null && _b !== void 0 ? _b : extensions.baseConfiguration.autoClosingBrackets));
                try {
                    return await settingRegistry.set(id, 'editorConfig', config);
                }
                catch (reason) {
                    console.error(`Failed to set ${id}: ${reason.message}`);
                }
            },
            label: trans.__('Auto Close Brackets in Text Editor'),
            isToggled: () => {
                var _a;
                return (_a = config.autoClosingBrackets) !== null && _a !== void 0 ? _a : extensions.baseConfiguration.autoClosingBrackets;
            }
        });
        commands.addCommand(CommandIDs.autoClosingBracketsUniversal, {
            execute: () => {
                const anyToggled = commands.isToggled(CommandIDs.autoClosingBrackets) ||
                    commands.isToggled(autoClosingBracketsNotebook) ||
                    commands.isToggled(autoClosingBracketsConsole);
                // if any auto closing brackets options is toggled, toggle both off
                if (anyToggled) {
                    void commands.execute(CommandIDs.autoClosingBrackets, {
                        force: false
                    });
                    void commands.execute(autoClosingBracketsNotebook, { force: false });
                    void commands.execute(autoClosingBracketsConsole, { force: false });
                }
                else {
                    // both are off, turn them on
                    void commands.execute(CommandIDs.autoClosingBrackets, {
                        force: true
                    });
                    void commands.execute(autoClosingBracketsNotebook, { force: true });
                    void commands.execute(autoClosingBracketsConsole, { force: true });
                }
            },
            label: trans.__('Auto Close Brackets'),
            isToggled: () => commands.isToggled(CommandIDs.autoClosingBrackets) ||
                commands.isToggled(autoClosingBracketsNotebook) ||
                commands.isToggled(autoClosingBracketsConsole)
        });
        /**
         * Create a menu for the editor.
         */
        commands.addCommand(CommandIDs.changeTheme, {
            label: args => {
                var _a, _b, _c, _d;
                return (_d = (_c = (_b = ((_a = args.displayName) !== null && _a !== void 0 ? _a : args.theme)) !== null && _b !== void 0 ? _b : config.theme) !== null && _c !== void 0 ? _c : extensions.baseConfiguration.theme) !== null && _d !== void 0 ? _d : trans.__('Editor Theme');
            },
            execute: async (args) => {
                var _a;
                config.theme = (_a = args['theme']) !== null && _a !== void 0 ? _a : config.theme;
                try {
                    return await settingRegistry.set(id, 'editorConfig', config);
                }
                catch (reason) {
                    console.error(`Failed to set theme - ${reason.message}`);
                }
            },
            isToggled: args => { var _a; return args['theme'] === ((_a = config.theme) !== null && _a !== void 0 ? _a : extensions.baseConfiguration.theme); }
        });
        commands.addCommand(CommandIDs.find, {
            label: trans.__('Find…'),
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const editor = widget.content.editor;
                editor.execCommand(search_dist_index_js_.findNext);
            },
            isEnabled
        });
        commands.addCommand(CommandIDs.goToLine, {
            label: trans.__('Go to Line…'),
            execute: args => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const editor = widget.content.editor;
                const line = args['line'];
                const column = args['column'];
                if (line !== undefined || column !== undefined) {
                    editor.setCursorPosition({
                        line: (line !== null && line !== void 0 ? line : 1) - 1,
                        column: (column !== null && column !== void 0 ? column : 1) - 1
                    });
                }
                else {
                    editor.execCommand(search_dist_index_js_.gotoLine);
                }
            },
            isEnabled
        });
        commands.addCommand(CommandIDs.changeLanguage, {
            label: args => {
                var _a, _b;
                return (_b = ((_a = args['displayName']) !== null && _a !== void 0 ? _a : args['name'])) !== null && _b !== void 0 ? _b : trans.__('Change editor language.');
            },
            execute: args => {
                var _a;
                const name = args['name'];
                const widget = tracker.currentWidget;
                if (name && widget) {
                    const spec = languages.findByName(name);
                    if (spec) {
                        if (Array.isArray(spec.mime)) {
                            widget.content.model.mimeType =
                                (_a = spec.mime[0]) !== null && _a !== void 0 ? _a : codeeditor_lib_index_js_.IEditorMimeTypeService.defaultMimeType;
                        }
                        else {
                            widget.content.model.mimeType = spec.mime;
                        }
                    }
                }
            },
            isEnabled,
            isToggled: args => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return false;
                }
                const mime = widget.content.model.mimeType;
                const spec = languages.findByMIME(mime);
                const name = spec && spec.name;
                return args['name'] === name;
            }
        });
        /**
         * Add the replace selection for text editor command
         */
        commands.addCommand(CommandIDs.replaceSelection, {
            execute: args => {
                var _a, _b;
                const text = args['text'] || '';
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                (_b = (_a = widget.content.editor).replaceSelection) === null || _b === void 0 ? void 0 : _b.call(_a, text);
            },
            isEnabled,
            label: trans.__('Replace Selection in Editor')
        });
        /**
         * Add the Create Console for Editor command
         */
        commands.addCommand(CommandIDs.createConsole, {
            execute: args => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                return getCreateConsoleFunction(commands, languages)(widget, args);
            },
            isEnabled,
            icon: ui_components_lib_index_js_.consoleIcon,
            label: trans.__('Create Console for Editor')
        });
        /**
         * Restart the Console Kernel linked to the current Editor
         */
        commands.addCommand(CommandIDs.restartConsole, {
            execute: async () => {
                var _a;
                const current = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!current || consoleTracker === null) {
                    return;
                }
                const widget = consoleTracker.find(widget => { var _a; return ((_a = widget.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) === current.context.path; });
                if (widget) {
                    return sessionDialogs.restart(widget.sessionContext);
                }
            },
            label: trans.__('Restart Kernel'),
            isEnabled: () => consoleTracker !== null && isEnabled()
        });
        /**
         * Add the Run Code command
         */
        commands.addCommand(CommandIDs.runCode, {
            execute: () => {
                var _a;
                // Run the appropriate code, taking into account a ```fenced``` code block.
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                let code = '';
                const editor = widget.editor;
                const path = widget.context.path;
                const extension = coreutils_lib_index_js_.PathExt.extname(path);
                const selection = editor.getSelection();
                const { start, end } = selection;
                let selected = start.column !== end.column || start.line !== end.line;
                if (selected) {
                    // Get the selected code from the editor.
                    const start = editor.getOffsetAt(selection.start);
                    const end = editor.getOffsetAt(selection.end);
                    code = editor.model.sharedModel.getSource().substring(start, end);
                }
                else if (coreutils_lib_index_js_.MarkdownCodeBlocks.isMarkdown(extension)) {
                    const text = editor.model.sharedModel.getSource();
                    const blocks = coreutils_lib_index_js_.MarkdownCodeBlocks.findMarkdownCodeBlocks(text);
                    for (const block of blocks) {
                        if (block.startLine <= start.line && start.line <= block.endLine) {
                            code = block.code;
                            selected = true;
                            break;
                        }
                    }
                }
                if (!selected) {
                    // no selection, submit whole line and advance
                    code = editor.getLine(selection.start.line);
                    const cursor = editor.getCursorPosition();
                    if (cursor.line + 1 === editor.lineCount) {
                        const text = editor.model.sharedModel.getSource();
                        editor.model.sharedModel.setSource(text + '\n');
                    }
                    editor.setCursorPosition({
                        line: cursor.line + 1,
                        column: cursor.column
                    });
                }
                const activate = false;
                if (code) {
                    return commands.execute('console:inject', { activate, code, path });
                }
                else {
                    return Promise.resolve(void 0);
                }
            },
            isEnabled,
            label: trans.__('Run Selected Code')
        });
        /**
         * Add the Run All Code command
         */
        commands.addCommand(CommandIDs.runAllCode, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                let code = '';
                const editor = widget.editor;
                const text = editor.model.sharedModel.getSource();
                const path = widget.context.path;
                const extension = coreutils_lib_index_js_.PathExt.extname(path);
                if (coreutils_lib_index_js_.MarkdownCodeBlocks.isMarkdown(extension)) {
                    // For Markdown files, run only code blocks.
                    const blocks = coreutils_lib_index_js_.MarkdownCodeBlocks.findMarkdownCodeBlocks(text);
                    for (const block of blocks) {
                        code += block.code;
                    }
                }
                else {
                    code = text;
                }
                const activate = false;
                if (code) {
                    return commands.execute('console:inject', { activate, code, path });
                }
                else {
                    return Promise.resolve(void 0);
                }
            },
            isEnabled,
            label: trans.__('Run All Code')
        });
        /**
         * Add markdown preview command
         */
        commands.addCommand(CommandIDs.markdownPreview, {
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const path = widget.context.path;
                return commands.execute('markdownviewer:open', {
                    path,
                    options: {
                        mode: 'split-right'
                    }
                });
            },
            isVisible: () => {
                const widget = tracker.currentWidget;
                return ((widget && coreutils_lib_index_js_.PathExt.extname(widget.context.path) === '.md') || false);
            },
            icon: ui_components_lib_index_js_.markdownIcon,
            label: trans.__('Show Markdown Preview')
        });
        /**
         * Add the New File command
         *
         * Defaults to Text/.txt if file type data is not specified
         */
        commands.addCommand(CommandIDs.createNew, {
            label: args => {
                var _a, _b;
                if (args.isPalette) {
                    return (_a = args.paletteLabel) !== null && _a !== void 0 ? _a : trans.__('New Text File');
                }
                return (_b = args.launcherLabel) !== null && _b !== void 0 ? _b : trans.__('Text File');
            },
            caption: args => { var _a; return (_a = args.caption) !== null && _a !== void 0 ? _a : trans.__('Create a new text file'); },
            icon: args => {
                var _a;
                return args.isPalette
                    ? undefined
                    : ui_components_lib_index_js_.LabIcon.resolve({
                        icon: (_a = args.iconName) !== null && _a !== void 0 ? _a : ui_components_lib_index_js_.textEditorIcon
                    });
            },
            execute: args => {
                var _a;
                const cwd = args.cwd || defaultBrowser.model.path;
                return createNew(commands, cwd, (_a = args.fileExt) !== null && _a !== void 0 ? _a : 'txt');
            }
        });
        /**
         * Add the New Markdown File command
         */
        commands.addCommand(CommandIDs.createNewMarkdown, {
            label: args => args['isPalette']
                ? trans.__('New Markdown File')
                : trans.__('Markdown File'),
            caption: trans.__('Create a new markdown file'),
            icon: args => (args['isPalette'] ? undefined : ui_components_lib_index_js_.markdownIcon),
            execute: args => {
                const cwd = args['cwd'] || defaultBrowser.model.path;
                return createNew(commands, cwd, 'md');
            }
        });
        /**
         * Add undo command
         */
        commands.addCommand(CommandIDs.undo, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                widget.editor.undo();
            },
            isEnabled: () => {
                var _a;
                if (!isEnabled()) {
                    return false;
                }
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return false;
                }
                // Ideally enable it when there are undo events stored
                // Reference issue #8590: Code mirror editor could expose the history of undo/redo events
                return true;
            },
            icon: ui_components_lib_index_js_.undoIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Undo')
        });
        /**
         * Add redo command
         */
        commands.addCommand(CommandIDs.redo, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                widget.editor.redo();
            },
            isEnabled: () => {
                var _a;
                if (!isEnabled()) {
                    return false;
                }
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return false;
                }
                // Ideally enable it when there are redo events stored
                // Reference issue #8590: Code mirror editor could expose the history of undo/redo events
                return true;
            },
            icon: ui_components_lib_index_js_.redoIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Redo')
        });
        /**
         * Add cut command
         */
        commands.addCommand(CommandIDs.cut, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                const editor = widget.editor;
                const text = getTextSelection(editor);
                lib_index_js_.Clipboard.copyToSystem(text);
                editor.replaceSelection && editor.replaceSelection('');
            },
            isEnabled: () => {
                var _a;
                if (!isEnabled()) {
                    return false;
                }
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return false;
                }
                // Enable command if there is a text selection in the editor
                return isSelected(widget.editor);
            },
            icon: ui_components_lib_index_js_.cutIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Cut')
        });
        /**
         * Add copy command
         */
        commands.addCommand(CommandIDs.copy, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                const editor = widget.editor;
                const text = getTextSelection(editor);
                lib_index_js_.Clipboard.copyToSystem(text);
            },
            isEnabled: () => {
                var _a;
                if (!isEnabled()) {
                    return false;
                }
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return false;
                }
                // Enable command if there is a text selection in the editor
                return isSelected(widget.editor);
            },
            icon: ui_components_lib_index_js_.copyIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Copy')
        });
        /**
         * Add paste command
         */
        commands.addCommand(CommandIDs.paste, {
            execute: async () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                const editor = widget.editor;
                // Get data from clipboard
                const clipboard = window.navigator.clipboard;
                const clipboardData = await clipboard.readText();
                if (clipboardData) {
                    // Paste data to the editor
                    editor.replaceSelection && editor.replaceSelection(clipboardData);
                }
            },
            isEnabled: () => { var _a; return Boolean(isEnabled() && ((_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content)); },
            icon: ui_components_lib_index_js_.pasteIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Paste')
        });
        /**
         * Add select all command
         */
        commands.addCommand(CommandIDs.selectAll, {
            execute: () => {
                var _a;
                const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
                if (!widget) {
                    return;
                }
                const editor = widget.editor;
                editor.execCommand(dist_index_js_.selectAll);
            },
            isEnabled: () => { var _a; return Boolean(isEnabled() && ((_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content)); },
            label: trans.__('Select All')
        });
    }
    Commands.addCommands = addCommands;
    function addCompleterCommands(commands, editorTracker, manager, translator) {
        const trans = (translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        commands.addCommand(CommandIDs.invokeCompleter, {
            label: trans.__('Display the completion helper.'),
            execute: () => {
                const id = editorTracker.currentWidget && editorTracker.currentWidget.id;
                if (id) {
                    return manager.invoke(id);
                }
            }
        });
        commands.addCommand(CommandIDs.selectCompleter, {
            label: trans.__('Select the completion suggestion.'),
            execute: () => {
                const id = editorTracker.currentWidget && editorTracker.currentWidget.id;
                if (id) {
                    return manager.select(id);
                }
            }
        });
        commands.addKeyBinding({
            command: CommandIDs.selectCompleter,
            keys: ['Enter'],
            selector: '.jp-FileEditor .jp-mod-completer-active'
        });
    }
    Commands.addCompleterCommands = addCompleterCommands;
    /**
     * Helper function to check if there is a text selection in the editor
     */
    function isSelected(editor) {
        const selectionObj = editor.getSelection();
        const { start, end } = selectionObj;
        const selected = start.column !== end.column || start.line !== end.line;
        return selected;
    }
    /**
     * Helper function to get text selection from the editor
     */
    function getTextSelection(editor) {
        const selectionObj = editor.getSelection();
        const start = editor.getOffsetAt(selectionObj.start);
        const end = editor.getOffsetAt(selectionObj.end);
        const text = editor.model.sharedModel.getSource().substring(start, end);
        return text;
    }
    /**
     * Function to create a new untitled text file, given the current working directory.
     */
    async function createNew(commands, cwd, ext = 'txt') {
        const model = await commands.execute('docmanager:new-untitled', {
            path: cwd,
            type: 'file',
            ext
        });
        if (model != undefined) {
            const widget = (await commands.execute('docmanager:open', {
                path: model.path,
                factory: FACTORY
            }));
            widget.isUntitled = true;
            return widget;
        }
    }
    /**
     * Wrapper function for adding the default launcher items for File Editor
     */
    function addLauncherItems(launcher, trans) {
        addCreateNewToLauncher(launcher, trans);
        addCreateNewMarkdownToLauncher(launcher, trans);
    }
    Commands.addLauncherItems = addLauncherItems;
    /**
     * Add Create New Text File to the Launcher
     */
    function addCreateNewToLauncher(launcher, trans) {
        launcher.add({
            command: CommandIDs.createNew,
            category: trans.__('Other'),
            rank: 1
        });
    }
    Commands.addCreateNewToLauncher = addCreateNewToLauncher;
    /**
     * Add Create New Markdown to the Launcher
     */
    function addCreateNewMarkdownToLauncher(launcher, trans) {
        launcher.add({
            command: CommandIDs.createNewMarkdown,
            category: trans.__('Other'),
            rank: 2
        });
    }
    Commands.addCreateNewMarkdownToLauncher = addCreateNewMarkdownToLauncher;
    /**
     * Add ___ File items to the Launcher for common file types associated with available kernels
     */
    function addKernelLanguageLauncherItems(launcher, trans, availableKernelFileTypes) {
        for (let ext of availableKernelFileTypes) {
            launcher.add({
                command: CommandIDs.createNew,
                category: trans.__('Other'),
                rank: 3,
                args: ext
            });
        }
    }
    Commands.addKernelLanguageLauncherItems = addKernelLanguageLauncherItems;
    /**
     * Wrapper function for adding the default items to the File Editor palette
     */
    function addPaletteItems(palette, trans) {
        addChangeTabsCommandsToPalette(palette, trans);
        addCreateNewCommandToPalette(palette, trans);
        addCreateNewMarkdownCommandToPalette(palette, trans);
        addChangeFontSizeCommandsToPalette(palette, trans);
    }
    Commands.addPaletteItems = addPaletteItems;
    /**
     * Add commands to change the tab indentation to the File Editor palette
     */
    function addChangeTabsCommandsToPalette(palette, trans) {
        const paletteCategory = trans.__('Text Editor');
        const args = {
            size: 4
        };
        const command = CommandIDs.changeTabs;
        palette.addItem({ command, args, category: paletteCategory });
        for (const size of [1, 2, 4, 8]) {
            const args = {
                size
            };
            palette.addItem({ command, args, category: paletteCategory });
        }
    }
    Commands.addChangeTabsCommandsToPalette = addChangeTabsCommandsToPalette;
    /**
     * Add a Create New File command to the File Editor palette
     */
    function addCreateNewCommandToPalette(palette, trans) {
        const paletteCategory = trans.__('Text Editor');
        palette.addItem({
            command: CommandIDs.createNew,
            args: { isPalette: true },
            category: paletteCategory
        });
    }
    Commands.addCreateNewCommandToPalette = addCreateNewCommandToPalette;
    /**
     * Add a Create New Markdown command to the File Editor palette
     */
    function addCreateNewMarkdownCommandToPalette(palette, trans) {
        const paletteCategory = trans.__('Text Editor');
        palette.addItem({
            command: CommandIDs.createNewMarkdown,
            args: { isPalette: true },
            category: paletteCategory
        });
    }
    Commands.addCreateNewMarkdownCommandToPalette = addCreateNewMarkdownCommandToPalette;
    /**
     * Add commands to change the font size to the File Editor palette
     */
    function addChangeFontSizeCommandsToPalette(palette, trans) {
        const paletteCategory = trans.__('Text Editor');
        const command = CommandIDs.changeFontSize;
        let args = { delta: 1 };
        palette.addItem({ command, args, category: paletteCategory });
        args = { delta: -1 };
        palette.addItem({ command, args, category: paletteCategory });
    }
    Commands.addChangeFontSizeCommandsToPalette = addChangeFontSizeCommandsToPalette;
    /**
     * Add New ___ File commands to the File Editor palette for common file types associated with available kernels
     */
    function addKernelLanguagePaletteItems(palette, trans, availableKernelFileTypes) {
        const paletteCategory = trans.__('Text Editor');
        for (let ext of availableKernelFileTypes) {
            palette.addItem({
                command: CommandIDs.createNew,
                args: { ...ext, isPalette: true },
                category: paletteCategory
            });
        }
    }
    Commands.addKernelLanguagePaletteItems = addKernelLanguagePaletteItems;
    /**
     * Wrapper function for adding the default menu items for File Editor
     */
    function addMenuItems(menu, tracker, consoleTracker, isEnabled) {
        // Add undo/redo hooks to the edit menu.
        menu.editMenu.undoers.redo.add({
            id: CommandIDs.redo,
            isEnabled
        });
        menu.editMenu.undoers.undo.add({
            id: CommandIDs.undo,
            isEnabled
        });
        // Add editor view options.
        menu.viewMenu.editorViewers.toggleLineNumbers.add({
            id: CommandIDs.currentLineNumbers,
            isEnabled
        });
        menu.viewMenu.editorViewers.toggleMatchBrackets.add({
            id: CommandIDs.currentMatchBrackets,
            isEnabled
        });
        menu.viewMenu.editorViewers.toggleWordWrap.add({
            id: CommandIDs.currentLineWrap,
            isEnabled
        });
        // Add a console creator the the file menu.
        menu.fileMenu.consoleCreators.add({
            id: CommandIDs.createConsole,
            isEnabled
        });
        // Add a code runner to the run menu.
        if (consoleTracker) {
            addCodeRunnersToRunMenu(menu, consoleTracker, isEnabled);
        }
    }
    Commands.addMenuItems = addMenuItems;
    /**
     * Add Create New ___ File commands to the File menu for common file types associated with available kernels
     */
    function addKernelLanguageMenuItems(menu, availableKernelFileTypes) {
        for (let ext of availableKernelFileTypes) {
            menu.fileMenu.newMenu.addItem({
                command: CommandIDs.createNew,
                args: ext,
                rank: 31
            });
        }
    }
    Commands.addKernelLanguageMenuItems = addKernelLanguageMenuItems;
    /**
     * Add a File Editor code runner to the Run menu
     */
    function addCodeRunnersToRunMenu(menu, consoleTracker, isEnabled) {
        const isEnabled_ = (current) => isEnabled() &&
            current.context &&
            !!consoleTracker.find(widget => { var _a; return ((_a = widget.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) === current.context.path; });
        menu.runMenu.codeRunners.restart.add({
            id: CommandIDs.restartConsole,
            isEnabled: isEnabled_
        });
        menu.runMenu.codeRunners.run.add({
            id: CommandIDs.runCode,
            isEnabled: isEnabled_
        });
        menu.runMenu.codeRunners.runAll.add({
            id: CommandIDs.runAllCode,
            isEnabled: isEnabled_
        });
    }
    Commands.addCodeRunnersToRunMenu = addCodeRunnersToRunMenu;
    function addOpenCodeViewerCommand(app, editorServices, tracker, trans) {
        const openCodeViewer = async (args) => {
            var _a;
            const func = editorServices.factoryService.newDocumentEditor;
            const factory = options => {
                return func(options);
            };
            // Derive mimetype from extension
            let mimetype = args.mimeType;
            if (!mimetype && args.extension) {
                mimetype = editorServices.mimeTypeService.getMimeTypeByFilePath(`temp.${args.extension.replace(/\\.$/, '')}`);
            }
            const widget = codeeditor_lib_index_js_.CodeViewerWidget.createCodeViewer({
                factory,
                content: args.content,
                mimeType: mimetype
            });
            widget.title.label = args.label || trans.__('Code Viewer');
            widget.title.caption = widget.title.label;
            // Get the fileType based on the mimetype to determine the icon
            const fileType = (0,index_es6_js_.find)(app.docRegistry.fileTypes(), fileType => mimetype ? fileType.mimeTypes.includes(mimetype) : false);
            widget.title.icon = (_a = fileType === null || fileType === void 0 ? void 0 : fileType.icon) !== null && _a !== void 0 ? _a : ui_components_lib_index_js_.textEditorIcon;
            if (args.widgetId) {
                widget.id = args.widgetId;
            }
            const main = new lib_index_js_.MainAreaWidget({ content: widget });
            await tracker.add(main);
            app.shell.add(main, 'main');
            return widget;
        };
        app.commands.addCommand(CommandIDs.openCodeViewer, {
            label: trans.__('Open Code Viewer'),
            execute: (args) => {
                return openCodeViewer(args);
            }
        });
    }
    Commands.addOpenCodeViewerCommand = addOpenCodeViewerCommand;
})(Commands || (Commands = {}));

;// CONCATENATED MODULE: ../packages/fileeditor-extension/lib/syntaxstatus.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */





/**
 * The JupyterLab plugin for the EditorSyntax status item.
 */
const editorSyntaxStatus = {
    id: '@jupyterlab/fileeditor-extension:editor-syntax-status',
    description: 'Adds a file editor syntax status widget.',
    autoStart: true,
    requires: [fileeditor_lib_index_js_.IEditorTracker, codemirror_lib_index_js_.IEditorLanguageRegistry, index_js_.ILabShell, translation_lib_index_js_.ITranslator],
    optional: [statusbar_lib_index_js_.IStatusBar],
    activate: (app, tracker, languages, labShell, translator, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const item = new fileeditor_lib_index_js_.EditorSyntaxStatus({
            commands: app.commands,
            languages,
            translator
        });
        labShell.currentChanged.connect(() => {
            const current = labShell.currentWidget;
            if (current && tracker.has(current) && item.model) {
                item.model.editor = current.content.editor;
            }
        });
        statusBar.registerStatusItem(editorSyntaxStatus.id, {
            item,
            align: 'left',
            rank: 0,
            isActive: () => !!labShell.currentWidget &&
                !!tracker.currentWidget &&
                labShell.currentWidget === tracker.currentWidget
        });
    }
};

;// CONCATENATED MODULE: ../packages/fileeditor-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module fileeditor-extension
 */





















/**
 * The editor tracker extension.
 */
const lib_plugin = {
    activate,
    id: '@jupyterlab/fileeditor-extension:plugin',
    description: 'Provides the file editor widget tracker.',
    requires: [
        codeeditor_lib_index_js_.IEditorServices,
        codemirror_lib_index_js_.IEditorExtensionRegistry,
        codemirror_lib_index_js_.IEditorLanguageRegistry,
        codemirror_lib_index_js_.IEditorThemeRegistry,
        filebrowser_lib_index_js_.IDefaultFileBrowser,
        settingregistry_lib_index_js_.ISettingRegistry
    ],
    optional: [
        console_lib_index_js_.IConsoleTracker,
        lib_index_js_.ICommandPalette,
        launcher_lib_index_js_.ILauncher,
        mainmenu_lib_index_js_.IMainMenu,
        index_js_.ILayoutRestorer,
        lib_index_js_.ISessionContextDialogs,
        toc_lib_index_js_.ITableOfContentsRegistry,
        lib_index_js_.IToolbarWidgetRegistry,
        translation_lib_index_js_.ITranslator,
        ui_components_lib_index_js_.IFormRendererRegistry
    ],
    provides: fileeditor_lib_index_js_.IEditorTracker,
    autoStart: true
};
/**
 * A plugin that provides a status item allowing the user to
 * switch tabs vs spaces and tab widths for text editors.
 */
const tabSpaceStatus = {
    id: '@jupyterlab/fileeditor-extension:tab-space-status',
    description: 'Adds a file editor indentation status widget.',
    autoStart: true,
    requires: [
        fileeditor_lib_index_js_.IEditorTracker,
        codemirror_lib_index_js_.IEditorExtensionRegistry,
        settingregistry_lib_index_js_.ISettingRegistry,
        translation_lib_index_js_.ITranslator
    ],
    optional: [statusbar_lib_index_js_.IStatusBar],
    activate: (app, editorTracker, extensions, settingRegistry, translator, statusBar) => {
        const trans = translator.load('jupyterlab');
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        // Create a menu for switching tabs vs spaces.
        const menu = new ui_components_lib_index_js_.MenuSvg({ commands: app.commands });
        const command = 'fileeditor:change-tabs';
        const { shell } = app;
        const args = {
            name: trans.__('Indent with Tab')
        };
        menu.addItem({ command, args });
        for (const size of ['1', '2', '4', '8']) {
            const args = {
                size,
                // Use a context to differentiate with string set as plural in 3.x
                name: trans._p('v4', 'Spaces: %1', size)
            };
            menu.addItem({ command, args });
        }
        // Create the status item.
        const item = new fileeditor_lib_index_js_.TabSpaceStatus({ menu, translator });
        // Keep a reference to the code editor config from the settings system.
        const updateIndentUnit = (settings) => {
            var _a, _b, _c;
            item.model.indentUnit =
                (_c = (_b = (_a = settings.get('editorConfig').composite) === null || _a === void 0 ? void 0 : _a.indentUnit) !== null && _b !== void 0 ? _b : extensions.baseConfiguration.indentUnit) !== null && _c !== void 0 ? _c : null;
        };
        void Promise.all([
            settingRegistry.load('@jupyterlab/fileeditor-extension:plugin'),
            app.restored
        ]).then(([settings]) => {
            updateIndentUnit(settings);
            settings.changed.connect(updateIndentUnit);
        });
        // Add the status item.
        statusBar.registerStatusItem('@jupyterlab/fileeditor-extension:tab-space-status', {
            item,
            align: 'right',
            rank: 1,
            isActive: () => {
                return (!!shell.currentWidget && editorTracker.has(shell.currentWidget));
            }
        });
    }
};
/**
 * Cursor position.
 */
const lineColStatus = {
    id: '@jupyterlab/fileeditor-extension:cursor-position',
    description: 'Adds a file editor cursor position status widget.',
    activate: (app, tracker, positionModel) => {
        positionModel.addEditorProvider((widget) => Promise.resolve(widget && tracker.has(widget)
            ? widget.content.editor
            : null));
    },
    requires: [fileeditor_lib_index_js_.IEditorTracker, codeeditor_lib_index_js_.IPositionModel],
    autoStart: true
};
const completerPlugin = {
    id: '@jupyterlab/fileeditor-extension:completer',
    description: 'Adds the completer capability to the file editor.',
    requires: [fileeditor_lib_index_js_.IEditorTracker],
    optional: [completer_lib_index_js_.ICompletionProviderManager, translation_lib_index_js_.ITranslator, lib_index_js_.ISanitizer],
    activate: activateFileEditorCompleterService,
    autoStart: true
};
/**
 * A plugin to search file editors
 */
const searchProvider = {
    id: '@jupyterlab/fileeditor-extension:search',
    description: 'Adds search capability to the file editor.',
    requires: [documentsearch_lib_index_js_.ISearchProviderRegistry],
    autoStart: true,
    activate: (app, registry) => {
        registry.add('jp-fileeditorSearchProvider', fileeditor_lib_index_js_.FileEditorSearchProvider);
    }
};
const languageServerPlugin = {
    id: '@jupyterlab/fileeditor-extension:language-server',
    description: 'Adds Language Server capability to the file editor.',
    requires: [
        fileeditor_lib_index_js_.IEditorTracker,
        lsp_lib_index_js_.ILSPDocumentConnectionManager,
        lsp_lib_index_js_.ILSPFeatureManager,
        lsp_lib_index_js_.ILSPCodeExtractorsManager,
        lsp_lib_index_js_.IWidgetLSPAdapterTracker
    ],
    activate: activateFileEditorLanguageServer,
    autoStart: true
};
/**
 * Export the plugins as default.
 */
const plugins = [
    lib_plugin,
    lineColStatus,
    completerPlugin,
    languageServerPlugin,
    searchProvider,
    editorSyntaxStatus,
    tabSpaceStatus
];
/* harmony default export */ const lib = (plugins);
/**
 * Activate the editor tracker plugin.
 */
function activate(app, editorServices, extensions, languages, themes, fileBrowser, settingRegistry, consoleTracker, palette, launcher, menu, restorer, sessionDialogs_, tocRegistry, toolbarRegistry, translator_, formRegistry) {
    const id = lib_plugin.id;
    const translator = translator_ !== null && translator_ !== void 0 ? translator_ : translation_lib_index_js_.nullTranslator;
    const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new lib_index_js_.SessionContextDialogs({ translator });
    const trans = translator.load('jupyterlab');
    const namespace = 'editor';
    let toolbarFactory;
    if (toolbarRegistry) {
        toolbarFactory = (0,lib_index_js_.createToolbarFactory)(toolbarRegistry, settingRegistry, FACTORY, id, translator);
    }
    const factory = new fileeditor_lib_index_js_.FileEditorFactory({
        editorServices,
        factoryOptions: {
            name: FACTORY,
            label: trans.__('Editor'),
            fileTypes: ['markdown', '*'],
            defaultFor: ['markdown', '*'],
            toolbarFactory,
            translator
        }
    });
    const { commands, restored, shell } = app;
    const tracker = new lib_index_js_.WidgetTracker({
        namespace
    });
    const isEnabled = () => tracker.currentWidget !== null &&
        tracker.currentWidget === shell.currentWidget;
    const commonLanguageFileTypeData = new Map([
        [
            'python',
            [
                {
                    fileExt: 'py',
                    iconName: 'ui-components:python',
                    launcherLabel: trans.__('Python File'),
                    paletteLabel: trans.__('New Python File'),
                    caption: trans.__('Create a new Python file')
                }
            ]
        ],
        [
            'julia',
            [
                {
                    fileExt: 'jl',
                    iconName: 'ui-components:julia',
                    launcherLabel: trans.__('Julia File'),
                    paletteLabel: trans.__('New Julia File'),
                    caption: trans.__('Create a new Julia file')
                }
            ]
        ],
        [
            'R',
            [
                {
                    fileExt: 'r',
                    iconName: 'ui-components:r-kernel',
                    launcherLabel: trans.__('R File'),
                    paletteLabel: trans.__('New R File'),
                    caption: trans.__('Create a new R file')
                }
            ]
        ]
    ]);
    // Use available kernels to determine which common file types should have 'Create New' options in the Launcher, File Editor palette, and File menu
    const getAvailableKernelFileTypes = async () => {
        var _a, _b;
        const specsManager = app.serviceManager.kernelspecs;
        await specsManager.ready;
        let fileTypes = new Set();
        const specs = (_b = (_a = specsManager.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs) !== null && _b !== void 0 ? _b : {};
        Object.keys(specs).forEach(spec => {
            const specModel = specs[spec];
            if (specModel) {
                const exts = commonLanguageFileTypeData.get(specModel.language);
                exts === null || exts === void 0 ? void 0 : exts.forEach(ext => fileTypes.add(ext));
            }
        });
        return fileTypes;
    };
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY }),
            name: widget => widget.context.path
        });
    }
    // Add a console creator to the File menu
    // Fetch the initial state of the settings.
    Promise.all([settingRegistry.load(id), restored])
        .then(([settings]) => {
        var _a, _b, _c;
        // As the menu are defined in the settings we must ensure they are loaded
        // before updating dynamically the submenu
        if (menu) {
            const languageMenu = (_a = menu.viewMenu.items.find(item => {
                var _a;
                return item.type === 'submenu' &&
                    ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-view-codemirror-language';
            })) === null || _a === void 0 ? void 0 : _a.submenu;
            if (languageMenu) {
                languages
                    .getLanguages()
                    .sort((a, b) => {
                    const aName = a.name;
                    const bName = b.name;
                    return aName.localeCompare(bName);
                })
                    .forEach(spec => {
                    // Avoid mode name with a curse word.
                    if (spec.name.toLowerCase().indexOf('brainf') === 0) {
                        return;
                    }
                    languageMenu.addItem({
                        command: CommandIDs.changeLanguage,
                        args: { ...spec } // TODO: Casting to `any` until lumino typings are fixed
                    });
                });
            }
            const themeMenu = (_b = menu.settingsMenu.items.find(item => {
                var _a;
                return item.type === 'submenu' &&
                    ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-settings-codemirror-theme';
            })) === null || _b === void 0 ? void 0 : _b.submenu;
            if (themeMenu) {
                for (const theme of themes.themes) {
                    themeMenu.addItem({
                        command: CommandIDs.changeTheme,
                        args: {
                            theme: theme.name,
                            displayName: (_c = theme.displayName) !== null && _c !== void 0 ? _c : theme.name
                        }
                    });
                }
            }
            // Add go to line capabilities to the edit menu.
            menu.editMenu.goToLiners.add({
                id: CommandIDs.goToLine,
                isEnabled: (w) => tracker.currentWidget !== null && tracker.has(w)
            });
        }
        Commands.updateSettings(settings, commands);
        Commands.updateTracker(tracker);
        settings.changed.connect(() => {
            Commands.updateSettings(settings, commands);
            Commands.updateTracker(tracker);
        });
    })
        .catch((reason) => {
        console.error(reason.message);
        Commands.updateTracker(tracker);
    });
    if (formRegistry) {
        const CMRenderer = formRegistry.getRenderer('@jupyterlab/codemirror-extension:plugin.defaultConfig');
        if (CMRenderer) {
            formRegistry.addRenderer('@jupyterlab/fileeditor-extension:plugin.editorConfig', CMRenderer);
        }
    }
    factory.widgetCreated.connect((sender, widget) => {
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        void tracker.add(widget);
        Commands.updateWidget(widget.content);
    });
    app.docRegistry.addWidgetFactory(factory);
    // Handle the settings of new widgets.
    tracker.widgetAdded.connect((sender, widget) => {
        Commands.updateWidget(widget.content);
    });
    Commands.addCommands(app.commands, settingRegistry, trans, id, isEnabled, tracker, fileBrowser, extensions, languages, consoleTracker, sessionDialogs);
    const codeViewerTracker = new lib_index_js_.WidgetTracker({
        namespace: 'codeviewer'
    });
    // Handle state restoration for code viewers
    if (restorer) {
        void restorer.restore(codeViewerTracker, {
            command: CommandIDs.openCodeViewer,
            args: widget => ({
                content: widget.content.content,
                label: widget.content.title.label,
                mimeType: widget.content.mimeType,
                widgetId: widget.content.id
            }),
            name: widget => widget.content.id
        });
    }
    Commands.addOpenCodeViewerCommand(app, editorServices, codeViewerTracker, trans);
    // Add a launcher item if the launcher is available.
    if (launcher) {
        Commands.addLauncherItems(launcher, trans);
    }
    if (palette) {
        Commands.addPaletteItems(palette, trans);
    }
    if (menu) {
        Commands.addMenuItems(menu, tracker, consoleTracker, isEnabled);
    }
    getAvailableKernelFileTypes()
        .then(availableKernelFileTypes => {
        if (launcher) {
            Commands.addKernelLanguageLauncherItems(launcher, trans, availableKernelFileTypes);
        }
        if (palette) {
            Commands.addKernelLanguagePaletteItems(palette, trans, availableKernelFileTypes);
        }
        if (menu) {
            Commands.addKernelLanguageMenuItems(menu, availableKernelFileTypes);
        }
    })
        .catch((reason) => {
        console.error(reason.message);
    });
    if (tocRegistry) {
        tocRegistry.add(new fileeditor_lib_index_js_.LaTeXTableOfContentsFactory(tracker));
        tocRegistry.add(new fileeditor_lib_index_js_.MarkdownTableOfContentsFactory(tracker));
        tocRegistry.add(new fileeditor_lib_index_js_.PythonTableOfContentsFactory(tracker));
    }
    return tracker;
}
/**
 * Activate the completer service for file editor.
 */
function activateFileEditorCompleterService(app, editorTracker, manager, translator, appSanitizer) {
    if (!manager) {
        return;
    }
    Commands.addCompleterCommands(app.commands, editorTracker, manager, translator);
    const sessionManager = app.serviceManager.sessions;
    const sanitizer = appSanitizer !== null && appSanitizer !== void 0 ? appSanitizer : new lib_index_js_.Sanitizer();
    const _activeSessions = new Map();
    const updateCompleter = async (_, widget) => {
        const completerContext = {
            editor: widget.content.editor,
            widget
        };
        await manager.updateCompleter(completerContext);
        const onRunningChanged = (_, models) => {
            const oldSession = _activeSessions.get(widget.id);
            // Search for a matching path.
            const model = (0,index_es6_js_.find)(models, m => m.path === widget.context.path);
            if (model) {
                // If there is a matching path, but it is the same
                // session as we previously had, do nothing.
                if (oldSession && oldSession.id === model.id) {
                    return;
                }
                // Otherwise, dispose of the old session and reset to
                // a new CompletionConnector.
                if (oldSession) {
                    _activeSessions.delete(widget.id);
                    oldSession.dispose();
                }
                const session = sessionManager.connectTo({ model });
                const newCompleterContext = {
                    editor: widget.content.editor,
                    widget,
                    session,
                    sanitizer
                };
                manager.updateCompleter(newCompleterContext).catch(console.error);
                _activeSessions.set(widget.id, session);
            }
            else {
                // If we didn't find a match, make sure
                // the connector is the contextConnector and
                // dispose of any previous connection.
                if (oldSession) {
                    _activeSessions.delete(widget.id);
                    oldSession.dispose();
                }
            }
        };
        onRunningChanged(sessionManager, Array.from(sessionManager.running()));
        sessionManager.runningChanged.connect(onRunningChanged);
        widget.disposed.connect(() => {
            sessionManager.runningChanged.disconnect(onRunningChanged);
            const session = _activeSessions.get(widget.id);
            if (session) {
                _activeSessions.delete(widget.id);
                session.dispose();
            }
        });
    };
    editorTracker.widgetAdded.connect(updateCompleter);
    manager.activeProvidersChanged.connect(() => {
        editorTracker.forEach(editorWidget => {
            updateCompleter(editorTracker, editorWidget).catch(console.error);
        });
    });
}
function activateFileEditorLanguageServer(app, editors, connectionManager, featureManager, extractorManager, adapterTracker) {
    editors.widgetAdded.connect(async (_, editor) => {
        const adapter = new fileeditor_lib_index_js_.FileEditorAdapter(editor, {
            connectionManager,
            featureManager,
            foreignCodeExtractorsManager: extractorManager,
            docRegistry: app.docRegistry
        });
        adapterTracker.add(adapter);
    });
}


/***/ })

}]);
//# sourceMappingURL=9701.d527cd71fb7bf1a722b5.js.map?v=d527cd71fb7bf1a722b5