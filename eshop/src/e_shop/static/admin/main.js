var utility = angular.module('utility', []);

if (!String.prototype.format) {
	String.prototype.format = function() {
		var fmt = this;
		var params = Array.prototype.slice.call(arguments);
		return fmt.replace(/(\{(\d+)\})/g, function(match, firstCap, index) {
			return params[index] || match;
		});
	};
}

var oldTrim = String.prototype.trim;
String.prototype.trim = function(c) {
	if (!c) {
		if (oldTrim) return oldTrim.call(this);
		else c = '\\s';
	}
	return this.replace(new RegExp('^'+c+'+', 'g'), function() {
			return '';
		}).replace(new RegExp(c+'+$', 'g'), function() {
			return '';
		});
};

utility.config(['$httpProvider', function($httpProvider) {
	$httpProvider.interceptors.push(function() {
		return {
			'response': function(response) {
				if (response.data && response.data.data) 
					response.data.data = angular.fromJson(response.data.data);
				return response;
			}
		};
	});
}]);

utility.factory('utility', function() {
	function _queryParams(obj) {
		var result = [];
		function _internal(prefix, obj) {
			angular.forEach(Object.getOwnPropertyNames(obj), function(prop) {
				if (angular.isObject(obj[prop])) {
					_internal(prop+'.', obj[prop]);
				} else {
					result.push(encodeURIComponent(prefix+prop) + '=' + encodeURIComponent(obj[prop]));
				}
			});
		}
		_internal('', obj);
		return result.join('&');
	}
	return {
		queryParams: function(obj) {
			var params = _queryParams(obj);
			if (params) return '?'+params;
			return '';
		}
	};
});

utility.factory('_', function() {
	return window._;
});

utility.factory('moment', function() {
	return window.moment;
});

utility.factory('history', function() {
	return window.history;
});

utility.factory('ajax', ['$http', function($http) {
	$http.defaults.headers.common['X-CSRFTOKEN'] = $('[name="csrfmiddlewaretoken"]').val();
	$http.defaults.headers.common.Authorization = 'Bearer '+window.access_token;
	return {
		get: function (url, param) {
			return $http.get(url, {
				params: param
			});
		},
		post: function (url, param) {
			return $http.post(url, param);
		},
		delete: function (url, param) {
			return $http.post(url, param);
		},
		save: function (url, param) {
			return $http.post(url, param);
		}
	};
}]);

utility.factory('enums', ['_', function() {
	return {
		fieldType: {
			string: {
				value: 0,
				desp: '字符串'
			},
			decimal: {
				value: 2,
				desp: '数字'
			},
			singleOptions: {
				value: 3,
				desp: '单选择项'
			},
			multipleOptions: {
				value: 4,
				desp: '多选择项'
			}
		},
		getDataSource: function(e) {
			return _.map(Object.getOwnPropertyNames(e), function(eName) {
				return {
					id: e[eName].value,
					text: e[eName].desp
				};
			});
		}
	};
}]);
