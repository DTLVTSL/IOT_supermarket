app.controller('AddController', ['$scope', '$firebaseArray', '$location', function($scope, $firebaseArray, $location){
		var products = new Firebase("https://smarkt-bac7b.firebaseio.com/sales/foo/lista/produtos");
		var prices = new Firebase("https://smarkt-bac7b.firebaseio.com/sales/foo/lista");
		$scope.products = $firebaseArray(products);
		$scope.prices = $firebaseArray(prices);
		$scope.addProduct = function() {
		var ref = new Firebase("https://smarkt-bac7b.firebaseio.com/sales/foo/lista/timeconf");
		ref.set({timeconf:Date.now()});
		
	};
	
}]);



