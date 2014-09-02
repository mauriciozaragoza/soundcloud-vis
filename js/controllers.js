angular.module('SoundApp.controllers', []).
controller('SoundControllers', ['$scope', '$http', '$sce', function($scope, $http, $sce) {
	$http.defaults.useXDomain = true;
	
	$scope.nSongs = 5;

	$scope.getSongs = function() {
		$http.get("http://127.0.0.1:9000", {
		    params: { 
		    	n: $scope.nSongs,
				genre: $scope.genre
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

