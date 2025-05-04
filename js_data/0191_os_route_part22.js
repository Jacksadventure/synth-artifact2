    const showAppManagement = loadTimeData.valueExists('showAppManagement') &&
        loadTimeData.getBoolean('showAppManagement');
    const showAndroidApps = loadTimeData.valueExists('androidAppsVisible') &&
        loadTimeData.getBoolean('androidAppsVisible');
    // Apps
    if (showAppManagement || showAndroidApps) {
      r.APPS = r.BASIC.createSection('/apps', 'apps');
      if (showAppManagement) {
        r.APP_MANAGEMENT = r.APPS.createChild('/app-management');
        r.APP_MANAGEMENT_DETAIL =
            r.APP_MANAGEMENT.createChild('/app-management/detail');
      }
      if (showAndroidApps) {
        r.ANDROID_APPS_DETAILS = r.APPS.createChild('/androidAppsDetails');
      }
    }