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

utility.factory('ajax', ['$http', function($http) {
	return {
		get: function (url, param) {
			return $http.get(url, {
				params: param,
				xsrfHeaderName: 'X-CSRFToken',
				xsrfCookieName: 'csrftoken'
			});
		},
		post: function (url, param) {
			return $http.post(url, param, {
				xsrfHeaderName: 'X-CSRFToken',
				xsrfCookieName: 'csrftoken'
			});
		},
		delete: function (url, param) {
			return $http.post(url, param, {
				xsrfHeaderName: 'X-CSRFToken',
				xsrfCookieName: 'csrftoken'
			});
		},
		save: function (url, param) {
			return $http.post(url, param, {
				xsrfHeaderName: 'X-CSRFToken',
				xsrfCookieName: 'csrftoken'
			});
		}
	};
}]);
