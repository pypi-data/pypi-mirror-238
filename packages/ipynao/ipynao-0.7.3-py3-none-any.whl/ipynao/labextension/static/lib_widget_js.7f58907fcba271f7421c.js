(self["webpackChunkipynao"] = self["webpackChunkipynao"] || []).push([["lib_widget_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  color: var(--jp-widgets-color) !important;\n  font-family: monospace;\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./lib/qimessaging.js":
/*!****************************!*\
  !*** ./lib/qimessaging.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.QiSession = void 0;
/*
 **  Copyright (C) Aldebaran Robotics
 **  See COPYING for the license
 **
 **  Author(s):
 **   - Laurent LEC    <llec@aldebaran-robotics.com>
 **
 */
const nao_socket_io_1 = __importDefault(__webpack_require__(/*! nao-socket.io */ "webpack/sharing/consume/default/nao-socket.io/nao-socket.io"));
class QiSession {
    constructor(ipAddress = 'nao.local', port = '80', connected, disconnected) {
        this.connected = connected;
        this.disconnected = disconnected;
        this._socket = nao_socket_io_1.default.connect('nao:nao@' + ipAddress + ':' + port, {
            resource: 'libs/qimessaging/2/socket.io',
            'force new connection': true,
        });
        this._dfd = [];
        this._sigs = [];
        this._idm = 0;
        this._socket.on('reply', (data) => {
            this.onReply(data);
        });
        this._socket.on('error', (data) => {
            this.onError(data);
        });
        this._socket.on('signal', (data) => {
            this.onSignal(data);
        });
        this._socket.on('disconnect', this.onDisconnect);
        this._socket.on('connect', this.onConnect);
        this.service = this.createMetaCall('ServiceDirectory', 'service', 'data');
    }
    isConnected() {
        const connected = this._socket !== undefined ? this._socket.socket.connected : false;
        return connected;
    }
    disconnect() {
        this._socket.disconnect();
    }
    onReply(data) {
        const idm = data['idm'];
        if (data['result'] !== undefined &&
            data['result']['metaobject'] !== undefined) {
            const replyObject = {
                __MetaObject: data['result']['metaobject'],
            };
            const pyIndex = data['result']['pyobject'];
            this._sigs[pyIndex] = [];
            const methods = replyObject.__MetaObject['methods'];
            for (const i in methods) {
                const methodName = methods[i]['name'];
                replyObject[methodName] = this.createMetaCall(pyIndex, methodName, 'data');
            }
            const signals = replyObject.__MetaObject['signals'];
            for (const i in signals) {
                const signalName = signals[i]['name'];
                replyObject[signalName] = this.createMetaSignal(pyIndex, signalName, false);
            }
            const properties = replyObject.__MetaObject['properties'];
            for (const i in properties) {
                const propertyName = properties[i]['name'];
                replyObject[propertyName] = this.createMetaSignal(pyIndex, propertyName, true);
            }
            this._dfd[idm].resolve(replyObject);
        }
        else {
            if (this._dfd[idm].__cbi !== undefined) {
                const cbi = this._dfd[idm].__cbi;
                this._sigs[cbi['obj']][cbi['signal']][data['result']] = cbi['cb'];
            }
            this._dfd[idm].resolve(data['result']);
        }
        delete this._dfd[idm];
    }
    onError(data) {
        if (data['idm'] !== undefined) {
            this._dfd[data['idm']].reject(data['result']);
            delete this._dfd[data['idm']];
        }
    }
    onSignal(data) {
        const result = data['result'];
        const callback = this._sigs[result['obj']][result['signal']][result['link']];
        if (callback !== undefined) {
            callback.apply(this, result['data']);
        }
    }
    onConnect() {
        if (this.connected) {
            this.connected(this);
        }
    }
    onDisconnect(_data) {
        for (const idm in this._dfd) {
            this._dfd[idm].reject('Call ' + idm + ' canceled: disconnected');
            delete this._dfd[idm];
        }
        if (this.disconnected) {
            this.disconnected();
        }
    }
    createMetaCall(obj, member, data) {
        return (...serviceArgs) => {
            ++this._idm;
            const promise = new Promise((resolve, reject) => {
                this._dfd[this._idm] = { resolve: resolve, reject: reject };
            });
            if (serviceArgs[0] === 'connect') {
                this.isConnected = this._socket.socket.connected;
                this._dfd[this._idm].__cbi = data;
            }
            this._socket.emit('call', {
                idm: this._idm,
                params: { obj: obj, member: member, args: serviceArgs },
            });
            return promise;
        };
    }
    createMetaSignal(obj, signal, isProperty) {
        const signalObject = {};
        this._sigs[obj][signal] = [];
        signalObject.connect = (cb) => {
            return this.createMetaCall(obj, signal, {
                obj: obj,
                signal: signal,
                cb: cb,
            })('connect');
        };
        signalObject.disconnect = (args) => {
            delete this._sigs[obj][signal][args];
            return this.createMetaCall(obj, signal, 'data')('disconnect', args);
        };
        if (!isProperty) {
            return signalObject;
        }
        signalObject.setValue = (...valueArgs) => {
            return this.createMetaCall(obj, signal, 'data').apply(this, ['setValue'].concat(valueArgs));
        };
        signalObject.value = () => {
            return this.createMetaCall(obj, signal, 'data')('value');
        };
        return signalObject;
    }
}
exports.QiSession = QiSession;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Isabel Paredes
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Isabel Paredes
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.NaoRobotView = exports.NaoRobotModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const qimessaging_1 = __webpack_require__(/*! ./qimessaging */ "./lib/qimessaging.js");
class NaoRobotModel extends base_1.DOMWidgetModel {
    constructor() {
        super(...arguments);
        this.connected = 'Disconnected';
        this.status = 'Not busy';
        this._services = {};
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: NaoRobotModel.model_name, _model_module: NaoRobotModel.model_module, _model_module_version: NaoRobotModel.model_module_version, _view_name: NaoRobotModel.view_name, _view_module: NaoRobotModel.view_module, _view_module_version: NaoRobotModel.view_module_version, connected: 'Disconnected', status: 'Not busy', counter: 0 });
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.on('msg:custom', this.onCommand);
    }
    changeStatus(statusMessage) {
        this.status = statusMessage;
        this.set('status', statusMessage);
        this.save_changes();
    }
    validateIPaddress(ipAddress) {
        // TODO: validate port also
        if (ipAddress.endsWith('.local')) {
            return true;
        }
        else {
            const regexp = new RegExp('^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(.(?!$)|$)){4}$');
            return regexp.test(ipAddress);
        }
    }
    connect(ipAddress, port, requestID) {
        return __awaiter(this, void 0, void 0, function* () {
            const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
            this.changeStatus('Establishing connection');
            if (!ipAddress) {
                // Use the IP address/domain name of the current page
                ipAddress = window.location.hostname;
                // Note: we don't validate this
            }
            else if (!this.validateIPaddress(ipAddress)) {
                this.changeStatus('Invalid IP address');
                console.warn('IP Address ', ipAddress, ' is not valid');
                return;
            }
            this._ipAddress = ipAddress;
            this._port = port;
            this.qiSession = new qimessaging_1.QiSession(ipAddress, port);
            // Timeout after ~10 seconds
            for (let i = 0; i < 100; i++) {
                if (this.qiSession.isConnected()) {
                    this.connected = 'Connected';
                    this.set('connected', 'Connected');
                    this.save_changes();
                    this.changeStatus('Available');
                    console.log('Connection successful after ', i / 10.0, ' seconds.');
                    break;
                }
                yield sleep(100);
            }
            // Handle connection failure
            if (!this.qiSession.isConnected()) {
                this.disconnect();
                console.error('Connection to ', ipAddress, ' could not be established.');
                this.changeStatus('Connection to ' + ipAddress + ' could not be established.');
            }
        });
    }
    disconnect() {
        if (this.qiSession && this.qiSession.isConnected()) {
            this.qiSession.disconnect();
        }
        this._services = {};
        this.set('connected', 'Disconnected');
        this.save_changes();
        this.changeStatus('Unavailable');
    }
    checkConnection(requestID) {
        return __awaiter(this, void 0, void 0, function* () {
            // Cannot reconnect without initial connection
            if (!this._ipAddress) {
                this.send({
                    isError: true,
                    data: 'Cannot connect without IP Address.',
                    requestID: requestID,
                });
                this.set('counter', this.get('counter') + 1);
                this.save_changes();
                return false;
            }
            // Reconnect if possible
            if (!this.qiSession.isConnected()) {
                this.disconnect();
                yield this.connect(this._ipAddress, this._port, requestID);
            }
            return true;
        });
    }
    createService(serviceName, requestID) {
        return __awaiter(this, void 0, void 0, function* () {
            const isConnected = yield this.checkConnection(requestID);
            if (!isConnected) {
                return;
            }
            // Skip if service exists already
            if (this._services[serviceName]) {
                console.log('Service ' + serviceName + ' exists.');
                return;
            }
            this.changeStatus('Creating service ' + serviceName);
            const servicePromise = this.qiSession.service(serviceName);
            // TODO: This func is not async in the kernel. To show error messages
            // the request ID is the next one which is used to call the service
            const naoService = yield servicePromise
                .then((resolution) => {
                return resolution;
            })
                .catch((rejection) => {
                this.changeStatus(rejection);
                this.send({
                    isError: true,
                    data: rejection,
                    requestID: requestID + 1,
                });
                this.set('counter', this.get('counter') + 1);
                this.save_changes();
                return rejection;
            });
            // Store service only when successfully created
            if (typeof naoService === 'object') {
                this._services[serviceName] = naoService;
                this.changeStatus(serviceName + ' available');
            }
        });
    }
    callService(serviceName, methodName, args, _kwargs, requestID) {
        return __awaiter(this, void 0, void 0, function* () {
            const isConnected = yield this.checkConnection(requestID);
            if (!isConnected) {
                return;
            }
            // Wait for service to become available
            const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
            this.changeStatus('Waiting for service ' + serviceName);
            // Timeout after ~10 seconds
            for (let i = 0; i < 100; i++) {
                if (this._services[serviceName]) {
                    console.log('Service available after ', i / 10.0, ' seconds.');
                    this.changeStatus(serviceName + ' available');
                    break;
                }
                yield sleep(100);
            }
            if (!this._services[serviceName]) {
                this.changeStatus(serviceName + ' not available');
                this.send({
                    isError: true,
                    data: serviceName + ' not available',
                    requestID: requestID,
                });
                this.set('counter', this.get('counter') + 1);
                this.save_changes();
                return;
            }
            if (!this._services[serviceName][methodName]) {
                this.changeStatus(`${methodName} does not exist for ${serviceName}`);
                this.send({
                    isError: true,
                    data: `${methodName} does not exist for ${serviceName}`,
                    requestID: requestID,
                });
                this.set('counter', this.get('counter') + 1);
                this.save_changes();
                return;
            }
            this.changeStatus('Running method ' + methodName);
            const servicePromise = this._services[serviceName][methodName](...args);
            yield servicePromise
                .then((resolution) => {
                this.changeStatus('Task completed');
                this.send({
                    isError: false,
                    data: resolution !== null && resolution !== void 0 ? resolution : true,
                    requestID: requestID,
                });
            })
                .catch((rejection) => {
                this.changeStatus(rejection);
                this.send({
                    isError: true,
                    data: rejection,
                    requestID: requestID,
                });
            });
            this.set('counter', this.get('counter') + 1);
            this.save_changes();
        });
    }
    onCommand(commandData, buffers) {
        return __awaiter(this, void 0, void 0, function* () {
            const cmd = commandData['command'];
            switch (cmd) {
                case 'connect':
                    yield this.connect(commandData['ipAddress'], commandData['port'], commandData['requestID']);
                    break;
                case 'disconnect':
                    this.disconnect();
                    break;
                case 'createService':
                    yield this.createService(commandData['service'], commandData['requestID']);
                    break;
                case 'callService':
                    yield this.callService(commandData['service'], commandData['method'], commandData['args'], commandData['kwargs'], commandData['requestID']);
                    break;
            }
        });
    }
}
exports.NaoRobotModel = NaoRobotModel;
NaoRobotModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
NaoRobotModel.model_name = 'NaoRobotModel';
NaoRobotModel.model_module = version_1.MODULE_NAME;
NaoRobotModel.model_module_version = version_1.MODULE_VERSION;
NaoRobotModel.view_name = 'NaoRobotView'; // Set to null if no view
NaoRobotModel.view_module = version_1.MODULE_NAME; // Set to null if no view
NaoRobotModel.view_module_version = version_1.MODULE_VERSION;
class NaoRobotView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget');
        // Connection element
        this.txt_connected = document.createElement('div');
        this.txt_connected.textContent = 'Disconnected';
        this.el.appendChild(this.txt_connected);
        // Status element
        this.txt_status = document.createElement('div');
        this.txt_status.textContent = 'Not busy';
        this.el.appendChild(this.txt_status);
        this.value_changed();
        this.model.on('change:connected', this.value_changed, this);
        this.model.on('change:status', this.value_changed, this);
    }
    value_changed() {
        this.txt_connected.textContent = this.model.get('connected');
        this.txt_status.textContent = this.model.get('status');
    }
}
exports.NaoRobotView = NaoRobotView;


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ipynao","version":"0.7.3","description":"A widget library for controlling Nao","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/jupyter-robotics/ipynao","bugs":{"url":"https://github.com/jupyter-robotics/ipynao/issues"},"license":"BSD-3-Clause","author":{"name":"Isabel Paredes","email":"isabel.paredes@quantstack.net"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/jupyter-robotics/ipynao"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack --mode=production","build:nbextension:dev":"webpack --mode=development","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipynao/labextension","clean:nbextension":"rimraf ipynao/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","nao-socket.io":"1.0.5"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipynao/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.7f58907fcba271f7421c.js.map