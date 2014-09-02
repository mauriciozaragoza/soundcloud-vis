angular.module('SoundApp.controllers', []).
controller('SoundControllers', ['$scope', '$http', function($scope, $http) {
	$http.defaults.useXDomain = true;
	
	$http.get("http://127.0.0.1:9000", {
	// $http.get("http://10.43.3.33:9000", {
	    params: { 
	    	n: 10
	    }
	}).success(function(data) {
		var fill = d3.scale.category20();

		var d = data.map(function(d) {
				return {text: d.name, size: d.duration};
			});

		d3.layout.cloud().size([300, 300])
			.words(d)
			.padding(5)
			.rotate(function() { return ~~(Math.random() * 2) * 90; })
			.font("Impact")
			.fontSize(function(d) { return d.size; })
			.on("end", draw)
			.start();

		function draw(words) {
			d3.select("body").append("svg")
				.attr("width", 300)
				.attr("height", 300)
				.append("g")
				.attr("transform", "translate(150,150)")
				.selectAll("text")
				.data(words)
				.enter().append("text")
				.style("font-size", function(d) { return d.size + "px"; })
				.style("font-family", "Impact")
				.style("fill", function(d, i) { return fill(i); })
				.attr("text-anchor", "middle")
				.attr("transform", function(d) {
			 		return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
				})
				.text(function(d) { return d.text; });
		}
	})

	$scope.range = function(n) {
        return new Array(parseInt(n));
    };
}]);