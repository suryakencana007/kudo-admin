(function(window, $, Class) {
	'use strict';

  // Cache frequently used object
  var document = window.document,
  location = window.location;

  // Create a namespace
  // To add a ns property to the object when you created. It assumed to be used to prefix such as a key name.
  // ns('foo.bar')
  // typeof foo.bar === 'object' // true
  // foo.bar.ns // "fooBar"
  //
  // Namespace you want to create
  // option. Object that you want to set to the name space (and function. Deprecated).
  //       Already exists object, value in the case was also object to extend.
  //			 If is not an object returns an exception (note that the value is in the case was a function would fall into this condition).
  var ns = function(ns, value) {
  	var path = ns.split('.'),
  	obj = window,
  	i, l, prop, last;
  	for (i = 0, l = path.length; i < l; ++i) {
  		prop = path[i];
  		last = i === l - 1;
  		if (obj[prop] === undefined) {
  			obj[prop] = last && value ? value : {};
  		} else {
        if ($.type(obj[prop]) !== 'object') throw new Error(prop + ' is not object.'); // Not acceptable because the complexity and dig than the object (function object)
        if (last && value) {
        	if ($.type(value) === 'object') {
        		$.extend(true, obj[prop], value);
        	} else throw new Error(value + ' value cannot extend.'); // Tell can not extend the exception object
        }
      }
      obj = obj[prop];
    }
    obj.ns || (obj.ns = ns.toLowerCase().replace(/\.(\w)/g, function(_, $1) {
    	return $1.toUpperCase();
    }));
     return obj;
  };

  ns('baka', {
  	w: $(window),
  	d: $(document),
  	h: $('html'),
  	ua: {}, // for navigator
  	ns: ns
  });

  // And outputs a log to the console
  (function() {
  	var supported = !!window.console;
  	baka.log = supported ?
  	function() {
  		if (!arguments.length) return;
  		var args = $.makeArray(arguments);
  		args.unshift(new Date().toTimeString().slice(0, 8));
  		'apply' in console.log ?
  		console.log.apply(console, args) :
  		console.dir ?
  		console.dir(args) :
  		console.log(args);
  	} :
  	function() {
  		if (!arguments.length) return;
  		var args = $.makeArray(arguments);
  		args.unshift(new Date().toTimeString().slice(0, 8));
  		$('#console').append(args.join(' '));
  	};
    // For no console.log browser
    supported || (window.console = {
    	log: function() {}
    });

    // whitecube baka.logger compatibility
    var makeLogFunc = function(level, name) {
    	var prefix = level + ' [' + name + ']';
    	return function() {
    		if (!arguments.length) return;
    		var args = $.makeArray(arguments);
    		args.unshift(prefix);
    	};
    };
    var makeLogger = function(name) {
    	return {
    		setDefaultLevel: function() {},
    		trace: makeLogFunc('trace', name),
    		debug: makeLogFunc('debug', name),
    		info: makeLogFunc('info', name),
    		warn: makeLogFunc('warn', name),
    		error: makeLogFunc('error', name)
    	};
    };
    baka.logger = function(name) {
    	if (!baka.logger.loggers[name]) {
    		baka.logger.loggers[name] = makeLogger(name);
    	}
    	return baka.logger.loggers[name];
    };
    baka.logger.loggers = {};
  })();
})(window, jQuery, Class);