"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[6457],{

/***/ 56457:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "ILoggerRegistry": () => (/* reexport */ ILoggerRegistry),
  "LogConsolePanel": () => (/* reexport */ LogConsolePanel),
  "LogOutputModel": () => (/* reexport */ LogOutputModel),
  "Logger": () => (/* reexport */ Logger),
  "LoggerOutputAreaModel": () => (/* reexport */ LoggerOutputAreaModel),
  "LoggerRegistry": () => (/* reexport */ LoggerRegistry),
  "ScrollingWidget": () => (/* reexport */ ScrollingWidget)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/outputarea@~4.1.0-alpha.2 (strict) (fallback: ../packages/outputarea/lib/index.js)
var index_js_ = __webpack_require__(65583);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/logconsole/lib/logger.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Log Output Model with timestamp which provides
 * item information for Output Area Model.
 */
class LogOutputModel extends lib_index_js_.OutputModel {
    /**
     * Construct a LogOutputModel.
     *
     * @param options - The model initialization options.
     */
    constructor(options) {
        super(options);
        this.timestamp = new Date(options.value.timestamp);
        this.level = options.value.level;
    }
}
/**
 * Implementation of `IContentFactory` for Output Area Model
 * which creates LogOutputModel instances.
 */
class LogConsoleModelContentFactory extends index_js_.OutputAreaModel.ContentFactory {
    /**
     * Create a rendermime output model from notebook output.
     */
    createOutputModel(options) {
        return new LogOutputModel(options);
    }
}
/**
 * Output Area Model implementation which is able to
 * limit number of outputs stored.
 */
class LoggerOutputAreaModel extends index_js_.OutputAreaModel {
    constructor({ maxLength, ...options }) {
        super(options);
        this.maxLength = maxLength;
    }
    /**
     * Add an output, which may be combined with previous output.
     *
     * @returns The total number of outputs.
     *
     * #### Notes
     * The output bundle is copied. Contiguous stream outputs of the same `name`
     * are combined. The oldest outputs are possibly removed to ensure the total
     * number of outputs is at most `.maxLength`.
     */
    add(output) {
        super.add(output);
        this._applyMaxLength();
        return this.length;
    }
    /**
     * Whether an output should combine with the previous output.
     *
     * We combine if the two outputs are in the same second, which is the
     * resolution for our time display.
     */
    shouldCombine(options) {
        const { value, lastModel } = options;
        const oldSeconds = Math.trunc(lastModel.timestamp.getTime() / 1000);
        const newSeconds = Math.trunc(value.timestamp / 1000);
        return oldSeconds === newSeconds;
    }
    /**
     * Get an item at the specified index.
     */
    get(index) {
        return super.get(index);
    }
    /**
     * Maximum number of outputs to store in the model.
     */
    get maxLength() {
        return this._maxLength;
    }
    set maxLength(value) {
        this._maxLength = value;
        this._applyMaxLength();
    }
    /**
     * Manually apply length limit.
     */
    _applyMaxLength() {
        if (this.list.length > this._maxLength) {
            this.list.removeRange(0, this.list.length - this._maxLength);
        }
    }
}
/**
 * A concrete implementation of ILogger.
 */
class Logger {
    /**
     * Construct a Logger.
     *
     * @param source - The name of the log source.
     */
    constructor(options) {
        this._isDisposed = false;
        this._contentChanged = new index_es6_js_.Signal(this);
        this._stateChanged = new index_es6_js_.Signal(this);
        this._rendermime = null;
        this._version = 0;
        this._level = 'warning';
        this.source = options.source;
        this.outputAreaModel = new LoggerOutputAreaModel({
            contentFactory: new LogConsoleModelContentFactory(),
            maxLength: options.maxLength
        });
    }
    /**
     * The maximum number of outputs stored.
     *
     * #### Notes
     * Oldest entries will be trimmed to ensure the length is at most
     * `.maxLength`.
     */
    get maxLength() {
        return this.outputAreaModel.maxLength;
    }
    set maxLength(value) {
        this.outputAreaModel.maxLength = value;
    }
    /**
     * The level of outputs logged
     */
    get level() {
        return this._level;
    }
    set level(newValue) {
        const oldValue = this._level;
        if (oldValue === newValue) {
            return;
        }
        this._level = newValue;
        this._log({
            output: {
                output_type: 'display_data',
                data: {
                    'text/plain': `Log level set to ${newValue}`
                }
            },
            level: 'metadata'
        });
        this._stateChanged.emit({ name: 'level', oldValue, newValue });
    }
    /**
     * Number of outputs logged.
     */
    get length() {
        return this.outputAreaModel.length;
    }
    /**
     * A signal emitted when the list of log messages changes.
     */
    get contentChanged() {
        return this._contentChanged;
    }
    /**
     * A signal emitted when the log state changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * Rendermime to use when rendering outputs logged.
     */
    get rendermime() {
        return this._rendermime;
    }
    set rendermime(value) {
        if (value !== this._rendermime) {
            const oldValue = this._rendermime;
            const newValue = (this._rendermime = value);
            this._stateChanged.emit({ name: 'rendermime', oldValue, newValue });
        }
    }
    /**
     * The number of messages that have ever been stored.
     */
    get version() {
        return this._version;
    }
    /**
     * Log an output to logger.
     *
     * @param log - The output to be logged.
     */
    log(log) {
        // Filter by our current log level
        if (Private.LogLevel[log.level] <
            Private.LogLevel[this._level]) {
            return;
        }
        let output = null;
        switch (log.type) {
            case 'text':
                output = {
                    output_type: 'display_data',
                    data: {
                        'text/plain': log.data
                    }
                };
                break;
            case 'html':
                output = {
                    output_type: 'display_data',
                    data: {
                        'text/html': log.data
                    }
                };
                break;
            case 'output':
                output = log.data;
                break;
            default:
                break;
        }
        if (output) {
            this._log({
                output,
                level: log.level
            });
        }
    }
    /**
     * Clear all outputs logged.
     */
    clear() {
        this.outputAreaModel.clear(false);
        this._contentChanged.emit('clear');
    }
    /**
     * Add a checkpoint to the log.
     */
    checkpoint() {
        this._log({
            output: {
                output_type: 'display_data',
                data: {
                    'text/html': '<hr/>'
                }
            },
            level: 'metadata'
        });
    }
    /**
     * Whether the logger is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the logger.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.clear();
        this._rendermime = null;
        index_es6_js_.Signal.clearData(this);
    }
    _log(options) {
        // First, make sure our version reflects the new message so things
        // triggering from the signals below have the correct version.
        this._version++;
        // Next, trigger any displays of the message
        this.outputAreaModel.add({
            ...options.output,
            timestamp: Date.now(),
            level: options.level
        });
        // Finally, tell people that the message was appended (and possibly
        // already displayed).
        this._contentChanged.emit('append');
    }
}
var Private;
(function (Private) {
    let LogLevel;
    (function (LogLevel) {
        LogLevel[LogLevel["debug"] = 0] = "debug";
        LogLevel[LogLevel["info"] = 1] = "info";
        LogLevel[LogLevel["warning"] = 2] = "warning";
        LogLevel[LogLevel["error"] = 3] = "error";
        LogLevel[LogLevel["critical"] = 4] = "critical";
        LogLevel[LogLevel["metadata"] = 5] = "metadata";
    })(LogLevel = Private.LogLevel || (Private.LogLevel = {}));
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/logconsole/lib/registry.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A concrete implementation of ILoggerRegistry.
 */
class LoggerRegistry {
    /**
     * Construct a LoggerRegistry.
     *
     * @param defaultRendermime - Default rendermime to render outputs
     * with when logger is not supplied with one.
     */
    constructor(options) {
        this._loggers = new Map();
        this._registryChanged = new index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._defaultRendermime = options.defaultRendermime;
        this._maxLength = options.maxLength;
    }
    /**
     * Get the logger for the specified source.
     *
     * @param source - The name of the log source.
     *
     * @returns The logger for the specified source.
     */
    getLogger(source) {
        const loggers = this._loggers;
        let logger = loggers.get(source);
        if (logger) {
            return logger;
        }
        logger = new Logger({ source, maxLength: this.maxLength });
        logger.rendermime = this._defaultRendermime;
        loggers.set(source, logger);
        this._registryChanged.emit('append');
        return logger;
    }
    /**
     * Get all loggers registered.
     *
     * @returns The array containing all registered loggers.
     */
    getLoggers() {
        return Array.from(this._loggers.values());
    }
    /**
     * A signal emitted when the logger registry changes.
     */
    get registryChanged() {
        return this._registryChanged;
    }
    /**
     * The max length for loggers.
     */
    get maxLength() {
        return this._maxLength;
    }
    set maxLength(value) {
        this._maxLength = value;
        this._loggers.forEach(logger => {
            logger.maxLength = value;
        });
    }
    /**
     * Whether the register is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the registry and all loggers.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._loggers.forEach(x => x.dispose());
        index_es6_js_.Signal.clearData(this);
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/logconsole/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The Logger Registry token.
 */
const ILoggerRegistry = new dist_index_js_.Token('@jupyterlab/logconsole:ILoggerRegistry', 'A service providing a logger infrastructure.');

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/logconsole/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




function toTitleCase(value) {
    return value.length === 0 ? value : value[0].toUpperCase() + value.slice(1);
}
/**
 * Log console output prompt implementation
 */
class LogConsoleOutputPrompt extends dist_index_es6_js_.Widget {
    constructor() {
        super();
        this._timestampNode = document.createElement('div');
        this.node.append(this._timestampNode);
    }
    /**
     * Date & time when output is logged.
     */
    set timestamp(value) {
        this._timestamp = value;
        this._timestampNode.innerHTML = this._timestamp.toLocaleTimeString();
        this.update();
    }
    /**
     * Log level
     */
    set level(value) {
        this._level = value;
        this.node.dataset.logLevel = value;
        this.update();
    }
    update() {
        if (this._level !== undefined && this._timestamp !== undefined) {
            this.node.title = `${this._timestamp.toLocaleString()}; ${toTitleCase(this._level)} level`;
        }
    }
}
/**
 * Output Area implementation displaying log outputs
 * with prompts showing log timestamps.
 */
class LogConsoleOutputArea extends index_js_.OutputArea {
    /**
     * Create an output item with a prompt and actual output
     */
    createOutputItem(model) {
        const panel = super.createOutputItem(model);
        if (panel === null) {
            // Could not render model
            return null;
        }
        // first widget in panel is prompt of type LoggerOutputPrompt
        const prompt = panel.widgets[0];
        prompt.timestamp = model.timestamp;
        prompt.level = model.level;
        return panel;
    }
    /**
     * Handle an input request from a kernel by doing nothing.
     */
    onInputRequest(msg, future) {
        return;
    }
}
/**
 * Implementation of `IContentFactory` for Output Area
 * which creates custom output prompts.
 */
class LogConsoleContentFactory extends index_js_.OutputArea.ContentFactory {
    /**
     * Create the output prompt for the widget.
     */
    createOutputPrompt() {
        return new LogConsoleOutputPrompt();
    }
}
/**
 * Implements a panel which supports pinning the position to the end if it is
 * scrolled to the end.
 *
 * #### Notes
 * This is useful for log viewing components or chat components that append
 * elements at the end. We would like to automatically scroll when the user
 * has scrolled to the bottom, but not change the scrolling when the user has
 * changed the scroll position.
 */
class ScrollingWidget extends dist_index_es6_js_.Widget {
    constructor({ content, ...options }) {
        super(options);
        this._observer = null;
        this.addClass('jp-Scrolling');
        const layout = (this.layout = new dist_index_es6_js_.PanelLayout());
        layout.addWidget(content);
        this._content = content;
        this._sentinel = document.createElement('div');
        this.node.appendChild(this._sentinel);
    }
    /**
     * The content widget.
     */
    get content() {
        return this._content;
    }
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        // defer so content gets a chance to attach first
        requestAnimationFrame(() => {
            this._sentinel.scrollIntoView();
            this._scrollHeight = this.node.scrollHeight;
        });
        // Set up intersection observer for the sentinel
        if (typeof IntersectionObserver !== 'undefined') {
            this._observer = new IntersectionObserver(args => {
                this._handleScroll(args);
            }, { root: this.node, threshold: 1 });
            this._observer.observe(this._sentinel);
        }
    }
    onBeforeDetach(msg) {
        if (this._observer) {
            this._observer.disconnect();
        }
    }
    onAfterShow(msg) {
        if (this._tracking) {
            this._sentinel.scrollIntoView();
        }
    }
    _handleScroll([entry]) {
        if (entry.isIntersecting) {
            this._tracking = true;
        }
        else if (this.isVisible) {
            const currentHeight = this.node.scrollHeight;
            if (currentHeight === this._scrollHeight) {
                // Likely the user scrolled manually
                this._tracking = false;
            }
            else {
                // We assume we scrolled because our size changed, so scroll to the end.
                this._sentinel.scrollIntoView();
                this._scrollHeight = currentHeight;
                this._tracking = true;
            }
        }
    }
}
/**
 * A StackedPanel implementation that creates Output Areas
 * for each log source and activates as source is switched.
 */
class LogConsolePanel extends dist_index_es6_js_.StackedPanel {
    /**
     * Construct a LogConsolePanel instance.
     *
     * @param loggerRegistry - The logger registry that provides
     * logs to be displayed.
     */
    constructor(loggerRegistry, translator) {
        super();
        this._outputAreas = new Map();
        this._source = null;
        this._sourceChanged = new index_es6_js_.Signal(this);
        this._sourceDisplayed = new index_es6_js_.Signal(this);
        this._loggersWatched = new Set();
        this.translator = translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._loggerRegistry = loggerRegistry;
        this.addClass('jp-LogConsolePanel');
        loggerRegistry.registryChanged.connect((sender, args) => {
            this._bindLoggerSignals();
        }, this);
        this._bindLoggerSignals();
        this._placeholder = new dist_index_es6_js_.Widget();
        this._placeholder.addClass('jp-LogConsoleListPlaceholder');
        this.addWidget(this._placeholder);
    }
    /**
     * The logger registry providing the logs.
     */
    get loggerRegistry() {
        return this._loggerRegistry;
    }
    /**
     * The current logger.
     */
    get logger() {
        if (this.source === null) {
            return null;
        }
        return this.loggerRegistry.getLogger(this.source);
    }
    /**
     * The log source displayed
     */
    get source() {
        return this._source;
    }
    set source(name) {
        if (name === this._source) {
            return;
        }
        const oldValue = this._source;
        const newValue = (this._source = name);
        this._showOutputFromSource(newValue);
        this._handlePlaceholder();
        this._sourceChanged.emit({ oldValue, newValue, name: 'source' });
    }
    /**
     * The source version displayed.
     */
    get sourceVersion() {
        const source = this.source;
        return source !== null
            ? this._loggerRegistry.getLogger(source).version
            : null;
    }
    /**
     * Signal for source changes
     */
    get sourceChanged() {
        return this._sourceChanged;
    }
    /**
     * Signal for source changes
     */
    get sourceDisplayed() {
        return this._sourceDisplayed;
    }
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this._updateOutputAreas();
        this._showOutputFromSource(this._source);
        this._handlePlaceholder();
    }
    onAfterShow(msg) {
        super.onAfterShow(msg);
        if (this.source !== null) {
            this._sourceDisplayed.emit({
                source: this.source,
                version: this.sourceVersion
            });
        }
    }
    _bindLoggerSignals() {
        const loggers = this._loggerRegistry.getLoggers();
        for (const logger of loggers) {
            if (this._loggersWatched.has(logger.source)) {
                continue;
            }
            logger.contentChanged.connect((sender, args) => {
                this._updateOutputAreas();
                this._handlePlaceholder();
            }, this);
            logger.stateChanged.connect((sender, change) => {
                if (change.name !== 'rendermime') {
                    return;
                }
                const viewId = `source:${sender.source}`;
                const outputArea = this._outputAreas.get(viewId);
                if (outputArea) {
                    if (change.newValue) {
                        // cast away readonly
                        outputArea.rendermime = change.newValue;
                    }
                    else {
                        outputArea.dispose();
                    }
                }
            }, this);
            this._loggersWatched.add(logger.source);
        }
    }
    _showOutputFromSource(source) {
        // If the source is null, pick a unique name so all output areas hide.
        const viewId = source === null ? 'null source' : `source:${source}`;
        this._outputAreas.forEach((outputArea, name) => {
            var _a, _b;
            // Show/hide the output area parents, the scrolling windows.
            if (outputArea.id === viewId) {
                (_a = outputArea.parent) === null || _a === void 0 ? void 0 : _a.show();
                if (outputArea.isVisible) {
                    this._sourceDisplayed.emit({
                        source: this.source,
                        version: this.sourceVersion
                    });
                }
            }
            else {
                (_b = outputArea.parent) === null || _b === void 0 ? void 0 : _b.hide();
            }
        });
        const title = source === null
            ? this._trans.__('Log Console')
            : this._trans.__('Log: %1', source);
        this.title.label = title;
        this.title.caption = title;
    }
    _handlePlaceholder() {
        if (this.source === null) {
            this._placeholder.node.textContent = this._trans.__('No source selected.');
            this._placeholder.show();
        }
        else if (this._loggerRegistry.getLogger(this.source).length === 0) {
            this._placeholder.node.textContent = this._trans.__('No log messages.');
            this._placeholder.show();
        }
        else {
            this._placeholder.hide();
            this._placeholder.node.textContent = '';
        }
    }
    _updateOutputAreas() {
        const loggerIds = new Set();
        const loggers = this._loggerRegistry.getLoggers();
        for (const logger of loggers) {
            const source = logger.source;
            const viewId = `source:${source}`;
            loggerIds.add(viewId);
            // add view for logger if not exist
            if (!this._outputAreas.has(viewId)) {
                const outputArea = new LogConsoleOutputArea({
                    rendermime: logger.rendermime,
                    contentFactory: new LogConsoleContentFactory(),
                    model: logger.outputAreaModel
                });
                outputArea.id = viewId;
                // Attach the output area so it is visible, so the accounting
                // functions below record the outputs actually displayed.
                const w = new ScrollingWidget({
                    content: outputArea
                });
                this.addWidget(w);
                this._outputAreas.set(viewId, outputArea);
                // This is where the source object is associated with the output area.
                // We capture the source from this environment in the closure.
                const outputUpdate = (sender) => {
                    // If the current log console panel source is the source associated
                    // with this output area, and the output area is visible, then emit
                    // the logConsolePanel source displayed signal.
                    if (this.source === source && sender.isVisible) {
                        // We assume that the output area has been updated to the current
                        // version of the source.
                        this._sourceDisplayed.emit({
                            source: this.source,
                            version: this.sourceVersion
                        });
                    }
                };
                // Notify messages were displayed any time the output area is updated
                // and update for any outputs rendered on construction.
                outputArea.outputLengthChanged.connect(outputUpdate, this);
                // Since the output area was attached above, we can rely on its
                // visibility to account for the messages displayed.
                outputUpdate(outputArea);
            }
        }
        // remove output areas that do not have corresponding loggers anymore
        const viewIds = this._outputAreas.keys();
        for (const viewId of viewIds) {
            if (!loggerIds.has(viewId)) {
                const outputArea = this._outputAreas.get(viewId);
                outputArea === null || outputArea === void 0 ? void 0 : outputArea.dispose();
                this._outputAreas.delete(viewId);
            }
        }
    }
}

;// CONCATENATED MODULE: ../packages/logconsole/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module logconsole
 */






/***/ })

}]);
//# sourceMappingURL=6457.deb9610b64ad38c0fb76.js.map?v=deb9610b64ad38c0fb76