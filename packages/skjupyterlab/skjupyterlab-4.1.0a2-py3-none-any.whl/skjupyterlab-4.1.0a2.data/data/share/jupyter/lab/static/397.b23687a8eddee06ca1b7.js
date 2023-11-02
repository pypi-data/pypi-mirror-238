"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[397],{

/***/ 10397:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "ModelDB": () => (/* reexport */ ModelDB),
  "ObservableJSON": () => (/* reexport */ ObservableJSON),
  "ObservableList": () => (/* reexport */ ObservableList),
  "ObservableMap": () => (/* reexport */ ObservableMap),
  "ObservableString": () => (/* reexport */ ObservableString),
  "ObservableUndoableList": () => (/* reexport */ ObservableUndoableList),
  "ObservableValue": () => (/* reexport */ ObservableValue)
});

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(78612);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/messaging@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/messaging/dist/index.es6.js)
var messaging_dist_index_es6_js_ = __webpack_require__(85755);
;// CONCATENATED MODULE: ../packages/observables/lib/observablemap.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A concrete implementation of IObservableMap<T>.
 */
class ObservableMap {
    /**
     * Construct a new observable map.
     */
    constructor(options = {}) {
        this._map = new Map();
        this._changed = new dist_index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._itemCmp = options.itemCmp || Private.itemCmp;
        if (options.values) {
            for (const key in options.values) {
                this._map.set(key, options.values[key]);
            }
        }
    }
    /**
     * The type of the Observable.
     */
    get type() {
        return 'Map';
    }
    /**
     * A signal emitted when the map has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Whether this map has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * The number of key-value pairs in the map.
     */
    get size() {
        return this._map.size;
    }
    /**
     * Set a key-value pair in the map
     *
     * @param key - The key to set.
     *
     * @param value - The value for the key.
     *
     * @returns the old value for the key, or undefined
     *   if that did not exist.
     *
     * @throws if the new value is undefined.
     *
     * #### Notes
     * This is a no-op if the value does not change.
     */
    set(key, value) {
        const oldVal = this._map.get(key);
        if (value === undefined) {
            throw Error('Cannot set an undefined value, use remove');
        }
        // Bail if the value does not change.
        const itemCmp = this._itemCmp;
        if (oldVal !== undefined && itemCmp(oldVal, value)) {
            return oldVal;
        }
        this._map.set(key, value);
        this._changed.emit({
            type: oldVal ? 'change' : 'add',
            key: key,
            oldValue: oldVal,
            newValue: value
        });
        return oldVal;
    }
    /**
     * Get a value for a given key.
     *
     * @param key - the key.
     *
     * @returns the value for that key.
     */
    get(key) {
        return this._map.get(key);
    }
    /**
     * Check whether the map has a key.
     *
     * @param key - the key to check.
     *
     * @returns `true` if the map has the key, `false` otherwise.
     */
    has(key) {
        return this._map.has(key);
    }
    /**
     * Get a list of the keys in the map.
     *
     * @returns - a list of keys.
     */
    keys() {
        const keyList = [];
        this._map.forEach((v, k) => {
            keyList.push(k);
        });
        return keyList;
    }
    /**
     * Get a list of the values in the map.
     *
     * @returns - a list of values.
     */
    values() {
        const valList = [];
        this._map.forEach((v, k) => {
            valList.push(v);
        });
        return valList;
    }
    /**
     * Remove a key from the map
     *
     * @param key - the key to remove.
     *
     * @returns the value of the given key,
     *   or undefined if that does not exist.
     *
     * #### Notes
     * This is a no-op if the value does not change.
     */
    delete(key) {
        const oldVal = this._map.get(key);
        const removed = this._map.delete(key);
        if (removed) {
            this._changed.emit({
                type: 'remove',
                key: key,
                oldValue: oldVal,
                newValue: undefined
            });
        }
        return oldVal;
    }
    /**
     * Set the ObservableMap to an empty map.
     */
    clear() {
        // Delete one by one to emit the correct signals.
        const keyList = this.keys();
        for (let i = 0; i < keyList.length; i++) {
            this.delete(keyList[i]);
        }
    }
    /**
     * Dispose of the resources held by the map.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
        this._map.clear();
    }
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The default strict equality item comparator.
     */
    function itemCmp(first, second) {
        return first === second;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/observables/lib/observablejson.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A concrete Observable map for JSON data.
 */
class ObservableJSON extends ObservableMap {
    /**
     * Construct a new observable JSON object.
     */
    constructor(options = {}) {
        super({
            itemCmp: index_js_.JSONExt.deepEqual,
            values: options.values
        });
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        const out = Object.create(null);
        const keys = this.keys();
        for (const key of keys) {
            const value = this.get(key);
            if (value !== undefined) {
                out[key] = index_js_.JSONExt.deepCopy(value);
            }
        }
        return out;
    }
}
/**
 * The namespace for ObservableJSON static data.
 */
(function (ObservableJSON) {
    /**
     * An observable JSON change message.
     */
    class ChangeMessage extends messaging_dist_index_es6_js_.Message {
        /**
         * Create a new metadata changed message.
         */
        constructor(type, args) {
            super(type);
            this.args = args;
        }
    }
    ObservableJSON.ChangeMessage = ChangeMessage;
})(ObservableJSON || (ObservableJSON = {}));

;// CONCATENATED MODULE: ../packages/observables/lib/observablestring.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A concrete implementation of [[IObservableString]]
 */
class ObservableString {
    /**
     * Construct a new observable string.
     */
    constructor(initialText = '') {
        this._text = '';
        this._isDisposed = false;
        this._changed = new dist_index_es6_js_.Signal(this);
        this._text = initialText;
    }
    /**
     * The type of the Observable.
     */
    get type() {
        return 'String';
    }
    /**
     * A signal emitted when the string has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Set the value of the string.
     */
    set text(value) {
        if (value.length === this._text.length && value === this._text) {
            return;
        }
        this._text = value;
        this._changed.emit({
            type: 'set',
            start: 0,
            end: value.length,
            value: value
        });
    }
    /**
     * Get the value of the string.
     */
    get text() {
        return this._text;
    }
    /**
     * Insert a substring.
     *
     * @param index - The starting index.
     *
     * @param text - The substring to insert.
     */
    insert(index, text) {
        this._text = this._text.slice(0, index) + text + this._text.slice(index);
        this._changed.emit({
            type: 'insert',
            start: index,
            end: index + text.length,
            value: text
        });
    }
    /**
     * Remove a substring.
     *
     * @param start - The starting index.
     *
     * @param end - The ending index.
     */
    remove(start, end) {
        const oldValue = this._text.slice(start, end);
        this._text = this._text.slice(0, start) + this._text.slice(end);
        this._changed.emit({
            type: 'remove',
            start: start,
            end: end,
            value: oldValue
        });
    }
    /**
     * Set the ObservableString to an empty string.
     */
    clear() {
        this.text = '';
    }
    /**
     * Test whether the string has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the string.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
        this.clear();
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
;// CONCATENATED MODULE: ../packages/observables/lib/observablelist.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A concrete implementation of [[IObservableList]].
 */
class ObservableList {
    /**
     * Construct a new observable map.
     */
    constructor(options = {}) {
        this._array = [];
        this._isDisposed = false;
        this._changed = new dist_index_es6_js_.Signal(this);
        if (options.values) {
            for (const value of options.values) {
                this._array.push(value);
            }
        }
        this._itemCmp = options.itemCmp || observablelist_Private.itemCmp;
    }
    /**
     * The type of this object.
     */
    get type() {
        return 'List';
    }
    /**
     * A signal emitted when the list has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The length of the list.
     */
    get length() {
        return this._array.length;
    }
    /**
     * Test whether the list has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the list.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
        this.clear();
    }
    /**
     * Create an iterator over the values in the list.
     *
     * @returns A new iterator starting at the front of the list.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     */
    [Symbol.iterator]() {
        return this._array[Symbol.iterator]();
    }
    /**
     * Get the value at the specified index.
     *
     * @param index - The positive integer index of interest.
     *
     * @returns The value at the specified index.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral or out of range.
     */
    get(index) {
        return this._array[index];
    }
    /**
     * Set the value at the specified index.
     *
     * @param index - The positive integer index of interest.
     *
     * @param value - The value to set at the specified index.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral or out of range.
     */
    set(index, value) {
        const oldValue = this._array[index];
        if (value === undefined) {
            throw new Error('Cannot set an undefined item');
        }
        // Bail if the value does not change.
        const itemCmp = this._itemCmp;
        if (itemCmp(oldValue, value)) {
            return;
        }
        this._array[index] = value;
        this._changed.emit({
            type: 'set',
            oldIndex: index,
            newIndex: index,
            oldValues: [oldValue],
            newValues: [value]
        });
    }
    /**
     * Add a value to the end of the list.
     *
     * @param value - The value to add to the end of the list.
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Constant.
     *
     * #### Notes
     * By convention, the oldIndex is set to -1 to indicate
     * an push operation.
     *
     * #### Iterator Validity
     * No changes.
     */
    push(value) {
        const num = this._array.push(value);
        this._changed.emit({
            type: 'add',
            oldIndex: -1,
            newIndex: this.length - 1,
            oldValues: [],
            newValues: [value]
        });
        return num;
    }
    /**
     * Insert a value into the list at a specific index.
     *
     * @param index - The index at which to insert the value.
     *
     * @param value - The value to set at the specified index.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * The `index` will be clamped to the bounds of the list.
     *
     * By convention, the oldIndex is set to -2 to indicate
     * an insert operation.
     *
     * The value -2 as oldIndex can be used to distinguish from the push
     * method which will use a value -1.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral.
     */
    insert(index, value) {
        if (index === this._array.length) {
            this._array.push(value);
        }
        else {
            algorithm_dist_index_es6_js_.ArrayExt.insert(this._array, index, value);
        }
        this._changed.emit({
            type: 'add',
            oldIndex: -2,
            newIndex: index,
            oldValues: [],
            newValues: [value]
        });
    }
    /**
     * Remove the first occurrence of a value from the list.
     *
     * @param value - The value of interest.
     *
     * @returns The index of the removed value, or `-1` if the value
     *   is not contained in the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed value and beyond are invalidated.
     */
    removeValue(value) {
        const itemCmp = this._itemCmp;
        const index = algorithm_dist_index_es6_js_.ArrayExt.findFirstIndex(this._array, item => {
            return itemCmp(item, value);
        });
        this.remove(index);
        return index;
    }
    /**
     * Remove and return the value at a specific index.
     *
     * @param index - The index of the value of interest.
     *
     * @returns The value at the specified index, or `undefined` if the
     *   index is out of range.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed value and beyond are invalidated.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral.
     */
    remove(index) {
        const value = algorithm_dist_index_es6_js_.ArrayExt.removeAt(this._array, index);
        if (value === undefined) {
            return;
        }
        this._changed.emit({
            type: 'remove',
            oldIndex: index,
            newIndex: -1,
            newValues: [],
            oldValues: [value]
        });
        return value;
    }
    /**
     * Remove all values from the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * All current iterators are invalidated.
     */
    clear() {
        const copy = this._array.slice();
        this._array.length = 0;
        this._changed.emit({
            type: 'remove',
            oldIndex: 0,
            newIndex: 0,
            newValues: [],
            oldValues: copy
        });
    }
    /**
     * Move a value from one index to another.
     *
     * @param fromIndex - The index of the element to move.
     *
     * @param toIndex - The index to move the element to.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the lesser of the `fromIndex` and the `toIndex`
     * and beyond are invalidated.
     *
     * #### Undefined Behavior
     * A `fromIndex` or a `toIndex` which is non-integral.
     */
    move(fromIndex, toIndex) {
        if (this.length <= 1 || fromIndex === toIndex) {
            return;
        }
        const values = [this._array[fromIndex]];
        algorithm_dist_index_es6_js_.ArrayExt.move(this._array, fromIndex, toIndex);
        this._changed.emit({
            type: 'move',
            oldIndex: fromIndex,
            newIndex: toIndex,
            oldValues: values,
            newValues: values
        });
    }
    /**
     * Push a set of values to the back of the list.
     *
     * @param values - An iterable set of values to add.
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Notes
     * By convention, the oldIndex is set to -1 to indicate
     * an push operation.
     *
     * #### Iterator Validity
     * No changes.
     */
    pushAll(values) {
        const newIndex = this.length;
        for (const value of values) {
            this._array.push(value);
        }
        this._changed.emit({
            type: 'add',
            oldIndex: -1,
            newIndex,
            oldValues: [],
            newValues: Array.from(values)
        });
        return this.length;
    }
    /**
     * Insert a set of items into the list at the specified index.
     *
     * @param index - The index at which to insert the values.
     *
     * @param values - The values to insert at the specified index.
     *
     * #### Complexity.
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * The `index` will be clamped to the bounds of the list.
     * By convention, the oldIndex is set to -2 to indicate
     * an insert operation.
     *
     * #### Undefined Behavior.
     * An `index` which is non-integral.
     */
    insertAll(index, values) {
        const newIndex = index;
        for (const value of values) {
            algorithm_dist_index_es6_js_.ArrayExt.insert(this._array, index++, value);
        }
        this._changed.emit({
            type: 'add',
            oldIndex: -2,
            newIndex,
            oldValues: [],
            newValues: Array.from(values)
        });
    }
    /**
     * Remove a range of items from the list.
     *
     * @param startIndex - The start index of the range to remove (inclusive).
     *
     * @param endIndex - The end index of the range to remove (exclusive).
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * Iterators pointing to the first removed value and beyond are invalid.
     *
     * #### Undefined Behavior
     * A `startIndex` or `endIndex` which is non-integral.
     */
    removeRange(startIndex, endIndex) {
        const oldValues = this._array.slice(startIndex, endIndex);
        for (let i = startIndex; i < endIndex; i++) {
            algorithm_dist_index_es6_js_.ArrayExt.removeAt(this._array, startIndex);
        }
        this._changed.emit({
            type: 'remove',
            oldIndex: startIndex,
            newIndex: -1,
            oldValues,
            newValues: []
        });
        return this.length;
    }
}
/**
 * The namespace for module private data.
 */
var observablelist_Private;
(function (Private) {
    /**
     * The default strict equality item cmp.
     */
    function itemCmp(first, second) {
        return first === second;
    }
    Private.itemCmp = itemCmp;
})(observablelist_Private || (observablelist_Private = {}));

;// CONCATENATED MODULE: ../packages/observables/lib/undoablelist.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A concrete implementation of an observable undoable list.
 */
class ObservableUndoableList extends ObservableList {
    /**
     * Construct a new undoable observable list.
     */
    constructor(serializer) {
        super();
        this._inCompound = false;
        this._isUndoable = true;
        this._madeCompoundChange = false;
        this._index = -1;
        this._stack = [];
        this._serializer = serializer;
        this.changed.connect(this._onListChanged, this);
    }
    /**
     * Whether the object can redo changes.
     */
    get canRedo() {
        return this._index < this._stack.length - 1;
    }
    /**
     * Whether the object can undo changes.
     */
    get canUndo() {
        return this._index >= 0;
    }
    /**
     * Begin a compound operation.
     *
     * @param isUndoAble - Whether the operation is undoable.
     *   The default is `true`.
     */
    beginCompoundOperation(isUndoAble) {
        this._inCompound = true;
        this._isUndoable = isUndoAble !== false;
        this._madeCompoundChange = false;
    }
    /**
     * End a compound operation.
     */
    endCompoundOperation() {
        this._inCompound = false;
        this._isUndoable = true;
        if (this._madeCompoundChange) {
            this._index++;
        }
    }
    /**
     * Undo an operation.
     */
    undo() {
        if (!this.canUndo) {
            return;
        }
        const changes = this._stack[this._index];
        this._isUndoable = false;
        for (const change of changes.reverse()) {
            this._undoChange(change);
        }
        this._isUndoable = true;
        this._index--;
    }
    /**
     * Redo an operation.
     */
    redo() {
        if (!this.canRedo) {
            return;
        }
        this._index++;
        const changes = this._stack[this._index];
        this._isUndoable = false;
        for (const change of changes) {
            this._redoChange(change);
        }
        this._isUndoable = true;
    }
    /**
     * Clear the change stack.
     */
    clearUndo() {
        this._index = -1;
        this._stack = [];
    }
    /**
     * Handle a change in the list.
     */
    _onListChanged(list, change) {
        if (this.isDisposed || !this._isUndoable) {
            return;
        }
        // Clear everything after this position if necessary.
        if (!this._inCompound || !this._madeCompoundChange) {
            this._stack = this._stack.slice(0, this._index + 1);
        }
        // Copy the change.
        const evt = this._copyChange(change);
        // Put the change in the stack.
        if (this._stack[this._index + 1]) {
            this._stack[this._index + 1].push(evt);
        }
        else {
            this._stack.push([evt]);
        }
        // If not in a compound operation, increase index.
        if (!this._inCompound) {
            this._index++;
        }
        else {
            this._madeCompoundChange = true;
        }
    }
    /**
     * Undo a change event.
     */
    _undoChange(change) {
        let index = 0;
        const serializer = this._serializer;
        switch (change.type) {
            case 'add':
                for (let length = change.newValues.length; length > 0; length--) {
                    this.remove(change.newIndex);
                }
                break;
            case 'set':
                index = change.oldIndex;
                for (const value of change.oldValues) {
                    this.set(index++, serializer.fromJSON(value));
                }
                break;
            case 'remove':
                index = change.oldIndex;
                for (const value of change.oldValues) {
                    this.insert(index++, serializer.fromJSON(value));
                }
                break;
            case 'move':
                this.move(change.newIndex, change.oldIndex);
                break;
            default:
                return;
        }
    }
    /**
     * Redo a change event.
     */
    _redoChange(change) {
        let index = 0;
        const serializer = this._serializer;
        switch (change.type) {
            case 'add':
                index = change.newIndex;
                for (const value of change.newValues) {
                    this.insert(index++, serializer.fromJSON(value));
                }
                break;
            case 'set':
                index = change.newIndex;
                for (const value of change.newValues) {
                    this.set(change.newIndex++, serializer.fromJSON(value));
                }
                break;
            case 'remove':
                for (let length = change.oldValues.length; length > 0; length--) {
                    this.remove(change.oldIndex);
                }
                break;
            case 'move':
                this.move(change.oldIndex, change.newIndex);
                break;
            default:
                return;
        }
    }
    /**
     * Copy a change as JSON.
     */
    _copyChange(change) {
        const oldValues = [];
        for (const value of change.oldValues) {
            oldValues.push(this._serializer.toJSON(value));
        }
        const newValues = [];
        for (const value of change.newValues) {
            newValues.push(this._serializer.toJSON(value));
        }
        return {
            type: change.type,
            oldIndex: change.oldIndex,
            newIndex: change.newIndex,
            oldValues,
            newValues
        };
    }
}
/**
 * Namespace for ObservableUndoableList utilities.
 */
(function (ObservableUndoableList) {
    /**
     * A default, identity serializer.
     */
    class IdentitySerializer {
        /**
         * Identity serialize.
         */
        toJSON(value) {
            return value;
        }
        /**
         * Identity deserialize.
         */
        fromJSON(value) {
            return value;
        }
    }
    ObservableUndoableList.IdentitySerializer = IdentitySerializer;
})(ObservableUndoableList || (ObservableUndoableList = {}));

;// CONCATENATED MODULE: ../packages/observables/lib/modeldb.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * A concrete implementation of an `IObservableValue`.
 */
class ObservableValue {
    /**
     * Constructor for the value.
     *
     * @param initialValue: the starting value for the `ObservableValue`.
     */
    constructor(initialValue = null) {
        this._value = null;
        this._changed = new dist_index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._value = initialValue;
    }
    /**
     * The observable type.
     */
    get type() {
        return 'Value';
    }
    /**
     * Whether the value has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * The changed signal.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Get the current value, or `undefined` if it has not been set.
     */
    get() {
        return this._value;
    }
    /**
     * Set the current value.
     */
    set(value) {
        const oldValue = this._value;
        if (index_js_.JSONExt.deepEqual(oldValue, value)) {
            return;
        }
        this._value = value;
        this._changed.emit({
            oldValue: oldValue,
            newValue: value
        });
    }
    /**
     * Dispose of the resources held by the value.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
        this._value = null;
    }
}
/**
 * The namespace for the `ObservableValue` class statics.
 */
(function (ObservableValue) {
    /**
     * The changed args object emitted by the `IObservableValue`.
     */
    class IChangedArgs {
    }
    ObservableValue.IChangedArgs = IChangedArgs;
})(ObservableValue || (ObservableValue = {}));
/**
 * A concrete implementation of an `IModelDB`.
 */
class ModelDB {
    /**
     * Constructor for the `ModelDB`.
     */
    constructor(options = {}) {
        /**
         * Whether the model has been populated with
         * any model values.
         */
        this.isPrepopulated = false;
        /**
         * Whether the model is collaborative.
         */
        this.isCollaborative = false;
        /**
         * A promise resolved when the model is connected
         * to its backend. For the in-memory ModelDB it
         * is immediately resolved.
         */
        this.connected = Promise.resolve(void 0);
        this._toDispose = false;
        this._isDisposed = false;
        this._disposables = new index_es6_js_.DisposableSet();
        this._basePath = options.basePath || '';
        if (options.baseDB) {
            this._db = options.baseDB;
        }
        else {
            this._db = new ObservableMap();
            this._toDispose = true;
        }
    }
    /**
     * The base path for the `ModelDB`. This is prepended
     * to all the paths that are passed in to the member
     * functions of the object.
     */
    get basePath() {
        return this._basePath;
    }
    /**
     * Whether the database is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Get a value for a path.
     *
     * @param path: the path for the object.
     *
     * @returns an `IObservable`.
     */
    get(path) {
        return this._db.get(this._resolvePath(path));
    }
    /**
     * Whether the `IModelDB` has an object at this path.
     *
     * @param path: the path for the object.
     *
     * @returns a boolean for whether an object is at `path`.
     */
    has(path) {
        return this._db.has(this._resolvePath(path));
    }
    /**
     * Create a string and insert it in the database.
     *
     * @param path: the path for the string.
     *
     * @returns the string that was created.
     */
    createString(path) {
        const str = new ObservableString();
        this._disposables.add(str);
        this.set(path, str);
        return str;
    }
    /**
     * Create an undoable list and insert it in the database.
     *
     * @param path: the path for the list.
     *
     * @returns the list that was created.
     *
     * #### Notes
     * The list can only store objects that are simple
     * JSON Objects and primitives.
     */
    createList(path) {
        const vec = new ObservableUndoableList(new ObservableUndoableList.IdentitySerializer());
        this._disposables.add(vec);
        this.set(path, vec);
        return vec;
    }
    /**
     * Create a map and insert it in the database.
     *
     * @param path: the path for the map.
     *
     * @returns the map that was created.
     *
     * #### Notes
     * The map can only store objects that are simple
     * JSON Objects and primitives.
     */
    createMap(path) {
        const map = new ObservableJSON();
        this._disposables.add(map);
        this.set(path, map);
        return map;
    }
    /**
     * Create an opaque value and insert it in the database.
     *
     * @param path: the path for the value.
     *
     * @returns the value that was created.
     */
    createValue(path) {
        const val = new ObservableValue();
        this._disposables.add(val);
        this.set(path, val);
        return val;
    }
    /**
     * Get a value at a path, or `undefined if it has not been set
     * That value must already have been created using `createValue`.
     *
     * @param path: the path for the value.
     */
    getValue(path) {
        const val = this.get(path);
        if (!val || val.type !== 'Value') {
            throw Error('Can only call getValue for an ObservableValue');
        }
        return val.get();
    }
    /**
     * Set a value at a path. That value must already have
     * been created using `createValue`.
     *
     * @param path: the path for the value.
     *
     * @param value: the new value.
     */
    setValue(path, value) {
        const val = this.get(path);
        if (!val || val.type !== 'Value') {
            throw Error('Can only call setValue on an ObservableValue');
        }
        val.set(value);
    }
    /**
     * Create a view onto a subtree of the model database.
     *
     * @param basePath: the path for the root of the subtree.
     *
     * @returns an `IModelDB` with a view onto the original
     *   `IModelDB`, with `basePath` prepended to all paths.
     */
    view(basePath) {
        const view = new ModelDB({ basePath, baseDB: this });
        this._disposables.add(view);
        return view;
    }
    /**
     * Set a value at a path. Not intended to
     * be called by user code, instead use the
     * `create*` factory methods.
     *
     * @param path: the path to set the value at.
     *
     * @param value: the value to set at the path.
     */
    set(path, value) {
        this._db.set(this._resolvePath(path), value);
    }
    /**
     * Dispose of the resources held by the database.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        if (this._toDispose) {
            this._db.dispose();
        }
        this._disposables.dispose();
    }
    /**
     * Compute the fully resolved path for a path argument.
     */
    _resolvePath(path) {
        if (this._basePath) {
            path = this._basePath + '.' + path;
        }
        return path;
    }
}

;// CONCATENATED MODULE: ../packages/observables/lib/index.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module observables
 */








/***/ })

}]);
//# sourceMappingURL=397.b23687a8eddee06ca1b7.js.map?v=b23687a8eddee06ca1b7