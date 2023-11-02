"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[4855],{

/***/ 64855:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "LogLevelSwitcher": () => (/* binding */ LogLevelSwitcher),
  "default": () => (/* binding */ lib)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/application@~4.1.0-alpha.2 (singleton) (fallback: ../packages/application/lib/index.js)
var index_js_ = __webpack_require__(65681);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/logconsole@~4.1.0-alpha.2 (singleton) (fallback: ../packages/logconsole/lib/index.js)
var logconsole_lib_index_js_ = __webpack_require__(94908);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var settingregistry_lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/logconsole-extension/lib/status.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * A pure functional component for a Log Console status item.
 *
 * @param props - the props for the component.
 *
 * @returns a tsx component for rendering the Log Console status.
 */
function LogConsoleStatusComponent(props) {
    const translator = props.translator || translation_lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    let title = '';
    if (props.newMessages > 0) {
        title = trans.__('%1 new messages, %2 log entries for %3', props.newMessages, props.logEntries, props.source);
    }
    else {
        title += trans.__('%1 log entries for %2', props.logEntries, props.source);
    }
    return (react_index_js_default().createElement(statusbar_lib_index_js_.GroupItem, { spacing: 0, onClick: props.handleClick, title: title },
        react_index_js_default().createElement(ui_components_lib_index_js_.listIcon.react, { top: '2px', stylesheet: 'statusBar' }),
        props.newMessages > 0 ? react_index_js_default().createElement(statusbar_lib_index_js_.TextItem, { source: props.newMessages }) : react_index_js_default().createElement((react_index_js_default()).Fragment, null)));
}
/**
 * A VDomRenderer widget for displaying the status of Log Console logs.
 */
class LogConsoleStatus extends ui_components_lib_index_js_.VDomRenderer {
    /**
     * Construct the log console status widget.
     *
     * @param options - The status widget initialization options.
     */
    constructor(options) {
        super(new LogConsoleStatus.Model(options.loggerRegistry));
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._handleClick = options.handleClick;
        this.addClass('jp-mod-highlighted');
        this.addClass('jp-LogConsoleStatusItem');
    }
    /**
     * Render the log console status item.
     */
    render() {
        if (this.model === null || this.model.version === 0) {
            return null;
        }
        const { flashEnabled, messages, source, version, versionDisplayed, versionNotified } = this.model;
        if (source !== null && flashEnabled && version > versionNotified) {
            this._flashHighlight();
            this.model.sourceNotified(source, version);
        }
        else if (source !== null && flashEnabled && version > versionDisplayed) {
            this._showHighlighted();
        }
        else {
            this._clearHighlight();
        }
        return (react_index_js_default().createElement(LogConsoleStatusComponent, { handleClick: this._handleClick, logEntries: messages, newMessages: version - versionDisplayed, source: this.model.source, translator: this.translator }));
    }
    _flashHighlight() {
        this._showHighlighted();
        // To make sure the browser triggers the animation, we remove the class,
        // wait for an animation frame, then add it back
        this.removeClass('jp-LogConsole-flash');
        requestAnimationFrame(() => {
            this.addClass('jp-LogConsole-flash');
        });
    }
    _showHighlighted() {
        this.addClass('jp-mod-selected');
    }
    _clearHighlight() {
        this.removeClass('jp-LogConsole-flash');
        this.removeClass('jp-mod-selected');
    }
}
/**
 * A namespace for Log Console log status.
 */
(function (LogConsoleStatus) {
    /**
     * A VDomModel for the LogConsoleStatus item.
     */
    class Model extends ui_components_lib_index_js_.VDomModel {
        /**
         * Create a new LogConsoleStatus model.
         *
         * @param loggerRegistry - The logger registry providing the logs.
         */
        constructor(loggerRegistry) {
            super();
            /**
             * A signal emitted when the flash enablement changes.
             */
            this.flashEnabledChanged = new index_es6_js_.Signal(this);
            this._flashEnabled = true;
            this._source = null;
            /**
             * The view status of each source.
             *
             * #### Notes
             * Keys are source names, value is a list of two numbers. The first
             * represents the version of the messages that was last displayed to the
             * user, the second represents the version that we last notified the user
             * about.
             */
            this._sourceVersion = new Map();
            this._loggerRegistry = loggerRegistry;
            this._loggerRegistry.registryChanged.connect(this._handleLogRegistryChange, this);
            this._handleLogRegistryChange();
        }
        /**
         * Number of messages currently in the current source.
         */
        get messages() {
            if (this._source === null) {
                return 0;
            }
            const logger = this._loggerRegistry.getLogger(this._source);
            return logger.length;
        }
        /**
         * The number of messages ever stored by the current source.
         */
        get version() {
            if (this._source === null) {
                return 0;
            }
            const logger = this._loggerRegistry.getLogger(this._source);
            return logger.version;
        }
        /**
         * The name of the active log source
         */
        get source() {
            return this._source;
        }
        set source(name) {
            if (this._source === name) {
                return;
            }
            this._source = name;
            // refresh rendering
            this.stateChanged.emit();
        }
        /**
         * The last source version that was displayed.
         */
        get versionDisplayed() {
            var _a, _b;
            if (this._source === null) {
                return 0;
            }
            return (_b = (_a = this._sourceVersion.get(this._source)) === null || _a === void 0 ? void 0 : _a.lastDisplayed) !== null && _b !== void 0 ? _b : 0;
        }
        /**
         * The last source version we notified the user about.
         */
        get versionNotified() {
            var _a, _b;
            if (this._source === null) {
                return 0;
            }
            return (_b = (_a = this._sourceVersion.get(this._source)) === null || _a === void 0 ? void 0 : _a.lastNotified) !== null && _b !== void 0 ? _b : 0;
        }
        /**
         * Flag to toggle flashing when new logs added.
         */
        get flashEnabled() {
            return this._flashEnabled;
        }
        set flashEnabled(enabled) {
            if (this._flashEnabled === enabled) {
                return;
            }
            this._flashEnabled = enabled;
            this.flashEnabledChanged.emit();
            // refresh rendering
            this.stateChanged.emit();
        }
        /**
         * Record the last source version displayed to the user.
         *
         * @param source - The name of the log source.
         * @param version - The version of the log that was displayed.
         *
         * #### Notes
         * This will also update the last notified version so that the last
         * notified version is always at least the last displayed version.
         */
        sourceDisplayed(source, version) {
            if (source === null || version === null) {
                return;
            }
            const versions = this._sourceVersion.get(source);
            let change = false;
            if (versions.lastDisplayed < version) {
                versions.lastDisplayed = version;
                change = true;
            }
            if (versions.lastNotified < version) {
                versions.lastNotified = version;
                change = true;
            }
            if (change && source === this._source) {
                this.stateChanged.emit();
            }
        }
        /**
         * Record a source version we notified the user about.
         *
         * @param source - The name of the log source.
         * @param version - The version of the log.
         */
        sourceNotified(source, version) {
            if (source === null) {
                return;
            }
            const versions = this._sourceVersion.get(source);
            if (versions.lastNotified < version) {
                versions.lastNotified = version;
                if (source === this._source) {
                    this.stateChanged.emit();
                }
            }
        }
        _handleLogRegistryChange() {
            const loggers = this._loggerRegistry.getLoggers();
            for (const logger of loggers) {
                if (!this._sourceVersion.has(logger.source)) {
                    logger.contentChanged.connect(this._handleLogContentChange, this);
                    this._sourceVersion.set(logger.source, {
                        lastDisplayed: 0,
                        lastNotified: 0
                    });
                }
            }
        }
        _handleLogContentChange({ source }, change) {
            if (source === this._source) {
                this.stateChanged.emit();
            }
        }
    }
    LogConsoleStatus.Model = Model;
})(LogConsoleStatus || (LogConsoleStatus = {}));

;// CONCATENATED MODULE: ../packages/logconsole-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module logconsole-extension
 */











const LOG_CONSOLE_PLUGIN_ID = '@jupyterlab/logconsole-extension:plugin';
/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.addCheckpoint = 'logconsole:add-checkpoint';
    CommandIDs.clear = 'logconsole:clear';
    CommandIDs.open = 'logconsole:open';
    CommandIDs.setLevel = 'logconsole:set-level';
})(CommandIDs || (CommandIDs = {}));
/**
 * The Log Console extension.
 */
const logConsolePlugin = {
    activate: activateLogConsole,
    id: LOG_CONSOLE_PLUGIN_ID,
    description: 'Provides the logger registry.',
    provides: logconsole_lib_index_js_.ILoggerRegistry,
    requires: [index_js_.ILabShell, rendermime_lib_index_js_.IRenderMimeRegistry, translation_lib_index_js_.ITranslator],
    optional: [lib_index_js_.ICommandPalette, index_js_.ILayoutRestorer, settingregistry_lib_index_js_.ISettingRegistry, statusbar_lib_index_js_.IStatusBar],
    autoStart: true
};
/**
 * Activate the Log Console extension.
 */
function activateLogConsole(app, labShell, rendermime, translator, palette, restorer, settingRegistry, statusBar) {
    const trans = translator.load('jupyterlab');
    let logConsoleWidget = null;
    let logConsolePanel = null;
    const loggerRegistry = new logconsole_lib_index_js_.LoggerRegistry({
        defaultRendermime: rendermime,
        // The maxLength is reset below from settings
        maxLength: 1000
    });
    const tracker = new lib_index_js_.WidgetTracker({
        namespace: 'logconsole'
    });
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.open,
            name: () => 'logconsole'
        });
    }
    const status = new LogConsoleStatus({
        loggerRegistry: loggerRegistry,
        handleClick: () => {
            var _a;
            if (!logConsoleWidget) {
                createLogConsoleWidget({
                    insertMode: 'split-bottom',
                    ref: (_a = app.shell.currentWidget) === null || _a === void 0 ? void 0 : _a.id
                });
            }
            else {
                app.shell.activateById(logConsoleWidget.id);
            }
        },
        translator
    });
    const createLogConsoleWidget = (options = {}) => {
        var _a, _b;
        logConsolePanel = new logconsole_lib_index_js_.LogConsolePanel(loggerRegistry, translator);
        logConsolePanel.source = (_b = (_a = options.source) !== null && _a !== void 0 ? _a : labShell.currentPath) !== null && _b !== void 0 ? _b : null;
        logConsoleWidget = new lib_index_js_.MainAreaWidget({ content: logConsolePanel });
        logConsoleWidget.addClass('jp-LogConsole');
        logConsoleWidget.title.closable = true;
        logConsoleWidget.title.icon = ui_components_lib_index_js_.listIcon;
        logConsoleWidget.title.label = trans.__('Log Console');
        const addCheckpointButton = new ui_components_lib_index_js_.CommandToolbarButton({
            commands: app.commands,
            id: CommandIDs.addCheckpoint
        });
        const clearButton = new ui_components_lib_index_js_.CommandToolbarButton({
            commands: app.commands,
            id: CommandIDs.clear
        });
        const notifyCommands = () => {
            app.commands.notifyCommandChanged(CommandIDs.addCheckpoint);
            app.commands.notifyCommandChanged(CommandIDs.clear);
            app.commands.notifyCommandChanged(CommandIDs.open);
            app.commands.notifyCommandChanged(CommandIDs.setLevel);
        };
        logConsoleWidget.toolbar.addItem('lab-log-console-add-checkpoint', addCheckpointButton);
        logConsoleWidget.toolbar.addItem('lab-log-console-clear', clearButton);
        logConsoleWidget.toolbar.addItem('level', new LogLevelSwitcher(logConsoleWidget.content, translator));
        logConsolePanel.sourceChanged.connect(() => {
            notifyCommands();
        });
        logConsolePanel.sourceDisplayed.connect((panel, { source, version }) => {
            status.model.sourceDisplayed(source, version);
        });
        logConsoleWidget.disposed.connect(() => {
            logConsoleWidget = null;
            logConsolePanel = null;
            notifyCommands();
        });
        app.shell.add(logConsoleWidget, 'down', {
            ref: options.ref,
            mode: options.insertMode,
            type: 'Log Console'
        });
        void tracker.add(logConsoleWidget);
        app.shell.activateById(logConsoleWidget.id);
        logConsoleWidget.update();
        notifyCommands();
    };
    app.commands.addCommand(CommandIDs.open, {
        label: trans.__('Show Log Console'),
        execute: (options = {}) => {
            // Toggle the display
            if (logConsoleWidget) {
                logConsoleWidget.dispose();
            }
            else {
                createLogConsoleWidget(options);
            }
        },
        isToggled: () => {
            return logConsoleWidget !== null;
        }
    });
    app.commands.addCommand(CommandIDs.addCheckpoint, {
        execute: () => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.checkpoint();
        },
        icon: ui_components_lib_index_js_.addIcon,
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: trans.__('Add Checkpoint')
    });
    app.commands.addCommand(CommandIDs.clear, {
        execute: () => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.clear();
        },
        icon: ui_components_lib_index_js_.clearIcon,
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: trans.__('Clear Log')
    });
    function toTitleCase(value) {
        return value.length === 0 ? value : value[0].toUpperCase() + value.slice(1);
    }
    app.commands.addCommand(CommandIDs.setLevel, {
        // TODO: find good icon class
        execute: (args) => {
            if (logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) {
                logConsolePanel.logger.level = args.level;
            }
        },
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: args => args['level']
            ? trans.__('Set Log Level to %1', toTitleCase(args.level))
            : trans.__('Set log level to `level`.')
    });
    if (palette) {
        palette.addItem({
            command: CommandIDs.open,
            category: trans.__('Main Area')
        });
    }
    if (statusBar) {
        statusBar.registerStatusItem('@jupyterlab/logconsole-extension:status', {
            item: status,
            align: 'left',
            isActive: () => { var _a; return ((_a = status.model) === null || _a === void 0 ? void 0 : _a.version) > 0; },
            activeStateChanged: status.model.stateChanged
        });
    }
    function setSource(source) {
        if (logConsolePanel) {
            logConsolePanel.source = source;
        }
        status.model.source = source;
    }
    void app.restored.then(() => {
        var _a;
        // Set source only after app is restored in order to allow restorer to
        // restore previous source first, which may set the renderer
        labShell.currentPathChanged.connect((_, { newValue }) => setSource(newValue));
        setSource((_a = labShell.currentPath) !== null && _a !== void 0 ? _a : null);
    });
    if (settingRegistry) {
        const updateSettings = (settings) => {
            loggerRegistry.maxLength = settings.get('maxLogEntries')
                .composite;
            status.model.flashEnabled = settings.get('flash').composite;
        };
        Promise.all([settingRegistry.load(LOG_CONSOLE_PLUGIN_ID), app.restored])
            .then(([settings]) => {
            updateSettings(settings);
            settings.changed.connect(settings => {
                updateSettings(settings);
            });
        })
            .catch((reason) => {
            console.error(reason.message);
        });
    }
    return loggerRegistry;
}
/**
 * A toolbar widget that switches log levels.
 */
class LogLevelSwitcher extends ui_components_lib_index_js_.ReactWidget {
    /**
     * Construct a new log level switcher.
     */
    constructor(widget, translator) {
        super();
        /**
         * Handle `change` events for the HTMLSelect component.
         */
        this.handleChange = (event) => {
            if (this._logConsole.logger) {
                this._logConsole.logger.level = event.target.value;
            }
            this.update();
        };
        /**
         * Handle `keydown` events for the HTMLSelect component.
         */
        this.handleKeyDown = (event) => {
            if (event.keyCode === 13) {
                this._logConsole.activate();
            }
        };
        this._id = `level-${dist_index_js_.UUID.uuid4()}`;
        this.translator = translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.addClass('jp-LogConsole-toolbarLogLevel');
        this._logConsole = widget;
        if (widget.source) {
            this.update();
        }
        widget.sourceChanged.connect(this._updateSource, this);
    }
    _updateSource(sender, { oldValue, newValue }) {
        // Transfer stateChanged handler to new source logger
        if (oldValue !== null) {
            const logger = sender.loggerRegistry.getLogger(oldValue);
            logger.stateChanged.disconnect(this.update, this);
        }
        if (newValue !== null) {
            const logger = sender.loggerRegistry.getLogger(newValue);
            logger.stateChanged.connect(this.update, this);
        }
        this.update();
    }
    render() {
        const logger = this._logConsole.logger;
        return (react_index_js_.createElement(react_index_js_.Fragment, null,
            react_index_js_.createElement("label", { htmlFor: this._id, className: logger === null
                    ? 'jp-LogConsole-toolbarLogLevel-disabled'
                    : undefined }, this._trans.__('Log Level:')),
            react_index_js_.createElement(ui_components_lib_index_js_.HTMLSelect, { id: this._id, className: "jp-LogConsole-toolbarLogLevelDropdown", onChange: this.handleChange, onKeyDown: this.handleKeyDown, value: logger === null || logger === void 0 ? void 0 : logger.level, "aria-label": this._trans.__('Log level'), disabled: logger === null, options: logger === null
                    ? []
                    : [
                        [this._trans.__('Critical'), 'Critical'],
                        [this._trans.__('Error'), 'Error'],
                        [this._trans.__('Warning'), 'Warning'],
                        [this._trans.__('Info'), 'Info'],
                        [this._trans.__('Debug'), 'Debug']
                    ].map(data => ({
                        label: data[0],
                        value: data[1].toLowerCase()
                    })) })));
    }
}
/* harmony default export */ const lib = (logConsolePlugin);


/***/ })

}]);
//# sourceMappingURL=4855.5b7cf89d653293d58b76.js.map?v=5b7cf89d653293d58b76