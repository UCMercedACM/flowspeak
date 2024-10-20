// See https://github.com/parse-community/Parse-SDK-JS/issues/936#issuecomment-538339659
import EventEmitter from  "react-native/Libraries/vendor/emitter/EventEmitter";
//var EventEmitter = require('../../../react-native/Libraries/vendor/emitter/EventEmitter');
EventEmitter.defaultMaxListeners = 40;
let Event = new EventEmitter();

export default Event;
