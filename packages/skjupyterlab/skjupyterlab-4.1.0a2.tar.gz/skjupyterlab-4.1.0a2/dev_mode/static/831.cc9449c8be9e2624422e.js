"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[831],{

/***/ 30831:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "ConnectionLost": () => (/* reexport */ ConnectionLost),
  "IConnectionLost": () => (/* reexport */ IConnectionLost),
  "ILabShell": () => (/* reexport */ ILabShell),
  "ILabStatus": () => (/* reexport */ ILabStatus),
  "ILayoutRestorer": () => (/* reexport */ ILayoutRestorer),
  "IMimeDocumentTracker": () => (/* reexport */ IMimeDocumentTracker),
  "IRouter": () => (/* reexport */ IRouter),
  "ITreePathUpdater": () => (/* reexport */ ITreePathUpdater),
  "JupyterFrontEnd": () => (/* reexport */ JupyterFrontEnd),
  "JupyterFrontEndContextMenu": () => (/* reexport */ JupyterFrontEndContextMenu),
  "JupyterLab": () => (/* reexport */ JupyterLab),
  "LabShell": () => (/* reexport */ LabShell),
  "LayoutRestorer": () => (/* reexport */ LayoutRestorer),
  "Router": () => (/* reexport */ Router),
  "createRendermimePlugin": () => (/* reexport */ createRendermimePlugin),
  "createRendermimePlugins": () => (/* reexport */ createRendermimePlugins),
  "createSemanticCommand": () => (/* reexport */ createSemanticCommand)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var lib_index_js_ = __webpack_require__(41948);
;// CONCATENATED MODULE: ../packages/application/lib/connectionlost.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A default connection lost handler, which brings up an error dialog.
 */
const ConnectionLost = async function (manager, err, translator) {
    translator = translator || lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    const title = trans.__('Server Connection Error');
    const networkMsg = trans.__('A connection to the Jupyter server could not be established.\n' +
        'JupyterLab will continue trying to reconnect.\n' +
        'Check your network connection or Jupyter server configuration.\n');
    return (0,index_js_.showErrorMessage)(title, { message: networkMsg });
};

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var services_lib_index_js_ = __webpack_require__(43411);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/application@^2.3.0-alpha.0 (singleton) (fallback: ../node_modules/@lumino/application/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(94418);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/application/lib/frontend.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The base Jupyter front-end application class.
 *
 * @typeparam `T` - The `shell` type. Defaults to `JupyterFrontEnd.IShell`.
 *
 * @typeparam `U` - The type for supported format names. Defaults to `string`.
 *
 * #### Notes
 * This type is useful as a generic application against which front-end plugins
 * can be authored. It inherits from the Lumino `Application`.
 */
class JupyterFrontEnd extends index_es6_js_.Application {
    /**
     * Construct a new JupyterFrontEnd object.
     */
    constructor(options) {
        super(options);
        this._formatChanged = new dist_index_es6_js_.Signal(this);
        // render context menu/submenus with inline svg icon tweaks
        this.contextMenu = new ui_components_lib_index_js_.ContextMenuSvg({
            commands: this.commands,
            renderer: options.contextMenuRenderer,
            groupByTarget: false,
            sortBySelector: false
        });
        // The default restored promise if one does not exist in the options.
        const restored = new Promise(resolve => {
            requestAnimationFrame(() => {
                resolve();
            });
        });
        this.commandLinker =
            options.commandLinker || new index_js_.CommandLinker({ commands: this.commands });
        this.docRegistry = options.docRegistry || new docregistry_lib_index_js_.DocumentRegistry();
        this.restored =
            options.restored ||
                this.started.then(() => restored).catch(() => restored);
        this.serviceManager = options.serviceManager || new services_lib_index_js_.ServiceManager();
    }
    /**
     * The application form factor, e.g., `desktop` or `mobile`.
     */
    get format() {
        return this._format;
    }
    set format(format) {
        if (this._format !== format) {
            this._format = format;
            document.body.dataset['format'] = format;
            this._formatChanged.emit(format);
        }
    }
    /**
     * A signal that emits when the application form factor changes.
     */
    get formatChanged() {
        return this._formatChanged;
    }
    /**
     * Walks up the DOM hierarchy of the target of the active `contextmenu`
     * event, testing each HTMLElement ancestor for a user-supplied function. This can
     * be used to find an HTMLElement on which to operate, given a context menu click.
     *
     * @param fn - a function that takes an `HTMLElement` and returns a
     *   boolean for whether it is the element the requester is seeking.
     *
     * @returns an HTMLElement or undefined, if none is found.
     */
    contextMenuHitTest(fn) {
        if (!this._contextMenuEvent ||
            !(this._contextMenuEvent.target instanceof Node)) {
            return undefined;
        }
        let node = this._contextMenuEvent.target;
        do {
            if (node instanceof HTMLElement && fn(node)) {
                return node;
            }
            node = node.parentNode;
        } while (node && node.parentNode && node !== node.parentNode);
        return undefined;
        // TODO: we should be able to use .composedPath() to simplify this function
        // down to something like the below, but it seems like composedPath is
        // sometimes returning an empty list.
        /*
        if (this._contextMenuEvent) {
          this._contextMenuEvent
            .composedPath()
            .filter(x => x instanceof HTMLElement)
            .find(test);
        }
        return undefined;
        */
    }
    /**
     * A method invoked on a document `'contextmenu'` event.
     */
    evtContextMenu(event) {
        this._contextMenuEvent = event;
        if (event.shiftKey ||
            Private.suppressContextMenu(event.target)) {
            return;
        }
        const opened = this.contextMenu.open(event);
        if (opened) {
            const items = this.contextMenu.menu.items;
            // If only the context menu information will be shown,
            // with no real commands, close the context menu and
            // allow the native one to open.
            if (items.length === 1 &&
                items[0].command === JupyterFrontEndContextMenu.contextMenu) {
                this.contextMenu.menu.close();
                return;
            }
            // Stop propagation and allow the application context menu to show.
            event.preventDefault();
            event.stopPropagation();
        }
    }
}
/**
 * The namespace for `JupyterFrontEnd` class statics.
 */
(function (JupyterFrontEnd) {
    /**
     * Is JupyterLab in document mode?
     *
     * @param path - Full URL of JupyterLab
     * @param paths - The current IPaths object hydrated from PageConfig.
     */
    function inDocMode(path, paths) {
        const docPattern = new RegExp(`^${paths.urls.doc}`);
        const match = path.match(docPattern);
        if (match) {
            return true;
        }
        else {
            return false;
        }
    }
    JupyterFrontEnd.inDocMode = inDocMode;
    /**
     * The application paths dictionary token.
     */
    JupyterFrontEnd.IPaths = new dist_index_js_.Token('@jupyterlab/application:IPaths', `A service providing information about various
  URLs and server paths for the current application. Use this service if you want to
  assemble URLs to use the JupyterLab REST API.`);
    /**
     * The application tree resolver token.
     *
     * #### Notes
     * Not all Jupyter front-end applications will have a tree resolver
     * implemented on the client-side. This token should not be required as a
     * dependency if it is possible to make it an optional dependency.
     */
    JupyterFrontEnd.ITreeResolver = new dist_index_js_.Token('@jupyterlab/application:ITreeResolver', 'A service to resolve the tree path.');
})(JupyterFrontEnd || (JupyterFrontEnd = {}));
/**
 * A namespace for module-private functionality.
 */
var Private;
(function (Private) {
    /**
     * Returns whether the element is itself, or a child of, an element with the `jp-suppress-context-menu` data attribute.
     */
    function suppressContextMenu(element) {
        return element.closest('[data-jp-suppress-context-menu]') !== null;
    }
    Private.suppressContextMenu = suppressContextMenu;
})(Private || (Private = {}));
/**
 * A namespace for the context menu override.
 */
var JupyterFrontEndContextMenu;
(function (JupyterFrontEndContextMenu) {
    /**
     * An id for a private context-menu-info ersatz command.
     */
    JupyterFrontEndContextMenu.contextMenu = '__internal:context-menu-info';
})(JupyterFrontEndContextMenu || (JupyterFrontEndContextMenu = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @lumino/properties@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/properties/dist/index.es6.js)
var properties_dist_index_es6_js_ = __webpack_require__(64260);
;// CONCATENATED MODULE: ../packages/application/lib/layoutrestorer.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/


/**
 * The layout restorer token.
 */
const ILayoutRestorer = new dist_index_js_.Token('@jupyterlab/application:ILayoutRestorer', 'A service providing application layout restoration functionality. Use this to have your activities restored across page loads.');
/**
 * The data connector key for restorer data.
 */
const KEY = 'layout-restorer:data';
/**
 * The default implementation of a layout restorer.
 *
 * #### Notes
 * The lifecycle for state restoration is subtle. The sequence of events is:
 *
 * 1. The layout restorer plugin is instantiated and makes a `fetch` call to
 *    the data connector that stores the layout restoration data. The `fetch`
 *    call returns a promise that resolves in step 6, below.
 *
 * 2. Other plugins that care about state restoration require the layout
 *    restorer as a dependency.
 *
 * 3. As each load-time plugin initializes (which happens before the front-end
 *    application has `started`), it instructs the layout restorer whether
 *    the restorer ought to `restore` its widgets by passing in its widget
 *    tracker.
 *    Alternatively, a plugin that does not require its own widget tracker
 *    (because perhaps it only creates a single widget, like a command palette),
 *    can simply `add` its widget along with a persistent unique name to the
 *    layout restorer so that its layout state can be restored when the lab
 *    application restores.
 *
 * 4. After all the load-time plugins have finished initializing, the front-end
 *    application `started` promise will resolve. This is the `first`
 *    promise that the layout restorer waits for. By this point, all of the
 *    plugins that care about restoration will have instructed the layout
 *    restorer to `restore` their widget trackers.
 *
 * 5. The layout restorer will then instruct each plugin's widget tracker
 *    to restore its state and reinstantiate whichever widgets it wants. The
 *    tracker returns a promise to the layout restorer that resolves when it
 *    has completed restoring the tracked widgets it cares about.
 *
 * 6. As each widget tracker finishes restoring the widget instances it cares
 *    about, it resolves the promise that was returned to the layout restorer
 *    (in step 5). After all of the promises that the restorer is awaiting have
 *    settled, the restorer then resolves the outstanding `fetch` promise
 *    (from step 1) and hands off a layout state object to the application
 *    shell's `restoreLayout` method for restoration.
 *
 * 7. Once the application shell has finished restoring the layout, the
 *    JupyterLab application's `restored` promise is resolved.
 *
 * Of particular note are steps 5 and 6: since data restoration of plugins
 * is accomplished by executing commands, the command that is used to restore
 * the data of each plugin must return a promise that only resolves when the
 * widget has been created and added to the plugin's widget tracker.
 */
class LayoutRestorer {
    /**
     * Create a layout restorer.
     */
    constructor(options) {
        this._deferred = new Array();
        this._deferredMainArea = null;
        this._firstDone = false;
        this._promisesDone = false;
        this._promises = [];
        this._restored = new dist_index_js_.PromiseDelegate();
        this._trackers = new Set();
        this._widgets = new Map();
        this._mode = 'multiple-document';
        this._connector = options.connector;
        this._first = options.first;
        this._registry = options.registry;
        if (options.mode) {
            this._mode = options.mode;
        }
        void this._first
            .then(() => {
            this._firstDone = true;
        })
            .then(() => Promise.all(this._promises))
            .then(() => {
            this._promisesDone = true;
            // Release the tracker set.
            this._trackers.clear();
        })
            .then(() => {
            this._restored.resolve(void 0);
        });
    }
    /**
     * Whether full layout restoration is deferred and is currently incomplete.
     *
     * #### Notes
     * This flag is useful for tracking when the application has started in
     * 'single-document' mode and the main area has not yet been restored.
     */
    get isDeferred() {
        return this._deferred.length > 0;
    }
    /**
     * A promise resolved when the layout restorer is ready to receive signals.
     */
    get restored() {
        return this._restored.promise;
    }
    /**
     * Add a widget to be tracked by the layout restorer.
     */
    add(widget, name) {
        layoutrestorer_Private.nameProperty.set(widget, name);
        this._widgets.set(name, widget);
        widget.disposed.connect(this._onWidgetDisposed, this);
    }
    /**
     * Fetch the layout state for the application.
     *
     * #### Notes
     * Fetching the layout relies on all widget restoration to be complete, so
     * calls to `fetch` are guaranteed to return after restoration is complete.
     */
    async fetch() {
        var _a;
        const blank = {
            fresh: true,
            mainArea: null,
            downArea: null,
            leftArea: null,
            rightArea: null,
            topArea: null,
            relativeSizes: null
        };
        const layout = this._connector.fetch(KEY);
        try {
            const [data] = await Promise.all([layout, this.restored]);
            if (!data) {
                return blank;
            }
            const { main, down, left, right, relativeSizes, top } = data;
            // If any data exists, then this is not a fresh session.
            const fresh = false;
            // Rehydrate main area.
            let mainArea = null;
            if (this._mode === 'multiple-document') {
                mainArea = this._rehydrateMainArea(main);
            }
            else {
                this._deferredMainArea = main;
            }
            // Rehydrate down area.
            const downArea = this._rehydrateDownArea(down);
            // Rehydrate left area.
            const leftArea = this._rehydrateSideArea(left);
            // Rehydrate right area.
            const rightArea = this._rehydrateSideArea(right);
            return {
                fresh,
                mainArea,
                downArea,
                leftArea,
                rightArea,
                relativeSizes: relativeSizes || null,
                topArea: (_a = top) !== null && _a !== void 0 ? _a : null
            };
        }
        catch (error) {
            return blank;
        }
    }
    /**
     * Restore the widgets of a particular widget tracker.
     *
     * @param tracker - The widget tracker whose widgets will be restored.
     *
     * @param options - The restoration options.
     */
    async restore(tracker, options) {
        if (this._firstDone) {
            throw new Error('restore() must be called before `first` has resolved.');
        }
        const { namespace } = tracker;
        if (this._trackers.has(namespace)) {
            throw new Error(`The tracker "${namespace}" is already restored.`);
        }
        const { args, command, name, when } = options;
        // Add the tracker to the private trackers collection.
        this._trackers.add(namespace);
        // Whenever a new widget is added to the tracker, record its name.
        tracker.widgetAdded.connect((_, widget) => {
            const widgetName = name(widget);
            if (widgetName) {
                this.add(widget, `${namespace}:${widgetName}`);
            }
        }, this);
        // Whenever a widget is updated, get its new name.
        tracker.widgetUpdated.connect((_, widget) => {
            const widgetName = name(widget);
            if (widgetName) {
                const name = `${namespace}:${widgetName}`;
                layoutrestorer_Private.nameProperty.set(widget, name);
                this._widgets.set(name, widget);
            }
        });
        const first = this._first;
        if (this._mode == 'multiple-document') {
            const promise = tracker
                .restore({
                args: args || (() => dist_index_js_.JSONExt.emptyObject),
                command,
                connector: this._connector,
                name,
                registry: this._registry,
                when: when ? [first].concat(when) : first
            })
                .catch(error => {
                console.error(error);
            });
            this._promises.push(promise);
            return promise;
        }
        tracker.defer({
            args: args || (() => dist_index_js_.JSONExt.emptyObject),
            command,
            connector: this._connector,
            name,
            registry: this._registry,
            when: when ? [first].concat(when) : first
        });
        this._deferred.push(tracker);
    }
    /**
     * Restore the application layout if its restoration has been deferred.
     *
     * @returns - the rehydrated main area.
     */
    async restoreDeferred() {
        if (!this.isDeferred) {
            return null;
        }
        // Empty the deferred list and wait for all trackers to restore.
        const wait = Promise.resolve();
        const promises = this._deferred.map(t => wait.then(() => t.restore()));
        this._deferred.length = 0;
        await Promise.all(promises);
        // Rehydrate the main area layout.
        return this._rehydrateMainArea(this._deferredMainArea);
    }
    /**
     * Save the layout state for the application.
     */
    save(layout) {
        // If there are promises that are unresolved, bail.
        if (!this._promisesDone) {
            const warning = 'save() was called prematurely.';
            console.warn(warning);
            return Promise.reject(warning);
        }
        const dehydrated = {};
        // Save the cached main area layout if restoration is deferred.
        dehydrated.main = this.isDeferred
            ? this._deferredMainArea
            : this._dehydrateMainArea(layout.mainArea);
        dehydrated.down = this._dehydrateDownArea(layout.downArea);
        dehydrated.left = this._dehydrateSideArea(layout.leftArea);
        dehydrated.right = this._dehydrateSideArea(layout.rightArea);
        dehydrated.relativeSizes = layout.relativeSizes;
        dehydrated.top = { ...layout.topArea };
        return this._connector.save(KEY, dehydrated);
    }
    /**
     * Dehydrate a main area description into a serializable object.
     */
    _dehydrateMainArea(area) {
        if (!area) {
            return null;
        }
        return layoutrestorer_Private.serializeMain(area);
    }
    /**
     * Rehydrate a serialized main area description object.
     *
     * #### Notes
     * This function consumes data that can become corrupted, so it uses type
     * coercion to guarantee the dehydrated object is safely processed.
     */
    _rehydrateMainArea(area) {
        if (!area) {
            return null;
        }
        return layoutrestorer_Private.deserializeMain(area, this._widgets);
    }
    /**
     * Dehydrate a down area description into a serializable object.
     */
    _dehydrateDownArea(area) {
        if (!area) {
            return null;
        }
        const dehydrated = {
            size: area.size
        };
        if (area.currentWidget) {
            const current = layoutrestorer_Private.nameProperty.get(area.currentWidget);
            if (current) {
                dehydrated.current = current;
            }
        }
        if (area.widgets) {
            dehydrated.widgets = area.widgets
                .map(widget => layoutrestorer_Private.nameProperty.get(widget))
                .filter(name => !!name);
        }
        return dehydrated;
    }
    /**
     * Rehydrate a serialized side area description object.
     *
     * #### Notes
     * This function consumes data that can become corrupted, so it uses type
     * coercion to guarantee the dehydrated object is safely processed.
     */
    _rehydrateDownArea(area) {
        var _a;
        if (!area) {
            return { currentWidget: null, size: 0.0, widgets: null };
        }
        const internal = this._widgets;
        const currentWidget = area.current && internal.has(`${area.current}`)
            ? internal.get(`${area.current}`)
            : null;
        const widgets = !Array.isArray(area.widgets)
            ? null
            : area.widgets
                .map(name => internal.has(`${name}`) ? internal.get(`${name}`) : null)
                .filter(widget => !!widget);
        return {
            currentWidget: currentWidget,
            size: (_a = area.size) !== null && _a !== void 0 ? _a : 0.0,
            widgets: widgets
        };
    }
    /**
     * Dehydrate a side area description into a serializable object.
     */
    _dehydrateSideArea(area) {
        if (!area) {
            return null;
        }
        const dehydrated = {
            collapsed: area.collapsed,
            visible: area.visible
        };
        if (area.currentWidget) {
            const current = layoutrestorer_Private.nameProperty.get(area.currentWidget);
            if (current) {
                dehydrated.current = current;
            }
        }
        if (area.widgets) {
            dehydrated.widgets = area.widgets
                .map(widget => layoutrestorer_Private.nameProperty.get(widget))
                .filter(name => !!name);
        }
        if (area.widgetStates) {
            dehydrated.widgetStates = area.widgetStates;
        }
        return dehydrated;
    }
    /**
     * Rehydrate a serialized side area description object.
     *
     * #### Notes
     * This function consumes data that can become corrupted, so it uses type
     * coercion to guarantee the dehydrated object is safely processed.
     */
    _rehydrateSideArea(area) {
        var _a, _b;
        if (!area) {
            return {
                collapsed: true,
                currentWidget: null,
                visible: true,
                widgets: null,
                widgetStates: {
                    ['null']: {
                        sizes: null,
                        expansionStates: null
                    }
                }
            };
        }
        const internal = this._widgets;
        const collapsed = (_a = area.collapsed) !== null && _a !== void 0 ? _a : false;
        const currentWidget = area.current && internal.has(`${area.current}`)
            ? internal.get(`${area.current}`)
            : null;
        const widgets = !Array.isArray(area.widgets)
            ? null
            : area.widgets
                .map(name => internal.has(`${name}`) ? internal.get(`${name}`) : null)
                .filter(widget => !!widget);
        const widgetStates = area.widgetStates;
        return {
            collapsed,
            currentWidget: currentWidget,
            widgets: widgets,
            visible: (_b = area.visible) !== null && _b !== void 0 ? _b : true,
            widgetStates: widgetStates
        };
    }
    /**
     * Handle a widget disposal.
     */
    _onWidgetDisposed(widget) {
        const name = layoutrestorer_Private.nameProperty.get(widget);
        this._widgets.delete(name);
    }
}
/*
 * A namespace for private data.
 */
var layoutrestorer_Private;
(function (Private) {
    /**
     * An attached property for a widget's ID in the serialized restore data.
     */
    Private.nameProperty = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'name',
        create: owner => ''
    });
    /**
     * Serialize individual areas within the main area.
     */
    function serializeArea(area) {
        if (!area || !area.type) {
            return null;
        }
        if (area.type === 'tab-area') {
            return {
                type: 'tab-area',
                currentIndex: area.currentIndex,
                widgets: area.widgets
                    .map(widget => Private.nameProperty.get(widget))
                    .filter(name => !!name)
            };
        }
        return {
            type: 'split-area',
            orientation: area.orientation,
            sizes: area.sizes,
            children: area.children
                .map(serializeArea)
                .filter(area => !!area)
        };
    }
    /**
     * Return a dehydrated, serializable version of the main dock panel.
     */
    function serializeMain(area) {
        const dehydrated = {
            dock: (area && area.dock && serializeArea(area.dock.main)) || null
        };
        if (area) {
            if (area.currentWidget) {
                const current = Private.nameProperty.get(area.currentWidget);
                if (current) {
                    dehydrated.current = current;
                }
            }
        }
        return dehydrated;
    }
    Private.serializeMain = serializeMain;
    /**
     * Deserialize individual areas within the main area.
     *
     * #### Notes
     * Because this data comes from a potentially unreliable foreign source, it is
     * typed as a `JSONObject`; but the actual expected type is:
     * `ITabArea | ISplitArea`.
     *
     * For fault tolerance, types are manually checked in deserialization.
     */
    function deserializeArea(area, names) {
        if (!area) {
            return null;
        }
        // Because this data is saved to a foreign data source, its type safety is
        // not guaranteed when it is retrieved, so exhaustive checks are necessary.
        const type = area.type || 'unknown';
        if (type === 'unknown' || (type !== 'tab-area' && type !== 'split-area')) {
            console.warn(`Attempted to deserialize unknown type: ${type}`);
            return null;
        }
        if (type === 'tab-area') {
            const { currentIndex, widgets } = area;
            const hydrated = {
                type: 'tab-area',
                currentIndex: currentIndex || 0,
                widgets: (widgets &&
                    widgets
                        .map(widget => names.get(widget))
                        .filter(widget => !!widget)) ||
                    []
            };
            // Make sure the current index is within bounds.
            if (hydrated.currentIndex > hydrated.widgets.length - 1) {
                hydrated.currentIndex = 0;
            }
            return hydrated;
        }
        const { orientation, sizes, children } = area;
        const hydrated = {
            type: 'split-area',
            orientation: orientation,
            sizes: sizes || [],
            children: (children &&
                children
                    .map(child => deserializeArea(child, names))
                    .filter(widget => !!widget)) ||
                []
        };
        return hydrated;
    }
    /**
     * Return the hydrated version of the main dock panel, ready to restore.
     *
     * #### Notes
     * Because this data comes from a potentially unreliable foreign source, it is
     * typed as a `JSONObject`; but the actual expected type is: `IMainArea`.
     *
     * For fault tolerance, types are manually checked in deserialization.
     */
    function deserializeMain(area, names) {
        if (!area) {
            return null;
        }
        const name = area.current || null;
        const dock = area.dock || null;
        return {
            currentWidget: (name && names.has(name) && names.get(name)) || null,
            dock: dock ? { main: deserializeArea(dock, names) } : null
        };
    }
    Private.deserializeMain = deserializeMain;
})(layoutrestorer_Private || (layoutrestorer_Private = {}));

;// CONCATENATED MODULE: ../packages/application/lib/mimerenderers.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The mime document tracker token.
 */
const IMimeDocumentTracker = new dist_index_js_.Token('@jupyterlab/application:IMimeDocumentTracker', 'A widget tracker for documents rendered using a mime renderer extension. Use this if you want to list and interact with documents rendered by such extensions.');
/**
 * Create rendermime plugins for rendermime extension modules.
 */
function createRendermimePlugins(extensions) {
    const plugins = [];
    const namespace = 'application-mimedocuments';
    const tracker = new index_js_.WidgetTracker({ namespace });
    extensions.forEach(mod => {
        let data = mod.default;
        // Handle CommonJS exports.
        if (!mod.hasOwnProperty('__esModule')) {
            data = mod;
        }
        if (!Array.isArray(data)) {
            data = [data];
        }
        data.forEach(item => {
            plugins.push(createRendermimePlugin(tracker, item));
        });
    });
    // Also add a meta-plugin handling state restoration
    // and exposing the mime document widget tracker.
    plugins.push({
        id: '@jupyterlab/application:mimedocument',
        description: 'Provides a mime document widget tracker.',
        optional: [ILayoutRestorer],
        provides: IMimeDocumentTracker,
        autoStart: true,
        activate: (app, restorer) => {
            if (restorer) {
                void restorer.restore(tracker, {
                    command: 'docmanager:open',
                    args: widget => ({
                        path: widget.context.path,
                        factory: mimerenderers_Private.factoryNameProperty.get(widget)
                    }),
                    name: widget => `${widget.context.path}:${mimerenderers_Private.factoryNameProperty.get(widget)}`
                });
            }
            return tracker;
        }
    });
    return plugins;
}
/**
 * Create rendermime plugins for rendermime extension modules.
 */
function createRendermimePlugin(tracker, item) {
    return {
        id: item.id,
        description: item.description,
        requires: [rendermime_lib_index_js_.IRenderMimeRegistry, lib_index_js_.ITranslator],
        autoStart: true,
        activate: (app, rendermime, translator) => {
            // Add the mime renderer.
            if (item.rank !== undefined) {
                rendermime.addFactory(item.rendererFactory, item.rank);
            }
            else {
                rendermime.addFactory(item.rendererFactory);
            }
            // Handle the widget factory.
            if (!item.documentWidgetFactoryOptions) {
                return;
            }
            const registry = app.docRegistry;
            let options = [];
            if (Array.isArray(item.documentWidgetFactoryOptions)) {
                options = item.documentWidgetFactoryOptions;
            }
            else {
                options = [
                    item.documentWidgetFactoryOptions
                ];
            }
            if (item.fileTypes) {
                item.fileTypes.forEach(ft => {
                    if (ft.icon) {
                        // upconvert the contents of the icon field to a proper LabIcon
                        ft = { ...ft, icon: ui_components_lib_index_js_.LabIcon.resolve({ icon: ft.icon }) };
                    }
                    app.docRegistry.addFileType(ft);
                });
            }
            options.forEach(option => {
                const toolbarFactory = option.toolbarFactory
                    ? (w) => option.toolbarFactory(w.content.renderer)
                    : undefined;
                const factory = new docregistry_lib_index_js_.MimeDocumentFactory({
                    renderTimeout: item.renderTimeout,
                    dataType: item.dataType,
                    rendermime,
                    modelName: option.modelName,
                    name: option.name,
                    primaryFileType: registry.getFileType(option.primaryFileType),
                    fileTypes: option.fileTypes,
                    defaultFor: option.defaultFor,
                    defaultRendered: option.defaultRendered,
                    toolbarFactory,
                    translator,
                    factory: item.rendererFactory
                });
                registry.addWidgetFactory(factory);
                factory.widgetCreated.connect((sender, widget) => {
                    mimerenderers_Private.factoryNameProperty.set(widget, factory.name);
                    // Notify the widget tracker if restore data needs to update.
                    widget.context.pathChanged.connect(() => {
                        void tracker.save(widget);
                    });
                    void tracker.add(widget);
                });
            });
        }
    };
}
/**
 * Private namespace for the module.
 */
var mimerenderers_Private;
(function (Private) {
    /**
     * An attached property for keeping the factory name
     * that was used to create a mimedocument.
     */
    Private.factoryNameProperty = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'factoryName',
        create: () => undefined
    });
})(mimerenderers_Private || (mimerenderers_Private = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/messaging@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/messaging/dist/index.es6.js)
var messaging_dist_index_es6_js_ = __webpack_require__(85755);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var polling_dist_index_es6_js_ = __webpack_require__(81967);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/application/lib/shell.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.









/**
 * The class name added to AppShell instances.
 */
const APPLICATION_SHELL_CLASS = 'jp-LabShell';
/**
 * The class name added to side bar instances.
 */
const SIDEBAR_CLASS = 'jp-SideBar';
/**
 * The class name added to the current widget's title.
 */
const CURRENT_CLASS = 'jp-mod-current';
/**
 * The class name added to the active widget's title.
 */
const ACTIVE_CLASS = 'jp-mod-active';
/**
 * The default rank of items added to a sidebar.
 */
const DEFAULT_RANK = 900;
const ACTIVITY_CLASS = 'jp-Activity';
/**
 * The JupyterLab application shell token.
 */
const ILabShell = new dist_index_js_.Token('@jupyterlab/application:ILabShell', 'A service for interacting with the JupyterLab shell. The top-level ``application`` object also has a reference to the shell, but it has a restricted interface in order to be agnostic to different shell implementations on the application. Use this to get more detailed information about currently active widgets and layout state.');
/**
 * The application shell for JupyterLab.
 */
class LabShell extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct a new application shell.
     */
    constructor(options) {
        super();
        /**
         * A message hook for child add/remove messages on the main area dock panel.
         */
        this._dockChildHook = (handler, msg) => {
            switch (msg.type) {
                case 'child-added':
                    msg.child.addClass(ACTIVITY_CLASS);
                    this._tracker.add(msg.child);
                    break;
                case 'child-removed':
                    msg.child.removeClass(ACTIVITY_CLASS);
                    this._tracker.remove(msg.child);
                    break;
                default:
                    break;
            }
            return true;
        };
        this._activeChanged = new dist_index_es6_js_.Signal(this);
        this._cachedLayout = null;
        this._currentChanged = new dist_index_es6_js_.Signal(this);
        this._currentPath = '';
        this._currentPathChanged = new dist_index_es6_js_.Signal(this);
        this._modeChanged = new dist_index_es6_js_.Signal(this);
        this._isRestored = false;
        this._layoutModified = new dist_index_es6_js_.Signal(this);
        this._layoutDebouncer = new polling_dist_index_es6_js_.Debouncer(() => {
            this._layoutModified.emit(undefined);
        }, 0);
        this._restored = new dist_index_js_.PromiseDelegate();
        this._tracker = new widgets_dist_index_es6_js_.FocusTracker();
        this._topHandlerHiddenByUser = false;
        this._idTypeMap = new Map();
        this._mainOptionsCache = new Map();
        this._sideOptionsCache = new Map();
        this._delayedWidget = new Array();
        this.addClass(APPLICATION_SHELL_CLASS);
        this.id = 'main';
        if ((options === null || options === void 0 ? void 0 : options.waitForRestore) === false) {
            this._userLayout = { 'multiple-document': {}, 'single-document': {} };
        }
        // Skip Links
        const skipLinkWidget = (this._skipLinkWidget = new shell_Private.SkipLinkWidget(this));
        this._skipLinkWidget.show();
        //  Wrap the skip widget to customize its position and size
        const skipLinkWrapper = new widgets_dist_index_es6_js_.Panel();
        skipLinkWrapper.addClass('jp-skiplink-wrapper');
        skipLinkWrapper.addWidget(skipLinkWidget);
        const headerPanel = (this._headerPanel = new widgets_dist_index_es6_js_.BoxPanel());
        const menuHandler = (this._menuHandler = new shell_Private.PanelHandler());
        menuHandler.panel.node.setAttribute('role', 'navigation');
        const topHandler = (this._topHandler = new shell_Private.PanelHandler());
        topHandler.panel.node.setAttribute('role', 'banner');
        const bottomPanel = (this._bottomPanel = new widgets_dist_index_es6_js_.BoxPanel());
        bottomPanel.node.setAttribute('role', 'contentinfo');
        const hboxPanel = new widgets_dist_index_es6_js_.BoxPanel();
        const vsplitPanel = (this._vsplitPanel =
            new shell_Private.RestorableSplitPanel());
        const dockPanel = (this._dockPanel = new ui_components_lib_index_js_.DockPanelSvg({
            hiddenMode: widgets_dist_index_es6_js_.Widget.HiddenMode.Display
        }));
        messaging_dist_index_es6_js_.MessageLoop.installMessageHook(dockPanel, this._dockChildHook);
        const hsplitPanel = (this._hsplitPanel =
            new shell_Private.RestorableSplitPanel());
        const downPanel = (this._downPanel = new ui_components_lib_index_js_.TabPanelSvg({
            tabsMovable: true
        }));
        const leftHandler = (this._leftHandler = new shell_Private.SideBarHandler());
        const rightHandler = (this._rightHandler = new shell_Private.SideBarHandler());
        const rootLayout = new widgets_dist_index_es6_js_.BoxLayout();
        headerPanel.id = 'jp-header-panel';
        menuHandler.panel.id = 'jp-menu-panel';
        topHandler.panel.id = 'jp-top-panel';
        bottomPanel.id = 'jp-bottom-panel';
        hboxPanel.id = 'jp-main-content-panel';
        vsplitPanel.id = 'jp-main-vsplit-panel';
        dockPanel.id = 'jp-main-dock-panel';
        hsplitPanel.id = 'jp-main-split-panel';
        downPanel.id = 'jp-down-stack';
        leftHandler.sideBar.addClass(SIDEBAR_CLASS);
        leftHandler.sideBar.addClass('jp-mod-left');
        leftHandler.sideBar.node.setAttribute('role', 'complementary');
        leftHandler.stackedPanel.id = 'jp-left-stack';
        rightHandler.sideBar.addClass(SIDEBAR_CLASS);
        rightHandler.sideBar.addClass('jp-mod-right');
        rightHandler.sideBar.node.setAttribute('role', 'complementary');
        rightHandler.stackedPanel.id = 'jp-right-stack';
        dockPanel.node.setAttribute('role', 'main');
        hboxPanel.spacing = 0;
        vsplitPanel.spacing = 1;
        dockPanel.spacing = 5;
        hsplitPanel.spacing = 1;
        headerPanel.direction = 'top-to-bottom';
        vsplitPanel.orientation = 'vertical';
        hboxPanel.direction = 'left-to-right';
        hsplitPanel.orientation = 'horizontal';
        bottomPanel.direction = 'bottom-to-top';
        widgets_dist_index_es6_js_.SplitPanel.setStretch(leftHandler.stackedPanel, 0);
        widgets_dist_index_es6_js_.SplitPanel.setStretch(downPanel, 0);
        widgets_dist_index_es6_js_.SplitPanel.setStretch(dockPanel, 1);
        widgets_dist_index_es6_js_.SplitPanel.setStretch(rightHandler.stackedPanel, 0);
        widgets_dist_index_es6_js_.BoxPanel.setStretch(leftHandler.sideBar, 0);
        widgets_dist_index_es6_js_.BoxPanel.setStretch(hsplitPanel, 1);
        widgets_dist_index_es6_js_.BoxPanel.setStretch(rightHandler.sideBar, 0);
        widgets_dist_index_es6_js_.SplitPanel.setStretch(vsplitPanel, 1);
        hsplitPanel.addWidget(leftHandler.stackedPanel);
        hsplitPanel.addWidget(dockPanel);
        hsplitPanel.addWidget(rightHandler.stackedPanel);
        vsplitPanel.addWidget(hsplitPanel);
        vsplitPanel.addWidget(downPanel);
        hboxPanel.addWidget(leftHandler.sideBar);
        hboxPanel.addWidget(vsplitPanel);
        hboxPanel.addWidget(rightHandler.sideBar);
        rootLayout.direction = 'top-to-bottom';
        rootLayout.spacing = 0; // TODO make this configurable?
        // Use relative sizing to set the width of the side panels.
        // This will still respect the min-size of children widget in the stacked
        // panel. The default sizes will be overwritten during layout restoration.
        vsplitPanel.setRelativeSizes([3, 1]);
        hsplitPanel.setRelativeSizes([1, 2.5, 1]);
        widgets_dist_index_es6_js_.BoxLayout.setStretch(headerPanel, 0);
        widgets_dist_index_es6_js_.BoxLayout.setStretch(menuHandler.panel, 0);
        widgets_dist_index_es6_js_.BoxLayout.setStretch(topHandler.panel, 0);
        widgets_dist_index_es6_js_.BoxLayout.setStretch(hboxPanel, 1);
        widgets_dist_index_es6_js_.BoxLayout.setStretch(bottomPanel, 0);
        rootLayout.addWidget(skipLinkWrapper);
        rootLayout.addWidget(headerPanel);
        rootLayout.addWidget(topHandler.panel);
        rootLayout.addWidget(hboxPanel);
        rootLayout.addWidget(bottomPanel);
        // initially hiding header and bottom panel when no elements inside,
        this._headerPanel.hide();
        this._bottomPanel.hide();
        this._downPanel.hide();
        this.layout = rootLayout;
        // Connect change listeners.
        this._tracker.currentChanged.connect(this._onCurrentChanged, this);
        this._tracker.activeChanged.connect(this._onActiveChanged, this);
        // Connect main layout change listener.
        this._dockPanel.layoutModified.connect(this._onLayoutModified, this);
        // Connect vsplit layout change listener
        this._vsplitPanel.updated.connect(this._onLayoutModified, this);
        // Connect down panel change listeners
        this._downPanel.currentChanged.connect(this._onLayoutModified, this);
        this._downPanel.tabBar.tabMoved.connect(this._onTabPanelChanged, this);
        this._downPanel.stackedPanel.widgetRemoved.connect(this._onTabPanelChanged, this);
        // Catch current changed events on the side handlers.
        this._leftHandler.updated.connect(this._onLayoutModified, this);
        this._rightHandler.updated.connect(this._onLayoutModified, this);
        // Catch update events on the horizontal split panel
        this._hsplitPanel.updated.connect(this._onLayoutModified, this);
        // Setup single-document-mode title bar
        const titleHandler = (this._titleHandler = new shell_Private.TitleHandler(this));
        this.add(titleHandler, 'top', { rank: 1000 }); // 添加标题
        if (this._dockPanel.mode === 'multiple-document') {
            this._topHandler.addWidget(this._menuHandler.panel, 100); // 菜单工具栏
            titleHandler.hide();
        }
        else {
            rootLayout.insertWidget(3, this._menuHandler.panel);
        }
        this.translator = lib_index_js_.nullTranslator;
        // Wire up signals to update the title panel of the simple interface mode to
        // follow the title of this.currentWidget
        this.currentChanged.connect((sender, args) => {
            let newValue = args.newValue;
            let oldValue = args.oldValue;
            // Stop watching the title of the previously current widget
            if (oldValue) {
                oldValue.title.changed.disconnect(this._updateTitlePanelTitle, this);
                if (oldValue instanceof docregistry_lib_index_js_.DocumentWidget) {
                    oldValue.context.pathChanged.disconnect(this._updateCurrentPath, this);
                }
            }
            // Start watching the title of the new current widget
            if (newValue) {
                newValue.title.changed.connect(this._updateTitlePanelTitle, this);
                this._updateTitlePanelTitle();
                if (newValue instanceof docregistry_lib_index_js_.DocumentWidget) {
                    newValue.context.pathChanged.connect(this._updateCurrentPath, this);
                }
            }
            this._updateCurrentPath();
        });
    }
    /**
     * A signal emitted when main area's active focus changes.
     */
    get activeChanged() {
        return this._activeChanged;
    }
    /**
     * The active widget in the shell's main area.
     */
    get activeWidget() {
        return this._tracker.activeWidget;
    }
    /**
     * Whether the add buttons for each main area tab bar are enabled.
     */
    get addButtonEnabled() {
        return this._dockPanel.addButtonEnabled;
    }
    set addButtonEnabled(value) {
        this._dockPanel.addButtonEnabled = value;
    }
    /**
     * A signal emitted when the add button on a main area tab bar is clicked.
     */
    get addRequested() {
        return this._dockPanel.addRequested;
    }
    /**
     * A signal emitted when main area's current focus changes.
     */
    get currentChanged() {
        return this._currentChanged;
    }
    /**
     * Current document path.
     */
    // FIXME deprecation `undefined` is to ensure backward compatibility in 4.x
    get currentPath() {
        return this._currentPath;
    }
    /**
     * A signal emitted when the path of the current document changes.
     *
     * This also fires when the current document itself changes.
     */
    get currentPathChanged() {
        return this._currentPathChanged;
    }
    /**
     * The current widget in the shell's main area.
     */
    get currentWidget() {
        return this._tracker.currentWidget;
    }
    /**
     * A signal emitted when the main area's layout is modified.
     */
    get layoutModified() {
        return this._layoutModified;
    }
    /**
     * Whether the left area is collapsed.
     */
    get leftCollapsed() {
        return !this._leftHandler.sideBar.currentTitle;
    }
    /**
     * Whether the left area is collapsed.
     */
    get rightCollapsed() {
        return !this._rightHandler.sideBar.currentTitle;
    }
    /**
     * Whether JupyterLab is in presentation mode with the
     * `jp-mod-presentationMode` CSS class.
     */
    get presentationMode() {
        return this.hasClass('jp-mod-presentationMode');
    }
    set presentationMode(value) {
        this.toggleClass('jp-mod-presentationMode', value);
    }
    /**
     * The main dock area's user interface mode.
     */
    get mode() {
        return this._dockPanel.mode;
    }
    set mode(mode) {
        const dock = this._dockPanel;
        if (mode === dock.mode) {
            return;
        }
        const applicationCurrentWidget = this.currentWidget;
        if (mode === 'single-document') {
            // Cache the current multi-document layout before changing the mode.
            this._cachedLayout = dock.saveLayout();
            dock.mode = mode;
            // In case the active widget in the dock panel is *not* the active widget
            // of the application, defer to the application.
            if (this.currentWidget) {
                dock.activateWidget(this.currentWidget);
            }
            // Adjust menu and title
            // 单文档界面布局设置
            //   (this.layout as BoxLayout).insertWidget(3, this._menuHandler.panel);
            this._titleHandler.show();
            //   this._updateTitlePanelTitle();
            //   if (this._topHandlerHiddenByUser) {
            //     this._topHandler.panel.hide();
            //   }
        }
        else {
            // Cache a reference to every widget currently in the dock panel before
            // changing its mode.
            const widgets = Array.from(dock.widgets());
            dock.mode = mode;
            // Restore cached layout if possible.
            if (this._cachedLayout) {
                // Remove any disposed widgets in the cached layout and restore.
                shell_Private.normalizeAreaConfig(dock, this._cachedLayout.main);
                dock.restoreLayout(this._cachedLayout);
                this._cachedLayout = null;
            }
            // If layout restoration has been deferred, restore layout now.
            if (this._layoutRestorer.isDeferred) {
                this._layoutRestorer
                    .restoreDeferred()
                    .then(mainArea => {
                    if (mainArea) {
                        const { currentWidget, dock } = mainArea;
                        if (dock) {
                            this._dockPanel.restoreLayout(dock);
                        }
                        if (currentWidget) {
                            this.activateById(currentWidget.id);
                        }
                    }
                })
                    .catch(reason => {
                    console.error('Failed to restore the deferred layout.');
                    console.error(reason);
                });
            }
            // Add any widgets created during single document mode, which have
            // subsequently been removed from the dock panel after the multiple document
            // layout has been restored. If the widget has add options cached for
            // the widget (i.e., if it has been placed with respect to another widget),
            // then take that into account.
            widgets.forEach(widget => {
                if (!widget.parent) {
                    this._addToMainArea(widget, {
                        ...this._mainOptionsCache.get(widget),
                        activate: false
                    });
                }
            });
            this._mainOptionsCache.clear();
            // In case the active widget in the dock panel is *not* the active widget
            // of the application, defer to the application.
            if (applicationCurrentWidget) {
                dock.activateWidget(applicationCurrentWidget);
            }
            // Adjust menu and title
            this.add(this._menuHandler.panel, 'top', { rank: 100 });
            this._titleHandler.hide();
        }
        // Set the mode data attribute on the applications shell node.
        this.node.dataset.shellMode = mode;
        this._downPanel.fit();
        // Emit the mode changed signal
        this._modeChanged.emit(mode);
    }
    /**
     * A signal emitted when the shell/dock panel change modes (single/multiple document).
     */
    get modeChanged() {
        return this._modeChanged;
    }
    /**
     * Promise that resolves when state is first restored, returning layout
     * description.
     */
    get restored() {
        return this._restored.promise;
    }
    get translator() {
        var _a;
        return (_a = this._translator) !== null && _a !== void 0 ? _a : lib_index_js_.nullTranslator;
    }
    set translator(value) {
        if (value !== this._translator) {
            this._translator = value;
            // Set translator for tab bars
            ui_components_lib_index_js_.TabBarSvg.translator = value;
            const trans = value.load('jupyterlab');
            this._menuHandler.panel.node.setAttribute('aria-label', trans.__('main'));
            this._leftHandler.sideBar.node.setAttribute('aria-label', trans.__('main sidebar'));
            this._leftHandler.sideBar.contentNode.setAttribute('aria-label', trans.__('main sidebar'));
            this._rightHandler.sideBar.node.setAttribute('aria-label', trans.__('alternate sidebar'));
            this._rightHandler.sideBar.contentNode.setAttribute('aria-label', trans.__('alternate sidebar'));
        }
    }
    /**
     * User customized shell layout.
     */
    get userLayout() {
        return dist_index_js_.JSONExt.deepCopy(this._userLayout);
    }
    /**
     * Activate a widget in its area.
     */
    activateById(id) {
        if (this._leftHandler.has(id)) {
            this._leftHandler.activate(id);
            return;
        }
        if (this._rightHandler.has(id)) {
            this._rightHandler.activate(id);
            return;
        }
        const tabIndex = this._downPanel.tabBar.titles.findIndex(title => title.owner.id === id);
        if (tabIndex >= 0) {
            this._downPanel.currentIndex = tabIndex;
            return;
        }
        const dock = this._dockPanel;
        const widget = (0,algorithm_dist_index_es6_js_.find)(dock.widgets(), value => value.id === id);
        if (widget) {
            dock.activateWidget(widget);
        }
    }
    /**
     * Activate the next Tab in the active TabBar.
     */
    activateNextTab() {
        const current = this._currentTabBar();
        if (!current) {
            return;
        }
        const ci = current.currentIndex;
        if (ci === -1) {
            return;
        }
        if (ci < current.titles.length - 1) {
            current.currentIndex += 1;
            if (current.currentTitle) {
                current.currentTitle.owner.activate();
            }
            return;
        }
        if (ci === current.titles.length - 1) {
            const nextBar = this._adjacentBar('next');
            if (nextBar) {
                nextBar.currentIndex = 0;
                if (nextBar.currentTitle) {
                    nextBar.currentTitle.owner.activate();
                }
            }
        }
    }
    /**
     * Activate the previous Tab in the active TabBar.
     */
    activatePreviousTab() {
        const current = this._currentTabBar();
        if (!current) {
            return;
        }
        const ci = current.currentIndex;
        if (ci === -1) {
            return;
        }
        if (ci > 0) {
            current.currentIndex -= 1;
            if (current.currentTitle) {
                current.currentTitle.owner.activate();
            }
            return;
        }
        if (ci === 0) {
            const prevBar = this._adjacentBar('previous');
            if (prevBar) {
                const len = prevBar.titles.length;
                prevBar.currentIndex = len - 1;
                if (prevBar.currentTitle) {
                    prevBar.currentTitle.owner.activate();
                }
            }
        }
    }
    /**
     * Activate the next TabBar.
     */
    activateNextTabBar() {
        const nextBar = this._adjacentBar('next');
        if (nextBar) {
            if (nextBar.currentTitle) {
                nextBar.currentTitle.owner.activate();
            }
        }
    }
    /**
     * Activate the next TabBar.
     */
    activatePreviousTabBar() {
        const nextBar = this._adjacentBar('previous');
        if (nextBar) {
            if (nextBar.currentTitle) {
                nextBar.currentTitle.owner.activate();
            }
        }
    }
    /**
     * Add a widget to the JupyterLab shell
     *
     * @param widget Widget
     * @param area Area
     * @param options Options
     */
    add(widget, area = 'main', options) {
        var _a;
        if (!this._userLayout) {
            this._delayedWidget.push({ widget, area, options });
            return;
        }
        let userPosition;
        if ((options === null || options === void 0 ? void 0 : options.type) && this._userLayout[this.mode][options.type]) {
            userPosition = this._userLayout[this.mode][options.type];
            this._idTypeMap.set(widget.id, options.type);
        }
        else {
            userPosition = this._userLayout[this.mode][widget.id];
        }
        if (options === null || options === void 0 ? void 0 : options.type) {
            this._idTypeMap.set(widget.id, options.type);
            widget.disposed.connect(() => {
                this._idTypeMap.delete(widget.id);
            });
        }
        area = (_a = userPosition === null || userPosition === void 0 ? void 0 : userPosition.area) !== null && _a !== void 0 ? _a : area;
        options =
            options || (userPosition === null || userPosition === void 0 ? void 0 : userPosition.options)
                ? {
                    ...options,
                    ...userPosition === null || userPosition === void 0 ? void 0 : userPosition.options
                }
                : undefined;
        switch (area || 'main') {
            case 'bottom':
                return this._addToBottomArea(widget, options);
            case 'down':
                return this._addToDownArea(widget, options);
            case 'header':
                return this._addToHeaderArea(widget, options);
            case 'left':
                return this._addToLeftArea(widget, options);
            case 'main':
                return this._addToMainArea(widget, options);
            case 'menu':
                return this._addToMenuArea(widget, options);
            case 'right':
                return this._addToRightArea(widget, options);
            case 'top':
                return this._addToTopArea(widget, options);
            default:
                throw new Error(`Invalid area: ${area}`);
        }
    }
    /**
     * Move a widget type to a new area.
     *
     * The type is determined from the `widget.id` and fallback to `widget.id`.
     *
     * #### Notes
     * If `mode` is undefined, both mode are updated.
     * The new layout is now persisted.
     *
     * @param widget Widget to move
     * @param area New area
     * @param mode Mode to change
     * @returns The new user layout
     */
    move(widget, area, mode) {
        var _a;
        const type = (_a = this._idTypeMap.get(widget.id)) !== null && _a !== void 0 ? _a : widget.id;
        for (const m of ['single-document', 'multiple-document'].filter(c => !mode || c === mode)) {
            this._userLayout[m][type] = {
                ...this._userLayout[m][type],
                area
            };
        }
        this.add(widget, area);
        return this._userLayout;
    }
    /**
     * Collapse the left area.
     */
    collapseLeft() {
        this._leftHandler.collapse();
        this._onLayoutModified();
    }
    /**
     * Collapse the right area.
     */
    collapseRight() {
        this._rightHandler.collapse();
        this._onLayoutModified();
    }
    /**
     * Dispose the shell.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._layoutDebouncer.dispose();
        super.dispose();
    }
    /**
     * Expand the left area.
     *
     * #### Notes
     * This will open the most recently used tab,
     * or the first tab if there is no most recently used.
     */
    expandLeft() {
        this._leftHandler.expand();
        this._onLayoutModified();
    }
    /**
     * Expand the right area.
     *
     * #### Notes
     * This will open the most recently used tab,
     * or the first tab if there is no most recently used.
     */
    expandRight() {
        this._rightHandler.expand();
        this._onLayoutModified();
    }
    /**
     * Close all widgets in the main and down area.
     */
    closeAll() {
        // Make a copy of all the widget in the dock panel (using `Array.from()`)
        // before removing them because removing them while iterating through them
        // modifies the underlying data of the iterator.
        Array.from(this._dockPanel.widgets()).forEach(widget => widget.close());
        this._downPanel.stackedPanel.widgets.forEach(widget => widget.close());
    }
    /**
     * Whether an side tab bar is visible or not.
     *
     * @param side Sidebar of interest
     * @returns Side tab bar visibility
     */
    isSideTabBarVisible(side) {
        switch (side) {
            case 'left':
                return this._leftHandler.isVisible;
            case 'right':
                return this._rightHandler.isVisible;
        }
    }
    /**
     * Whether the top bar in simple mode is visible or not.
     *
     * @returns Top bar visibility
     */
    isTopInSimpleModeVisible() {
        return !this._topHandlerHiddenByUser;
    }
    /**
     * True if the given area is empty.
     */
    isEmpty(area) {
        switch (area) {
            case 'bottom':
                return this._bottomPanel.widgets.length === 0;
            case 'down':
                return this._downPanel.stackedPanel.widgets.length === 0;
            case 'header':
                return this._headerPanel.widgets.length === 0;
            case 'left':
                return this._leftHandler.stackedPanel.widgets.length === 0;
            case 'main':
                return this._dockPanel.isEmpty;
            case 'menu':
                return this._menuHandler.panel.widgets.length === 0;
            case 'right':
                return this._rightHandler.stackedPanel.widgets.length === 0;
            case 'top':
                return this._topHandler.panel.widgets.length === 0;
            default:
                return true;
        }
    }
    /**
     * Restore the layout state and configuration for the application shell.
     *
     * #### Notes
     * This should only be called once.
     */
    async restoreLayout(mode, layoutRestorer, configuration = {}) {
        var _a, _b, _c, _d;
        // Set the configuration and add widgets added before the shell was ready.
        this._userLayout = {
            'single-document': (_a = configuration['single-document']) !== null && _a !== void 0 ? _a : {},
            'multiple-document': (_b = configuration['multiple-document']) !== null && _b !== void 0 ? _b : {}
        };
        this._delayedWidget.forEach(({ widget, area, options }) => {
            this.add(widget, area, options);
        });
        this._delayedWidget.length = 0;
        this._layoutRestorer = layoutRestorer;
        // Get the layout from the restorer
        const layout = await layoutRestorer.fetch();
        // Reset the layout
        const { mainArea, downArea, leftArea, rightArea, topArea, relativeSizes } = layout;
        // Rehydrate the main area.
        if (mainArea) {
            const { currentWidget, dock } = mainArea;
            if (dock && mode === 'multiple-document') {
                this._dockPanel.restoreLayout(dock);
            }
            if (mode) {
                this.mode = mode;
            }
            if (currentWidget) {
                this.activateById(currentWidget.id);
            }
        }
        else {
            // This is needed when loading in an empty workspace in single doc mode
            if (mode) {
                this.mode = mode;
            }
        }
        if ((topArea === null || topArea === void 0 ? void 0 : topArea.simpleVisibility) !== undefined) {
            this._topHandlerHiddenByUser = !topArea.simpleVisibility;
            if (this.mode === 'single-document') {
                this._topHandler.panel.setHidden(this._topHandlerHiddenByUser);
            }
        }
        // Rehydrate the down area
        if (downArea) {
            const { currentWidget, widgets, size } = downArea;
            const widgetIds = (_c = widgets === null || widgets === void 0 ? void 0 : widgets.map(widget => widget.id)) !== null && _c !== void 0 ? _c : [];
            // Remove absent widgets
            this._downPanel.tabBar.titles
                .filter(title => !widgetIds.includes(title.owner.id))
                .map(title => title.owner.close());
            // Add new widgets
            const titleIds = this._downPanel.tabBar.titles.map(title => title.owner.id);
            widgets === null || widgets === void 0 ? void 0 : widgets.filter(widget => !titleIds.includes(widget.id)).map(widget => this._downPanel.addWidget(widget));
            // Reorder tabs
            while (!algorithm_dist_index_es6_js_.ArrayExt.shallowEqual(widgetIds, this._downPanel.tabBar.titles.map(title => title.owner.id))) {
                this._downPanel.tabBar.titles.forEach((title, index) => {
                    const position = widgetIds.findIndex(id => title.owner.id == id);
                    if (position >= 0 && position != index) {
                        this._downPanel.tabBar.insertTab(position, title);
                    }
                });
            }
            if (currentWidget) {
                const index = this._downPanel.stackedPanel.widgets.findIndex(widget => widget.id === currentWidget.id);
                if (index) {
                    this._downPanel.currentIndex = index;
                    (_d = this._downPanel.currentWidget) === null || _d === void 0 ? void 0 : _d.activate();
                }
            }
            if (size && size > 0.0) {
                this._vsplitPanel.setRelativeSizes([1.0 - size, size]);
            }
            else {
                // Close all tabs and hide the panel
                this._downPanel.stackedPanel.widgets.forEach(widget => widget.close());
                this._downPanel.hide();
            }
        }
        // Rehydrate the left area.
        if (leftArea) {
            this._leftHandler.rehydrate(leftArea);
        }
        else {
            if (mode === 'single-document') {
                this.collapseLeft();
            }
        }
        // Rehydrate the right area.
        if (rightArea) {
            this._rightHandler.rehydrate(rightArea);
        }
        else {
            if (mode === 'single-document') {
                this.collapseRight();
            }
        }
        // Restore the relative sizes.
        if (relativeSizes) {
            this._hsplitPanel.setRelativeSizes(relativeSizes);
        }
        if (!this._isRestored) {
            // Make sure all messages in the queue are finished before notifying
            // any extensions that are waiting for the promise that guarantees the
            // application state has been restored.
            messaging_dist_index_es6_js_.MessageLoop.flush();
            this._restored.resolve(layout);
        }
    }
    /**
     * Save the dehydrated state of the application shell.
     */
    saveLayout() {
        // If the application is in single document mode, use the cached layout if
        // available. Otherwise, default to querying the dock panel for layout.
        const layout = {
            mainArea: {
                currentWidget: this._tracker.currentWidget,
                dock: this.mode === 'single-document'
                    ? this._cachedLayout || this._dockPanel.saveLayout()
                    : this._dockPanel.saveLayout()
            },
            downArea: {
                currentWidget: this._downPanel.currentWidget,
                widgets: Array.from(this._downPanel.stackedPanel.widgets),
                size: this._vsplitPanel.relativeSizes()[1]
            },
            leftArea: this._leftHandler.dehydrate(),
            rightArea: this._rightHandler.dehydrate(),
            topArea: { simpleVisibility: !this._topHandlerHiddenByUser },
            relativeSizes: this._hsplitPanel.relativeSizes()
        };
        return layout;
    }
    /**
     * Toggle top header visibility in simple mode
     *
     * Note: Does nothing in multi-document mode
     */
    toggleTopInSimpleModeVisibility() {
        if (this.mode === 'single-document') {
            if (this._topHandler.panel.isVisible) {
                this._topHandlerHiddenByUser = true;
                this._topHandler.panel.hide();
            }
            else {
                this._topHandlerHiddenByUser = false;
                this._topHandler.panel.show();
                this._updateTitlePanelTitle();
            }
            this._onLayoutModified();
        }
    }
    /**
     * Toggle side tab bar visibility
     *
     * @param side Sidebar of interest
     */
    toggleSideTabBarVisibility(side) {
        if (side === 'right') {
            if (this._rightHandler.isVisible) {
                this._rightHandler.hide();
            }
            else {
                this._rightHandler.show();
            }
        }
        else {
            if (this._leftHandler.isVisible) {
                this._leftHandler.hide();
            }
            else {
                this._leftHandler.show();
            }
        }
    }
    /**
     * Update the shell configuration.
     *
     * @param config Shell configuration
     */
    updateConfig(config) {
        if (config.hiddenMode) {
            switch (config.hiddenMode) {
                case 'display':
                    this._dockPanel.hiddenMode = widgets_dist_index_es6_js_.Widget.HiddenMode.Display;
                    break;
                case 'scale':
                    this._dockPanel.hiddenMode = widgets_dist_index_es6_js_.Widget.HiddenMode.Scale;
                    break;
                case 'contentVisibility':
                    this._dockPanel.hiddenMode = widgets_dist_index_es6_js_.Widget.HiddenMode.ContentVisibility;
                    break;
            }
        }
    }
    /**
     * Returns the widgets for an application area.
     */
    widgets(area) {
        switch (area !== null && area !== void 0 ? area : 'main') {
            case 'main':
                return this._dockPanel.widgets();
            case 'left':
                return (0,algorithm_dist_index_es6_js_.map)(this._leftHandler.sideBar.titles, t => t.owner);
            case 'right':
                return (0,algorithm_dist_index_es6_js_.map)(this._rightHandler.sideBar.titles, t => t.owner);
            case 'header':
                return this._headerPanel.children();
            case 'top':
                return this._topHandler.panel.children();
            case 'menu':
                return this._menuHandler.panel.children();
            case 'bottom':
                return this._bottomPanel.children();
            default:
                throw new Error(`Invalid area: ${area}`);
        }
    }
    /**
     * Handle `after-attach` messages for the application shell.
     */
    onAfterAttach(msg) {
        this.node.dataset.shellMode = this.mode;
    }
    /**
     * Update the title panel title based on the title of the current widget.
     */
    _updateTitlePanelTitle() {
        let current = this.currentWidget;
        const inputElement = this._titleHandler.inputElement;
        inputElement.value = current ? current.title.label : '';
        inputElement.title = current ? current.title.caption : '';
    }
    /**
     * The path of the current widget changed, fire the _currentPathChanged signal.
     */
    _updateCurrentPath() {
        let current = this.currentWidget;
        let newValue = '';
        if (current && current instanceof docregistry_lib_index_js_.DocumentWidget) {
            newValue = current.context.path;
        }
        this._currentPathChanged.emit({
            newValue: newValue,
            oldValue: this._currentPath
        });
        this._currentPath = newValue;
    }
    /**
     * Add a widget to the left content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    _addToLeftArea(widget, options) {
        if (!widget.id) {
            console.error('Widgets added to app shell must have unique id property.');
            return;
        }
        options = options || this._sideOptionsCache.get(widget) || {};
        this._sideOptionsCache.set(widget, options);
        const rank = 'rank' in options ? options.rank : DEFAULT_RANK;
        this._leftHandler.addWidget(widget, rank);
        this._onLayoutModified();
    }
    /**
     * Add a widget to the main content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     * All widgets added to the main area should be disposed after removal
     * (disposal before removal will remove the widget automatically).
     *
     * In the options, `ref` defaults to `null`, `mode` defaults to `'tab-after'`,
     * and `activate` defaults to `true`.
     */
    _addToMainArea(widget, options) {
        if (!widget.id) {
            console.error('Widgets added to app shell must have unique id property.');
            return;
        }
        options = options || {};
        const dock = this._dockPanel;
        const mode = options.mode || 'tab-after';
        let ref = this.currentWidget;
        if (options.ref) {
            ref = (0,algorithm_dist_index_es6_js_.find)(dock.widgets(), value => value.id === options.ref) || null;
        }
        const { title } = widget;
        // Add widget ID to tab so that we can get a handle on the tab's widget
        // (for context menu support)
        title.dataset = { ...title.dataset, id: widget.id };
        if (title.icon instanceof ui_components_lib_index_js_.LabIcon) {
            // bind an appropriate style to the icon
            title.icon = title.icon.bindprops({
                stylesheet: 'mainAreaTab'
            });
        }
        else if (typeof title.icon === 'string' || !title.icon) {
            // add some classes to help with displaying css background imgs
            title.iconClass = (0,ui_components_lib_index_js_.classes)(title.iconClass, 'jp-Icon');
        }
        dock.addWidget(widget, { mode, ref });
        // The dock panel doesn't account for placement information while
        // in single document mode, so upon rehydrating any widgets that were
        // added will not be in the correct place. Cache the placement information
        // here so that we can later rehydrate correctly.
        if (dock.mode === 'single-document') {
            this._mainOptionsCache.set(widget, options);
        }
        if (options.activate !== false) {
            dock.activateWidget(widget);
        }
    }
    /**
     * Add a widget to the right content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    _addToRightArea(widget, options) {
        if (!widget.id) {
            console.error('Widgets added to app shell must have unique id property.');
            return;
        }
        options = options || this._sideOptionsCache.get(widget) || {};
        const rank = 'rank' in options ? options.rank : DEFAULT_RANK;
        this._sideOptionsCache.set(widget, options);
        this._rightHandler.addWidget(widget, rank);
        this._onLayoutModified();
    }
    /**
     * Add a widget to the top content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    _addToTopArea(widget, options) {
        var _a;
        if (!widget.id) {
            console.error('Widgets added to app shell must have unique id property.');
            return;
        }
        options = options || {};
        const rank = (_a = options.rank) !== null && _a !== void 0 ? _a : DEFAULT_RANK;
        this._topHandler.addWidget(widget, rank);
        this._onLayoutModified();
        if (this._topHandler.panel.isHidden) {
            this._topHandler.panel.show();
        }
    }
    /**
     * Add a widget to the title content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    _addToMenuArea(widget, options) {
        var _a;
        if (!widget.id) {
            console.error('Widgets added to app shell must have unique id property.');
            return;
        }
        options = options || {};
        const rank = (_a = options.rank) !== null && _a !== void 0 ? _a : DEFAULT_RANK;
        this._menuHandler.addWidget(widget, rank);
        this._onLayoutModified();
        if (this._menuHandler.panel.isHidden) {
            this._menuHandler.panel.show();
        }
    }
    /**
     * Add a widget to the header content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    _addToHeaderArea(widget, options) {
        if (!widget.id) {
            console.error('Widgets added to app shell must have unique id property.');
            return;
        }
        // Temporary: widgets are added to the panel in order of insertion.
        this._headerPanel.addWidget(widget);
        this._onLayoutModified();
        if (this._headerPanel.isHidden) {
            this._headerPanel.show();
        }
    }
    /**
     * Add a widget to the bottom content area.
     *
     * #### Notes
     * Widgets must have a unique `id` property, which will be used as the DOM id.
     */
    _addToBottomArea(widget, options) {
        if (!widget.id) {
            console.error('Widgets added to app shell must have unique id property.');
            return;
        }
        // Temporary: widgets are added to the panel in order of insertion.
        this._bottomPanel.addWidget(widget);
        this._onLayoutModified();
        if (this._bottomPanel.isHidden) {
            this._bottomPanel.show();
        }
    }
    _addToDownArea(widget, options) {
        if (!widget.id) {
            console.error('Widgets added to app shell must have unique id property.');
            return;
        }
        options = options || {};
        const { title } = widget;
        // Add widget ID to tab so that we can get a handle on the tab's widget
        // (for context menu support)
        title.dataset = { ...title.dataset, id: widget.id };
        if (title.icon instanceof ui_components_lib_index_js_.LabIcon) {
            // bind an appropriate style to the icon
            title.icon = title.icon.bindprops({
                stylesheet: 'mainAreaTab'
            });
        }
        else if (typeof title.icon === 'string' || !title.icon) {
            // add some classes to help with displaying css background imgs
            title.iconClass = (0,ui_components_lib_index_js_.classes)(title.iconClass, 'jp-Icon');
        }
        this._downPanel.addWidget(widget);
        this._onLayoutModified();
        if (this._downPanel.isHidden) {
            this._downPanel.show();
        }
    }
    /*
     * Return the tab bar adjacent to the current TabBar or `null`.
     */
    _adjacentBar(direction) {
        const current = this._currentTabBar();
        if (!current) {
            return null;
        }
        const bars = Array.from(this._dockPanel.tabBars());
        const len = bars.length;
        const index = bars.indexOf(current);
        if (direction === 'previous') {
            return index > 0 ? bars[index - 1] : index === 0 ? bars[len - 1] : null;
        }
        // Otherwise, direction is 'next'.
        return index < len - 1
            ? bars[index + 1]
            : index === len - 1
                ? bars[0]
                : null;
    }
    /*
     * Return the TabBar that has the currently active Widget or null.
     */
    _currentTabBar() {
        const current = this._tracker.currentWidget;
        if (!current) {
            return null;
        }
        const title = current.title;
        const bars = this._dockPanel.tabBars();
        return (0,algorithm_dist_index_es6_js_.find)(bars, bar => bar.titles.indexOf(title) > -1) || null;
    }
    /**
     * Handle a change to the dock area active widget.
     */
    _onActiveChanged(sender, args) {
        if (args.newValue) {
            args.newValue.title.className += ` ${ACTIVE_CLASS}`;
        }
        if (args.oldValue) {
            args.oldValue.title.className = args.oldValue.title.className.replace(ACTIVE_CLASS, '');
        }
        this._activeChanged.emit(args);
    }
    /**
     * Handle a change to the dock area current widget.
     */
    _onCurrentChanged(sender, args) {
        if (args.newValue) {
            args.newValue.title.className += ` ${CURRENT_CLASS}`;
        }
        if (args.oldValue) {
            args.oldValue.title.className = args.oldValue.title.className.replace(CURRENT_CLASS, '');
        }
        this._currentChanged.emit(args);
        this._onLayoutModified();
    }
    /**
     * Handle a change on the down panel widgets
     */
    _onTabPanelChanged() {
        if (this._downPanel.stackedPanel.widgets.length === 0) {
            this._downPanel.hide();
        }
        this._onLayoutModified();
    }
    /**
     * Handle a change to the layout.
     */
    _onLayoutModified() {
        void this._layoutDebouncer.invoke();
    }
}
var shell_Private;
(function (Private) {
    /**
     * A less-than comparison function for side bar rank items.
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
    /**
     * Removes widgets that have been disposed from an area config, mutates area.
     */
    function normalizeAreaConfig(parent, area) {
        if (!area) {
            return;
        }
        if (area.type === 'tab-area') {
            area.widgets = area.widgets.filter(widget => !widget.isDisposed && widget.parent === parent);
            return;
        }
        area.children.forEach(child => {
            normalizeAreaConfig(parent, child);
        });
    }
    Private.normalizeAreaConfig = normalizeAreaConfig;
    /**
     * A class which manages a panel and sorts its widgets by rank.
     */
    class PanelHandler {
        constructor() {
            /**
             * A message hook for child add/remove messages on the main area dock panel.
             */
            this._panelChildHook = (handler, msg) => {
                switch (msg.type) {
                    case 'child-added':
                        {
                            const widget = msg.child;
                            // If we already know about this widget, we're done
                            if (this._items.find(v => v.widget === widget)) {
                                break;
                            }
                            // Otherwise, add to the end by default
                            const rank = this._items[this._items.length - 1].rank;
                            this._items.push({ widget, rank });
                        }
                        break;
                    case 'child-removed':
                        {
                            const widget = msg.child;
                            algorithm_dist_index_es6_js_.ArrayExt.removeFirstWhere(this._items, v => v.widget === widget);
                        }
                        break;
                    default:
                        break;
                }
                return true;
            };
            this._items = new Array();
            this._panel = new widgets_dist_index_es6_js_.Panel();
            messaging_dist_index_es6_js_.MessageLoop.installMessageHook(this._panel, this._panelChildHook);
        }
        /**
         * Get the panel managed by the handler.
         */
        get panel() {
            return this._panel;
        }
        /**
         * Add a widget to the panel.
         *
         * If the widget is already added, it will be moved.
         */
        addWidget(widget, rank) {
            widget.parent = null;
            const item = { widget, rank };
            const index = algorithm_dist_index_es6_js_.ArrayExt.upperBound(this._items, item, Private.itemCmp);
            algorithm_dist_index_es6_js_.ArrayExt.insert(this._items, index, item);
            this._panel.insertWidget(index, widget);
        }
    }
    Private.PanelHandler = PanelHandler;
    /**
     * A class which manages a side bar and related stacked panel.
     */
    class SideBarHandler {
        /**
         * Construct a new side bar handler.
         */
        constructor() {
            this._isHiddenByUser = false;
            this._items = new Array();
            this._updated = new dist_index_es6_js_.Signal(this);
            this._sideBar = new widgets_dist_index_es6_js_.TabBar({
                insertBehavior: 'none',
                removeBehavior: 'none',
                allowDeselect: true,
                orientation: 'vertical'
            });
            this._stackedPanel = new widgets_dist_index_es6_js_.StackedPanel();
            this._sideBar.hide();
            this._stackedPanel.hide();
            this._lastCurrent = null;
            this._sideBar.currentChanged.connect(this._onCurrentChanged, this);
            this._sideBar.tabActivateRequested.connect(this._onTabActivateRequested, this);
            this._stackedPanel.widgetRemoved.connect(this._onWidgetRemoved, this);
        }
        /**
         * Whether the side bar is visible
         */
        get isVisible() {
            return this._sideBar.isVisible;
        }
        /**
         * Get the tab bar managed by the handler.
         */
        get sideBar() {
            return this._sideBar;
        }
        /**
         * Get the stacked panel managed by the handler
         */
        get stackedPanel() {
            return this._stackedPanel;
        }
        /**
         * Signal fires when the stack panel or the sidebar changes
         */
        get updated() {
            return this._updated;
        }
        /**
         * Handles a movement to the handles of a widget
         */
        _onHandleMoved() {
            return this._refreshVisibility();
        }
        /**
         * Handles changes to the expansion status of a widget
         */
        _onExpansionToggle(sender, index) {
            return this._refreshVisibility();
        }
        /**
         * Expand the sidebar.
         *
         * #### Notes
         * This will open the most recently used tab, or the first tab
         * if there is no most recently used.
         */
        expand() {
            const previous = this._lastCurrent || (this._items.length > 0 && this._items[0].widget);
            if (previous) {
                this.activate(previous.id);
            }
        }
        /**
         * Activate a widget residing in the side bar by ID.
         *
         * @param id - The widget's unique ID.
         */
        activate(id) {
            const widget = this._findWidgetByID(id);
            if (widget) {
                this._sideBar.currentTitle = widget.title;
                widget.activate();
            }
        }
        /**
         * Test whether the sidebar has the given widget by id.
         */
        has(id) {
            return this._findWidgetByID(id) !== null;
        }
        /**
         * Collapse the sidebar so no items are expanded.
         */
        collapse() {
            this._sideBar.currentTitle = null;
        }
        /**
         * Add a widget and its title to the stacked panel and side bar.
         *
         * If the widget is already added, it will be moved.
         */
        addWidget(widget, rank) {
            var _a, _b, _c, _d;
            widget.parent = null;
            widget.hide();
            const item = { widget, rank };
            const index = this._findInsertIndex(item);
            algorithm_dist_index_es6_js_.ArrayExt.insert(this._items, index, item);
            this._stackedPanel.insertWidget(index, widget);
            const title = this._sideBar.insertTab(index, widget.title);
            // Store the parent id in the title dataset
            // in order to dispatch click events to the right widget.
            title.dataset = { id: widget.id };
            if (title.icon instanceof ui_components_lib_index_js_.LabIcon) {
                // bind an appropriate style to the icon
                title.icon = title.icon.bindprops({
                    stylesheet: 'sideBar'
                });
            }
            else if (typeof title.icon === 'string' && title.icon != '') {
                // add some classes to help with displaying css background imgs
                title.iconClass = (0,ui_components_lib_index_js_.classes)(title.iconClass, 'jp-Icon', 'jp-Icon-20');
            }
            else if (!title.icon && !title.label) {
                // add a fallback icon if there is no title label nor icon
                title.icon = ui_components_lib_index_js_.tabIcon.bindprops({
                    stylesheet: 'sideBar'
                });
            }
            // @ts-expect-error sometimes widget is an Accordion Panel
            (_b = (_a = widget.content) === null || _a === void 0 ? void 0 : _a.expansionToggled) === null || _b === void 0 ? void 0 : _b.connect(this._onExpansionToggle, this);
            // @ts-expect-error sometimes widget is a SidePanel
            (_d = (_c = widget.content) === null || _c === void 0 ? void 0 : _c.handleMoved) === null || _d === void 0 ? void 0 : _d.connect(this._onHandleMoved, this);
            this._refreshVisibility();
        }
        /**
         * Dehydrate the side bar data.
         */
        dehydrate() {
            const collapsed = this._sideBar.currentTitle === null;
            const widgets = Array.from(this._stackedPanel.widgets);
            const currentWidget = widgets[this._sideBar.currentIndex];
            const widgetStates = {};
            this._stackedPanel.widgets.forEach((w) => {
                if (w.id && w.content instanceof widgets_dist_index_es6_js_.SplitPanel) {
                    widgetStates[w.id] = {
                        sizes: w.content.relativeSizes(),
                        expansionStates: w.content.widgets.map(wi => wi.isVisible)
                    };
                }
            });
            return {
                collapsed,
                currentWidget,
                visible: !this._isHiddenByUser,
                widgets,
                widgetStates
            };
        }
        /**
         * Rehydrate the side bar.
         */
        rehydrate(data) {
            if (data.currentWidget) {
                this.activate(data.currentWidget.id);
            }
            if (data.collapsed) {
                this.collapse();
            }
            if (!data.visible) {
                this.hide();
            }
            if (data.widgetStates) {
                this._stackedPanel.widgets.forEach((w) => {
                    var _a;
                    if (w.id && w.content instanceof widgets_dist_index_es6_js_.SplitPanel) {
                        const state = (_a = data.widgetStates[w.id]) !== null && _a !== void 0 ? _a : {};
                        w.content.widgets.forEach((wi, widx) => {
                            var _a;
                            const expansion = ((_a = state.expansionStates) !== null && _a !== void 0 ? _a : [])[widx];
                            if (typeof expansion === 'boolean' &&
                                w.content instanceof widgets_dist_index_es6_js_.AccordionPanel) {
                                expansion ? w.content.expand(widx) : w.content.collapse(widx);
                            }
                        });
                        if (state.sizes) {
                            w.content.setRelativeSizes(state.sizes);
                        }
                    }
                });
            }
        }
        /**
         * Hide the side bar even if it contains widgets
         */
        hide() {
            this._isHiddenByUser = true;
            this._refreshVisibility();
        }
        /**
         * Show the side bar if it contains widgets
         */
        show() {
            this._isHiddenByUser = false;
            this._refreshVisibility();
        }
        /**
         * Find the insertion index for a rank item.
         */
        _findInsertIndex(item) {
            return algorithm_dist_index_es6_js_.ArrayExt.upperBound(this._items, item, Private.itemCmp);
        }
        /**
         * Find the index of the item with the given widget, or `-1`.
         */
        _findWidgetIndex(widget) {
            return algorithm_dist_index_es6_js_.ArrayExt.findFirstIndex(this._items, i => i.widget === widget);
        }
        /**
         * Find the widget which owns the given title, or `null`.
         */
        _findWidgetByTitle(title) {
            const item = (0,algorithm_dist_index_es6_js_.find)(this._items, value => value.widget.title === title);
            return item ? item.widget : null;
        }
        /**
         * Find the widget with the given id, or `null`.
         */
        _findWidgetByID(id) {
            const item = (0,algorithm_dist_index_es6_js_.find)(this._items, value => value.widget.id === id);
            return item ? item.widget : null;
        }
        /**
         * Refresh the visibility of the side bar and stacked panel.
         */
        _refreshVisibility() {
            this._stackedPanel.setHidden(this._sideBar.currentTitle === null);
            this._sideBar.setHidden(this._isHiddenByUser || this._sideBar.titles.length === 0);
            this._updated.emit();
        }
        /**
         * Handle the `currentChanged` signal from the sidebar.
         */
        _onCurrentChanged(sender, args) {
            const oldWidget = args.previousTitle
                ? this._findWidgetByTitle(args.previousTitle)
                : null;
            const newWidget = args.currentTitle
                ? this._findWidgetByTitle(args.currentTitle)
                : null;
            if (oldWidget) {
                oldWidget.hide();
            }
            if (newWidget) {
                newWidget.show();
            }
            this._lastCurrent = newWidget || oldWidget;
            this._refreshVisibility();
        }
        /**
         * Handle a `tabActivateRequest` signal from the sidebar.
         */
        _onTabActivateRequested(sender, args) {
            args.title.owner.activate();
        }
        /*
         * Handle the `widgetRemoved` signal from the stacked panel.
         */
        _onWidgetRemoved(sender, widget) {
            if (widget === this._lastCurrent) {
                this._lastCurrent = null;
            }
            algorithm_dist_index_es6_js_.ArrayExt.removeAt(this._items, this._findWidgetIndex(widget));
            this._sideBar.removeTab(widget.title);
            this._refreshVisibility();
        }
    }
    Private.SideBarHandler = SideBarHandler;
    class SkipLinkWidget extends widgets_dist_index_es6_js_.Widget {
        /**
         * Construct a new skipLink widget.
         */
        constructor(shell) {
            super();
            this.addClass('jp-skiplink');
            this.id = 'jp-skiplink';
            this._shell = shell;
            this._createSkipLink('Skip to left side bar');
        }
        handleEvent(event) {
            switch (event.type) {
                case 'click':
                    this._focusLeftSideBar();
                    break;
            }
        }
        /**
         * Handle `after-attach` messages for the widget.
         */
        onAfterAttach(msg) {
            super.onAfterAttach(msg);
            this.node.addEventListener('click', this);
        }
        /**
         * A message handler invoked on a `'before-detach'`
         * message
         */
        onBeforeDetach(msg) {
            this.node.removeEventListener('click', this);
            super.onBeforeDetach(msg);
        }
        _focusLeftSideBar() {
            this._shell.expandLeft();
        }
        _createSkipLink(skipLinkText) {
            const skipLink = document.createElement('a');
            skipLink.href = '#';
            skipLink.tabIndex = 1;
            skipLink.text = skipLinkText;
            skipLink.className = 'skip-link';
            this.node.appendChild(skipLink);
        }
    }
    Private.SkipLinkWidget = SkipLinkWidget;
    class TitleHandler extends widgets_dist_index_es6_js_.Widget {
        /**
         * Construct a new title handler.
         */
        constructor(shell) {
            super();
            this._selected = false;
            const inputElement = document.createElement('input');
            inputElement.type = 'text';
            this.node.appendChild(inputElement);
            this._shell = shell;
            this.id = 'jp-title-panel-title';
        }
        /**
         * Handle `after-attach` messages for the widget.
         */
        onAfterAttach(msg) {
            super.onAfterAttach(msg);
            this.inputElement.addEventListener('keyup', this);
            this.inputElement.addEventListener('click', this);
            this.inputElement.addEventListener('blur', this);
        }
        /**
         * Handle `before-detach` messages for the widget.
         */
        onBeforeDetach(msg) {
            super.onBeforeDetach(msg);
            this.inputElement.removeEventListener('keyup', this);
            this.inputElement.removeEventListener('click', this);
            this.inputElement.removeEventListener('blur', this);
        }
        handleEvent(event) {
            switch (event.type) {
                case 'keyup':
                    void this._evtKeyUp(event);
                    break;
                case 'click':
                    this._evtClick(event);
                    break;
                case 'blur':
                    this._selected = false;
                    break;
            }
        }
        /**
         * Handle `keyup` events on the handler.
         */
        async _evtKeyUp(event) {
            if (event.key == 'Enter') {
                const widget = this._shell.currentWidget;
                if (widget == null) {
                    return;
                }
                const oldName = widget.title.label;
                const inputElement = this.inputElement;
                const newName = inputElement.value;
                inputElement.blur();
                if (newName !== oldName) {
                    widget.title.label = newName;
                }
                else {
                    inputElement.value = oldName;
                }
            }
        }
        /**
         * Handle `click` events on the handler.
         */
        _evtClick(event) {
            // only handle primary button clicks
            if (event.button !== 0 || this._selected) {
                return;
            }
            const inputElement = this.inputElement;
            event.preventDefault();
            event.stopPropagation();
            this._selected = true;
            const selectEnd = inputElement.value.indexOf('.');
            if (selectEnd === -1) {
                inputElement.select();
            }
            else {
                inputElement.setSelectionRange(0, selectEnd);
            }
        }
        /**
         * The input element containing the parent widget's title.
         */
        get inputElement() {
            return this.node.children[0];
        }
    }
    Private.TitleHandler = TitleHandler;
    class RestorableSplitPanel extends widgets_dist_index_es6_js_.SplitPanel {
        constructor(options = {}) {
            super(options);
            this.updated = new dist_index_es6_js_.Signal(this);
        }
        /**
         * Emit 'updated' signal on 'update' requests.
         */
        onUpdateRequest(msg) {
            super.onUpdateRequest(msg);
            this.updated.emit();
        }
    }
    Private.RestorableSplitPanel = RestorableSplitPanel;
})(shell_Private || (shell_Private = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var disposable_dist_index_es6_js_ = __webpack_require__(78612);
;// CONCATENATED MODULE: ../packages/application/lib/status.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * The application status signals and flags class.
 */
class LabStatus {
    /**
     * Construct a new  status object.
     */
    constructor(app) {
        this._busyCount = 0;
        this._dirtyCount = 0;
        this._busySignal = new dist_index_es6_js_.Signal(app);
        this._dirtySignal = new dist_index_es6_js_.Signal(app);
    }
    /**
     * Returns a signal for when application changes its busy status.
     */
    get busySignal() {
        return this._busySignal;
    }
    /**
     * Returns a signal for when application changes its dirty status.
     */
    get dirtySignal() {
        return this._dirtySignal;
    }
    /**
     * Whether the application is busy.
     */
    get isBusy() {
        return this._busyCount > 0;
    }
    /**
     * Whether the application is dirty.
     */
    get isDirty() {
        return this._dirtyCount > 0;
    }
    /**
     * Set the application state to dirty.
     *
     * @returns A disposable used to clear the dirty state for the caller.
     */
    setDirty() {
        const oldDirty = this.isDirty;
        this._dirtyCount++;
        if (this.isDirty !== oldDirty) {
            this._dirtySignal.emit(this.isDirty);
        }
        return new disposable_dist_index_es6_js_.DisposableDelegate(() => {
            const oldDirty = this.isDirty;
            this._dirtyCount = Math.max(0, this._dirtyCount - 1);
            if (this.isDirty !== oldDirty) {
                this._dirtySignal.emit(this.isDirty);
            }
        });
    }
    /**
     * Set the application state to busy.
     *
     * @returns A disposable used to clear the busy state for the caller.
     */
    setBusy() {
        const oldBusy = this.isBusy;
        this._busyCount++;
        if (this.isBusy !== oldBusy) {
            this._busySignal.emit(this.isBusy);
        }
        return new disposable_dist_index_es6_js_.DisposableDelegate(() => {
            const oldBusy = this.isBusy;
            this._busyCount--;
            if (this.isBusy !== oldBusy) {
                this._busySignal.emit(this.isBusy);
            }
        });
    }
}

;// CONCATENATED MODULE: ../packages/application/lib/lab.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * JupyterLab is the main application class. It is instantiated once and shared.
 */
class JupyterLab extends JupyterFrontEnd {
    /**
     * Construct a new JupyterLab object.
     */
    constructor(options = { shell: new LabShell() }) {
        super({
            ...options,
            shell: options.shell || new LabShell(),
            serviceManager: options.serviceManager ||
                new services_lib_index_js_.ServiceManager({
                    standby: () => {
                        return !this._info.isConnected || 'when-hidden';
                    }
                })
        });
        /**
         * The name of the JupyterLab application.
         */
        this.name = coreutils_lib_index_js_.PageConfig.getOption('appName') || 'JupyterLab';
        /**
         * A namespace/prefix plugins may use to denote their provenance.
         */
        this.namespace = coreutils_lib_index_js_.PageConfig.getOption('appNamespace') || this.name;
        /**
         * A list of all errors encountered when registering plugins.
         */
        this.registerPluginErrors = [];
        /**
         * The application busy and dirty status signals and flags.
         */
        this.status = new LabStatus(this);
        /**
         * The version of the JupyterLab application.
         */
        this.version = coreutils_lib_index_js_.PageConfig.getOption('appVersion') || 'unknown';
        this._info = JupyterLab.defaultInfo;
        this._allPluginsActivated = new dist_index_js_.PromiseDelegate();
        // Create an IInfo dictionary from the options to override the defaults.
        const info = Object.keys(JupyterLab.defaultInfo).reduce((acc, val) => {
            if (val in options) {
                acc[val] = JSON.parse(JSON.stringify(options[val]));
            }
            return acc;
        }, {});
        // Populate application info.
        this._info = { ...JupyterLab.defaultInfo, ...info };
        this.restored = this.shell.restored
            .then(async () => {
            const activated = [];
            const deferred = this.activateDeferredPlugins().catch(error => {
                console.error('Error when activating deferred plugins\n:', error);
            });
            activated.push(deferred);
            if (this._info.deferred) {
                const customizedDeferred = Promise.all(this._info.deferred.matches.map(pluginID => this.activatePlugin(pluginID))).catch(error => {
                    console.error('Error when activating customized list of deferred plugins:\n', error);
                });
                activated.push(customizedDeferred);
            }
            Promise.all(activated)
                .then(() => {
                this._allPluginsActivated.resolve();
            })
                .catch(() => undefined);
        })
            .catch(() => undefined);
        // Populate application paths override the defaults if necessary.
        const defaultURLs = JupyterLab.defaultPaths.urls;
        const defaultDirs = JupyterLab.defaultPaths.directories;
        const optionURLs = (options.paths && options.paths.urls) || {};
        const optionDirs = (options.paths && options.paths.directories) || {};
        this._paths = {
            urls: Object.keys(defaultURLs).reduce((acc, key) => {
                if (key in optionURLs) {
                    const value = optionURLs[key];
                    acc[key] = value;
                }
                else {
                    acc[key] = defaultURLs[key];
                }
                return acc;
            }, {}),
            directories: Object.keys(JupyterLab.defaultPaths.directories).reduce((acc, key) => {
                if (key in optionDirs) {
                    const value = optionDirs[key];
                    acc[key] = value;
                }
                else {
                    acc[key] = defaultDirs[key];
                }
                return acc;
            }, {})
        };
        if (this._info.devMode) {
            this.shell.addClass('jp-mod-devMode');
        }
        // Add initial model factory.
        this.docRegistry.addModelFactory(new docregistry_lib_index_js_.Base64ModelFactory());
        if (options.mimeExtensions) {
            for (const plugin of createRendermimePlugins(options.mimeExtensions)) {
                this.registerPlugin(plugin);
            }
        }
    }
    /**
     * The JupyterLab application information dictionary.
     */
    get info() {
        return this._info;
    }
    /**
     * The JupyterLab application paths dictionary.
     */
    get paths() {
        return this._paths;
    }
    /**
     * Promise that resolves when all the plugins are activated, including the deferred.
     */
    get allPluginsActivated() {
        return this._allPluginsActivated.promise;
    }
    /**
     * Register plugins from a plugin module.
     *
     * @param mod - The plugin module to register.
     */
    registerPluginModule(mod) {
        let data = mod.default;
        // Handle commonjs exports.
        if (!mod.hasOwnProperty('__esModule')) {
            data = mod;
        }
        if (!Array.isArray(data)) {
            data = [data];
        }
        data.forEach(item => {
            try {
                this.registerPlugin(item);
            }
            catch (error) {
                this.registerPluginErrors.push(error);
            }
        });
    }
    /**
     * Register the plugins from multiple plugin modules.
     *
     * @param mods - The plugin modules to register.
     */
    registerPluginModules(mods) {
        mods.forEach(mod => {
            this.registerPluginModule(mod);
        });
    }
}
/**
 * The namespace for `JupyterLab` class statics.
 */
(function (JupyterLab) {
    /**
     * The layout restorer token.
     */
    JupyterLab.IInfo = new dist_index_js_.Token('@jupyterlab/application:IInfo', 'A service providing metadata about the current application, including disabled extensions and whether dev mode is enabled.');
    /**
     * The default JupyterLab application info.
     */
    JupyterLab.defaultInfo = {
        devMode: coreutils_lib_index_js_.PageConfig.getOption('devMode').toLowerCase() === 'true',
        deferred: { patterns: [], matches: [] },
        disabled: { patterns: [], matches: [] },
        mimeExtensions: [],
        availablePlugins: [],
        filesCached: coreutils_lib_index_js_.PageConfig.getOption('cacheFiles').toLowerCase() === 'true',
        isConnected: true
    };
    /**
     * The default JupyterLab application paths.
     */
    JupyterLab.defaultPaths = {
        urls: {
            base: coreutils_lib_index_js_.PageConfig.getOption('baseUrl'),
            notFound: coreutils_lib_index_js_.PageConfig.getOption('notFoundUrl'),
            app: coreutils_lib_index_js_.PageConfig.getOption('appUrl'),
            doc: coreutils_lib_index_js_.PageConfig.getOption('docUrl'),
            static: coreutils_lib_index_js_.PageConfig.getOption('staticUrl'),
            settings: coreutils_lib_index_js_.PageConfig.getOption('settingsUrl'),
            themes: coreutils_lib_index_js_.PageConfig.getOption('themesUrl'),
            translations: coreutils_lib_index_js_.PageConfig.getOption('translationsApiUrl'),
            hubHost: coreutils_lib_index_js_.PageConfig.getOption('hubHost') || undefined,
            hubPrefix: coreutils_lib_index_js_.PageConfig.getOption('hubPrefix') || undefined,
            hubUser: coreutils_lib_index_js_.PageConfig.getOption('hubUser') || undefined,
            hubServerName: coreutils_lib_index_js_.PageConfig.getOption('hubServerName') || undefined
        },
        directories: {
            appSettings: coreutils_lib_index_js_.PageConfig.getOption('appSettingsDir'),
            schemas: coreutils_lib_index_js_.PageConfig.getOption('schemasDir'),
            static: coreutils_lib_index_js_.PageConfig.getOption('staticDir'),
            templates: coreutils_lib_index_js_.PageConfig.getOption('templatesDir'),
            themes: coreutils_lib_index_js_.PageConfig.getOption('themesDir'),
            userSettings: coreutils_lib_index_js_.PageConfig.getOption('userSettingsDir'),
            serverRoot: coreutils_lib_index_js_.PageConfig.getOption('serverRoot'),
            workspaces: coreutils_lib_index_js_.PageConfig.getOption('workspacesDir')
        }
    };
})(JupyterLab || (JupyterLab = {}));

;// CONCATENATED MODULE: ../packages/application/lib/router.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




/**
 * A static class that routes URLs within the application.
 */
class Router {
    /**
     * Create a URL router.
     */
    constructor(options) {
        /**
         * If a matching rule's command resolves with the `stop` token during routing,
         * no further matches will execute.
         */
        this.stop = new dist_index_js_.Token('@jupyterlab/application:Router#stop');
        this._routed = new dist_index_es6_js_.Signal(this);
        this._rules = new Map();
        this.base = options.base;
        this.commands = options.commands;
    }
    /**
     * Returns the parsed current URL of the application.
     */
    get current() {
        var _a, _b;
        const { base } = this;
        const parsed = coreutils_lib_index_js_.URLExt.parse(window.location.href);
        const { search, hash } = parsed;
        const path = (_b = (_a = parsed.pathname) === null || _a === void 0 ? void 0 : _a.replace(base, '/')) !== null && _b !== void 0 ? _b : '';
        const request = path + search + hash;
        return { hash, path, request, search };
    }
    /**
     * A signal emitted when the router routes a route.
     */
    get routed() {
        return this._routed;
    }
    /**
     * Navigate to a new path within the application.
     *
     * @param path - The new path or empty string if redirecting to root.
     *
     * @param options - The navigation options.
     */
    navigate(path, options = {}) {
        const { base } = this;
        const { history } = window;
        const { hard } = options;
        const old = document.location.href;
        const url = path && path.indexOf(base) === 0 ? path : coreutils_lib_index_js_.URLExt.join(base, path);
        if (url === old) {
            return hard ? this.reload() : undefined;
        }
        history.pushState({}, '', url);
        if (hard) {
            return this.reload();
        }
        if (!options.skipRouting) {
            // Because a `route()` call may still be in the stack after having received
            // a `stop` token, wait for the next stack frame before calling `route()`.
            requestAnimationFrame(() => {
                void this.route();
            });
        }
    }
    /**
     * Register to route a path pattern to a command.
     *
     * @param options - The route registration options.
     *
     * @returns A disposable that removes the registered rule from the router.
     */
    register(options) {
        var _a;
        const { command, pattern } = options;
        const rank = (_a = options.rank) !== null && _a !== void 0 ? _a : 100;
        const rules = this._rules;
        rules.set(pattern, { command, rank });
        return new disposable_dist_index_es6_js_.DisposableDelegate(() => {
            rules.delete(pattern);
        });
    }
    /**
     * Cause a hard reload of the document.
     */
    reload() {
        window.location.reload();
    }
    /**
     * Route a specific path to an action.
     *
     * #### Notes
     * If a pattern is matched, its command will be invoked with arguments that
     * match the `IRouter.ILocation` interface.
     */
    route() {
        const { commands, current, stop } = this;
        const { request } = current;
        const routed = this._routed;
        const rules = this._rules;
        const matches = [];
        // Collect all rules that match the URL.
        rules.forEach((rule, pattern) => {
            if (request === null || request === void 0 ? void 0 : request.match(pattern)) {
                matches.push(rule);
            }
        });
        // Order the matching rules by rank and enqueue them.
        const queue = matches.sort((a, b) => b.rank - a.rank);
        const done = new dist_index_js_.PromiseDelegate();
        // Process each enqueued command sequentially and short-circuit if a promise
        // resolves with the `stop` token.
        const next = async () => {
            if (!queue.length) {
                routed.emit(current);
                done.resolve(undefined);
                return;
            }
            const { command } = queue.pop();
            try {
                const request = this.current.request;
                const result = await commands.execute(command, current);
                if (result === stop) {
                    queue.length = 0;
                    console.debug(`Routing ${request} was short-circuited by ${command}`);
                }
            }
            catch (reason) {
                console.warn(`Routing ${request} to ${command} failed`, reason);
            }
            void next();
        };
        void next();
        return done.promise;
    }
}

;// CONCATENATED MODULE: ../packages/application/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A token for which a plugin can provide to respond to connection failures
 * to the application server.
 */
const IConnectionLost = new dist_index_js_.Token('@jupyterlab/application:IConnectionLost', `A service for invoking the dialog shown
  when JupyterLab has lost its connection to the server. Use this if, for some reason,
  you want to bring up the "connection lost" dialog under new circumstances.`);
/**
 * The application status token.
 */
const ILabStatus = new dist_index_js_.Token('@jupyterlab/application:ILabStatus', `A service for interacting with the application busy/dirty
  status. Use this if you want to set the application "busy" favicon, or to set
  the application "dirty" status, which asks the user for confirmation before leaving the application page.`);
/**
 * The URL Router token.
 */
const IRouter = new dist_index_js_.Token('@jupyterlab/application:IRouter', 'The URL router used by the application. Use this to add custom URL-routing for your extension (e.g., to invoke a command if the user navigates to a sub-path).');

;// CONCATENATED MODULE: ../packages/application/lib/treepathupdater.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

/**
 * The tree path updater token.
 */
const ITreePathUpdater = new dist_index_js_.Token('@jupyterlab/application:ITreePathUpdater', 'A service to update the tree path.');

;// CONCATENATED MODULE: ../packages/application/lib/utils.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
/**
 * Create the command options from the given semantic commands list
 * and the given default values.
 *
 * @param app Jupyter Application
 * @param semanticCommands Single semantic command  or a list of commands
 * @param defaultValues Default values
 * @param trans Translation bundle
 * @returns Command options
 */
function createSemanticCommand(app, semanticCommands, defaultValues, trans) {
    const { commands, shell } = app;
    const commandList = Array.isArray(semanticCommands)
        ? semanticCommands
        : [semanticCommands];
    return {
        label: concatenateTexts('label'),
        caption: concatenateTexts('caption'),
        isEnabled: () => {
            var _a;
            const isEnabled = reduceAttribute('isEnabled');
            return ((isEnabled.length > 0 &&
                !isEnabled.some(enabled => enabled === false)) ||
                ((_a = defaultValues.isEnabled) !== null && _a !== void 0 ? _a : false));
        },
        isToggled: () => {
            var _a;
            const isToggled = reduceAttribute('isToggled');
            return (isToggled.some(enabled => enabled === true) ||
                ((_a = defaultValues.isToggled) !== null && _a !== void 0 ? _a : false));
        },
        isVisible: () => {
            var _a;
            const isVisible = reduceAttribute('isVisible');
            return ((isVisible.length > 0 &&
                !isVisible.some(visible => visible === false)) ||
                ((_a = defaultValues.isVisible) !== null && _a !== void 0 ? _a : true));
        },
        execute: async () => {
            const widget = shell.currentWidget;
            const commandIds = commandList.map(cmd => widget !== null ? cmd.getActiveCommandId(widget) : null);
            const toExecute = commandIds.filter(commandId => commandId !== null && commands.isEnabled(commandId));
            let result = null;
            if (toExecute.length > 0) {
                for (const commandId of toExecute) {
                    result = await commands.execute(commandId);
                    if (typeof result === 'boolean' && result === false) {
                        // If a command returns a boolean, assume it is the execution success status
                        // So break if it is false.
                        break;
                    }
                }
            }
            else if (defaultValues.execute) {
                result = await commands.execute(defaultValues.execute);
            }
            return result;
        }
    };
    function reduceAttribute(attribute) {
        const widget = shell.currentWidget;
        const commandIds = commandList.map(cmd => widget !== null ? cmd.getActiveCommandId(widget) : null);
        const attributes = commandIds
            .filter(commandId => commandId !== null)
            .map(commandId => commands[attribute](commandId));
        return attributes;
    }
    function concatenateTexts(attribute) {
        return () => {
            var _a;
            const texts = reduceAttribute(attribute).map((text, textIndex) => attribute == 'caption' && textIndex > 0
                ? text.toLocaleLowerCase()
                : text);
            switch (texts.length) {
                case 0:
                    return (_a = defaultValues[attribute]) !== null && _a !== void 0 ? _a : '';
                case 1:
                    return texts[0];
                default: {
                    const hasEllipsis = texts.some(l => /…$/.test(l));
                    const main = texts
                        .slice(undefined, -1)
                        .map(l => l.replace(/…$/, ''))
                        .join(', ');
                    const end = texts.slice(-1)[0].replace(/…$/, '') + (hasEllipsis ? '…' : '');
                    return trans.__('%1 and %2', main, end);
                }
            }
        };
    }
}

;// CONCATENATED MODULE: ../packages/application/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module application
 */












/***/ })

}]);
//# sourceMappingURL=831.cc9449c8be9e2624422e.js.map?v=cc9449c8be9e2624422e