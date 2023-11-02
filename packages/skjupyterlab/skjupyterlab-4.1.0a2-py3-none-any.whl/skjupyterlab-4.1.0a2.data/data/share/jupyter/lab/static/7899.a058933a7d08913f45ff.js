"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[7899],{

/***/ 37634:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var __webpack_unused_export__;


var m = __webpack_require__(40510);
if (true) {
  exports.s = m.createRoot;
  __webpack_unused_export__ = m.hydrateRoot;
} else { var i; }


/***/ }),

/***/ 97899:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ lib),
  "toggleHeader": () => (/* binding */ toggleHeader)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/application@~4.1.0-alpha.2 (singleton) (fallback: ../packages/application/lib/index.js)
var index_js_ = __webpack_require__(65681);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var settingregistry_lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statedb@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statedb/lib/index.js)
var statedb_lib_index_js_ = __webpack_require__(1458);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(78612);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(81967);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var services_lib_index_js_ = __webpack_require__(43411);
;// CONCATENATED MODULE: ../packages/apputils-extension/lib/announcements.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */





const COMMAND_HELP_OPEN = 'help:open';
const NEWS_API_URL = '/lab/api/news';
const UPDATE_API_URL = '/lab/api/update';
const PRIVACY_URL = 'https://jupyterlab.readthedocs.io/en/latest/privacy_policies.html';
/**
 * Call the announcement API
 *
 * @param endpoint Endpoint to request
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endpoint, init = {}) {
    // Make request to Jupyter API
    const settings = services_lib_index_js_.ServerConnection.makeSettings();
    const requestUrl = coreutils_lib_index_js_.URLExt.join(settings.baseUrl, endpoint);
    let response;
    try {
        response = await services_lib_index_js_.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new services_lib_index_js_.ServerConnection.NetworkError(error);
    }
    const data = await response.json();
    if (!response.ok) {
        throw new services_lib_index_js_.ServerConnection.ResponseError(response, data.message);
    }
    return data;
}
const announcements = {
    id: '@jupyterlab/apputils-extension:announcements',
    description: 'Add the announcement feature. It will fetch news on the internet and check for application updates.',
    autoStart: true,
    optional: [settingregistry_lib_index_js_.ISettingRegistry, translation_lib_index_js_.ITranslator],
    activate: (app, settingRegistry, translator) => {
        var _a;
        const CONFIG_SECTION_NAME = announcements.id.replace(/[^\w]/g, '');
        void Promise.all([
            app.restored,
            (_a = settingRegistry === null || settingRegistry === void 0 ? void 0 : settingRegistry.load('@jupyterlab/apputils-extension:notification')) !== null && _a !== void 0 ? _a : Promise.resolve(null),
            // Use config instead of state to store independently of the workspace
            // if a news has been displayed or not.
            services_lib_index_js_.ConfigSection.create({
                name: CONFIG_SECTION_NAME
            })
        ]).then(async ([_, settings, config]) => {
            const trans = (translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator).load('jupyterlab');
            // Store dismiss state
            lib_index_js_.Notification.manager.changed.connect((manager, change) => {
                var _a;
                if (change.type !== 'removed') {
                    return;
                }
                const { id, tags } = ((_a = change
                    .notification.options.data) !== null && _a !== void 0 ? _a : {});
                if ((tags !== null && tags !== void 0 ? tags : []).some(tag => ['news', 'update'].includes(tag)) && id) {
                    const update = {};
                    update[id] = { seen: true, dismissed: true };
                    config.update(update).catch(reason => {
                        console.error(`Failed to update the announcements config:\n${reason}`);
                    });
                }
            });
            const mustFetchNews = settings === null || settings === void 0 ? void 0 : settings.get('fetchNews').composite;
            if (mustFetchNews === 'none') {
                const notificationId = lib_index_js_.Notification.emit(trans.__('Would you like to receive official Jupyter news?\nPlease read the privacy policy.'), 'default', {
                    autoClose: false,
                    actions: [
                        {
                            label: trans.__('Open privacy policy'),
                            caption: PRIVACY_URL,
                            callback: event => {
                                event.preventDefault();
                                if (app.commands.hasCommand(COMMAND_HELP_OPEN)) {
                                    void app.commands.execute(COMMAND_HELP_OPEN, {
                                        text: trans.__('Privacy policies'),
                                        url: PRIVACY_URL
                                    });
                                }
                                else {
                                    window.open(PRIVACY_URL, '_blank', 'noreferrer');
                                }
                            },
                            displayType: 'link'
                        },
                        {
                            label: trans.__('Yes'),
                            callback: () => {
                                lib_index_js_.Notification.dismiss(notificationId);
                                config
                                    .update({})
                                    .then(() => fetchNews())
                                    .catch(reason => {
                                    console.error(`Failed to get the news:\n${reason}`);
                                });
                                settings === null || settings === void 0 ? void 0 : settings.set('fetchNews', 'true').catch((reason) => {
                                    console.error(`Failed to save setting 'fetchNews':\n${reason}`);
                                });
                            }
                        },
                        {
                            label: trans.__('No'),
                            callback: () => {
                                lib_index_js_.Notification.dismiss(notificationId);
                                settings === null || settings === void 0 ? void 0 : settings.set('fetchNews', 'false').catch((reason) => {
                                    console.error(`Failed to save setting 'fetchNews':\n${reason}`);
                                });
                            }
                        }
                    ]
                });
            }
            else {
                await fetchNews();
            }
            async function fetchNews() {
                var _a, _b, _c, _d;
                if (((_a = settings === null || settings === void 0 ? void 0 : settings.get('fetchNews').composite) !== null && _a !== void 0 ? _a : 'false') === 'true') {
                    try {
                        const response = await requestAPI(NEWS_API_URL);
                        for (const { link, message, type, options } of response.news) {
                            // @ts-expect-error data has no index
                            const id = options.data['id'];
                            // Filter those notifications
                            const state = (_b = config.data[id]) !== null && _b !== void 0 ? _b : {
                                seen: false,
                                dismissed: false
                            };
                            if (!state.dismissed) {
                                options.actions = [
                                    {
                                        label: trans.__('Hide'),
                                        caption: trans.__('Never show this notification again.'),
                                        callback: () => {
                                            const update = {};
                                            update[id] = { seen: true, dismissed: true };
                                            config.update(update).catch(reason => {
                                                console.error(`Failed to update the announcements config:\n${reason}`);
                                            });
                                        }
                                    }
                                ];
                                if ((link === null || link === void 0 ? void 0 : link.length) === 2) {
                                    options.actions.push({
                                        label: link[0],
                                        caption: link[1],
                                        callback: () => {
                                            window.open(link[1], '_blank', 'noreferrer');
                                        },
                                        displayType: 'link'
                                    });
                                }
                                if (!state.seen) {
                                    options.autoClose = 5000;
                                    const update = {};
                                    update[id] = { seen: true };
                                    config.update(update).catch(reason => {
                                        console.error(`Failed to update the announcements config:\n${reason}`);
                                    });
                                }
                                lib_index_js_.Notification.emit(message, type, options);
                            }
                        }
                    }
                    catch (reason) {
                        console.log('Failed to get the announcements.', reason);
                    }
                }
                if ((_c = settings === null || settings === void 0 ? void 0 : settings.get('checkForUpdates').composite) !== null && _c !== void 0 ? _c : true) {
                    const response = await requestAPI(UPDATE_API_URL);
                    if (response.notification) {
                        const { link, message, type, options } = response.notification;
                        // @ts-expect-error data has no index
                        const id = options.data['id'];
                        const state = (_d = config.data[id]) !== null && _d !== void 0 ? _d : {
                            seen: false,
                            dismissed: false
                        };
                        if (!state.dismissed) {
                            let notificationId;
                            options.actions = [
                                {
                                    label: trans.__('Do not check for updates'),
                                    caption: trans.__('If pressed, you will not be prompted if a new JupyterLab version is found.'),
                                    callback: () => {
                                        settings === null || settings === void 0 ? void 0 : settings.set('checkForUpdates', false).then(() => {
                                            lib_index_js_.Notification.dismiss(notificationId);
                                        }).catch((reason) => {
                                            console.error('Failed to set the `checkForUpdates` setting.', reason);
                                        });
                                    }
                                }
                            ];
                            if ((link === null || link === void 0 ? void 0 : link.length) === 2) {
                                options.actions.push({
                                    label: link[0],
                                    caption: link[1],
                                    callback: () => {
                                        window.open(link[1], '_blank', 'noreferrer');
                                    },
                                    displayType: 'link'
                                });
                            }
                            if (!state.seen) {
                                options.autoClose = 5000;
                                const update = {};
                                update[id] = { seen: true };
                                config.update(update).catch(reason => {
                                    console.error(`Failed to update the announcements config:\n${reason}`);
                                });
                            }
                            notificationId = lib_index_js_.Notification.emit(message, type, options);
                        }
                    }
                }
            }
        });
    }
};

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
// EXTERNAL MODULE: ../node_modules/react-dom/client.js
var client = __webpack_require__(37634);
;// CONCATENATED MODULE: ../packages/apputils-extension/lib/notificationplugin.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */








/**
 * Toast close button class
 */
const TOAST_CLOSE_BUTTON_CLASS = 'jp-Notification-Toast-Close';
/**
 * Toast close button class right margin required due to custom hover effect
 */
const TOAST_CLOSE_BUTTON_MARGIN_CLASS = 'jp-Notification-Toast-Close-Margin';
/**
 * Maximal number of characters displayed in a notification.
 */
const MAX_MESSAGE_LENGTH = 140;
var CommandIDs;
(function (CommandIDs) {
    /**
     * Dismiss a notification
     */
    CommandIDs.dismiss = 'apputils:dismiss-notification';
    /**
     * Display all notifications
     */
    CommandIDs.display = 'apputils:display-notifications';
    /**
     * Create a notification
     */
    CommandIDs.notify = 'apputils:notify';
    /**
     * Update a notification
     */
    CommandIDs.update = 'apputils:update-notification';
})(CommandIDs || (CommandIDs = {}));
/**
 * Half spacing between subitems in a status item.
 */
const HALF_SPACING = 4;
/**
 * Notification center view
 */
function NotificationCenter(props) {
    const { manager, onClose, trans } = props;
    // Markdown parsed notifications
    const [notifications, setNotifications] = react_index_js_.useState([]);
    // Load asynchronously react-toastify icons
    const [icons, setIcons] = react_index_js_.useState(null);
    react_index_js_.useEffect(() => {
        async function onChanged() {
            setNotifications(await Promise.all(manager.notifications.map(async (n) => {
                return Object.freeze({
                    ...n
                });
            })));
        }
        if (notifications.length !== manager.count) {
            void onChanged();
        }
        manager.changed.connect(onChanged);
        return () => {
            manager.changed.disconnect(onChanged);
        };
    }, [manager]);
    react_index_js_.useEffect(() => {
        Private.getIcons()
            .then(toastifyIcons => {
            setIcons(toastifyIcons);
        })
            .catch(r => {
            console.error(`Failed to get react-toastify icons:\n${r}`);
        });
    }, []);
    return (react_index_js_.createElement(ui_components_lib_index_js_.UseSignal, { signal: manager.changed }, () => (react_index_js_.createElement(react_index_js_.Fragment, null,
        react_index_js_.createElement("h2", { className: "jp-Notification-Header jp-Toolbar" },
            react_index_js_.createElement("span", { className: "jp-Toolbar-item" }, manager.count > 0
                ? trans._n('%1 notification', '%1 notifications', manager.count)
                : trans.__('No notifications')),
            react_index_js_.createElement("span", { className: "jp-Toolbar-item jp-Toolbar-spacer" }),
            react_index_js_.createElement(ui_components_lib_index_js_.ToolbarButtonComponent, { actualOnClick: true, onClick: () => {
                    manager.dismiss();
                }, icon: ui_components_lib_index_js_.deleteIcon, tooltip: trans.__('Dismiss all notifications'), enabled: manager.count > 0 }),
            react_index_js_.createElement(ui_components_lib_index_js_.ToolbarButtonComponent, { actualOnClick: true, onClick: onClose, icon: ui_components_lib_index_js_.closeIcon, tooltip: trans.__('Hide notifications') })),
        react_index_js_.createElement("ol", { className: "jp-Notification-List" }, notifications.map(notification => {
            var _a;
            const { id, message, type, options } = notification;
            const toastType = type === 'in-progress' ? 'default' : type;
            const closeNotification = () => {
                manager.dismiss(id);
            };
            const icon = type === 'default'
                ? null
                : type === 'in-progress'
                    ? (_a = icons === null || icons === void 0 ? void 0 : icons.spinner) !== null && _a !== void 0 ? _a : null
                    : icons && icons[type];
            return (react_index_js_.createElement("li", { className: "jp-Notification-List-Item", key: notification.id, onClick: event => {
                    // Stop propagation to avoid closing the popup on click
                    event.stopPropagation();
                } },
                react_index_js_.createElement("div", { className: `Toastify__toast Toastify__toast-theme--light Toastify__toast--${toastType} jp-Notification-Toast-${toastType}` },
                    react_index_js_.createElement("div", { className: "Toastify__toast-body" },
                        icon && (react_index_js_.createElement("div", { className: "Toastify__toast-icon" }, icon({ theme: 'light', type: toastType }))),
                        react_index_js_.createElement("div", null, Private.createContent(message, closeNotification, options.actions))),
                    react_index_js_.createElement(Private.CloseButton, { close: closeNotification, closeIcon: ui_components_lib_index_js_.deleteIcon.react, title: trans.__('Dismiss notification'), closeIconMargin: true }))));
        }))))));
}
/**
 * Status widget model
 */
class NotificationStatusModel extends ui_components_lib_index_js_.VDomModel {
    constructor(manager) {
        super();
        this.manager = manager;
        this._highlight = false;
        this._listOpened = false;
        this._doNotDisturbMode = false;
        this._count = manager.count;
        this.manager.changed.connect(this.onNotificationChanged, this);
    }
    /**
     * Number of notifications.
     */
    get count() {
        return this._count;
    }
    /**
     * Whether to silence all notifications or not.
     */
    get doNotDisturbMode() {
        return this._doNotDisturbMode;
    }
    set doNotDisturbMode(v) {
        this._doNotDisturbMode = v;
    }
    /**
     * Whether to highlight the status widget or not.
     */
    get highlight() {
        return this._highlight;
    }
    /**
     * Whether the popup is opened or not.
     */
    get listOpened() {
        return this._listOpened;
    }
    set listOpened(v) {
        this._listOpened = v;
        if (this._listOpened || this._highlight) {
            this._highlight = false;
        }
        this.stateChanged.emit();
    }
    onNotificationChanged(_, change) {
        // Set private attribute to trigger only once the signal emission
        this._count = this.manager.count;
        const { autoClose } = change.notification.options;
        const noToast = this.doNotDisturbMode ||
            (typeof autoClose === 'number' && autoClose <= 0);
        // Highlight if
        //   the list is not opened (the style change if list is opened due to clickedItem style in statusbar.)
        //   the change type is not removed
        //   the notification will be hidden
        if (!this._listOpened && change.type !== 'removed' && noToast) {
            this._highlight = true;
        }
        this.stateChanged.emit();
    }
}
/**
 * Status view
 */
function NotificationStatus(props) {
    return (react_index_js_.createElement(statusbar_lib_index_js_.GroupItem, { spacing: HALF_SPACING, onClick: () => {
            props.onClick();
        }, title: props.count > 0
            ? props.trans._n('%1 notification', '%1 notifications', props.count)
            : props.trans.__('No notifications') },
        react_index_js_.createElement(statusbar_lib_index_js_.TextItem, { className: "jp-Notification-Status-Text", source: `${props.count}` }),
        react_index_js_.createElement(ui_components_lib_index_js_.bellIcon.react, { top: '2px', stylesheet: 'statusBar' })));
}
/**
 * Add notification center and toast
 */
const notificationPlugin = {
    id: '@jupyterlab/apputils-extension:notification',
    description: 'Add the notification center and its status indicator.',
    autoStart: true,
    optional: [statusbar_lib_index_js_.IStatusBar, settingregistry_lib_index_js_.ISettingRegistry, translation_lib_index_js_.ITranslator],
    activate: (app, statusBar, settingRegistry, translator) => {
        Private.translator = translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator;
        const trans = Private.translator.load('jupyterlab');
        const model = new NotificationStatusModel(lib_index_js_.Notification.manager);
        model.doNotDisturbMode = false;
        if (settingRegistry) {
            void Promise.all([
                settingRegistry.load(notificationPlugin.id),
                app.restored
            ]).then(([plugin]) => {
                const updateSettings = () => {
                    model.doNotDisturbMode = plugin.get('doNotDisturbMode')
                        .composite;
                };
                updateSettings();
                plugin.changed.connect(updateSettings);
            });
        }
        app.commands.addCommand(CommandIDs.notify, {
            label: trans.__('Emit a notification'),
            caption: trans.__('Notification is described by {message: string, type?: string, options?: {autoClose?: number | false, actions: {label: string, commandId: string, args?: ReadOnlyJSONObject, caption?: string, className?: string}[], data?: ReadOnlyJSONValue}}.'),
            execute: args => {
                var _a;
                const { message, type } = args;
                const options = (_a = args.options) !== null && _a !== void 0 ? _a : {};
                return lib_index_js_.Notification.manager.notify(message, type !== null && type !== void 0 ? type : 'default', {
                    ...options,
                    actions: options.actions
                        ? options.actions.map((action) => {
                            return {
                                ...action,
                                callback: () => {
                                    app.commands
                                        .execute(action.commandId, action.args)
                                        .catch(r => {
                                        console.error(`Failed to executed '${action.commandId}':\n${r}`);
                                    });
                                }
                            };
                        })
                        : null
                });
            }
        });
        app.commands.addCommand(CommandIDs.update, {
            label: trans.__('Update a notification'),
            caption: trans.__('Notification is described by {id: string, message: string, type?: string, options?: {autoClose?: number | false, actions: {label: string, commandId: string, args?: ReadOnlyJSONObject, caption?: string, className?: string}[], data?: ReadOnlyJSONValue}}.'),
            execute: args => {
                const { id, message, type, ...options } = args;
                return lib_index_js_.Notification.manager.update({
                    id,
                    message,
                    type: type !== null && type !== void 0 ? type : 'default',
                    ...options,
                    actions: options.actions
                        ? options.actions.map((action) => {
                            return {
                                ...action,
                                callback: () => {
                                    app.commands
                                        .execute(action.commandId, action.args)
                                        .catch(r => {
                                        console.error(`Failed to executed '${action.commandId}':\n${r}`);
                                    });
                                }
                            };
                        })
                        : null
                });
            }
        });
        app.commands.addCommand(CommandIDs.dismiss, {
            label: trans.__('Dismiss a notification'),
            execute: args => {
                const { id } = args;
                lib_index_js_.Notification.manager.dismiss(id);
            }
        });
        let popup = null;
        model.listOpened = false;
        const notificationList = lib_index_js_.ReactWidget.create(react_index_js_.createElement(NotificationCenter, { manager: lib_index_js_.Notification.manager, onClose: () => {
                popup === null || popup === void 0 ? void 0 : popup.dispose();
            }, trans: trans }));
        notificationList.addClass('jp-Notification-Center');
        async function onNotification(manager, change) {
            var _a;
            if (model.doNotDisturbMode || (popup !== null && !popup.isDisposed)) {
                return;
            }
            const { message, type, options, id } = change.notification;
            if (typeof options.autoClose === 'number' && options.autoClose <= 0) {
                // If the notification is silent, bail early.
                return;
            }
            switch (change.type) {
                case 'added':
                    await Private.createToast(id, message, type, options);
                    break;
                case 'updated':
                    {
                        const toast = await Private.toast();
                        const actions = options.actions;
                        const autoClose = (_a = options.autoClose) !== null && _a !== void 0 ? _a : (actions && actions.length > 0 ? false : null);
                        if (toast.isActive(id)) {
                            // Update existing toast
                            const closeToast = () => {
                                // Dismiss the displayed toast
                                toast.dismiss(id);
                                // Dismiss the notification from the queue
                                manager.dismiss(id);
                            };
                            toast.update(id, {
                                type: type === 'in-progress' ? null : type,
                                isLoading: type === 'in-progress',
                                autoClose: autoClose,
                                render: Private.createContent(message, closeToast, options.actions)
                            });
                        }
                        else {
                            // Needs to recreate a closed toast
                            await Private.createToast(id, message, type, options);
                        }
                    }
                    break;
                case 'removed':
                    await Private.toast().then(t => {
                        t.dismiss(id);
                    });
                    break;
            }
        }
        lib_index_js_.Notification.manager.changed.connect(onNotification);
        const displayNotifications = () => {
            if (popup) {
                popup.dispose();
                popup = null;
            }
            else {
                popup = (0,statusbar_lib_index_js_.showPopup)({
                    body: notificationList,
                    anchor: notificationStatus,
                    align: 'right',
                    hasDynamicSize: true,
                    startHidden: true
                });
                // Dismiss all toasts when opening the notification center
                Private.toast()
                    .then(t => {
                    t.dismiss();
                })
                    .catch(r => {
                    console.error(`Failed to dismiss all toasts:\n${r}`);
                })
                    .finally(() => {
                    popup === null || popup === void 0 ? void 0 : popup.launch();
                    // Focus on the pop-up
                    notificationList.node.focus();
                    popup === null || popup === void 0 ? void 0 : popup.disposed.connect(() => {
                        model.listOpened = false;
                        popup = null;
                    });
                });
            }
            model.listOpened = popup !== null;
        };
        app.commands.addCommand(CommandIDs.display, {
            label: trans.__('Show Notifications'),
            execute: displayNotifications
        });
        const notificationStatus = lib_index_js_.ReactWidget.create(react_index_js_.createElement(ui_components_lib_index_js_.UseSignal, { signal: model.stateChanged }, () => {
            if (model.highlight || (popup && !popup.isDisposed)) {
                notificationStatus.addClass('jp-mod-selected');
            }
            else {
                notificationStatus.removeClass('jp-mod-selected');
            }
            return (react_index_js_.createElement(NotificationStatus, { count: model.count, highlight: model.highlight, trans: trans, onClick: displayNotifications }));
        }));
        notificationStatus.addClass('jp-Notification-Status');
        if (statusBar) {
            statusBar.registerStatusItem(notificationPlugin.id, {
                item: notificationStatus,
                align: 'right',
                rank: -1
            });
        }
    }
};
var Private;
(function (Private) {
    /**
     * Translator object for private namespace
     */
    Private.translator = translation_lib_index_js_.nullTranslator;
    /**
     * Pointer to asynchronously loaded react-toastify
     */
    let toastify = null;
    function CloseButton(props) {
        var _a;
        return (react_index_js_.createElement("button", { className: `jp-Button jp-mod-minimal ${TOAST_CLOSE_BUTTON_CLASS}${props.closeIconMargin ? ` ${TOAST_CLOSE_BUTTON_MARGIN_CLASS}` : ''}`, title: (_a = props.title) !== null && _a !== void 0 ? _a : '', onClick: props.close },
            react_index_js_.createElement(props.closeIcon, { className: "jp-icon-hover", tag: "span" })));
    }
    Private.CloseButton = CloseButton;
    function ToastifyCloseButton(props) {
        const trans = Private.translator.load('jupyterlab');
        return (react_index_js_.createElement(CloseButton, { close: props.closeToast, closeIcon: ui_components_lib_index_js_.closeIcon.react, title: trans.__('Hide notification') }));
    }
    let waitForToastify = null;
    /**
     * Asynchronously load the toast container
     *
     * @returns The toast object
     */
    async function toast() {
        if (waitForToastify === null) {
            waitForToastify = new dist_index_js_.PromiseDelegate();
        }
        else {
            await waitForToastify.promise;
        }
        if (toastify === null) {
            toastify = await __webpack_require__.e(/* import() */ 53).then(__webpack_require__.t.bind(__webpack_require__, 60053, 23));
            const container = document.body.appendChild(document.createElement('div'));
            container.id = 'react-toastify-container';
            const root = (0,client/* createRoot */.s)(container);
            root.render(react_index_js_.createElement(toastify.ToastContainer, { draggable: false, closeOnClick: false, hideProgressBar: true, newestOnTop: true, pauseOnFocusLoss: true, pauseOnHover: true, position: "bottom-right", className: "jp-toastContainer", transition: toastify.Slide, closeButton: ToastifyCloseButton }));
            waitForToastify.resolve();
        }
        return toastify.toast;
    }
    Private.toast = toast;
    /**
     * react-toastify icons loader
     */
    async function getIcons() {
        if (toastify === null) {
            await toast();
        }
        return toastify.Icons;
    }
    Private.getIcons = getIcons;
    const displayType2Class = {
        accent: 'jp-mod-accept',
        link: 'jp-mod-link',
        warn: 'jp-mod-warn',
        default: ''
    };
    /**
     * Create a button with customized callback in a toast
     */
    function ToastButton({ action, closeToast }) {
        var _a, _b;
        const clickHandler = (event) => {
            action.callback(event);
            if (!event.defaultPrevented) {
                closeToast();
            }
        };
        const classes = [
            'jp-toast-button',
            displayType2Class[(_a = action.displayType) !== null && _a !== void 0 ? _a : 'default']
        ].join(' ');
        return (react_index_js_.createElement(ui_components_lib_index_js_.Button, { title: (_b = action.caption) !== null && _b !== void 0 ? _b : action.label, className: classes, onClick: clickHandler, small: true }, action.label));
    }
    /**
     * Helper function to construct the notification content
     *
     * @param message Message to print in the notification
     * @param closeHandler Function closing the notification
     * @param actions Toast actions
     */
    function createContent(message, closeHandler, actions) {
        var _a;
        const shortenMessage = message.length > MAX_MESSAGE_LENGTH
            ? message.slice(0, MAX_MESSAGE_LENGTH) + '…'
            : message;
        return (react_index_js_.createElement(react_index_js_.Fragment, null,
            react_index_js_.createElement("div", { className: "jp-toast-message" }, shortenMessage.split('\n').map((part, index) => (react_index_js_.createElement(react_index_js_.Fragment, { key: `part-${index}` },
                index > 0 ? react_index_js_.createElement("br", null) : null,
                part)))),
            ((_a = actions === null || actions === void 0 ? void 0 : actions.length) !== null && _a !== void 0 ? _a : 0) > 0 && (react_index_js_.createElement("div", { className: "jp-toast-buttonBar" },
                react_index_js_.createElement("div", { className: "jp-toast-spacer" }),
                actions.map((action, idx) => {
                    return (react_index_js_.createElement(ToastButton, { key: 'button-' + idx, action: action, closeToast: closeHandler }));
                })))));
    }
    Private.createContent = createContent;
    /**
     * Create a toast notification
     *
     * @param toastId Toast unique id
     * @param message Toast message
     * @param type Toast type
     * @param options Toast options
     * @returns Toast id
     */
    async function createToast(toastId, message, type, options = {}) {
        const { actions, autoClose, data } = options;
        const t = await toast();
        const toastOptions = {
            autoClose: autoClose !== null && autoClose !== void 0 ? autoClose : (actions && actions.length > 0 ? false : undefined),
            data: data,
            className: `jp-Notification-Toast-${type}`,
            toastId,
            type: type === 'in-progress' ? null : type,
            isLoading: type === 'in-progress'
        };
        return t(({ closeToast }) => createContent(message, () => {
            if (closeToast)
                closeToast();
            lib_index_js_.Notification.manager.dismiss(toastId);
        }, actions), toastOptions);
    }
    Private.createToast = createToast;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/commands@^2.0.1 (singleton) (fallback: ../node_modules/@lumino/commands/dist/index.es6.js)
var commands_dist_index_es6_js_ = __webpack_require__(18955);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/apputils-extension/lib/palette.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/







/**
 * The command IDs used by the apputils extension.
 */
var palette_CommandIDs;
(function (CommandIDs) {
    CommandIDs.activate = 'apputils:activate-command-palette';
})(palette_CommandIDs || (palette_CommandIDs = {}));
const PALETTE_PLUGIN_ID = '@jupyterlab/apputils-extension:palette';
/**
 * A thin wrapper around the `CommandPalette` class to conform with the
 * JupyterLab interface for the application-wide command palette.
 */
class Palette {
    /**
     * Create a palette instance.
     */
    constructor(palette, translator) {
        this.translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        this._palette = palette;
        this._palette.title.label = '';
        this._palette.title.caption = trans.__('Command Palette');
    }
    /**
     * The placeholder text of the command palette's search input.
     */
    set placeholder(placeholder) {
        this._palette.inputNode.placeholder = placeholder;
    }
    get placeholder() {
        return this._palette.inputNode.placeholder;
    }
    /**
     * Activate the command palette for user input.
     */
    activate() {
        this._palette.activate();
    }
    /**
     * Add a command item to the command palette.
     *
     * @param options - The options for creating the command item.
     *
     * @returns A disposable that will remove the item from the palette.
     */
    addItem(options) {
        const item = this._palette.addItem(options);
        return new index_es6_js_.DisposableDelegate(() => {
            this._palette.removeItem(item);
        });
    }
}
/**
 * A namespace for `Palette` statics.
 */
(function (Palette) {
    /**
     * Activate the command palette.
     */
    function activate(app, translator, settingRegistry) {
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const palette = palette_Private.createPalette(app, translator);
        const modalPalette = new lib_index_js_.ModalCommandPalette({ commandPalette: palette });
        let modal = false;
        palette.node.setAttribute('role', 'region');
        palette.node.setAttribute('aria-label', trans.__('Command Palette Section'));
        shell.add(palette, 'left', { rank: 300, type: 'Command Palette' });
        if (settingRegistry) {
            const loadSettings = settingRegistry.load(PALETTE_PLUGIN_ID);
            const updateSettings = (settings) => {
                const newModal = settings.get('modal').composite;
                if (modal && !newModal) {
                    palette.parent = null;
                    modalPalette.detach();
                    shell.add(palette, 'left', { rank: 300, type: 'Command Palette' });
                }
                else if (!modal && newModal) {
                    palette.parent = null;
                    modalPalette.palette = palette;
                    palette.show();
                    modalPalette.attach();
                }
                modal = newModal;
            };
            Promise.all([loadSettings, app.restored])
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
        // Show the current palette shortcut in its title.
        const updatePaletteTitle = () => {
            const binding = (0,algorithm_dist_index_es6_js_.find)(app.commands.keyBindings, b => b.command === palette_CommandIDs.activate);
            if (binding) {
                const ks = binding.keys.map(commands_dist_index_es6_js_.CommandRegistry.formatKeystroke).join(', ');
                palette.title.caption = trans.__('Commands (%1)', ks);
            }
            else {
                palette.title.caption = trans.__('Commands');
            }
        };
        updatePaletteTitle();
        app.commands.keyBindingChanged.connect(() => {
            updatePaletteTitle();
        });
        commands.addCommand(palette_CommandIDs.activate, {
            execute: () => {
                if (modal) {
                    modalPalette.activate();
                }
                else {
                    shell.activateById(palette.id);
                }
            },
            label: trans.__('Activate Command Palette')
        });
        palette.inputNode.placeholder = trans.__('SEARCH');
        return new Palette(palette, translator);
    }
    Palette.activate = activate;
    /**
     * Restore the command palette.
     */
    function restore(app, restorer, translator) {
        const palette = palette_Private.createPalette(app, translator);
        // Let the application restorer track the command palette for restoration of
        // application state (e.g. setting the command palette as the current side bar
        // widget).
        restorer.add(palette, 'command-palette');
    }
    Palette.restore = restore;
})(Palette || (Palette = {}));
/**
 * The namespace for module private data.
 */
var palette_Private;
(function (Private) {
    /**
     * The private command palette instance.
     */
    let palette;
    /**
     * Create the application-wide command palette.
     */
    function createPalette(app, translator) {
        if (!palette) {
            // use a renderer tweaked to use inline svg icons
            palette = new widgets_dist_index_es6_js_.CommandPalette({
                commands: app.commands,
                renderer: ui_components_lib_index_js_.CommandPaletteSvg.defaultRenderer
            });
            palette.id = 'command-palette';
            palette.title.icon = ui_components_lib_index_js_.paletteIcon;
            const trans = translator.load('jupyterlab');
            palette.title.label = trans.__('Commands');
        }
        return palette;
    }
    Private.createPalette = createPalette;
})(palette_Private || (palette_Private = {}));

;// CONCATENATED MODULE: ../packages/apputils-extension/lib/settingconnector.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



/**
 * A data connector for fetching settings.
 *
 * #### Notes
 * This connector adds a query parameter to the base services setting manager.
 */
class SettingConnector extends statedb_lib_index_js_.DataConnector {
    constructor(connector) {
        super();
        this._throttlers = Object.create(null);
        this._connector = connector;
    }
    /**
     * Fetch settings for a plugin.
     * @param id - The plugin ID
     *
     * #### Notes
     * The REST API requests are throttled at one request per plugin per 100ms.
     */
    fetch(id) {
        const throttlers = this._throttlers;
        if (!(id in throttlers)) {
            throttlers[id] = new dist_index_es6_js_.Throttler(() => this._connector.fetch(id), 100);
        }
        return throttlers[id].invoke();
    }
    async list(query = 'all') {
        const { isDisabled } = coreutils_lib_index_js_.PageConfig.Extension;
        const { ids, values } = await this._connector.list(query === 'ids' ? 'ids' : undefined);
        if (query === 'all') {
            return { ids, values };
        }
        if (query === 'ids') {
            return { ids };
        }
        return {
            ids: ids.filter(id => !isDisabled(id)),
            values: values.filter(({ id }) => !isDisabled(id))
        };
    }
    async save(id, raw) {
        await this._connector.save(id, raw);
    }
}

;// CONCATENATED MODULE: ../packages/apputils-extension/lib/settingsplugin.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * The default setting registry provider.
 */
const settingsPlugin = {
    id: '@jupyterlab/apputils-extension:settings',
    description: 'Provides the setting registry.',
    activate: async (app) => {
        const { isDisabled } = coreutils_lib_index_js_.PageConfig.Extension;
        const connector = new SettingConnector(app.serviceManager.settings);
        // On startup, check if a plugin is available in the application.
        // This helps avoid loading plugin files from other lab-based applications
        // that have placed their schemas next to the JupyterLab schemas. Different lab-based
        // applications might not have the same set of plugins loaded on the page.
        // As an example this helps prevent having new toolbar items added by another application
        // appear in JupyterLab as a side-effect when they are defined via the settings system.
        const registry = new settingregistry_lib_index_js_.SettingRegistry({
            connector,
            plugins: (await connector.list('active')).values.filter(value => app.hasPlugin(value.id))
        });
        // If there are plugins that have schemas that are not in the setting
        // registry after the application has restored, try to load them manually
        // because otherwise, its settings will never become available in the
        // setting registry.
        void app.restored.then(async () => {
            const plugins = await connector.list('ids');
            plugins.ids.forEach(async (id) => {
                if (!app.hasPlugin(id) || isDisabled(id) || id in registry.plugins) {
                    return;
                }
                try {
                    await registry.load(id);
                }
                catch (error) {
                    console.warn(`Settings failed to load for (${id})`, error);
                    if (!app.isPluginActivated(id)) {
                        console.warn(`If 'jupyter.lab.transform=true' in the plugin schema, this ` +
                            `may happen if {autoStart: false} in (${id}) or if it is ` +
                            `one of the deferredExtensions in page config.`);
                    }
                }
            });
        });
        return registry;
    },
    autoStart: true,
    provides: settingregistry_lib_index_js_.ISettingRegistry
};

;// CONCATENATED MODULE: ../packages/apputils-extension/lib/statusbarplugin.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




/**
 * A plugin that provides a kernel status item to the status bar.
 */
const kernelStatus = {
    id: '@jupyterlab/apputils-extension:kernel-status',
    description: 'Provides the kernel status indicator model.',
    autoStart: true,
    requires: [statusbar_lib_index_js_.IStatusBar],
    provides: lib_index_js_.IKernelStatusModel,
    optional: [lib_index_js_.ISessionContextDialogs, translation_lib_index_js_.ITranslator, index_js_.ILabShell],
    activate: (app, statusBar, sessionDialogs_, translator_, labShell) => {
        const translator = translator_ !== null && translator_ !== void 0 ? translator_ : translation_lib_index_js_.nullTranslator;
        const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new lib_index_js_.SessionContextDialogs({ translator });
        // When the status item is clicked, launch the kernel
        // selection dialog for the current session.
        const changeKernel = async () => {
            if (!item.model.sessionContext) {
                return;
            }
            await sessionDialogs.selectKernel(item.model.sessionContext);
        };
        // Create the status item.
        const item = new lib_index_js_.KernelStatus({ onClick: changeKernel }, translator);
        const providers = new Set();
        const addSessionProvider = (provider) => {
            providers.add(provider);
            if (app.shell.currentWidget) {
                updateSession(app.shell, {
                    newValue: app.shell.currentWidget,
                    oldValue: null
                });
            }
        };
        function updateSession(shell, changes) {
            var _a;
            const { oldValue, newValue } = changes;
            // Clean up after the old value if it exists,
            // listen for changes to the title of the activity
            if (oldValue) {
                oldValue.title.changed.disconnect(onTitleChanged);
            }
            item.model.sessionContext =
                (_a = [...providers]
                    .map(provider => provider(changes.newValue))
                    .filter(session => session !== null)[0]) !== null && _a !== void 0 ? _a : null;
            if (newValue && item.model.sessionContext) {
                onTitleChanged(newValue.title);
                newValue.title.changed.connect(onTitleChanged);
            }
        }
        // When the title of the active widget changes, update the label
        // of the hover text.
        const onTitleChanged = (title) => {
            item.model.activityName = title.label;
        };
        if (labShell) {
            labShell.currentChanged.connect(updateSession);
        }
        statusBar.registerStatusItem(kernelStatus.id, {
            item,
            align: 'left',
            rank: 1,
            isActive: () => item.model.sessionContext !== null
        });
        return { addSessionProvider };
    }
};
/*
 * A plugin providing running terminals and sessions information
 * to the status bar.
 */
const runningSessionsStatus = {
    id: '@jupyterlab/apputils-extension:running-sessions-status',
    description: 'Add the running sessions and terminals status bar item.',
    autoStart: true,
    requires: [statusbar_lib_index_js_.IStatusBar, translation_lib_index_js_.ITranslator],
    activate: (app, statusBar, translator) => {
        const item = new lib_index_js_.RunningSessions({
            onClick: () => app.shell.activateById('jp-running-sessions'),
            serviceManager: app.serviceManager,
            translator
        });
        item.model.sessions = Array.from(app.serviceManager.sessions.running()).length;
        item.model.terminals = Array.from(app.serviceManager.terminals.running()).length;
        statusBar.registerStatusItem(runningSessionsStatus.id, {
            item,
            align: 'left',
            rank: 0
        });
    }
};

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/mainmenu@~4.1.0-alpha.2 (singleton) (fallback: ../packages/mainmenu/lib/index.js)
var mainmenu_lib_index_js_ = __webpack_require__(5184);
;// CONCATENATED MODULE: ../packages/apputils-extension/style/scrollbar.raw.css
const scrollbar_raw_namespaceObject = "/*\n * Copyright (c) Jupyter Development Team.\n * Distributed under the terms of the Modified BSD License.\n */\n\n/*\n * Webkit scrollbar styling.\n * Separate file which is dynamically loaded based on user/theme settings.\n */\n\n/* use standard opaque scrollbars for most nodes */\n\n::-webkit-scrollbar,\n::-webkit-scrollbar-corner {\n  background: var(--jp-scrollbar-background-color);\n}\n\n::-webkit-scrollbar-thumb {\n  background: rgb(var(--jp-scrollbar-thumb-color));\n  border: var(--jp-scrollbar-thumb-margin) solid transparent;\n  background-clip: content-box;\n  border-radius: var(--jp-scrollbar-thumb-radius);\n}\n\n::-webkit-scrollbar-track:horizontal {\n  border-left: var(--jp-scrollbar-endpad) solid\n    var(--jp-scrollbar-background-color);\n  border-right: var(--jp-scrollbar-endpad) solid\n    var(--jp-scrollbar-background-color);\n}\n\n::-webkit-scrollbar-track:vertical {\n  border-top: var(--jp-scrollbar-endpad) solid\n    var(--jp-scrollbar-background-color);\n  border-bottom: var(--jp-scrollbar-endpad) solid\n    var(--jp-scrollbar-background-color);\n}\n\n/* for code nodes, use a transparent style of scrollbar */\n\n.CodeMirror-hscrollbar::-webkit-scrollbar,\n.CodeMirror-vscrollbar::-webkit-scrollbar,\n.CodeMirror-hscrollbar::-webkit-scrollbar-corner,\n.CodeMirror-vscrollbar::-webkit-scrollbar-corner {\n  background-color: transparent;\n}\n\n.CodeMirror-hscrollbar::-webkit-scrollbar-thumb,\n.CodeMirror-vscrollbar::-webkit-scrollbar-thumb {\n  background: rgba(var(--jp-scrollbar-thumb-color), 0.5);\n  border: var(--jp-scrollbar-thumb-margin) solid transparent;\n  background-clip: content-box;\n  border-radius: var(--jp-scrollbar-thumb-radius);\n}\n\n.CodeMirror-hscrollbar::-webkit-scrollbar-track:horizontal {\n  border-left: var(--jp-scrollbar-endpad) solid transparent;\n  border-right: var(--jp-scrollbar-endpad) solid transparent;\n}\n\n.CodeMirror-vscrollbar::-webkit-scrollbar-track:vertical {\n  border-top: var(--jp-scrollbar-endpad) solid transparent;\n  border-bottom: var(--jp-scrollbar-endpad) solid transparent;\n}\n";
;// CONCATENATED MODULE: ../packages/apputils-extension/lib/themesplugins.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/







var themesplugins_CommandIDs;
(function (CommandIDs) {
    CommandIDs.changeTheme = 'apputils:change-theme';
    CommandIDs.changePreferredLightTheme = 'apputils:change-light-theme';
    CommandIDs.changePreferredDarkTheme = 'apputils:change-dark-theme';
    CommandIDs.toggleAdaptiveTheme = 'apputils:adaptive-theme';
    CommandIDs.themeScrollbars = 'apputils:theme-scrollbars';
    CommandIDs.changeFont = 'apputils:change-font';
    CommandIDs.incrFontSize = 'apputils:incr-font-size';
    CommandIDs.decrFontSize = 'apputils:decr-font-size';
})(themesplugins_CommandIDs || (themesplugins_CommandIDs = {}));
function createStyleSheet(text) {
    const style = document.createElement('style');
    style.setAttribute('type', 'text/css');
    style.appendChild(document.createTextNode(text));
    return style;
}
/**
 * The default theme manager provider.
 */
const themesPlugin = {
    id: '@jupyterlab/apputils-extension:themes',
    description: 'Provides the theme manager.',
    requires: [settingregistry_lib_index_js_.ISettingRegistry, index_js_.JupyterFrontEnd.IPaths, translation_lib_index_js_.ITranslator],
    optional: [lib_index_js_.ISplashScreen],
    activate: (app, settings, paths, translator, splash) => {
        const trans = translator.load('jupyterlab');
        const host = app.shell;
        const commands = app.commands;
        const url = coreutils_lib_index_js_.URLExt.join(coreutils_lib_index_js_.PageConfig.getBaseUrl(), paths.urls.themes);
        const key = themesPlugin.id;
        const manager = new lib_index_js_.ThemeManager({
            key,
            host,
            settings,
            splash: splash !== null && splash !== void 0 ? splash : undefined,
            url
        });
        let scrollbarsStyleElement = null;
        // Keep a synchronously set reference to the current theme,
        // since the asynchronous setting of the theme in `changeTheme`
        // can lead to an incorrect toggle on the currently used theme.
        let currentTheme;
        manager.themeChanged.connect((sender, args) => {
            // Set data attributes on the application shell for the current theme.
            currentTheme = args.newValue;
            document.body.dataset.jpThemeLight = String(manager.isLight(currentTheme));
            document.body.dataset.jpThemeName = currentTheme;
            if (document.body.dataset.jpThemeScrollbars !==
                String(manager.themeScrollbars(currentTheme))) {
                document.body.dataset.jpThemeScrollbars = String(manager.themeScrollbars(currentTheme));
                if (manager.themeScrollbars(currentTheme)) {
                    if (!scrollbarsStyleElement) {
                        scrollbarsStyleElement = createStyleSheet(scrollbar_raw_namespaceObject);
                    }
                    if (!scrollbarsStyleElement.parentElement) {
                        document.body.appendChild(scrollbarsStyleElement);
                    }
                }
                else {
                    if (scrollbarsStyleElement && scrollbarsStyleElement.parentElement) {
                        scrollbarsStyleElement.parentElement.removeChild(scrollbarsStyleElement);
                    }
                }
            }
            commands.notifyCommandChanged(themesplugins_CommandIDs.changeTheme);
        });
        commands.addCommand(themesplugins_CommandIDs.changeTheme, {
            label: args => {
                if (args.theme === undefined) {
                    return trans.__('Switch to the provided `theme`.');
                }
                const theme = args['theme'];
                const displayName = manager.getDisplayName(theme);
                return args['isPalette']
                    ? trans.__('Use Theme: %1', displayName)
                    : displayName;
            },
            isToggled: args => args['theme'] === currentTheme,
            execute: args => {
                const theme = args['theme'];
                if (theme === manager.theme) {
                    return;
                }
                // Disable adaptive theme if users decide to change the theme when adaptive theme is on
                if (manager.isToggledAdaptiveTheme()) {
                    return manager.toggleAdaptiveTheme();
                }
                return manager.setTheme(theme);
            }
        });
        commands.addCommand(themesplugins_CommandIDs.changePreferredLightTheme, {
            label: args => {
                if (args.theme === undefined) {
                    return trans.__('Switch to the provided light `theme`.');
                }
                const theme = args['theme'];
                const displayName = manager.getDisplayName(theme);
                return args['isPalette']
                    ? trans.__('Set Preferred Light Theme: %1', displayName)
                    : displayName;
            },
            isToggled: args => args['theme'] === manager.preferredLightTheme,
            execute: args => {
                const theme = args['theme'];
                if (theme === manager.preferredLightTheme) {
                    return;
                }
                return manager.setPreferredLightTheme(theme);
            }
        });
        commands.addCommand(themesplugins_CommandIDs.changePreferredDarkTheme, {
            label: args => {
                if (args.theme === undefined) {
                    return trans.__('Switch to the provided dark `theme`.');
                }
                const theme = args['theme'];
                const displayName = manager.getDisplayName(theme);
                return args['isPalette']
                    ? trans.__('Set Preferred Dark Theme: %1', displayName)
                    : displayName;
            },
            isToggled: args => args['theme'] === manager.preferredDarkTheme,
            execute: args => {
                const theme = args['theme'];
                if (theme === manager.preferredDarkTheme) {
                    return;
                }
                return manager.setPreferredDarkTheme(theme);
            }
        });
        commands.addCommand(themesplugins_CommandIDs.toggleAdaptiveTheme, {
            // Avoid lengthy option text in menu
            label: args => args['isPalette']
                ? trans.__('Synchronize Styling Theme with System Settings')
                : trans.__('Synchronize with System Settings'),
            isToggled: () => manager.isToggledAdaptiveTheme(),
            execute: () => {
                manager.toggleAdaptiveTheme().catch(console.warn);
            }
        });
        commands.addCommand(themesplugins_CommandIDs.themeScrollbars, {
            label: trans.__('Theme Scrollbars'),
            isToggled: () => manager.isToggledThemeScrollbars(),
            execute: () => manager.toggleThemeScrollbars()
        });
        commands.addCommand(themesplugins_CommandIDs.changeFont, {
            label: args => args['enabled'] ? `${args['font']}` : trans.__('waiting for fonts'),
            isEnabled: args => args['enabled'],
            isToggled: args => manager.getCSS(args['key']) === args['font'],
            execute: args => manager.setCSSOverride(args['key'], args['font'])
        });
        commands.addCommand(themesplugins_CommandIDs.incrFontSize, {
            label: args => {
                switch (args.key) {
                    case 'code-font-size':
                        return trans.__('Increase Code Font Size');
                    case 'content-font-size1':
                        return trans.__('Increase Content Font Size');
                    case 'ui-font-size1':
                        return trans.__('Increase UI Font Size');
                    default:
                        return trans.__('Increase Font Size');
                }
            },
            execute: args => manager.incrFontSize(args['key'])
        });
        commands.addCommand(themesplugins_CommandIDs.decrFontSize, {
            label: args => {
                switch (args.key) {
                    case 'code-font-size':
                        return trans.__('Decrease Code Font Size');
                    case 'content-font-size1':
                        return trans.__('Decrease Content Font Size');
                    case 'ui-font-size1':
                        return trans.__('Decrease UI Font Size');
                    default:
                        return trans.__('Decrease Font Size');
                }
            },
            execute: args => manager.decrFontSize(args['key'])
        });
        return manager;
    },
    autoStart: true,
    provides: lib_index_js_.IThemeManager
};
/**
 * The default theme manager's UI command palette and main menu functionality.
 *
 * #### Notes
 * This plugin loads separately from the theme manager plugin in order to
 * prevent blocking of the theme manager while it waits for the command palette
 * and main menu to become available.
 */
const themesPaletteMenuPlugin = {
    id: '@jupyterlab/apputils-extension:themes-palette-menu',
    description: 'Adds theme commands to the menu and the command palette.',
    requires: [lib_index_js_.IThemeManager, translation_lib_index_js_.ITranslator],
    optional: [lib_index_js_.ICommandPalette, mainmenu_lib_index_js_.IMainMenu],
    activate: (app, manager, translator, palette, mainMenu) => {
        const trans = translator.load('jupyterlab');
        // If we have a main menu, add the theme manager to the settings menu.
        if (mainMenu) {
            void app.restored.then(() => {
                var _a;
                const isPalette = false;
                const themeMenu = (_a = mainMenu.settingsMenu.items.find(item => {
                    var _a;
                    return item.type === 'submenu' &&
                        ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-settings-apputilstheme';
                })) === null || _a === void 0 ? void 0 : _a.submenu;
                // choose a theme
                if (themeMenu) {
                    manager.themes.forEach((theme, index) => {
                        themeMenu.insertItem(index, {
                            command: themesplugins_CommandIDs.changeTheme,
                            args: { isPalette, theme }
                        });
                    });
                }
            });
        }
        // If we have a command palette, add theme switching options to it.
        if (palette) {
            void app.restored.then(() => {
                const category = trans.__('Theme');
                const command = themesplugins_CommandIDs.changeTheme;
                const isPalette = true;
                // choose a theme
                manager.themes.forEach(theme => {
                    palette.addItem({ command, args: { isPalette, theme }, category });
                });
                // choose preferred light theme
                manager.themes.forEach(theme => {
                    palette.addItem({
                        command: themesplugins_CommandIDs.changePreferredLightTheme,
                        args: { isPalette, theme },
                        category
                    });
                });
                // choose preferred dark theme
                manager.themes.forEach(theme => {
                    palette.addItem({
                        command: themesplugins_CommandIDs.changePreferredDarkTheme,
                        args: { isPalette, theme },
                        category
                    });
                });
                // toggle adaptive theme
                palette.addItem({
                    command: themesplugins_CommandIDs.toggleAdaptiveTheme,
                    args: { isPalette },
                    category
                });
                // toggle scrollbar theming
                palette.addItem({ command: themesplugins_CommandIDs.themeScrollbars, category });
                // increase/decrease code font size
                palette.addItem({
                    command: themesplugins_CommandIDs.incrFontSize,
                    args: {
                        key: 'code-font-size'
                    },
                    category
                });
                palette.addItem({
                    command: themesplugins_CommandIDs.decrFontSize,
                    args: {
                        key: 'code-font-size'
                    },
                    category
                });
                // increase/decrease content font size
                palette.addItem({
                    command: themesplugins_CommandIDs.incrFontSize,
                    args: {
                        key: 'content-font-size1'
                    },
                    category
                });
                palette.addItem({
                    command: themesplugins_CommandIDs.decrFontSize,
                    args: {
                        key: 'content-font-size1'
                    },
                    category
                });
                // increase/decrease ui font size
                palette.addItem({
                    command: themesplugins_CommandIDs.incrFontSize,
                    args: {
                        key: 'ui-font-size1'
                    },
                    category
                });
                palette.addItem({
                    command: themesplugins_CommandIDs.decrFontSize,
                    args: {
                        key: 'ui-font-size1'
                    },
                    category
                });
            });
        }
    },
    autoStart: true
};

;// CONCATENATED MODULE: ../packages/apputils-extension/lib/toolbarregistryplugin.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/**
 * The default toolbar registry.
 */
const toolbarRegistry = {
    id: '@jupyterlab/apputils-extension:toolbar-registry',
    description: 'Provides toolbar items registry.',
    autoStart: true,
    provides: lib_index_js_.IToolbarWidgetRegistry,
    activate: (app) => {
        const registry = new lib_index_js_.ToolbarWidgetRegistry({
            defaultFactory: (0,lib_index_js_.createDefaultFactory)(app.commands)
        });
        return registry;
    }
};

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/filebrowser@~4.1.0-alpha.2 (singleton) (fallback: ../packages/filebrowser/lib/index.js)
var filebrowser_lib_index_js_ = __webpack_require__(35855);
;// CONCATENATED MODULE: ../packages/apputils-extension/lib/workspacesplugin.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








var workspacesplugin_CommandIDs;
(function (CommandIDs) {
    CommandIDs.saveWorkspace = 'workspace-ui:save';
    CommandIDs.saveWorkspaceAs = 'workspace-ui:save-as';
})(workspacesplugin_CommandIDs || (workspacesplugin_CommandIDs = {}));
const WORKSPACE_NAME = 'jupyterlab-workspace';
const WORKSPACE_EXT = '.' + WORKSPACE_NAME;
const LAST_SAVE_ID = 'workspace-ui:lastSave';
const ICON_NAME = 'jp-JupyterIcon';
/**
 * The workspace MIME renderer and save plugin.
 */
const workspacesPlugin = {
    id: '@jupyterlab/apputils-extension:workspaces',
    description: 'Add workspace file type and commands.',
    autoStart: true,
    requires: [
        filebrowser_lib_index_js_.IDefaultFileBrowser,
        lib_index_js_.IWindowResolver,
        statedb_lib_index_js_.IStateDB,
        translation_lib_index_js_.ITranslator,
        index_js_.JupyterFrontEnd.IPaths
    ],
    optional: [index_js_.IRouter],
    activate: (app, fileBrowser, resolver, state, translator, paths, router) => {
        // The workspace factory creates dummy widgets to load a new workspace.
        const factory = new workspacesplugin_Private.WorkspaceFactory({
            workspaces: app.serviceManager.workspaces,
            router,
            state,
            translator,
            paths
        });
        const trans = translator.load('jupyterlab');
        app.docRegistry.addFileType({
            name: WORKSPACE_NAME,
            contentType: 'file',
            fileFormat: 'text',
            displayName: trans.__('JupyterLab workspace File'),
            extensions: [WORKSPACE_EXT],
            mimeTypes: ['text/json'],
            iconClass: ICON_NAME
        });
        app.docRegistry.addWidgetFactory(factory);
        app.commands.addCommand(workspacesplugin_CommandIDs.saveWorkspaceAs, {
            label: trans.__('Save Current Workspace As…'),
            execute: async () => {
                const data = app.serviceManager.workspaces.fetch(resolver.name);
                await workspacesplugin_Private.saveAs(fileBrowser, app.serviceManager.contents, data, state, translator);
            }
        });
        app.commands.addCommand(workspacesplugin_CommandIDs.saveWorkspace, {
            label: trans.__('Save Current Workspace'),
            execute: async () => {
                const { contents } = app.serviceManager;
                const data = app.serviceManager.workspaces.fetch(resolver.name);
                const lastSave = (await state.fetch(LAST_SAVE_ID));
                if (lastSave === undefined) {
                    await workspacesplugin_Private.saveAs(fileBrowser, contents, data, state, translator);
                }
                else {
                    await workspacesplugin_Private.save(lastSave, contents, data, state);
                }
            }
        });
    }
};
var workspacesplugin_Private;
(function (Private) {
    /**
     * Save workspace to a user provided location
     */
    async function save(userPath, contents, data, state) {
        let name = userPath.split('/').pop();
        // Add extension if not provided or remove extension from name if it was.
        if (name !== undefined && name.includes('.')) {
            name = name.split('.')[0];
        }
        else {
            userPath = userPath + WORKSPACE_EXT;
        }
        // Save last save location, for save button to work
        await state.save(LAST_SAVE_ID, userPath);
        const resolvedData = await data;
        resolvedData.metadata.id = `${name}`;
        await contents.save(userPath, {
            type: 'file',
            format: 'text',
            content: JSON.stringify(resolvedData)
        });
    }
    Private.save = save;
    /**
     * Ask user for location, and save workspace.
     * Default location is the current directory in the file browser
     */
    async function saveAs(browser, contents, data, state, translator) {
        var _a;
        translator = translator || translation_lib_index_js_.nullTranslator;
        const lastSave = await state.fetch(LAST_SAVE_ID);
        let defaultName;
        if (lastSave === undefined) {
            defaultName = 'new-workspace';
        }
        else {
            defaultName = (_a = lastSave.split('/').pop()) === null || _a === void 0 ? void 0 : _a.split('.')[0];
        }
        const defaultPath = browser.model.path + '/' + defaultName + WORKSPACE_EXT;
        const userPath = await getSavePath(defaultPath, translator);
        if (userPath) {
            await save(userPath, contents, data, state);
        }
    }
    Private.saveAs = saveAs;
    /**
     * This widget factory is used to handle double click on workspace
     */
    class WorkspaceFactory extends docregistry_lib_index_js_.ABCWidgetFactory {
        /**
         * Construct a widget factory that uploads a workspace and navigates to it.
         *
         * @param options - The instantiation options for a `WorkspaceFactory`.
         */
        constructor(options) {
            const trans = (options.translator || translation_lib_index_js_.nullTranslator).load('jupyterlab');
            super({
                name: 'Workspace loader',
                label: trans.__('Workspace loader'),
                fileTypes: [WORKSPACE_NAME],
                defaultFor: [WORKSPACE_NAME],
                readOnly: true
            });
            this._application = options.paths.urls.app;
            this._router = options.router;
            this._state = options.state;
            this._workspaces = options.workspaces;
        }
        /**
         * Loads the workspace into load, and jump to it
         * @param context This is used queried to query the workspace content
         */
        createNewWidget(context) {
            // Save a file's contents as a workspace and navigate to that workspace.
            void context.ready.then(async () => {
                const file = context.model;
                const workspace = file.toJSON();
                const path = context.path;
                const id = workspace.metadata.id;
                // Save the file contents as a workspace.
                await this._workspaces.save(id, workspace);
                // Save last save location for the save command.
                await this._state.save(LAST_SAVE_ID, path);
                // Navigate to new workspace.
                const url = coreutils_lib_index_js_.URLExt.join(this._application, 'workspaces', id);
                if (this._router) {
                    this._router.navigate(url, { hard: true });
                }
                else {
                    document.location.href = url;
                }
            });
            return dummyWidget(context);
        }
    }
    Private.WorkspaceFactory = WorkspaceFactory;
    /**
     * Returns a dummy widget with disposed content that doesn't render in the UI.
     *
     * @param context - The file context.
     */
    function dummyWidget(context) {
        const widget = new docregistry_lib_index_js_.DocumentWidget({ content: new widgets_dist_index_es6_js_.Widget(), context });
        widget.content.dispose();
        return widget;
    }
    /**
     * Ask user for a path to save to.
     * @param defaultPath Path already present when the dialog is shown
     */
    async function getSavePath(defaultPath, translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        const saveBtn = lib_index_js_.Dialog.okButton({
            label: trans.__('Save'),
            ariaLabel: trans.__('Save Current Workspace')
        });
        const result = await (0,lib_index_js_.showDialog)({
            title: trans.__('Save Current Workspace As…'),
            body: new SaveWidget(defaultPath),
            buttons: [lib_index_js_.Dialog.cancelButton(), saveBtn]
        });
        if (result.button.label === trans.__('Save')) {
            return result.value;
        }
        else {
            return null;
        }
    }
    /**
     * A widget that gets a file path from a user.
     */
    class SaveWidget extends widgets_dist_index_es6_js_.Widget {
        /**
         * Gets a modal node for getting save location. Will have a default to the current opened directory
         * @param path Default location
         */
        constructor(path) {
            super({ node: createSaveNode(path) });
        }
        /**
         * Gets the save path entered by the user
         */
        getValue() {
            return this.node.value;
        }
    }
    /**
     * Create the node for a save widget.
     */
    function createSaveNode(path) {
        const input = document.createElement('input');
        input.value = path;
        return input;
    }
})(workspacesplugin_Private || (workspacesplugin_Private = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/domutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/domutils/dist/index.es6.js)
var domutils_dist_index_es6_js_ = __webpack_require__(92654);
;// CONCATENATED MODULE: ../packages/apputils-extension/lib/shortcuts.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */




/**
 * The class name for each row of ContextShortcutTable
 */
const SHORTCUT_TABLE_ROW_CLASS = 'jp-ContextualShortcut-TableRow';
/**
 * The class name for the last row of ContextShortcutTable
 */
const SHORTCUT_TABLE_LAST_ROW_CLASS = 'jp-ContextualShortcut-TableLastRow';
/**
 * The class name for each item of ContextShortcutTable
 */
const SHORTCUT_TABLE_ITEM_CLASS = 'jp-ContextualShortcut-TableItem';
/**
 * The class name for each button-like symbol representing a key used in a shortcut in the ContextShortcutTable
 */
const SHORTCUT_KEY_CLASS = 'jp-ContextualShortcut-Key';
function displayShortcuts(options) {
    const { commands, trans, activeElement } = options;
    const elt = activeElement !== null && activeElement !== void 0 ? activeElement : document.activeElement;
    /**
     * Find the distance from the target node to the first matching node.
     *
     * Based on Lumino private function commands.Private.targetDistance
     * This traverses the DOM path from `elt` to the root
     * computes the distance from `elt` to the first node which matches
     * the CSS selector. If no match is found, `-1` is returned.
     *
     * It also stops traversal if the `data-lm-suppress-shortcuts` or
     * `data-p-suppress-shortcuts` attributes are found.
     */
    function formatKeys(keys) {
        const topContainer = [];
        keys.forEach((key, index) => {
            const container = [];
            key.split(' ').forEach((ch, chIndex) => {
                container.push(react_index_js_.createElement("span", { className: SHORTCUT_KEY_CLASS, key: `ch-${chIndex}` },
                    react_index_js_.createElement("kbd", null, ch)), react_index_js_.createElement(react_index_js_.Fragment, { key: `fragment-${chIndex}` }, " + "));
            });
            topContainer.push(react_index_js_.createElement("span", { key: `key-${index}` }, container.slice(0, -1)), react_index_js_.createElement(react_index_js_.Fragment, { key: `fragment-${index}` }, " + "));
        });
        return react_index_js_.createElement("span", null, topContainer.slice(0, -1));
    }
    function capitalizeString(str) {
        const capitalizedStr = str.charAt(0).toUpperCase() + str.slice(1);
        return capitalizedStr;
    }
    function formatLabel(b) {
        const label = commands.label(b.command);
        const commandID = b.command.split(':')[1];
        const automaticLabel = commandID.split('-');
        let capitalizedLabel = '';
        for (let i = 0; i < automaticLabel.length; i++) {
            const str = capitalizeString(automaticLabel[i]);
            capitalizedLabel = capitalizedLabel + ' ' + str;
        }
        if (label.length > 0) {
            return label;
        }
        else {
            return capitalizedLabel;
        }
    }
    function matchDistance(selector, elt) {
        let targ = elt;
        for (let dist = 0; targ !== null && targ !== targ.parentElement; targ = targ.parentElement, ++dist) {
            if (targ.hasAttribute('data-lm-suppress-shortcuts')) {
                return -1;
            }
            if (targ.matches(selector)) {
                return dist;
            }
        }
        return -1;
    }
    // Find active keybindings for target element
    const activeBindings = new Map();
    for (let i = 0; i < commands.keyBindings.length; i++) {
        const kb = commands.keyBindings[i];
        let distance = matchDistance(kb.selector, elt);
        if (distance < 0) {
            continue;
        }
        let formatted = commands_dist_index_es6_js_.CommandRegistry.formatKeystroke(kb.keys);
        if (activeBindings.has(formatted)) {
            let oldBinding = activeBindings.get(formatted);
            // if the existing binding takes precedence, ignore this binding by continuing
            if (oldBinding[0] < distance ||
                (oldBinding[0] === distance &&
                    domutils_dist_index_es6_js_.Selector.calculateSpecificity(oldBinding[1].selector) >
                        domutils_dist_index_es6_js_.Selector.calculateSpecificity(kb.selector))) {
                continue;
            }
        }
        activeBindings.set(formatted, [distance, kb]);
    }
    // Group shortcuts by distance
    let maxDistance = -1;
    const groupedBindings = new Map();
    for (let [distance, binding] of activeBindings.values()) {
        maxDistance = Math.max(distance, maxDistance);
        if (!groupedBindings.has(distance)) {
            groupedBindings.set(distance, []);
        }
        groupedBindings.get(distance).push(binding);
    }
    // Display shortcuts by group
    const bindingTable = [];
    for (let d = 0; d <= maxDistance; d++) {
        if (groupedBindings.has(d)) {
            bindingTable.push(groupedBindings.get(d).map(b => (react_index_js_.createElement("tr", { className: SHORTCUT_TABLE_ROW_CLASS, key: `${b.command}-${b.keys.join('-').replace(' ', '_')}` },
                react_index_js_.createElement("td", { className: SHORTCUT_TABLE_ITEM_CLASS }, formatLabel(b)),
                react_index_js_.createElement("td", { className: SHORTCUT_TABLE_ITEM_CLASS }, formatKeys([...b.keys]))))));
            bindingTable.push(react_index_js_.createElement("tr", { className: SHORTCUT_TABLE_LAST_ROW_CLASS, key: `group-${d}-last` }));
        }
    }
    const body = (react_index_js_.createElement("table", null,
        react_index_js_.createElement("tbody", null, bindingTable)));
    return (0,lib_index_js_.showDialog)({
        title: trans.__('Keyboard Shortcuts'),
        body,
        buttons: [
            lib_index_js_.Dialog.cancelButton({
                label: trans.__('Close')
            })
        ]
    });
}

;// CONCATENATED MODULE: ../packages/apputils-extension/lib/index.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module apputils-extension
 */



















/**
 * The interval in milliseconds before recover options appear during splash.
 */
const SPLASH_RECOVER_TIMEOUT = 12000;
/**
 * The command IDs used by the apputils plugin.
 */
var lib_CommandIDs;
(function (CommandIDs) {
    CommandIDs.loadState = 'apputils:load-statedb';
    CommandIDs.print = 'apputils:print';
    CommandIDs.reset = 'apputils:reset';
    CommandIDs.resetOnLoad = 'apputils:reset-on-load';
    CommandIDs.runFirstEnabled = 'apputils:run-first-enabled';
    CommandIDs.runAllEnabled = 'apputils:run-all-enabled';
    CommandIDs.toggleHeader = 'apputils:toggle-header';
    CommandIDs.displayShortcuts = 'apputils:display-shortcuts';
})(lib_CommandIDs || (lib_CommandIDs = {}));
/**
 * The default command palette extension.
 */
const palette = {
    id: '@jupyterlab/apputils-extension:palette',
    description: 'Provides the command palette.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    provides: lib_index_js_.ICommandPalette,
    optional: [settingregistry_lib_index_js_.ISettingRegistry],
    activate: (app, translator, settingRegistry) => {
        return Palette.activate(app, translator, settingRegistry);
    }
};
/**
 * The default command palette's restoration extension.
 *
 * #### Notes
 * The command palette's restoration logic is handled separately from the
 * command palette provider extension because the layout restorer dependency
 * causes the command palette to be unavailable to other extensions earlier
 * in the application load cycle.
 */
const paletteRestorer = {
    id: '@jupyterlab/apputils-extension:palette-restorer',
    description: 'Restores the command palette.',
    autoStart: true,
    requires: [index_js_.ILayoutRestorer, translation_lib_index_js_.ITranslator],
    activate: (app, restorer, translator) => {
        Palette.restore(app, restorer, translator);
    }
};
/**
 * The default window name resolver provider.
 */
const resolver = {
    id: '@jupyterlab/apputils-extension:resolver',
    description: 'Provides the window name resolver.',
    autoStart: true,
    provides: lib_index_js_.IWindowResolver,
    requires: [index_js_.JupyterFrontEnd.IPaths, index_js_.IRouter],
    activate: async (app, paths, router) => {
        const { hash, search } = router.current;
        const query = coreutils_lib_index_js_.URLExt.queryStringToObject(search || '');
        const solver = new lib_index_js_.WindowResolver();
        const workspace = coreutils_lib_index_js_.PageConfig.getOption('workspace');
        const treePath = coreutils_lib_index_js_.PageConfig.getOption('treePath');
        const mode = coreutils_lib_index_js_.PageConfig.getOption('mode') === 'multiple-document' ? 'lab' : 'doc';
        // This is used as a key in local storage to refer to workspaces, either the name
        // of the workspace or the string PageConfig.defaultWorkspace. Both lab and doc modes share the same workspace.
        const candidate = workspace ? workspace : coreutils_lib_index_js_.PageConfig.defaultWorkspace;
        const rest = treePath ? coreutils_lib_index_js_.URLExt.join('tree', treePath) : '';
        try {
            await solver.resolve(candidate);
            return solver;
        }
        catch (error) {
            // Window resolution has failed so the URL must change. Return a promise
            // that never resolves to prevent the application from loading plugins
            // that rely on `IWindowResolver`.
            return new Promise(() => {
                const { base } = paths.urls;
                const pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
                const random = pool[Math.floor(Math.random() * pool.length)];
                let path = coreutils_lib_index_js_.URLExt.join(base, mode, 'workspaces', `auto-${random}`);
                path = rest ? coreutils_lib_index_js_.URLExt.join(path, coreutils_lib_index_js_.URLExt.encodeParts(rest)) : path;
                // Reset the workspace on load.
                query['reset'] = '';
                const url = path + coreutils_lib_index_js_.URLExt.objectToQueryString(query) + (hash || '');
                router.navigate(url, { hard: true });
            });
        }
    }
};
/**
 * The default splash screen provider.
 */
const splash = {
    id: '@jupyterlab/apputils-extension:splash',
    description: 'Provides the splash screen.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    provides: lib_index_js_.ISplashScreen,
    activate: (app, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands, restored } = app;
        // Create splash element and populate it.
        const splash = document.createElement('div');
        const galaxy = document.createElement('div');
        const logo = document.createElement('div');
        splash.id = 'jupyterlab-splash';
        galaxy.id = 'galaxy';
        logo.id = 'main-logo';
        ui_components_lib_index_js_.jupyterFaviconIcon.element({
            container: logo,
            stylesheet: 'splash'
        });
        galaxy.appendChild(logo);
        ['1', '2', '3'].forEach(id => {
            const moon = document.createElement('div');
            const planet = document.createElement('div');
            moon.id = `moon${id}`;
            moon.className = 'moon orbit';
            planet.id = `planet${id}`;
            planet.className = 'planet';
            moon.appendChild(planet);
            galaxy.appendChild(moon);
        });
        splash.appendChild(galaxy);
        // Create debounced recovery dialog function.
        let dialog;
        const recovery = new dist_index_es6_js_.Throttler(async () => {
            if (dialog) {
                return;
            }
            dialog = new lib_index_js_.Dialog({
                title: trans.__('Loading…'),
                body: trans.__(`The loading screen is taking a long time.
Would you like to clear the workspace or keep waiting?`),
                buttons: [
                    lib_index_js_.Dialog.cancelButton({ label: trans.__('Keep Waiting') }),
                    lib_index_js_.Dialog.warnButton({ label: trans.__('Clear Workspace') })
                ]
            });
            try {
                const result = await dialog.launch();
                dialog.dispose();
                dialog = null;
                if (result.button.accept && commands.hasCommand(lib_CommandIDs.reset)) {
                    return commands.execute(lib_CommandIDs.reset);
                }
                // Re-invoke the recovery timer in the next frame.
                requestAnimationFrame(() => {
                    // Because recovery can be stopped, handle invocation rejection.
                    void recovery.invoke().catch(_ => undefined);
                });
            }
            catch (error) {
                /* no-op */
            }
        }, { limit: SPLASH_RECOVER_TIMEOUT, edge: 'trailing' });
        // Return ISplashScreen.
        let splashCount = 0;
        return {
            show: (light = true) => {
                splash.classList.remove('splash-fade');
                splash.classList.toggle('light', light);
                splash.classList.toggle('dark', !light);
                splashCount++;
                document.body.appendChild(splash);
                // Because recovery can be stopped, handle invocation rejection.
                void recovery.invoke().catch(_ => undefined);
                return new index_es6_js_.DisposableDelegate(async () => {
                    await restored;
                    if (--splashCount === 0) {
                        void recovery.stop();
                        if (dialog) {
                            dialog.dispose();
                            dialog = null;
                        }
                        splash.classList.add('splash-fade');
                        window.setTimeout(() => {
                            document.body.removeChild(splash);
                        }, 200);
                    }
                });
            }
        };
    }
};
const print = {
    id: '@jupyterlab/apputils-extension:print',
    description: 'Add the print capability',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    activate: (app, translator) => {
        const trans = translator.load('jupyterlab');
        app.commands.addCommand(lib_CommandIDs.print, {
            label: trans.__('Print…'),
            isEnabled: () => {
                const widget = app.shell.currentWidget;
                return lib_index_js_.Printing.getPrintFunction(widget) !== null;
            },
            execute: async () => {
                const widget = app.shell.currentWidget;
                const printFunction = lib_index_js_.Printing.getPrintFunction(widget);
                if (printFunction) {
                    await printFunction();
                }
            }
        });
    }
};
const toggleHeader = {
    id: '@jupyterlab/apputils-extension:toggle-header',
    description: 'Adds a command to display the main area widget content header.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    optional: [lib_index_js_.ICommandPalette],
    activate: (app, translator, palette) => {
        const trans = translator.load('jupyterlab');
        const category = trans.__('Main Area');
        app.commands.addCommand(lib_CommandIDs.toggleHeader, {
            label: trans.__('Show Header Above Content'),
            isEnabled: () => app.shell.currentWidget instanceof lib_index_js_.MainAreaWidget &&
                !app.shell.currentWidget.contentHeader.isDisposed &&
                app.shell.currentWidget.contentHeader.widgets.length > 0,
            isToggled: () => {
                const widget = app.shell.currentWidget;
                return widget instanceof lib_index_js_.MainAreaWidget
                    ? !widget.contentHeader.isHidden
                    : false;
            },
            execute: async () => {
                const widget = app.shell.currentWidget;
                if (widget instanceof lib_index_js_.MainAreaWidget) {
                    widget.contentHeader.setHidden(!widget.contentHeader.isHidden);
                }
            }
        });
        if (palette) {
            palette.addItem({ command: lib_CommandIDs.toggleHeader, category });
        }
    }
};
/**
 * Update the browser title based on the workspace and the current
 * active item.
 */
async function updateTabTitle(workspace, db, name) {
    var _a, _b;
    const data = await db.toJSON();
    let current = (_b = (_a = data['layout-restorer:data']) === null || _a === void 0 ? void 0 : _a.main) === null || _b === void 0 ? void 0 : _b.current;
    if (current === undefined) {
        document.title = `${coreutils_lib_index_js_.PageConfig.getOption('appName') || 'JupyterLab'}${workspace.startsWith('auto-') ? ` (${workspace})` : ``}`;
    }
    else {
        // File name from current path
        let currentFile = coreutils_lib_index_js_.PathExt.basename(decodeURIComponent(window.location.href));
        // Truncate to first 12 characters of current document name + ... if length > 15
        currentFile =
            currentFile.length > 15
                ? currentFile.slice(0, 12).concat(`…`)
                : currentFile;
        // Number of restorable items that are either notebooks or editors
        const count = Object.keys(data).filter(item => item.startsWith('notebook') || item.startsWith('editor')).length;
        if (workspace.startsWith('auto-')) {
            document.title = `${currentFile} (${workspace}${count > 1 ? ` : ${count}` : ``}) - ${name}`;
        }
        else {
            document.title = `${currentFile}${count > 1 ? ` (${count})` : ``} - ${name}`;
        }
    }
}
/**
 * The default state database for storing application state.
 *
 * #### Notes
 * If this extension is loaded with a window resolver, it will automatically add
 * state management commands, URL support for `clone` and `reset`, and workspace
 * auto-saving. Otherwise, it will return a simple in-memory state database.
 */
const state = {
    id: '@jupyterlab/apputils-extension:state',
    description: 'Provides the application state. It is stored per workspaces.',
    autoStart: true,
    provides: statedb_lib_index_js_.IStateDB,
    requires: [index_js_.JupyterFrontEnd.IPaths, index_js_.IRouter, translation_lib_index_js_.ITranslator],
    optional: [lib_index_js_.IWindowResolver],
    activate: (app, paths, router, translator, resolver) => {
        const trans = translator.load('jupyterlab');
        if (resolver === null) {
            return new statedb_lib_index_js_.StateDB();
        }
        let resolved = false;
        const { commands, name, serviceManager } = app;
        const { workspaces } = serviceManager;
        const workspace = resolver.name;
        const transform = new dist_index_js_.PromiseDelegate();
        const db = new statedb_lib_index_js_.StateDB({ transform: transform.promise });
        const save = new dist_index_es6_js_.Debouncer(async () => {
            const id = workspace;
            const metadata = { id };
            const data = await db.toJSON();
            await workspaces.save(id, { data, metadata });
        });
        // Any time the local state database changes, save the workspace.
        db.changed.connect(() => void save.invoke(), db);
        db.changed.connect(() => updateTabTitle(workspace, db, name));
        commands.addCommand(lib_CommandIDs.loadState, {
            label: trans.__('Load state for the current workspace.'),
            execute: async (args) => {
                // Since the command can be executed an arbitrary number of times, make
                // sure it is safe to call multiple times.
                if (resolved) {
                    return;
                }
                const { hash, path, search } = args;
                const query = coreutils_lib_index_js_.URLExt.queryStringToObject(search || '');
                const clone = typeof query['clone'] === 'string'
                    ? query['clone'] === ''
                        ? coreutils_lib_index_js_.PageConfig.defaultWorkspace
                        : query['clone']
                    : null;
                const source = clone || workspace || null;
                if (source === null) {
                    console.error(`${lib_CommandIDs.loadState} cannot load null workspace.`);
                    return;
                }
                try {
                    const saved = await workspaces.fetch(source);
                    // If this command is called after a reset, the state database
                    // will already be resolved.
                    if (!resolved) {
                        resolved = true;
                        transform.resolve({ type: 'overwrite', contents: saved.data });
                    }
                }
                catch ({ message }) {
                    console.warn(`Fetching workspace "${workspace}" failed.`, message);
                    // If the workspace does not exist, cancel the data transformation
                    // and save a workspace with the current user state data.
                    if (!resolved) {
                        resolved = true;
                        transform.resolve({ type: 'cancel', contents: null });
                    }
                }
                if (source === clone) {
                    // Maintain the query string parameters but remove `clone`.
                    delete query['clone'];
                    const url = path + coreutils_lib_index_js_.URLExt.objectToQueryString(query) + hash;
                    const cloned = save.invoke().then(() => router.stop);
                    // After the state has been cloned, navigate to the URL.
                    void cloned.then(() => {
                        router.navigate(url);
                    });
                    return cloned;
                }
                // After the state database has finished loading, save it.
                await save.invoke();
            }
        });
        commands.addCommand(lib_CommandIDs.reset, {
            label: trans.__('Reset Application State'),
            execute: async ({ reload }) => {
                await db.clear();
                await save.invoke();
                if (reload) {
                    router.reload();
                }
            }
        });
        commands.addCommand(lib_CommandIDs.resetOnLoad, {
            label: trans.__('Reset state when loading for the workspace.'),
            execute: (args) => {
                const { hash, path, search } = args;
                const query = coreutils_lib_index_js_.URLExt.queryStringToObject(search || '');
                const reset = 'reset' in query;
                const clone = 'clone' in query;
                if (!reset) {
                    return;
                }
                // If the state database has already been resolved, resetting is
                // impossible without reloading.
                if (resolved) {
                    return router.reload();
                }
                // Empty the state database.
                resolved = true;
                transform.resolve({ type: 'clear', contents: null });
                // Maintain the query string parameters but remove `reset`.
                delete query['reset'];
                const url = path + coreutils_lib_index_js_.URLExt.objectToQueryString(query) + hash;
                const cleared = db.clear().then(() => save.invoke());
                // After the state has been reset, navigate to the URL.
                if (clone) {
                    void cleared.then(() => {
                        router.navigate(url, { hard: true });
                    });
                }
                else {
                    void cleared.then(() => {
                        router.navigate(url);
                    });
                }
                return cleared;
            }
        });
        router.register({
            command: lib_CommandIDs.loadState,
            pattern: /.?/,
            rank: 30 // High priority: 30:100.
        });
        router.register({
            command: lib_CommandIDs.resetOnLoad,
            pattern: /(\?reset|\&reset)($|&)/,
            rank: 20 // High priority: 20:100.
        });
        return db;
    }
};
/**
 * The default session context dialogs extension.
 */
const sessionDialogs = {
    id: '@jupyterlab/apputils-extension:sessionDialogs',
    description: 'Provides the session context dialogs.',
    provides: lib_index_js_.ISessionContextDialogs,
    optional: [translation_lib_index_js_.ITranslator],
    autoStart: true,
    activate: async (app, translator) => {
        return new lib_index_js_.SessionContextDialogs({
            translator: translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator
        });
    }
};
/**
 * Utility commands
 */
const utilityCommands = {
    id: '@jupyterlab/apputils-extension:utilityCommands',
    description: 'Adds meta commands to run set of other commands.',
    requires: [translation_lib_index_js_.ITranslator],
    optional: [lib_index_js_.ICommandPalette],
    autoStart: true,
    activate: (app, translator, palette) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        commands.addCommand(lib_CommandIDs.runFirstEnabled, {
            label: trans.__('Run First Enabled Command'),
            execute: args => {
                const commands = args.commands;
                const commandArgs = args.args;
                const argList = Array.isArray(args);
                for (let i = 0; i < commands.length; i++) {
                    const cmd = commands[i];
                    const arg = argList ? commandArgs[i] : commandArgs;
                    if (app.commands.isEnabled(cmd, arg)) {
                        return app.commands.execute(cmd, arg);
                    }
                }
            }
        });
        // Add a command for taking lists of commands and command arguments
        // and running all the enabled commands.
        commands.addCommand(lib_CommandIDs.runAllEnabled, {
            label: trans.__('Run All Enabled Commands Passed as Args'),
            execute: async (args) => {
                var _a, _b;
                const commands = (_a = args.commands) !== null && _a !== void 0 ? _a : [];
                const commandArgs = args.args;
                const argList = Array.isArray(args);
                const errorIfNotEnabled = (_b = args.errorIfNotEnabled) !== null && _b !== void 0 ? _b : false;
                for (let i = 0; i < commands.length; i++) {
                    const cmd = commands[i];
                    const arg = argList ? commandArgs[i] : commandArgs;
                    if (app.commands.isEnabled(cmd, arg)) {
                        await app.commands.execute(cmd, arg);
                    }
                    else {
                        if (errorIfNotEnabled) {
                            console.error(`${cmd} is not enabled.`);
                        }
                    }
                }
            },
            isEnabled: args => {
                var _a;
                const commands = (_a = args.commands) !== null && _a !== void 0 ? _a : [];
                const commandArgs = args.args;
                const argList = Array.isArray(args);
                return commands.some((cmd, idx) => app.commands.isEnabled(cmd, argList ? commandArgs[idx] : commandArgs));
            }
        });
        commands.addCommand(lib_CommandIDs.displayShortcuts, {
            label: trans.__('Show Keyboard Shortcuts'),
            caption: trans.__('Show relevant keyboard shortcuts for the current active widget'),
            execute: args => {
                var _a;
                const currentWidget = app.shell.currentWidget;
                const included = currentWidget === null || currentWidget === void 0 ? void 0 : currentWidget.node.contains(document.activeElement);
                if (!included && currentWidget instanceof lib_index_js_.MainAreaWidget) {
                    const currentNode = (_a = currentWidget.content.node) !== null && _a !== void 0 ? _a : currentWidget === null || currentWidget === void 0 ? void 0 : currentWidget.node;
                    currentNode === null || currentNode === void 0 ? void 0 : currentNode.focus();
                }
                const options = { commands, trans };
                return displayShortcuts(options);
            }
        });
        if (palette) {
            const category = trans.__('Help');
            palette.addItem({ command: lib_CommandIDs.displayShortcuts, category });
        }
    }
};
/**
 * The default HTML sanitizer.
 */
const sanitizer = {
    id: '@jupyterlab/apputils-extension:sanitizer',
    description: 'Provides the HTML sanitizer.',
    autoStart: true,
    provides: lib_index_js_.ISanitizer,
    requires: [settingregistry_lib_index_js_.ISettingRegistry],
    activate: (app, settings) => {
        const sanitizer = new lib_index_js_.Sanitizer();
        const loadSetting = (setting) => {
            const allowedSchemes = setting.get('allowedSchemes')
                .composite;
            const autolink = setting.get('autolink').composite;
            if (allowedSchemes) {
                sanitizer.setAllowedSchemes(allowedSchemes);
            }
            sanitizer.setAutolink(autolink);
        };
        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        settings
            .load('@jupyterlab/apputils-extension:sanitizer')
            .then(setting => {
            // Read the settings
            loadSetting(setting);
            // Listen for your plugin setting changes using Signal
            setting.changed.connect(loadSetting);
        })
            .catch(reason => {
            console.error(`Failed to load sanitizer settings:`, reason);
        });
        return sanitizer;
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    announcements,
    kernelStatus,
    notificationPlugin,
    palette,
    paletteRestorer,
    print,
    resolver,
    runningSessionsStatus,
    sanitizer,
    settingsPlugin,
    state,
    splash,
    sessionDialogs,
    themesPlugin,
    themesPaletteMenuPlugin,
    toggleHeader,
    toolbarRegistry,
    utilityCommands,
    workspacesPlugin
];
/* harmony default export */ const lib = (plugins);


/***/ })

}]);
//# sourceMappingURL=7899.a058933a7d08913f45ff.js.map?v=a058933a7d08913f45ff