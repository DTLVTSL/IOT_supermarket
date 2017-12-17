app.controller('EditController', ['$scope','$location', '$routeParams', '$firebaseObject', '$firebaseArray',
    function($scope,$location,$routeParams, $firebaseObject,$firebaseArray){
	var ref = new Firebase("https://smarkt-bac7b.firebaseio.com/sales/foo/lista/produtos/"+Date.now());
	var newObj = {prod: $routeParams.id}; 
	ref.set(newObj);
	
	
		$scope.product = $firebaseObject(ref);
    $scope.editProduct = function() {
        $scope.product.$save({
            qty: $scope.product.Quantity
            
        });
        $scope.edit_form.$setPristine();
        $scope.product = {};
        $location.path('/');
        
    };
     
}]);
