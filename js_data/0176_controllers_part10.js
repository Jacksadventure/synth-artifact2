      $scope.account = SharedData;
      $scope.account.authId = currentAccount.idToken;
      $scope.account.name = currentAccount.profile.name;
      $scope.account.givenName = currentAccount.profile['given_name'];
      $scope.account.familyName = currentAccount.profile['family_name'];
      $scope.account.headline = currentAccount.profile.headline;
      $scope.account.industry = currentAccount.profile.industry;
      $scope.account.currentPositions = currentAccount.profile.positions ? _.map(currentAccount.profile.positions.values, function (position) {
        return position;
      }) : [];
      $scope.account.identities = currentAccount.profile.identities;
      $scope.account.publicProfileUrl = currentAccount.profile.publicProfileUrl;