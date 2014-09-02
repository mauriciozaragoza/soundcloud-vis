angular.module('SoundApp.controllers', []).
controller('SoundControllers', ['$scope', '$http', '$sce', function($scope, $http, $sce) {
	$http.defaults.useXDomain = true;
	
	$scope.getSongs = function() {
		$http.get("http://127.0.0.1:9000", {
		    params: { 
		    	n: 5
		    }
		}).success(function(data) {
			$scope.tracks = data;
		})
	};

	$scope.getSongs();

	$scope.range = function(n) {
        return new Array(parseInt(n));
    };
}]);