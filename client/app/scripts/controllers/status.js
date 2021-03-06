GLClient.controller('StatusCtrl',
  ['$scope', '$rootScope', '$location', '$route', '$routeParams', '$modal', '$http', 'Authentication', 'Tip', 'WBTip', 'ReceiverPreferences',
  function($scope, $rootScope, $location, $route, $routeParams, $modal, $http, Authentication, Tip, WBTip, ReceiverPreferences) {

    $scope.tip_id = $routeParams.tip_id;
    $scope.session = Authentication.id;
    $scope.target_file = '#';

    $scope.uploads = {};
    $scope.hideUploadWhenFinished = true;

    $scope.showEditLabelInput = false;

    $scope.getFields = function(field) {
      var ret = [];
      var fields;
      if (field === undefined) {
        fields = $scope.tip.fields;
      } else {
        fields = field.children;
      }

      angular.forEach(fields, function(field, k) {
        ret.push(field);
      });

      return ret;
    };

    $scope.hasMultipleEntries = function(field_answer) {
      if (field_answer !== undefined) {
        return field_answer.length > 1;
      }

      return false;
    }

    $scope.filterFields = function(field) {
      return field.type !== 'fileupload';
    };

    $scope.filterReceivers = function(receiver) {
      return receiver.configuration !== 'hidden';
    };

    if (Authentication.role === 'wb') {
      $scope.fileupload_url = '/wbtip/upload';

      $scope.tip = new WBTip(function(tip) {

        $scope.tip = tip;

        angular.forEach($scope.contexts, function(context, k){
          if (context.id === tip.context_id) {
            $scope.current_context = context;
          }
        });

        if (tip.receivers.length === 1 && tip.msg_receiver_selected === null) {
          tip.msg_receiver_selected = tip.msg_receivers_selector[0].key;
        }

        tip.updateMessages();

        $scope.$watch('tip.msg_receiver_selected', function (newVal, oldVal) {
          if (newVal && newVal !== oldVal) {
            if ($scope.tip) {
              $scope.tip.updateMessages();
            }
          }
        }, false);

      });

    } else if (Authentication.role === 'receiver') {
      $scope.preferences = ReceiverPreferences.get();
    
      var TipID = {tip_id: $scope.tip_id};
      $scope.tip = new Tip(TipID, function(tip) {

        $scope.tip = tip;

        $scope.showEditLabelInput = $scope.tip.label == '';

        $scope.tip_unencrypted = false;
        angular.forEach(tip.receivers, function(receiver){
          if (receiver.pgp_key_status === 'disabled' && receiver.receiver_id !== tip.receiver_id) {
            $scope.tip_unencrypted = true;
          }
        });

        angular.forEach($scope.contexts, function(context, k){
          if (context.id === $scope.tip.context_id) {
            $scope.current_context = context;
          }
        });

      });
    } else {
      if($location.path() === '/status') {
        // wb
        $location.path('/');
      } else {
        // receiver
        var search = 'src=' + $location.path();
        $location.path('/login');
        $location.search(search);
      }
    }

    $scope.editLabel = function(event) {
      $scope.showEditLabelInput = true;
      event.stopPropagation();
    }

    $scope.updateLabel = function(event, label) {
      $scope.tip.updateLabel(label);
      $scope.showEditLabelInput = false;
      event.stopPropagation();
    }

    $scope.newComment = function() {
      $scope.tip.newComment($scope.tip.newCommentContent);
      $scope.tip.newCommentContent = '';
    };

    $scope.newMessage = function() {
      $scope.tip.newMessage($scope.tip.newMessageContent);
      $scope.tip.newMessageContent = '';
    };

    $scope.tip_delete = function () {
      var modalInstance = $modal.open({
        templateUrl: 'views/partials/tip_operation_delete.html',
        controller: TipOperationsCtrl,
        resolve: {
          tip: function () {
            return $scope.tip;
          },
          operation: function () {
            return 'delete';
          }
        }
      });
    };

    $scope.tip_postpone = function () {
      var modalInstance = $modal.open({
        templateUrl: 'views/partials/tip_operation_postpone.html',
        controller: TipOperationsCtrl,
        resolve: {
          tip: function () {
            return $scope.tip;
          },
          operation: function () {
            return 'postpone';
          }
        }
      });
    };

}]);
